"""Pruebas automáticas de nAIhual (app/index.html + app/data/*.js), en modo vista previa y en modo pública.

Uso (desde la raíz del repositorio):
    python3 pruebas/prueba_piloto.py

Necesita Python 3 y Playwright con Chromium (vienen instalados en el entorno de Claude Code en la nube;
no son dependencias de la app). Levanta un servidor local en 127.0.0.1, abre la app a 390 px de ancho
y usa catálogos y configuraciones de prueba (inventados solo para la prueba, nunca se publican):
0, 1 y 3 cafés, vista interna encendida o apagada, y la beta (en el teléfono y con base de datos simulada).
Las cifras del catálogo (cuántos lugares, cuántos por categoría) se calculan de data/lugares.js: no hay que cambiarlas a mano.
No prueba un celular real ni que Google Maps caiga en el lugar correcto: eso lo tiene que hacer una persona.
"""
import collections
import functools
import http.server
import json
import os
import re
import socketserver
import sys
import threading
from urllib.parse import unquote

from playwright.sync_api import sync_playwright

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
APP = os.path.join(ROOT, 'app')
EXE = '/opt/pw-browsers/chromium'
RESULTS = []
HOSTS = {}
PERMITIDOS = {'127.0.0.1', 'fonts.googleapis.com', 'fonts.gstatic.com', 'file'}


def catalogo_real():
    regs = []
    for linea in open(os.path.join(APP, 'data', 'lugares.js'), encoding='utf-8'):
        linea = linea.strip()
        if linea.startswith('{"id"'):
            regs.append(json.loads(linea.rstrip(',')))
    return [r for r in regs if r.get('estado') not in ('pausado', 'retirado')]


CATALOGO = catalogo_real()
TOTAL = len(CATALOGO)
# Publicados según las mismas reglas de la app (estado, dirección, fuente, fecha y quién verificó).
PUBLICADOS = len([r for r in CATALOGO if r.get('estado') == 'publicado' and r.get('direccion') and r.get('fuente') and r.get('fecha_verificacion') and r.get('verifico')])
N_PLAYLISTS = len(re.findall(r"\{ id: '", open(os.path.join(APP, 'data', 'playlists.js'), encoding='utf-8').read()))
N_REFS = len(re.findall(r"\{ id: '", open(os.path.join(APP, 'data', 'referencias.js'), encoding='utf-8').read()))
N_AFUERA = len(re.findall(r"rumbo: \d", open(os.path.join(APP, 'data', 'referencias.js'), encoding='utf-8').read()))
N_FUENTES = len(re.findall(r"\{ id: '", open(os.path.join(APP, 'data', 'fuentes.js'), encoding='utf-8').read()))
POR_CAT = collections.Counter(r['categoria'] for r in CATALOGO)
# Nombres reales del catálogo: ninguno debe verse en la experiencia del visitante mientras esté en borrador.
# Solo los de 6 letras o más, para no confundirlos con palabras de la app.
NOMBRES_REALES = sorted({r['nombre'] for r in CATALOGO if len(r['nombre']) >= 6})


def check(name, ok, detail=''):
    RESULTS.append((name, bool(ok), detail))
    print(('PASA ' if ok else 'FALLA') + ' · ' + name + (' · ' + str(detail) if detail else ''))


def lugar(id_, nombre, **kw):
    r = {'id': id_, 'nombre': nombre, 'categoria': 'cafe', 'direccion': '', 'maps_url': '', 'fuente': '', 'fuente_url': '',
         'fecha_verificacion': '', 'verifico': '', 'estado': 'borrador', 'patrocinado': False, 'horario': '', 'fuente_horario': '',
         'precio': '', 'fuente_precio': '', 'guardianes': [], 'frase': {'es': 'Frase de prueba.', 'en': 'Test phrase.'}}
    r.update(kw)
    return r


def completo(id_, nombre, **kw):
    base = dict(direccion='Calle de Prueba ' + id_, fuente='Fuente de prueba', fecha_verificacion='2026-10-20',
                verifico='Persona de prueba', estado='publicado')
    base.update(kw)
    return lugar(id_, nombre, **base)


# Fichas incompletas o no publicables: ninguna debe entrar al recorrido.
INCOMPLETAS = [
    completo('sinfuente', 'Café Sin Fuente', fuente=''),
    completo('sinfecha', 'Café Sin Fecha', fecha_verificacion=''),
    completo('fechamala', 'Café Fecha Mala', fecha_verificacion='2026-02-31'),
    completo('fechafutura', 'Café Fecha Futura', fecha_verificacion='2099-01-01'),
    completo('sinverifico', 'Café Sin Verificó', verifico=''),
    completo('sindireccion', 'Café Sin Dirección', direccion=''),
    completo('mapsmalo', 'Café Maps Malo', maps_url='https://ejemplo.invalid/mapa'),
    completo('borrador', 'Café Borrador', estado='borrador'),
    completo('pausado', 'Café Pausado', estado='pausado'),
    completo('retirado', 'Café Retirado', estado='retirado'),
    completo('horasinfuente', 'Café Horario Sin Fuente', estado='borrador', horario='7:00 a 18:00'),
]
FIX = {
    'cero': INCOMPLETAS,
    'uno': INCOMPLETAS[:3] + [completo('uno', 'Café Uno', horario='7:00 a 18:00', fuente_horario='Letrero del local (prueba)')] + INCOMPLETAS[3:],
    'cuatro': [
        completo('a', 'Café A', fuente_url='https://example.com/fuente-a'),
        completo('b', 'Café B', patrocinado=True),
        INCOMPLETAS[0],
        completo('c', 'Café C', maps_url='https://maps.app.goo.gl/prueba'),
        completo('d', 'Café D'),
    ],
}


def serve():
    class Quiet(http.server.SimpleHTTPRequestHandler):
        def log_message(self, *a):
            pass
    handler = functools.partial(Quiet, directory=APP)
    httpd = socketserver.TCPServer(('127.0.0.1', 0), handler)
    threading.Thread(target=httpd.serve_forever, daemon=True).start()
    return httpd, 'http://127.0.0.1:%d/index.html' % httpd.server_address[1]


def js(name, value):
    return 'window.%s = %s;' % (name, json.dumps(value, ensure_ascii=False))


def new_page(browser, url, fixture=None, scheme='light', config=None, hash_='', claude=None):
    """config: dict = configuración de prueba · 'sin' = como si faltara data/config.js · None = la real."""
    ctx = browser.new_context(viewport={'width': 390, 'height': 844}, color_scheme=scheme, has_touch=True)
    page = ctx.new_page()
    errors = []
    hosts = HOSTS.setdefault(id(ctx), set())
    page.on('console', lambda m: errors.append(m.text) if m.type == 'error' and 'data/config.js' not in m.text and not (config == 'sin' and '404' in m.text) else None)
    page.on('pageerror', lambda e: errors.append(str(e)))
    page.on('request', lambda r: hosts.add(r.url.split('/')[2] if '://' in r.url and not r.url.startswith('data:') else r.url.split(':')[0]))
    def ok(body):
        return lambda r: r.fulfill(status=200, content_type='application/javascript; charset=utf-8', body=body)
    if fixture is not None:
        page.route('**/data/lugares.js', ok(js('NAIHUAL_LUGARES', fixture)))
    if config == 'sin':
        page.route('**/data/config.js', lambda r: r.fulfill(status=404, body=''))
    elif config is not None:
        page.route('**/data/config.js', ok(js('NAIHUAL_CONFIG', config)))
    if claude is not None:
        # Simula la función del visor de Claude (window.claude.use('sample')). Nunca llama a Claude de verdad.
        page.add_init_script('''(() => { window.__calls = []; window.__reply = %s;
          const fake = function () { return Promise.reject({ code: 'invalid_request' }); };
          fake.json = (input, opts) => { window.__calls.push(input); const r = window.__reply;
            return new Promise((res, rej) => setTimeout(() => r && r.__error ? rej({ code: r.__error, message: 'x' }) : res(r), 120)); };
          window.claude = { use: (n) => Promise.resolve(n === 'sample' ? Object.freeze(fake) : null) }; })();''' % json.dumps(claude, ensure_ascii=False))
    page.goto(url + hash_)
    page.wait_for_selector('main > *')
    return ctx, page, errors


def no_hscroll(page):
    return page.evaluate('document.documentElement.scrollWidth <= window.innerWidth')


def pedir_cafe(page):
    page.click('#chips [data-chip="cafe"]')
    page.wait_for_timeout(150)
    return page.locator('.msg').last


def contrast(page, sel):
    return page.evaluate('''(sel) => {
      const el = document.querySelector(sel); const cs = getComputedStyle(el);
      const rgb = s => s.match(/[\\d.]+/g).slice(0, 3).map(Number);
      const lum = c => { const v = c.map(x => { x /= 255; return x <= .03928 ? x / 12.92 : Math.pow((x + .055) / 1.055, 2.4); }); return .2126 * v[0] + .7152 * v[1] + .0722 * v[2]; };
      const a = lum(rgb(cs.color)), b = lum(rgb(cs.backgroundColor));
      return (Math.max(a, b) + .05) / (Math.min(a, b) + .05);
    }''', sel)




def sin_nombres(texto):
    return [n for n in NOMBRES_REALES if n in texto]


PUB = {'modo': 'publica', 'claude_responde': True, 'beta': True}
PREV = {'modo': 'vista_previa', 'claude_responde': True, 'beta': True}
GUARDIANES = ["No'j", "Iq'", 'Kej', "E'"]
FRASES_PROHIBIDAS = ['Caminá con respeto', '¿Cómo me porto', 'reglas fijas, sin IA', '¿En qué te ayudo', "Soy No'j", 'Tips para', 'en revisión: todavía no tengo lugares con fuente']


def ruta_norte_publicada():
    base = [('catedral', 'Catedral de San José', 'cultura', 3.6, 4.5),
            ('arco', 'Arco de Santa Catalina', 'cultura', 5, 2), ('merced', 'Iglesia de La Merced', 'cultura', 6, 1), ('siena', 'Siena Luz', 'cafe', 6, 2.5)]
    return [completo(i, n, categoria=c, mapa={'avenida': a, 'calle': k, 'aprox': False}) for i, n, c, a, k in base]


def cafe_flow_checks(page, name, want, mode):
    m = pedir_cafe(page)
    cards = m.locator('.cards.pilot [data-place]')
    ids = [cards.nth(i).get_attribute('data-place') for i in range(cards.count())]
    check('[%s] «%s»: muestra %d café(s)' % (mode, name, want), len(ids) == want, ids)
    bad = [i for i in ids if i in {r['id'] for r in INCOMPLETAS}]
    check('[%s] «%s»: ninguna ficha incompleta en el recorrido' % (mode, name), not bad, bad)
    for i in range(cards.count()):
        c = cards.nth(i)
        seal = c.locator('details.seal')
        check('[%s] «%s» · %s: sello «Verificado · 20 oct 2026»' % (mode, name, ids[i]), seal.get_attribute('data-seal') == 'ok' and 'Verificado · 20 oct 2026' in seal.inner_text())
        seal.locator('summary').click()
        check('[%s] «%s» · %s: el sello muestra fuente y quién comprobó' % (mode, name, ids[i]), 'Fuente:' in seal.inner_text() and 'Persona de prueba' in seal.inner_text())
        a = c.locator('a.btn[href*="google.com/maps"], a.btn[href*="maps.app.goo.gl"]')
        href = a.get_attribute('href') if a.count() else ''
        ok = href.startswith('https://www.google.com/maps/search/?api=1&query=') and ('Calle de Prueba ' + ids[i]) in unquote(href) or href == 'https://maps.app.goo.gl/prueba'
        check('[%s] «%s» · %s: «Cómo llegar» usable y con nombre accesible' % (mode, name, ids[i]), a.count() == 1 and ok and a.get_attribute('aria-label').startswith('Cómo llegar a '), href)
    return m, ids


def main():
    httpd, url = serve()
    with sync_playwright() as pw:
        browser = pw.chromium.launch(executable_path=EXE) if os.path.exists(EXE) else pw.chromium.launch()

        # =============== 0. Datos: todo lo que se nombra existe ===============
        ids = {r['id'] for r in CATALOGO}
        code = open(os.path.join(APP, 'index.html'), encoding='utf-8').read()
        pls = open(os.path.join(APP, 'data', 'playlists.js'), encoding='utf-8').read()
        refs = open(os.path.join(APP, 'data', 'referencias.js'), encoding='utf-8').read()
        nombrados = set(re.findall(r"'p:([a-z0-9]+)'", code)) | set(re.findall(r"lugar: '([a-z0-9]+)'", pls + refs)) | set(re.findall(r"paradas: \[([^\]]*)\]", pls) and re.findall(r"'([a-z0-9]+)'", ' '.join(re.findall(r"paradas: \[(.*?)\] \}", pls, re.S))))
        nombrados -= {'cafe', 'comida', 'id'}
        faltan = sorted(n for n in nombrados if n not in ids and not n.startswith('lugar'))
        check('Datos: las respuestas fijas, las playlists y las referencias nombran solo lugares activos del catálogo', not faltan, faltan)

        # =============== A. VISTA PREVIA con el catálogo real ===============
        ctx, page, errors = new_page(browser, url)
        M = '[vista previa]'
        check(M + ' Carga el catálogo (%d), la configuración y las fuentes (%d)' % (TOTAL, N_FUENTES), page.evaluate("n => window.NAIHUAL_LUGARES.filter(r => r.estado !== 'retirado' && r.estado !== 'pausado').length === n[0] && window.NAIHUAL_CONFIG.modo === 'vista_previa' && window.NAIHUAL_FUENTES.length === n[1]", [TOTAL, N_FUENTES]))
        check(M + ' Catálogo: ningún id repetido y ninguna frase con reseñas', len({r['id'] for r in CATALOGO}) == TOTAL and not [r['id'] for r in CATALOGO if any(x in ' '.join((r.get('frase') or {}).values()).lower() for x in ['reseña', 'comentarios de maps', 'calificaci', 'agregador'])])
        check(M + ' Inicio: portada ilustrada, «Quiero un café» y «Recién llegué»', page.locator('.hero-art svg').count() == 1 and page.locator('#cta-cafe').inner_text().strip() == 'Quiero un café' and page.locator('[data-ask="empezar"]').count() == 1)
        g = [page.locator('.guard-strip .gbtn b').nth(i).inner_text() for i in range(page.locator('.guard-strip .gbtn').count())]
        check(M + " Inicio: exactamente 4 guardianes, en orden No'j, Iq', Kej, E'", g == GUARDIANES, g)
        check(M + ' Inicio: retratos, no letras sueltas', page.locator('.guard-strip svg.portrait').count() == 4)
        check(M + ' Inicio: %d playlists con su mapa, autor y gasto' % N_PLAYLISTS, page.locator('.route-card').count() == N_PLAYLISTS and page.locator('.route-card svg path.route').count() == N_PLAYLISTS and page.locator('.route-card [data-autor]').count() == N_PLAYLISTS)
        check(M + ' Inicio: «¿Cómo venís a Antigua?» con 4 perfiles, sin agente', page.locator('[data-perfil]').count() == 4 and 'Agente' not in page.inner_text('[data-perfil-pick]'))
        check(M + ' Inicio vivo: saludo según la hora, cielo del momento e idea del guía', page.locator('[data-saludo]').count() == 1 and page.locator('.hero-art svg[data-momento]').count() == 1 and page.locator('[data-sugerencia] .idea').count() == 1)
        k1 = page.locator('[data-idea-key]').get_attribute('data-idea-key')
        page.click('[data-idea]')
        check(M + ' «Otra idea» cambia la sugerencia', page.locator('[data-idea-key]').get_attribute('data-idea-key') != k1)
        page.click('[data-wtoggle="que"]')
        check(M + ' Widget: se contrae con un toque', page.locator('[data-widget="que"].closed').count() == 1 and page.locator('[data-wtoggle="que"][aria-expanded="false"]').count() == 1)
        page.click('[data-perfil="mochilero"]')
        check(M + ' Perfil «Viajo con poco»: primero su playlist, marcada «Para vos», sin esconder las otras', page.locator('.route-card').first.get_attribute('data-route') == 'tanque' and page.locator('.route-card').count() == N_PLAYLISTS and page.locator('.route-card').first.locator('[data-para-vos]').count() == 1)
        page.reload()
        page.wait_for_selector('main > *')
        check(M + ' El perfil y el widget contraído se quedan en el teléfono', page.locator('[data-perfil="mochilero"][aria-checked="true"]').count() == 1 and page.locator('[data-widget="que"].closed').count() == 1)
        page.click('[data-perfil="local"]')
        page.click('[data-perfil="turista"]')
        on = page.evaluate("[...document.querySelectorAll('[data-perfil][aria-checked=\"true\"]')].map(b => b.dataset.perfil)")
        check(M + ' Perfiles como interruptores: hasta 2 encendidos (el tercero apaga el primero)', sorted(on) == ['local', 'turista'], on)
        page.click('[data-perfil="local"]')
        page.click('[data-perfil="turista"]')
        page.click('[data-wtoggle="que"]')
        check(M + ' Apagados, vuelve el orden de siempre', page.locator('[data-perfil][aria-checked="true"]').count() == 0 and page.locator('.route-card').first.get_attribute('data-route') == 'centro')
        check(M + ' Inicio: 4 accesos (Lugares, Cultura maya, Costumbres, Guardianes)', page.locator('.tiles .tile').count() == 4)
        check(M + ' Inicio: sin Aliados Fundadores ni Q250', page.locator('section.biz').count() == 0 and 'Q250' not in page.inner_text('main') and 'Aliados' not in page.inner_text('main'))
        intro = page.locator('[data-intro]')
        check(M + ' Inicio: «Qué es nAIhual» con la frase del fundador', intro.count() == 1 and 'gracias a su gente' in intro.inner_text())
        bru = page.locator('[data-brujula]')
        bt = bru.inner_text() if bru.count() else ''
        check(M + ' Inicio: brújula del paisaje con sus 4 puntos y fuentes', bru.count() == 1 and all(x in bru.locator('.art > svg').inner_html() for x in ['Cerro de la Cruz', 'Volcán de Agua', 'Fuego', 'Acatenango', 'Sale el sol']) and 'Wikipedia' in bt and bru.locator('svg.portrait').count() == 4)
        check(M + ' Inicio: la brújula no nombra puntos sin fuente', not any(x in bru.inner_html() for x in ['Cucurucho', 'Chipilapa', 'Calvario', 'Tanque', 'Pueblos Mágicos']))
        heading = lambda: float(page.locator('#bru-art > svg').get_attribute('data-heading'))
        page.click('[data-bru-land="agua"]')
        check(M + ' Brújula: «Volcán de Agua» enfrente gira a 185.6° (calculado de las coordenadas)', abs(heading() - 185.6) < 0.05, heading())
        page.click('[data-bru-land="fuego"]')
        check(M + ' Brújula: «Fuego» enfrente gira a 240°', abs(heading() - 240.0) < 0.05, heading())
        page.click('[data-bru-north]')
        check(M + ' Brújula: «Norte arriba» vuelve a 0° y su botón tiene nombre', heading() == 0 and page.inner_text('[data-bru-north]').strip() == 'Norte arriba')
        orient = lambda a: page.evaluate("a => { window.dispatchEvent(new DeviceOrientationEvent('deviceorientation', {alpha: a, beta: 80, gamma: 0, absolute: false})); }", a)
        page.click('[data-bru-sensor]')
        orient(100)
        page.wait_for_timeout(120)
        check(M + ' Brújula con sensor: pide calibrar con un volcán', 'Apuntá la parte de arriba del teléfono' in page.inner_text('#bru-status'))
        page.click('[data-bru-land="agua"]')
        orient(100 - 54.4)
        page.wait_for_timeout(120)
        check(M + ' Brújula con sensor: calibrada con Agua, al girar 54.4° queda Fuego enfrente', abs(heading() - 240.0) < 0.2, heading())
        page.locator('[data-bru-test] summary').click()
        orient(100)
        page.wait_for_timeout(60)
        page.click('[data-bru-test-at="agua"]')
        orient(100 - 54.4)
        page.wait_for_timeout(60)
        page.click('[data-bru-test-at="fuego"]')
        orient(100 - 62.3)
        page.wait_for_timeout(60)
        page.click('[data-bru-test-at="acate"]')
        orient(100 + 175.6)
        page.wait_for_timeout(60)
        page.click('[data-bru-test-at="cerro"]')
        rows = page.locator('[data-test-row]')
        check(M + ' Prueba de la brújula: compara esperado y medido (Fuego, Acatenango)', rows.count() == 2 and '54.4°' in rows.nth(0).inner_text() and '62.3°' in rows.nth(1).inner_text(), [rows.nth(i).inner_text() for i in range(rows.count())])
        check(M + ' Prueba de la brújula: mide el Cerro de la Cruz', page.locator('[data-test-cerro]').count() == 1 and '10.0°' in page.inner_text('[data-test-cerro]'), page.inner_text('[data-test-cerro]') if page.locator('[data-test-cerro]').count() else '')
        page.click('[data-bru-fb="si"]')
        page.click('[data-bru-save]')
        res = page.evaluate('(JSON.parse(localStorage.getItem("naihual.beta") || "[]").filter(x => x.tipo === "brujula")[0]) || null')
        check(M + ' Prueba de la brújula: se guarda en la beta para que Claude la lea', res is not None and res['fuego_esperado'] == 54.4 and abs(res['fuego_medido'] - 54.4) < 0.05 and res['coincide'] == 'si' and abs(res['cerro_medido'] - 10.0) < 0.05, res)
        page.evaluate('localStorage.removeItem("naihual.beta")')
        page.click('[data-bru-sensor]')
        check(M + ' 390 px sin desplazamiento horizontal (brújula)', no_hscroll(page))
        page.reload()
        page.wait_for_selector('main > *')
        page.click('[data-bru-sensor]')
        page.wait_for_function("document.getElementById('bru-status').textContent.indexOf('no deja usar el sensor') >= 0", timeout=6000)
        check(M + ' Brújula: si el teléfono no manda el sensor, lo dice y se puede tocar el volcán', 'no deja usar el sensor' in page.inner_text('#bru-status'))
        check(M + ' Inicio: tarjeta de la beta', page.locator('[data-beta-card]').count() == 1 and '0 anotaciones' in page.locator('[data-beta-card]').inner_text().lower())
        check(M + ' Botón de emergencias visible', page.locator('#sos').is_visible())
        page.click('#sos')
        check(M + ' Emergencias: «Pendiente de números oficiales», sin números', 'Pendiente de números oficiales' in page.inner_text('#dlg') and not any(ch.isdigit() for ch in page.inner_text('#dlg')))
        page.keyboard.press('Escape')
        check(M + ' 390 px sin desplazamiento horizontal (Inicio)', no_hscroll(page))
        tabs = page.locator('#tabs button').all_inner_texts()
        check(M + ' Barra: Inicio, Rutas, «+ Publicar» al centro, Guía, Guardados', [x.split('\n')[0].strip() for x in tabs] == ['Inicio', 'Rutas', 'Publicar', 'Guía', 'Guardados'], tabs)
        page.click('#tabs [data-publish]')
        page.click('[data-bform="post"] label.chip:has(input[value="evento"])')
        page.fill('[data-bform="post"] textarea[name="texto"]', 'Hay concierto en el Tanque el sábado')
        page.click('[data-bform="post"] button[type="submit"]')
        post = page.evaluate('(JSON.parse(localStorage.getItem("naihual.beta") || "[]").filter(x => x.tipo === "post")[0]) || null')
        check(M + ' «+ Publicar»: en 3 toques queda en tu muro, «por confirmar»', post is not None and post['tema'] == 'evento' and post['estado'] == 'por_confirmar' and 'Publicado' in page.inner_text('#toast'), post)
        page.evaluate('localStorage.removeItem("naihual.beta")')
        page.reload()
        page.wait_for_selector('main > *')

        # Café en 1 toque desde Inicio
        page.click('#cta-cafe')
        page.wait_for_timeout(200)
        m = page.locator('.msg').last
        cards = m.locator('.cards.pilot [data-place]')
        check(M + ' «Quiero un café» en 1 toque: abre la Guía con 3 cafés', page.locator('.guide-head').count() == 1 and cards.count() == 3)
        check(M + ' Cafés sin «Por verificar»: cada uno con su «Referencia web»', m.locator('details.seal[data-seal="ref"]').count() == 3 and 'Por verificar' not in m.inner_text())
        hrefs = [cards.nth(i).locator('a.btn').get_attribute('href') for i in range(3)]
        check(M + ' «Cómo llegar» de cada café es un enlace de Google Maps', all(h.startswith('https://www.google.com/maps/search/?api=1&query=') for h in hrefs), hrefs)
        check(M + " La bienvenida la da No'j, sin autopresentación", "No'j · te cuenta el porqué" in page.locator('.msg').first.inner_text() and '¿Qué tenés ganas de hacer en Antigua?' in page.locator('.msg').first.inner_text())
        for chip in ['empezar', 'horas', 'comida', 'dia', 'cultura', 'costumbres']:
            page.click('#chips [data-chip="%s"]' % chip)
            page.wait_for_timeout(60)
        chat = page.inner_text('main')
        check(M + ' Guía: respuestas con tarjetas visuales (fotos provisionales, mapas, costumbres)', page.locator('main .pcard').count() >= 3 and page.locator('main .rcard').count() >= 1 and page.locator('main .tipcard').count() >= 1)
        check(M + ' Guía: sin frases de sermón ni de sistema', not [f for f in FRASES_PROHIBIDAS if f in chat], [f for f in FRASES_PROHIBIDAS if f in chat])
        check(M + ' «Otro guía» se ve como las otras opciones del chat (no como interruptor)', page.evaluate("getComputedStyle(document.querySelector('#chips [data-next]')).borderRadius") == page.evaluate("getComputedStyle(document.querySelector('#chips [data-chip=\"cafe\"]')).borderRadius"))
        check(M + ' Guía: sin asteriscos dentro de las burbujas', all('*' not in b for b in page.locator('.bubble').all_inner_texts()))
        check(M + ' Guía: lo cultural lleva ⓘ', page.locator('main .tipcard details.info').count() >= 1)
        page.fill('#q', 'xyz qwerty')
        page.press('#q', 'Enter')
        page.wait_for_timeout(80)
        opts = page.locator('.msg').last.locator('.chip').all_inner_texts()
        check(M + ' Pregunta no entendida: aclaración breve con 4 opciones', opts == ['Un café', 'Por dónde empiezo', 'Cultura maya', 'Costumbres de aquí'], opts)
        page.locator('.msg').last.locator('.chip').nth(2).click()
        page.wait_for_timeout(80)
        check(M + ' Elegir una opción de la aclaración la responde', page.locator('.msg').last.locator('.tipcard').count() >= 1)
        seq = []
        for _ in range(4):
            page.click('#chips [data-next]')
            page.wait_for_timeout(40)
            seq.append(page.locator('.guide-head b').inner_text())
        check(M + " «Otro guía» recorre Iq' → Kej → E' → No'j", seq == ["Iq'", 'Kej', "E'", "No'j"], seq)
        for txt, want in [("quiero hablar con E'", "E'"), ("Iq'", "Iq'"), ('kej por favor', 'Kej'), ("No'j", "No'j")]:
            page.fill('#q', txt)
            page.press('#q', 'Enter')
            page.wait_for_timeout(40)
            got = page.locator('.guide-head b').inner_text()
            check(M + ' Pedir por nombre: «%s»' % txt, got == want, got)
        page.fill('#q', 'quiero hablar con batz')
        page.press('#q', 'Enter')
        check(M + " Pedir a B'atz' no lo vuelve guardián", page.locator('.guide-head b').inner_text() == "No'j")
        page.locator('.guide-head .minis button').nth(3).click()
        check(M + ' Tocar un retrato cambia de guardián', page.locator('.guide-head b').inner_text() == "E'")
        check(M + ' 390 px sin desplazamiento horizontal (Guía)', no_hscroll(page))

        # Rutas
        page.click('[data-tab="rutas"]')
        check(M + ' Rutas: mapa esquemático con la ruta dibujada y 6 paradas numeradas', page.locator('.mapframe svg path.route:not(.faint)').count() == 1 and page.locator('.mapframe .stop').count() == 6)
        check(M + ' Rutas: referencias del paisaje (%d), las de afuera al borde (%d)' % (N_REFS, N_AFUERA), page.locator('.mapframe [data-ref]').count() == N_REFS and page.locator('.mapframe [data-afuera]').count() == N_AFUERA and all(x in page.inner_html('.mapframe') for x in ['Jocotenango', 'Volcán de Agua', 'Volcán de Fuego', 'Santa Ana', 'San Cristóbal El Bajo', 'Cerro de la Cruz', 'La Recolección']))
        page.click('.mapframe [data-ref="jocotenango"]')
        check(M + ' Mapa: el nombre aparece al tocar el ícono (y no antes)', page.locator('.mapframe [data-ref="jocotenango"].open').count() == 1 and page.evaluate("getComputedStyle(document.querySelector('.mapframe [data-ref=\"santaana\"] text')).opacity") == '0')
        check(M + ' Rutas: los nombres del borde no se tapan entre sí', page.evaluate('''() => { const b = [...document.querySelectorAll('.mapframe [data-afuera] text')].map(t => t.getBoundingClientRect());
            return b.every((r, i) => b.every((q, j) => i === j || r.right <= q.left || q.right <= r.left || r.bottom <= q.top || q.bottom <= r.top)); }'''))
        check(M + ' Rutas: nombres de calles y aviso «Esquema · no a escala»', page.locator('.mapframe text.lbl').count() >= 10 and 'ESQUEMA · NO A ESCALA' in page.inner_text('[data-map-note]').upper())
        page.click('[data-selroute="conventos"]')
        check(M + ' Rutas: elegir otra ruta la dibuja (4 paradas)', page.locator('.mapframe .stop').count() == 4 and page.locator('.stops li').count() == 4)
        check(M + ' Rutas: un lugar temporalmente cerrado (Once Once) no entra a la ruta', 'Once Once' not in page.inner_text('main'))
        h = page.locator('[data-route-detail] a.btn.anil').get_attribute('href')
        check(M + ' «Abrir ruta a pie» arma un enlace de Google Maps con origen, destino y paradas', h.startswith('https://www.google.com/maps/dir/?api=1&travelmode=walking&origin=') and '&destination=' in h and '&waypoints=' in h, h[:90])
        check(M + ' 390 px sin desplazamiento horizontal (Rutas)', no_hscroll(page))
        page.locator('.stops li button').first.click()
        d = page.inner_text('main')
        check(M + ' Ficha desde la ruta: foto provisional y «Referencia web», sin «Por verificar» ni «Le falta»', page.locator('.d-hero .ph').count() == 1 and page.locator('details.seal[data-seal="ref"]').count() == 1 and 'Le falta:' not in d and 'Por verificar' not in d)
        check(M + ' Ficha: mapa chico con el lugar y «Cómo llegar»', page.locator('.minimap .pin').count() == 1 and page.locator('main a.btn[href*="google.com/maps"]').count() >= 1)
        check(M + ' 390 px sin desplazamiento horizontal (Ficha)', no_hscroll(page))
        page.click('[data-back]')
        check(M + ' «Volver» regresa a la ruta', page.locator('.mapframe').count() == 1)

        # Explorar
        page.click('[data-tab="inicio"]')
        page.click('[data-go="explorar"]')
        filtros = page.evaluate("[...document.querySelectorAll('[data-filter]')].map(b => [b.dataset.filter, b.textContent.trim()]).filter(f => !['all', 'route', 'tip'].includes(f[0]))")
        check(M + ' Explorar: un filtro por cada categoría del catálogo', sorted(f[0] for f in filtros) == sorted(POR_CAT), filtros)
        for cat, nombre in filtros:
            page.click('[data-filter="%s"]' % cat)
            n_pins = page.locator('.grid [data-pin^="p:"]').count()
            n_art = page.locator('.grid svg.art[data-scene="%s"]' % cat).count()
            check(M + ' Explorar: filtro «%s» con %d lugares, cada uno con su dibujo y su color' % (nombre, POR_CAT[cat]), n_pins == POR_CAT[cat] and n_art == POR_CAT[cat], (n_pins, n_art))
        page.click('[data-filter="all"]')
        check(M + ' Explorar: muro visual con lugares, rutas y costumbres', page.locator('.grid [data-pin^="p:"]').count() == TOTAL and page.locator('.grid [data-pin^="r:"]').count() == N_PLAYLISTS)
        page.click('[data-filter="all"]')
        page.fill('#fq', 'matcha')
        page.wait_for_timeout(80)
        check(M + ' Buscar «matcha» encuentra Komori', page.locator('.grid [data-open="p:komori"]').count() == 1)
        page.locator('.grid [data-open="p:komori"]').click()
        check(M + ' Ficha sin dirección: sin «Cómo llegar» y sin mapa', page.locator('main a[href*="maps"]').count() == 0 and page.locator('.minimap').count() == 0)
        check(M + ' Ficha: la frase de Diego va firmada («— Diego»), no como verdad', page.locator('.lead [data-frase-de]').count() == 1 and '— Diego' in page.inner_text('.lead') and '«Literal el mejor matcha.»' in page.inner_text('.lead'))
        page.click('[data-back]')
        page.fill('#fq', '')
        check(M + ' 390 px sin desplazamiento horizontal (Explorar)', no_hscroll(page))

        # Guardados
        page.locator('.pin-wrap:has([data-pin="r:norte"]) .heart').click()
        page.click('[data-tab="guardados"]')
        check(M + ' Guardados: arma un plan con mapa y enlace a pie', page.locator('.minimap .stop').count() == 4 and page.locator('main a.btn.anil[href*="/maps/dir/"]').count() == 1)
        check(M + ' La pestaña Guardados cuenta lo guardado', '1' in page.locator('[data-tab="guardados"]').inner_text())
        check(M + ' 390 px sin desplazamiento horizontal (Guardados)', no_hscroll(page))

        # Cultura, nawales, costumbres, guardianes
        page.click('[data-tab="inicio"]')
        page.click('[data-go="cultura"]')
        check(M + ' Cultura maya: consejos con ⓘ y acceso a los nawales', page.locator('.tipcard').count() == 9 and page.locator('.tipcard details.info').count() == 9)
        check(M + ' Cultura maya: la imagen de los 260 días (13 × 20)', page.locator('[data-art="cholqij"] > svg circle').count() == 260)
        page.click('[data-go="nawales"]')
        check(M + ' Los 20 nawales, con los 4 guardianes resaltados', page.locator('.nawal').count() == 20 and page.locator('.nawal.guard').count() == 4)
        check(M + ' Aviso: nAIhual no calcula tu nawal', 'no calcula tu nawal' in page.inner_text('main'))
        page.click('[data-nawal="iq"]')
        check(M + " Nawal Iq': ficha y «Hablar con Iq'»", page.locator('.facts div').count() == 2 and page.locator('main [data-guide="iq"]').count() == 1)
        check(M + ' Nawal: sin «Luz» ni «Sombra» (describen personas; B8)', 'Sombra' not in page.inner_text('main') and 'Luz' not in page.inner_text('.facts'))
        page.click('[data-tab="inicio"]')
        page.click('[data-go="costumbres"]')
        cos = page.inner_text('main')
        check(M + ' Costumbres de aquí: 2, sin sermones', page.locator('.tipcard').count() == 2 and not [f for f in FRASES_PROHIBIDAS if f in cos])
        page.click('[data-tab="inicio"]')
        page.click('[data-go="guardianes"]')
        gs = page.locator('.gfull h2').all_inner_texts()
        check(M + ' Guardianes: 4 en orden, con rumbo y ⓘ', gs == GUARDIANES and 'Oriente · rojo' in page.inner_text('main') and page.locator('details.info[data-info="guard"]').count() == 1, gs)
        check(M + ' Guardianes: la rueda de rumbos con los 4 retratos', page.locator('[data-art="rumbos"] svg.portrait').count() == 4)
        check(M + ' 390 px sin desplazamiento horizontal (Guardianes)', no_hscroll(page))

        # Beta del fundador (sin visor: se guarda en este teléfono)
        page.click('[data-tab="inicio"]')
        page.click('[data-beta-card] [data-go="beta"]')
        b = page.inner_text('main')
        check(M + ' Beta: dice dónde se guarda (este teléfono)', page.locator('[data-beta-where="local"]').count() == 1 and 'solo en este teléfono' in b)
        page.locator('[data-beta-new] summary').click()
        page.fill('[data-bform="nuevo"] input[name="nombre"]', 'Lugar de prueba')
        page.fill('[data-bform="nuevo"] input[name="maps"]', 'http://no-seguro')
        page.click('[data-bform="nuevo"] button[type="submit"]')
        check(M + ' Beta: rechaza un enlace que no empieza con https://', page.locator('[data-beta-msg="badLink"]').count() == 1 and page.locator('[data-beta-item]').count() == 0)
        page.fill('[data-bform="nuevo"] input[name="nombre"]', 'Lugar de prueba')
        page.fill('[data-bform="nuevo"] input[name="maps"]', 'https://maps.app.goo.gl/prueba')
        page.select_option('[data-bform="nuevo"] select[name="momento"]', 'comida')
        page.check('[data-bform="nuevo"] input[name="gusta"]')
        page.fill('[data-bform="nuevo"] textarea[name="texto"]', 'Nota de prueba')
        page.click('[data-bform="nuevo"] button[type="submit"]')
        it = page.locator('[data-beta-item="nuevo"]')
        check(M + ' Beta: «Agregar un lugar» queda en la lista con momento, me gustó y nota', it.count() == 1 and all(x in it.inner_text() for x in ['Lugar de prueba', 'Comida', 'Me gustó', 'Nota de prueba']))
        check(M + ' Beta: cada anotación dice si Claude ya la revisó', page.locator('[data-beta-item="nuevo"] [data-rev="sin"]').count() == 1)
        check(M + ' Beta: explica qué pasa con lo que anotás', page.locator('[data-beta-how]').count() == 1 and 'leé la beta' in page.locator('[data-beta-how]').text_content())
        check(M + ' Sin la palabra «fundador» en pantalla', 'fundador' not in page.inner_text('body').lower())
        check(M + ' Beta: se guardó en el teléfono', page.evaluate('JSON.parse(localStorage.getItem("naihual.beta")).length') == 1)
        page.fill('#bq', 'pizz')
        page.wait_for_timeout(80)
        check(M + ' Beta: «Anotar rápido» encuentra lugares mientras escribís', page.locator('#bq-out [data-visit]').count() >= 1)
        page.locator('#bq-out [data-visit]').first.click()
        check(M + ' Beta: tocar un lugar abre «Tu visita» con el número de 0 a 10 y el comentario', page.locator('#dlg [data-bform="visita"] input[type=range]').count() == 1 and page.locator('#dlg textarea').count() == 1)
        page.locator('#dlg input[type=range]').fill('10')
        check(M + ' Visita: con 10 avisa que es lo mejor que has probado', page.locator('#dlg [data-score-warn]').is_visible() and page.inner_text('#dlg [data-score-out]') == '10')
        page.locator('#dlg input[type=range]').fill('8')
        page.fill('#dlg textarea', 'Buena masa')
        page.click('#dlg button[type="submit"]')
        v = page.evaluate('JSON.parse(localStorage.getItem("naihual.beta")).filter(x => x.tipo === "visita")')
        check(M + ' Visita: se guarda con su número (privado) y el comentario', len(v) == 1 and v[0]['puntaje'] == 8 and v[0]['texto'] == 'Buena masa' and v[0]['fui'] is True, v)
        check(M + ' Beta: el número privado no se muestra; solo dice «Con número privado»', '8/10' not in page.inner_text('main') and page.locator('[data-puntaje-privado]').count() == 1)
        nb = page.locator('[data-beta-item]').count()
        page.locator('[data-beta-list] [data-del-ask]').first.click()
        check(M + ' Beta: «Borrar» primero pregunta y no borra', page.locator('[data-beta-item]').count() == nb and page.locator('[data-del-yes]').count() == 1)
        page.click('[data-del-no]')
        check(M + ' Beta: «No» cancela', page.locator('[data-del-yes]').count() == 0 and page.locator('[data-beta-item]').count() == nb)
        page.locator('[data-beta-list] [data-del-ask]').first.click()
        page.click('[data-del-yes]')
        check(M + ' Beta: «Sí, borrar» la borra', page.locator('[data-beta-item]').count() == nb - 1)
        # Lo que escribe una persona nunca se ejecuta como código.
        page.evaluate("document.querySelector('[data-beta-new]').open = true")
        page.fill('[data-bform="nuevo"] input[name="nombre"]', '<img src=x onerror="window.__xss=1">')
        page.fill('[data-bform="nuevo"] textarea[name="texto"]', '<script>window.__xss=2</script>')
        page.click('[data-bform="nuevo"] button[type="submit"]')
        page.evaluate("document.querySelector('[data-beta-new]').open = false")
        page.click('[data-wall] [data-publish]')
        page.click('[data-bform="post"] button[type="submit"]')
        check(M + ' Publicar sin texto: lo dice y no cierra', 'Escribí algo' in page.inner_text('[data-post-msg]') and page.locator('#dlg[open]').count() == 1)
        page.fill('[data-bform="post"] textarea[name="texto"]', 'Hola')
        page.fill('[data-bform="post"] input[name="maps"]', 'https://evil.example/x')
        page.click('[data-bform="post"] button[type="submit"]')
        check(M + ' Publicar: el enlace tiene que ser de Google Maps', 'Google Maps' in page.inner_text('[data-post-msg]') and page.locator('#dlg[open]').count() == 1)
        page.click('#dlg [data-close]')
        rotos = [{'_id': 'local-roto', 'tipo': 'post', 'tema': 'lugar', 'texto': 'Viejo', 'estado': 'confirmado', 'fecha': '2026-10-01', 'orden': {'lugar': 'ag001', 'guardian': 'zzz', 'tema': 'xx'}}]
        prev = page.evaluate('localStorage.getItem("naihual.beta")')
        page.evaluate('r => { const a = JSON.parse(localStorage.getItem("naihual.beta") || "[]"); localStorage.setItem("naihual.beta", JSON.stringify(a.concat(r))); }', rotos)
        page.goto(url + '#beta')
        page.reload()
        page.wait_for_selector('[data-wall]')
        check(M + ' Muro: una publicación con un lugar o un guía que ya no existen no rompe la pantalla', page.locator('[data-wall] .post').count() >= 1 and 'Viejo' in page.inner_text('[data-wall]') and not errors, errors[-2:])
        page.evaluate('p => localStorage.setItem("naihual.beta", p || "[]")', prev)
        page.goto(url + '#beta')
        page.reload()
        page.wait_for_selector('[data-wall]')
        check(M + ' Seguridad: lo que se anota se muestra como texto, no como código', page.evaluate('window.__xss === undefined') and page.locator('main img[src="x"]').count() == 0 and '<img src=x' in page.inner_text('main'))
        check(M + ' 390 px sin desplazamiento horizontal (Beta)', no_hscroll(page))
        page.click('[data-tab="inicio"]')
        page.click('[data-go="explorar"]')
        page.locator('[data-open="p:siena"]').first.click()
        page.click('[data-beta-like="siena"]')
        page.locator('[data-vamos="siena"]').first.evaluate("a => { a.removeAttribute('target'); a.setAttribute('href', '#'); }")
        page.locator('[data-vamos="siena"]').first.click()
        page.wait_for_timeout(500)
        check(M + ' «Vamos» deja la pregunta «¿Fuiste a Siena Luz?» con «Sí, fui» y «Todavía no»', page.locator('#fui-bar:not([hidden])').count() == 1 and 'Fuiste a Siena Luz' in page.inner_text('#fui-bar'))
        page.click('[data-fui-yes]')
        check(M + ' «Sí, fui» abre «Tu visita»', page.locator('#dlg [data-bform="visita"][data-lugar="siena"]').count() == 1)
        page.click('#dlg [data-close]')
        page.click('[data-fui-no]')
        check(M + ' «Todavía no» quita la pregunta', page.locator('#fui-bar:not([hidden])').count() == 0)
        check(M + ' Ficha: sello «Referencia web» con su fuente', page.locator('details.seal[data-seal="ref"]').count() == 1 and 'Por verificar' not in page.inner_text('main'))
        check(M + ' Ficha: «Me gustó» marca el lugar', page.locator('[data-beta-like="siena"][aria-pressed="true"]').count() == 1 and page.locator('[data-liked]').count() == 1)
        check(M + ' Ficha: el formulario arranca en «Nota»', page.locator('[data-bform="ficha"] select[name="tipo"]').input_value() == 'nota')
        page.select_option('[data-bform="ficha"] select[name="tipo"]', 'dato')
        page.fill('[data-bform="ficha"] textarea[name="texto"]', 'La dirección cambió')
        page.click('[data-bform="ficha"] button[type="submit"]')
        check(M + ' Al guardar aparece el aviso «Guardado en tu beta» con «Ver»', page.locator('#toast:not([hidden])').count() == 1 and 'Guardado en tu beta' in page.inner_text('#toast') and page.locator('#toast [data-go="beta"]').count() == 1)
        check(M + ' Ficha: «Dato mal» se guarda', page.evaluate('JSON.parse(localStorage.getItem("naihual.beta")).some(x => x.tipo === "dato" && x.lugar === "siena" && x.texto === "La dirección cambió")'))
        page.click('[data-beta-like="siena"]')
        check(M + ' Ficha: tocar otra vez quita el «Me gustó»', page.locator('[data-beta-like="siena"][aria-pressed="false"]').count() == 1)
        page.evaluate('localStorage.removeItem("naihual.beta")')

        # Vista interna (antes, una pregunta para que haya registro de la última respuesta)
        page.click('[data-tab="guia"]')
        page.fill('#q', 'cultura maya')
        page.press('#q', 'Enter')
        page.click('[data-tab="inicio"]')
        page.click('footer [data-go="taller"]')
        t = page.inner_text('main')
        check(M + ' Vista interna: aviso y revisión de las %d fichas' % TOTAL, 'no la ve el visitante' in t and ('Publicadas hoy: %d de %d' % (PUBLICADOS, TOTAL)) in t and page.locator('[data-review]').count() == TOTAL)
        check(M + ' Revisión: Coffea sin la frase sin fuente', 'Afirmación retirada hasta tener fuente' in t and 'Entre las 100 mejores coffee shops del mundo.' not in page.inner_text('body').replace('«Entre las 100 mejores coffee shops del mundo».', ''))
        for sec, sel, n in [('textos', '[data-copy]', 13), ('modelo', '[data-capa]', 6), ('aprendizaje', '.flow li', 7), ('arquitectura', '.layer', 9), ('sistema', '.sw', 18)]:
            page.click('[data-sec="%s"]' % sec)
            check(M + ' Vista interna · %s' % sec, page.locator(sel).count() >= n and no_hscroll(page), page.locator(sel).count())
        page.click('[data-sec="modelo"]')
        mo = page.inner_text('main')
        check(M + ' Modelo: monetización primaria = hotel socio con QR, pendiente; Q250 fuera', 'Hotel socio con QR' in mo and 'Pendiente de evolución y planificación' in mo and 'Pro existe solo así' in mo and 'fue solo una idea' in mo)
        page.click('[data-sec="aprendizaje"]')
        a = page.inner_text('main')
        check(M + ' Aprendizaje: «Diseño futuro / no activo» y «Datos ficticios de demostración»', 'Diseño futuro / no activo' in a and 'Datos ficticios de demostración' in a)
        page.click('[data-demo-fb="si"]')
        check(M + ' La demo «¿Te sirvió?» no guarda nada', 'no se guardó ni se envió nada' in page.inner_text('main') and page.evaluate('Object.keys(localStorage).every(k => k === "naihual.app1" || k === "naihual.beta" || k === "naihual.aprendido" || k === "naihual.fuiste" || k === "naihual.widgets")'))
        page.click('[data-sec="arquitectura"]')
        r = page.inner_text('main')
        check(M + ' Arquitectura: registro de la última respuesta y fuentes del mapa', 'reglas-fijas 3.7' in r and 'Beta' in r and 'Wikivoyage' in r and 'NotebookLM Enterprise' in r)
        page.evaluate('localStorage.setItem("naihual.fuiste", JSON.stringify({lugar: "siena", nombre: "Siena Luz"}))')
        page.goto(url + '#guia')
        page.reload()
        page.wait_for_selector('#fui-bar:not([hidden])')
        r = page.evaluate("() => [document.getElementById('fui-bar').getBoundingClientRect().bottom, document.getElementById('q').getBoundingClientRect().top]")
        check(M + ' Guía: la pregunta «¿Fuiste?» no tapa la caja para escribir', r[0] <= r[1], r)
        page.click('[data-fui-no]')
        code = open(os.path.join(APP, 'index.html'), encoding='utf-8').read()
        check(M + ' Sin llaves de API ni conexiones a servicios en el código', not any(x in code for x in ['AIza', 'generativelanguage.googleapis', 'apiKey', 'api_key=']))
        check(M + ' Sin datos de lugares escritos dentro del programa', 'Coffea Cafés Especiales' not in code.split('<script>')[1].split('// ===================== CLAUDE')[0] and "name: '12 Onzas'" not in code)
        check(M + ' La reserva del directorio no se carga', page.evaluate('window.NAIHUAL_RESERVA === undefined'))
        check(M + ' Red: solo archivos propios y la letra de Google Fonts', {h.split(':')[0] for h in HOSTS[id(ctx)]} <= PERMITIDOS, sorted(HOSTS[id(ctx)]))
        check(M + ' Consola sin errores', not errors, errors)
        ctx.close()

        # =============== B. PÚBLICA con el catálogo real ===============
        M = '[pública]'
        ctx, page, errors = new_page(browser, url, None, 'light', PUB, '', {'texto': 'hola', 'lugares': [], 'consejos': [], 'opciones': []})
        body = page.inner_text('main')
        check(M + ' Idea del guía: lo maya sale con * y su aviso, también aquí', page.locator('[data-sugerencia] details.info').count() == 1 and '*' in page.inner_text('[data-sugerencia] .bubble'))
        check(M + ' Sin «+ Publicar» para el visitante', page.locator('[data-publish]').count() == 0)
        check(M + ' Sin emergencias, sin vista interna y sin Claude', not page.locator('#sos').is_visible() and page.locator('[data-go="taller"]').count() == 0 and page.locator('[data-ai]').count() == 0)
        check(M + ' Inicio: ninguna ruta ni lugar por verificar; avisa que las rutas vienen en camino', page.locator('.route-card').count() == 0 and 'Las rutas vienen en camino' in body and not sin_nombres(body))
        page.click('#cta-cafe')
        page.wait_for_timeout(150)
        m = page.locator('.msg').last
        check(M + ' Café sin cafés publicados: «Estoy probando los cafés uno por uno», sin enlaces', 'Estoy probando los cafés uno por uno.' in m.inner_text() and m.locator('a').count() == 0 and m.locator('[data-place]').count() == 0)
        for chip in ['empezar', 'horas', 'comida', 'dia', 'cultura', 'costumbres']:
            page.click('#chips [data-chip="%s"]' % chip)
            page.wait_for_timeout(60)
        page.fill('#q', 'Recomendame algo bonito')
        page.press('#q', 'Enter')
        page.wait_for_timeout(300)
        chat = page.inner_text('main')
        check(M + ' Guía: ningún lugar por verificar, ni por nombre', page.locator('main [data-place]').count() == 0 and not sin_nombres(chat), sin_nombres(chat))
        check(M + ' Guía: dice «Esta parte la estoy terminando de probar» y ofrece cultura', 'Esta parte la estoy terminando de probar.' in chat and page.locator('main .tipcard').count() >= 1)
        check(M + ' Guía: sin frases de sermón ni de sistema', not [f for f in FRASES_PROHIBIDAS if f in chat] and 'Por verificar' not in chat)
        check(M + ' Claude no responde en modo pública', page.evaluate('window.__calls.length') == 0)
        page.click('[data-tab="rutas"]')
        check(M + ' Rutas: estado vacío diseñado', 'Las rutas vienen en camino' in page.inner_text('main') and page.locator('.empty .map svg').count() == 1)
        page.click('[data-tab="inicio"]')
        page.click('[data-go="explorar"]')
        ex = page.inner_text('main')
        check(M + ' Explorar: solo cultura y costumbres, sin lugares', page.locator('.grid [data-pin^="p:"]').count() == PUBLICADOS and page.locator('.grid [data-pin^="t:"]').count() == 11 and (PUBLICADOS or not sin_nombres(ex)))
        page.click('[data-filter="cafe"]')
        check(M + ' Explorar · Cafés: estado vacío diseñado', 'Esta parte todavía la estoy probando.' in page.inner_text('main'))
        page.click('[data-filter="all"]')
        page.locator('.pin-wrap:has([data-pin="t:foto"]) .heart').click()
        page.click('[data-tab="guardados"]')
        check(M + ' Guardados con un consejo: avisa que el plan espera lugares', 'Todavía no hay.' in page.inner_text('main') and page.locator('.grid [data-pin]').count() == 1)
        check(M + ' Consola sin errores', not errors, errors)
        ctx.close()
        ctx, page, errors = new_page(browser, url, None, 'light', PUB, '#constructor')
        check('[pública] Un enlace raro (#constructor) abre Inicio sin romperse', page.locator('.hero').count() == 1 and '[object' not in page.inner_text('main'))
        ctx.close()
        for h in ['#taller', '#revision']:
            ctx, page, errors = new_page(browser, url, None, 'light', PUB, h)
            check(M + ' El enlace %s no abre la vista interna' % h, page.locator('[id^="taller-"]').count() == 0 and page.locator('.hero').count() == 1)
            ctx.close()
        ctx, page, errors = new_page(browser, url, None, 'light', 'sin')
        check('[sin config] Sin archivo de configuración = modo pública', not page.locator('#sos').is_visible() and page.locator('.route-card').count() == 0 and page.locator('[data-go="taller"]').count() == 0)
        ctx.close()

        # =============== C. Catálogos de prueba ===============
        for name, want in [('cero', 0), ('uno', 1), ('cuatro', 3)]:
            ctx, page, errors = new_page(browser, url, FIX[name], 'light', PUB)
            page.click('[data-tab="guia"]')
            m, ids = cafe_flow_checks(page, name, want, 'pública')
            if name == 'uno':
                c = m.locator('.cards.pilot details.seal').first
                check('[pública] Horario solo con su fuente (dentro del sello)', 'Horario: 7:00 a 18:00' in c.inner_text())
            if name == 'cuatro':
                check('[pública] Orden = orden del catálogo (el patrocinio no lo cambia)', ids == ['a', 'b', 'c'], ids)
                cards = m.locator('.cards.pilot [data-place]')
                check('[pública] El patrocinado se identifica', 'Patrocinado' in cards.nth(1).inner_text() and 'Patrocinado' not in cards.nth(0).inner_text())
                check('[pública] La fuente con enlace se puede abrir', cards.nth(0).locator('details.seal a[href="https://example.com/fuente-a"]').count() == 1)
                check('[pública] 390 px sin desplazamiento horizontal (3 cafés)', no_hscroll(page))
                page.click('#lang-en')
                check('[pública] Inglés: «Verified · Oct 20, 2026»', 'Verified · Oct 20, 2026' in page.locator('.cards.pilot').last.inner_text())
                page.click('#lang-es')
            page.click('[data-tab="inicio"]')
            page.click('[data-go="explorar"]')
            feed = page.inner_text('main')
            n_pub = {'cero': 0, 'uno': 1, 'cuatro': 4}[name]
            check('[pública] «%s»: Explorar muestra solo los publicados (%d)' % (name, n_pub), page.locator('.grid [data-pin^="p:"]').count() == n_pub and 'Café Sin Fuente' not in feed and 'Café Borrador' not in feed and 'Café Pausado' not in feed and 'Café Retirado' not in feed)
            check('[pública] «%s»: consola sin errores' % name, not errors, errors)
            ctx.close()
        con_aviso = [dict(r, aviso='Temporalmente cerrado (prueba)') if r['id'] == 'arco' else r for r in ruta_norte_publicada()]
        ctx, page, errors = new_page(browser, url, con_aviso + [completo('cerrado', 'Café Cerrado', aviso='Cerrado (prueba)'), completo('abierto', 'Café Abierto')], 'light', PUB)
        check('[pública] Una ruta con un lugar cerrado no se ofrece', page.locator('.route-card').count() == 0)
        page.click('[data-tab="guia"]')
        m = pedir_cafe(page)
        ids = [m.locator('.cards.pilot [data-place]').nth(i).get_attribute('data-place') for i in range(m.locator('.cards.pilot [data-place]').count())]
        check('[pública] Un café cerrado no sale en «Quiero un café»', 'cerrado' not in ids and 'abierto' in ids, ids)
        ctx.close()
        ctx, page, errors = new_page(browser, url, ruta_norte_publicada(), 'light', PUB)
        check('[pública] Ruta completa publicada: aparece en Inicio con su mapa', page.locator('.route-card').count() == 1)
        page.click('[data-tab="guia"]')
        m = pedir_cafe(page)
        check('[pública] Siena publicada sale como café; la ruta lista también se puede ver', m.locator('.cards.pilot [data-place="siena"]').count() == 1)
        ctx.close()
        solo_ruta = [r for r in ruta_norte_publicada() if r['id'] != 'siena'] + [completo('siena', 'Siena Luz', categoria='comida', mapa={'avenida': 6, 'calle': 2.5, 'aprox': False})]
        ctx, page, errors = new_page(browser, url, solo_ruta, 'light', PUB)
        page.click('[data-tab="guia"]')
        m = pedir_cafe(page)
        check('[pública] Sin cafés pero con una ruta lista: «Mientras, esta ruta ya está lista»', 'Mientras, esta ruta ya está lista:' in m.inner_text() and m.locator('.rcard').count() == 1)
        ctx.close()
        mezcla = [lugar('b1', 'Café Borrador Uno', direccion='Calle B1'), completo('p1', 'Café Publicado'), lugar('b2', 'Café Borrador Dos', direccion='Calle B2'), lugar('b3', 'Café Sin Dirección')]
        ctx, page, errors = new_page(browser, url, mezcla, 'light', PREV)
        page.click('[data-tab="guia"]')
        m = pedir_cafe(page)
        ids = [m.locator('.cards.pilot [data-place]').nth(i).get_attribute('data-place') for i in range(m.locator('.cards.pilot [data-place]').count())]
        check('[vista previa] Café: primero lo publicado, después lo por verificar con dirección', ids == ['p1', 'b1', 'b2'], ids)
        check('[vista previa] Sin fuente no hay sello; el publicado, «Verificado»', m.locator('details.seal[data-seal="ok"]').count() == 1 and m.locator('details.seal').count() == 1)
        ctx.close()

        # =============== D. Claude responde (vista previa, simulado) · orden de búsqueda en 3 pasos ===============
        ok_reply = {'texto': 'Te cuento algo para empezar con calma.', 'consejos': ['foto', 'inventado'], 'lugares': ['doce', 'inventado'],
                    'otros': [{'nombre': 'Lugar que conoce la IA', 'porque': 'Lo que se sabe de él.'}], 'cultural': False, 'suficiente': True,
                    'opciones': ['Contame más'], 'aprendido': ['La gente quiere empezar con calma.']}
        ctx, page, errors = new_page(browser, url, None, 'light', None, '', ok_reply)
        page.wait_for_selector('[data-ai="listo"]')
        check('[Claude] Avisa la prueba privada y que solo guarda lo que aprende, por confirmar', 'solo guarda lo que aprende' in page.inner_text('main'))
        page.click('[data-tab="guia"]')
        page.fill('#q', '¿Qué me recomendás hacer hoy?')
        page.press('#q', 'Enter')
        check('[Claude] Muestra «pensando» y un botón para detener', page.locator('[data-kind="thinking"]').count() == 1 and page.locator('[data-stop]').count() == 1)
        page.wait_for_selector('[data-kind="ai"]')
        last = page.locator('.msg').last
        check('[Claude] Responde el guardián de turno, marcado «con Claude»', 'Te cuento algo para empezar con calma.' in last.inner_text() and 'con Claude' in last.inner_text())
        check('[Claude] Muestra un solo consejo y descarta ids inventados', last.locator('.tipcard').count() == 1)
        check('[Claude] Paso 1: muestra la ficha del catálogo con «Vamos» e «Info»', last.locator('[data-place="doce"]').count() == 1 and last.locator('[data-place="doce"] a.btn').inner_text().strip() == 'Vamos' and last.locator('[data-place="doce"] button.btn[data-open="p:doce"]').count() == 1)
        ia = last.locator('[data-ia-place]')
        hrefs = [ia.locator('a').nth(k).get_attribute('href') for k in range(ia.locator('a').count())] if ia.count() else []
        check('[Claude] Paso 2: lugar que sabe la IA, marcado «Según la IA · confirmá en Google», con «Vamos» (ruta) e «Info» (Google Maps)', ia.count() == 1 and 'Según la IA · confirmá en Google' in ia.inner_text() and len(hrefs) == 2 and hrefs[0].startswith('https://www.google.com/maps/dir/?api=1&destination=') and hrefs[1].startswith('https://www.google.com/maps/search/?api=1&query='), hrefs)
        check('[Claude] Ofrece sus opciones', last.locator('[data-say="Contame más"]').count() == 1)
        calls = page.evaluate('window.__calls')
        first = calls[0][0]['content'] if calls else ''
        check('[Claude] Recibe el orden de búsqueda, «guía, no juez» y los datos', all(x in first for x in ['Orden para buscar', 'Sos guía, no juez', '"catalogo"', '"libretas"', '"playlists"', '"aprendido_confirmado"', 'Nunca afirmes horarios, precios']) and 'en_revision_no_nombrar' not in first and calls[0][-1]['content'] == '¿Qué me recomendás hacer hoy?')
        check('[Claude] Los datos llevan la fuente pública de cada lugar', 'Guatemala.com' in first and 'fundador' not in first)
        import re as _re
        cat_ids = _re.findall(r'"id":"([a-z0-9]+)","nombre"', first)
        check('[Claude] Manda un catálogo corto (máximo 60 de %d) y el número privado nunca se dice' % TOTAL, 0 < len(cat_ids) <= 60 and 'Nunca lo digas' in first and '"puntaje' not in first and '"gusto_privado"' in first, len(cat_ids))
        check('[Claude] Las frases de Diego le llegan firmadas, como opinión', '"frase_de":"Diego"' in first and 'nunca como verdad' in first)
        check('[Claude] Buscar ignora palabras vacías («qué», «recomendás»): manda solo la muestra por categoría', len([i for i in cat_ids if i not in ('noj', 'iq', 'kej', 'e')]) <= 6 * 4, len(cat_ids))
        check('[Claude] Lo aprendido queda «por confirmar»', page.evaluate('JSON.parse(localStorage.getItem("naihual.aprendido") || "[]").some(x => x.estado === "por_confirmar" && x.texto === "La gente quiere empezar con calma.")'))
        n = len(calls)
        page.evaluate("window.__reply = {texto: 'Un café distinto.', lugares: ['siena'], otros: [], consejos: [], cultural: false, suficiente: true, opciones: [], aprendido: []}")
        page.click('#chips [data-chip="cafe"]')
        page.wait_for_function('n => window.__calls.length > n', arg=n, timeout=5000)
        page.wait_for_function("(() => { const m = document.querySelectorAll('.msg'); return m[m.length - 1].dataset.kind === 'ai'; })()", timeout=5000)
        lastc = page.evaluate('window.__calls')[-1][0]['content']
        check('[Claude] Los botones también los contesta Claude, con su rama y sin repetir lo ya mostrado', '"ya_mostrados":["12 Onzas"' in lastc and 'Tu rama como' in lastc and 'No repitas lugares' in lastc, lastc[-300:])
        coffea = page.evaluate("window.NAIHUAL_LUGARES.find(x => x.id === 'coffea').nombre")
        page.evaluate("n => { window.__reply = {texto: 'Otra opción con contexto.', lugares: [], otros: [{nombre: n, porque: 'x'}], consejos: ['foto'], cultural: false, suficiente: true, opciones: [], aprendido: []}; }", coffea)
        page.fill('#q', 'Recomendame algo bonito para visitar')
        page.press('#q', 'Enter')
        page.wait_for_timeout(500)
        last = page.locator('.msg').last
        check('[Claude] Si la IA nombra un lugar del catálogo, sale su ficha (no una tarjeta suelta)', last.locator('[data-place="coffea"]').count() == 1 and last.locator('[data-ia-place]').count() == 0)
        check('[Claude] Un consejo que ya salió no se repite', last.locator('.tipcard').count() == 0)
        page.click('[data-tab="inicio"]')
        page.click('[data-beta-card] [data-go="beta"]')
        check('[Claude] La beta muestra lo aprendido por confirmar', page.locator('[data-learn="por_confirmar"]').count() == 1)
        page.click('[data-learn-ok]')
        check('[Claude] Confirmar lo pasa a «Confirmado»', page.locator('[data-learn="confirmado"]').count() == 1)
        page.click('[data-tab="guia"]')
        page.fill('#q', 'Contame qué aprendiste')
        page.press('#q', 'Enter')
        page.wait_for_timeout(500)
        calls = page.evaluate('window.__calls')
        check('[Claude] Lo confirmado entra en el paso 1 de la siguiente respuesta', 'La gente quiere empezar con calma.' in calls[-1][0]['content'])
        page.evaluate("window.__reply = {tema: 'evento', guardian: 'iq', lugar_id: 'doce', titulo: 'Catación los jueves', resumen: 'Diego cuenta que hay catación.'}")
        page.click('#tabs [data-publish]')
        page.fill('[data-bform="post"] textarea[name="texto"]', 'En 12 Onzas hacen catación los jueves')
        page.click('[data-bform="post"] button[type="submit"]')
        page.wait_for_function('(JSON.parse(localStorage.getItem("naihual.beta") || "[]").filter(x => x.tipo === "post")[0] || {}).orden', timeout=5000)
        po = page.evaluate('JSON.parse(localStorage.getItem("naihual.beta")).filter(x => x.tipo === "post")[0]')
        check('[Claude] «+ Publicar»: Claude lo ordena solo (tema, guardián y lugar del catálogo)', po['orden']['guardian'] == 'iq' and po['orden']['lugar'] == 'doce' and po['orden']['tema'] == 'evento', po)
        page.click('[data-tab="inicio"]')
        page.click('[data-beta-card] [data-go="beta"]')
        check('[Claude] Tu muro muestra la publicación ordenada, con su guía', page.locator('[data-wall] [data-post-guia="iq"]').count() == 1 and 'Catación los jueves' in page.inner_text('[data-wall]'))
        page.click('[data-wall] [data-post-ok]')
        check('[Claude] Confirmarla la marca «Confirmado»', page.locator('[data-wall] [data-post="confirmado"]').count() == 1)
        page.evaluate("window.__reply = {texto: 'Ok.', lugares: [], otros: [], consejos: [], cultural: false, suficiente: true, opciones: [], aprendido: []}")
        page.click('[data-tab="guia"]')
        page.fill('#q', '¿Qué hay los jueves?')
        page.press('#q', 'Enter')
        page.wait_for_function('n => window.__calls.length > n', arg=len(calls) + 1, timeout=5000)
        check('[Claude] Lo publicado y confirmado ya lo usa el chat (paso 1)', 'catación los jueves' in page.evaluate('window.__calls')[-1][0]['content'])
        page.wait_for_function("(() => { const m = document.querySelectorAll('.msg'); return m[m.length - 1].dataset.kind === 'ai'; })()", timeout=5000)
        page.evaluate("window.__reply = {texto: 'No tengo eso todavía.', lugares: [], otros: [], consejos: [], cultural: false, suficiente: false, opciones: [], aprendido: [], no_se: true, falta: 'galerías de pintores de Comalapa'}")
        page.fill('#q', '¿Dónde venden cuadros de mi tío Juan, pintor de Comalapa?')
        page.press('#q', 'Enter')
        page.wait_for_function('JSON.parse(localStorage.getItem("naihual.aprendido") || "[]").some(x => x.estado === "por_investigar")', timeout=5000)
        apr = page.evaluate('JSON.parse(localStorage.getItem("naihual.aprendido") || "[]")')
        check('[Claude] Si no sabe, queda «para investigar» qué faltaba', any(x['estado'] == 'por_investigar' and 'galerías de pintores de Comalapa' in x['texto'] for x in apr), apr)
        check('[Claude] La pregunta tal cual no se guarda', not any('pregunta' in x or 'tío Juan' in x['texto'] for x in apr), apr)
        page.evaluate("window.__reply = {texto: '<img src=x onerror=\"window.__xss=3\">Hola', lugares: [], otros: [{nombre: '<b onmouseover=x>Raro</b>', porque: '<script>window.__xss=4</script>'}], consejos: [], cultural: false, suficiente: true, opciones: ['<i>uno</i>'], aprendido: []}")
        page.fill('#q', 'algo raro para probar')
        page.press('#q', 'Enter')
        page.wait_for_function("document.querySelectorAll('[data-kind=\"ai\"]').length >= 7", timeout=5000)
        last = page.locator('.msg').last
        check('[Claude] Seguridad: lo que responde Claude se muestra como texto, no como código', page.evaluate('window.__xss === undefined') and last.locator('img, b, i, script').count() == 0 and '<img src=x' in last.inner_text())
        page.evaluate("window.__reply = {__error: 'not_granted'}")
        page.fill('#q', 'hola de nuevo, contame algo')
        page.press('#q', 'Enter')
        page.wait_for_timeout(500)
        check('[Claude] Si no está permitido, responden las reglas y el pie lo dice', 'no está permitido' in page.locator('.msg').last.inner_text() and page.locator('[data-ai="no-disponible"]').count() == 1)
        check('[Claude] Consola sin errores', not errors, errors)
        ctx.close()

        # =============== E. Beta con la base de datos del visor (simulada) ===============
        ctx = browser.new_context(viewport={'width': 390, 'height': 844}, has_touch=True)
        page = ctx.new_page()
        errors = []
        page.on('pageerror', lambda e: errors.append(str(e)))
        page.route('**/data/config.js', lambda r: r.fulfill(status=200, content_type='application/javascript; charset=utf-8', body=js('NAIHUAL_CONFIG', PREV)))
        page.add_init_script('''(() => { const store = {}; const subs = [];
          const snap = () => ({ docs: Object.keys(store).map(id => ({ id, exists: true, data: () => Object.assign({}, store[id]), metadata: {} })), size: Object.keys(store).length, empty: !Object.keys(store).length, docChanges: () => [], metadata: {} });
          const emit = () => setTimeout(() => subs.forEach(f => f(snap())), 30);
          const db = { collection: (path) => ({ path, onSnapshot: (f) => { subs.push(f); emit(); return () => {}; },
                         add: (d) => { const id = 'd' + Object.keys(store).length; store[id] = d; emit(); return Promise.resolve({ id }); } }),
                       doc: (path) => { const id = path.split('/')[1]; return { id, path, set: (d) => { store[id] = d; emit(); return Promise.resolve(); }, update: (d) => { store[id] = Object.assign({}, store[id], d); emit(); return Promise.resolve(); }, delete: () => { delete store[id]; emit(); return Promise.resolve(); } }; } };
          window.__store = store; window.__db = db; window.__assetsDeleted = [];
          const assets = { upload: () => Promise.reject(new Error('sin subir')), delete: (id) => { window.__assetsDeleted.push(id); return Promise.resolve(); } };
          window.claude = { use: (n) => Promise.resolve(n === 'db' ? Object.freeze(db) : n === 'assets' ? Object.freeze(assets) : null) }; })();''')
        page.goto(url + '#beta')
        page.wait_for_selector('[data-beta-where="db"]', timeout=5000)
        check('[beta · visor] Dice que se guarda en la base de datos del visor', 'Claude la puede leer' in page.inner_text('main'))
        page.locator('[data-beta-new] summary').click()
        page.fill('[data-bform="nuevo"] input[name="nombre"]', 'Lugar del visor')
        page.click('[data-bform="nuevo"] button[type="submit"]')
        page.wait_for_selector('[data-beta-item="nuevo"]', timeout=5000)
        check('[beta · visor] El lugar nuevo llega a la base de datos y vuelve a la lista', page.evaluate('Object.values(window.__store).some(x => x.tipo === "nuevo" && x.nombre === "Lugar del visor")') and not page.evaluate('localStorage.getItem("naihual.beta")'))
        page.click('#tabs [data-publish]')
        page.fill('[data-bform="post"] textarea[name="texto"]', 'Publicado en el visor')
        page.click('[data-bform="post"] button[type="submit"]')
        page.wait_for_selector('[data-wall] [data-post-ok]', timeout=5000)
        page.click('[data-wall] [data-post-ok]')
        page.wait_for_selector('[data-wall] [data-post="confirmado"]', timeout=5000)
        check('[beta · visor] «+ Publicar» llega a la base de datos y «Confirmar» la actualiza', page.evaluate('Object.values(window.__store).some(x => x.tipo === "post" && x.texto === "Publicado en el visor" && x.estado === "confirmado")'))
        page.evaluate("Object.keys(window.__store).filter(k => window.__store[k].tipo === 'post').forEach(k => window.__db.doc('beta/' + k).delete())")
        page.wait_for_function("document.querySelectorAll('[data-wall] .post').length === 0", timeout=5000)
        page.evaluate("window.__db.collection('beta').add({tipo: 'nota', lugar: 'siena', nombre: 'Siena Luz', texto: 'Con foto', foto: 'https://example.invalid/f.jpg', foto_id: 'foto123', fecha: '2026-10-28T10:00:00Z'})")
        page.wait_for_function("document.querySelectorAll('[data-beta-item]').length === 2", timeout=5000)
        page.locator('[data-beta-item="nota"] [data-del-ask]').click()
        page.click('[data-del-yes]')
        page.wait_for_function("document.querySelectorAll('[data-beta-item]').length === 1", timeout=5000)
        check('[beta · visor] Borrar una anotación borra también su foto', page.evaluate('window.__assetsDeleted') == ['foto123'] and not page.evaluate('Object.values(window.__store).some(x => x.foto_id === "foto123")'))
        page.click('[data-tab="inicio"]')
        page.click('[data-go="explorar"]')
        page.locator('[data-open="p:siena"]').first.click()
        page.click('[data-beta-like="siena"]')
        page.wait_for_selector('[data-beta-like="siena"][aria-pressed="true"]', timeout=5000)
        check('[beta · visor] «Me gustó» se guarda como un solo documento por lugar', page.evaluate('window.__store["gusta-siena"] && window.__store["gusta-siena"].lugar === "siena"'))
        check('[beta · visor] Consola sin errores', not errors, errors)
        ctx.close()
        ctx, page, errors = new_page(browser, url, None, 'light', PUB, '#beta')
        check('[pública] Sin beta: ni tarjeta, ni pantalla, ni botones', page.locator('[data-beta-card], [data-beta-ficha], [data-bform]').count() == 0 and page.locator('[data-intro]').count() == 1)
        ctx.close()
        for apagada in [{'beta': False}, {'beta_fundador': False}]:
            ctx, page, errors = new_page(browser, url, None, 'light', dict(PREV, **apagada))
            check('«%s: false»: sin tarjeta de la beta' % list(apagada)[0], page.locator('[data-beta-card]').count() == 0)
            ctx.close()

        # =============== F. Teclado, accesibilidad básica y contraste ===============
        ctx, page, errors = new_page(browser, url, FIX['cuatro'], 'light', PUB)
        reached = False
        for _ in range(12):
            page.keyboard.press('Tab')
            if page.evaluate('document.activeElement && document.activeElement.id') == 'cta-cafe':
                reached = True
                break
        check('Teclado: Tab llega a «Quiero un café» en Inicio', reached)
        page.keyboard.press('Enter')
        page.wait_for_timeout(200)
        check('Teclado: Enter abre los cafés', page.locator('.cards.pilot [data-place]').count() == 3)
        def unnamed():
            return page.evaluate('''() => [...document.querySelectorAll('button, a[href], input, summary')].filter(e => e.offsetParent !== null || e.closest('dialog[open]'))
              .filter(e => e.tagName === 'SUMMARY' || !e.closest('details:not([open])'))
              .filter(e => !((e.getAttribute('aria-label') || '').trim() || (e.innerText || '').trim() || (e.placeholder || '').trim())).map(e => e.outerHTML.slice(0, 90))''')
        check('Accesibilidad básica: controles con nombre (Guía)', not unnamed(), unnamed())
        page.locator('.cards.pilot details.seal summary').first.focus()
        page.keyboard.press('Enter')
        check('Teclado: el sello se abre con Enter', page.evaluate('document.querySelector(".cards.pilot details.seal").open') is True)
        for v in ['inicio', 'rutas', 'guardados']:
            page.click('[data-tab="%s"]' % v)
            check('Accesibilidad básica: controles con nombre (%s)' % v, not unnamed(), unnamed())
        chicos = []
        for v in ['inicio', 'rutas', 'guia', 'guardados']:
            page.click('[data-tab="%s"]' % v)
            page.wait_for_timeout(100)
            chicos += page.evaluate("""() => [...document.querySelectorAll('button, a[href], summary')].filter(e => e.offsetParent !== null && !(e.tagName !== 'SUMMARY' && e.closest('details:not([open])')))
              .map(e => { const r = e.getBoundingClientRect(); return [e.outerHTML.slice(0, 50), Math.round(r.width), Math.round(r.height)]; }).filter(x => x[1] < 44 || x[2] < 44)""")
        check('Tamaño táctil: todos los controles visibles miden al menos 44 px', not chicos, chicos[:5])
        dup = page.evaluate('() => { const ids = [...document.querySelectorAll("[id]")].map(e => e.id); return ids.filter((x, i) => ids.indexOf(x) !== i); }')
        check('Accesibilidad básica: sin id duplicados', not dup, dup)
        check('Accesibilidad básica: idioma del documento', page.evaluate('document.documentElement.lang') == 'es')
        ctx.close()
        for scheme in ['light', 'dark']:
            c2, p2, e2 = new_page(browser, url, FIX['cuatro'], scheme, PREV)
            vals = {'café': contrast(p2, '#cta-cafe'), 'pestaña activa': contrast(p2, '#tabs [aria-current="page"]'), 'beta': contrast(p2, '[data-beta-card] .btn.primary')}
            p2.click('#cta-cafe')
            p2.wait_for_timeout(150)
            vals['sello verificado'] = contrast(p2, 'details.seal.ok summary')
            vals['patrocinado'] = contrast(p2, '.tag.sp')
            # Etiquetas que no siempre están en pantalla: se agregan para medirlas («Según la IA» y «Temporalmente cerrado»).
            p2.evaluate("document.querySelector('main').insertAdjacentHTML('beforeend', '<span class=\"tag check\" id=\"m-check\">Según la IA</span><span class=\"tag warn\" id=\"m-warn\">Cerrado</span>')")
            vals['según la IA'] = contrast(p2, '#m-check')
            vals['aviso'] = contrast(p2, '#m-warn')
            vals['chip café'] = contrast(p2, '#chips .chip.pilot')
            check('Contraste ≥ 4.5 en botones y etiquetas (%s)' % scheme, all(v >= 4.5 for v in vals.values()), {k: round(v, 2) for k, v in vals.items()})
            c2.close()

        # =============== H. Recorridos de turista (toques desde Inicio) y enlaces ===============
        ctx, page, errors = new_page(browser, url)
        check('Recorrido 1 · llegar sin saber nada: Inicio explica qué es, quién guía y qué hacer (0 toques)', page.locator('.hero h1').count() == 1 and page.locator('.guard-strip .gbtn').count() == 4 and page.locator('#cta-cafe').is_visible())
        page.click('#cta-cafe')
        check('Recorrido 2 · café en 1 toque', page.locator('.cards.pilot [data-place]').count() >= 1)
        page.click('[data-tab="inicio"]')
        page.locator('.route-card').first.click()
        link = page.locator('[data-route-detail] a.btn.anil')
        check('Recorrido 3 · ruta y Google Maps en 2 toques', link.count() == 1 and '/maps/dir/' in link.get_attribute('href'))
        page.click('[data-tab="guia"]')
        page.fill('#q', '¿Qué hago hoy?')
        page.press('#q', 'Enter')
        page.wait_for_timeout(100)
        check('Recorrido 4 · pregunta libre en 2 toques (pestaña y enviar)', page.locator('.msg').count() >= 3)
        page.click('[data-tab="inicio"]')
        page.locator('.route-card').first.click()
        page.click('[data-route-detail] [data-toggle]')
        page.click('[data-tab="guardados"]')
        check('Recorrido 5 · guardar y ver el plan en 3 toques', page.locator('.minimap .stop').count() >= 2)
        # Cada «Cómo llegar» y cada «Abrir ruta» se arma con el nombre, la dirección y Antigua Guatemala.
        datos = page.evaluate("window.NAIHUAL_LUGARES.filter(p => p.estado !== 'pausado' && p.estado !== 'retirado').map(p => [p.id, p.nombre, p.direccion, p.maps_url || ''])")
        page.click('[data-tab="inicio"]')
        page.click('[data-go="explorar"]')
        # Abre cada ficha y lee su botón dentro de la página, en una sola pasada (los clics dibujan al instante).
        hrefs = page.evaluate('''(ids) => ids.map(id => {
            document.querySelector('.grid [data-open="p:' + id + '"]').click();
            const a = document.querySelector('.actions a.btn[href*="maps"]'); const h = a ? a.getAttribute('href') : null;
            document.querySelector('[data-back]').click(); return h; })''', [d[0] for d in datos])
        malos = []
        for (pid, nombre, dire, murl), h in zip(datos, hrefs):
            if dire:
                href = unquote(h or '')
                if not ((murl and href == unquote(murl)) or (nombre in href and dire in href and 'Antigua Guatemala' in href)):
                    malos.append(pid)
            elif h:
                malos.append(pid + ' (sin dirección y con botón)')
        check('Enlaces · los «Cómo llegar» de los %d lugares: el enlace de Google Maps del lugar o nombre + dirección; sin dirección, sin botón' % TOTAL, len(hrefs) == TOTAL and not malos, malos)
        page.click('[data-tab="rutas"]')
        bad = []
        for rid, n in [('centro', 6), ('conventos', 4), ('norte', 4), ('tanque', 3)]:
            page.click('[data-selroute="%s"]' % rid)
            h = unquote(page.locator('[data-route-detail] a.btn.anil').get_attribute('href'))
            if h.count('Antigua Guatemala') != n or h.split('waypoints=')[1].count('|') != n - 3:
                bad.append(rid)
        check('Enlaces · las %d playlists llevan origen, destino y todas sus paradas' % N_PLAYLISTS, not bad, bad)
        check('Recorridos · consola sin errores', not errors, errors)
        ctx.close()

        # =============== G. Abrir el archivo directo ===============
        ctx = browser.new_context(viewport={'width': 390, 'height': 844})
        page = ctx.new_page()
        errs = []
        page.on('pageerror', lambda e: errs.append(str(e)))
        page.goto('file://' + os.path.join(APP, 'index.html'))
        page.wait_for_selector('.hero')
        check('Abre directo desde el archivo (file://) con los datos', page.evaluate("window.NAIHUAL_LUGARES.filter(r => r.estado !== 'retirado' && r.estado !== 'pausado').length") == TOTAL and not errs, errs)
        ctx.close()
        browser.close()
    httpd.shutdown()
    fails = [r for r in RESULTS if not r[1]]
    print('\nResultado: %d de %d pruebas pasan.' % (len(RESULTS) - len(fails), len(RESULTS)))
    return 1 if fails else 0


if __name__ == '__main__':
    sys.exit(main())
