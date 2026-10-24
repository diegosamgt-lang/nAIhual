"""Pruebas automáticas de nAIhual 2.0 (app/index.html + app/data/*.js), en modo vista previa y en modo pública.

Uso (desde la raíz del repositorio):
    python3 pruebas/prueba_piloto.py

Necesita Python 3 y Playwright con Chromium (vienen instalados en el entorno de Claude Code en la nube;
no son dependencias de la app). Levanta un servidor local en 127.0.0.1, abre la app a 390 px de ancho
y usa catálogos y configuraciones de prueba (inventados solo para la prueba, nunca se publican):
0, 1 y 3 cafés, vista interna encendida o apagada, y la ventana de Aliados Fundadores con distintas fechas.
No prueba un celular real ni que Google Maps caiga en el lugar correcto: eso lo tiene que hacer una persona.
"""
import functools
import http.server
import json
import os
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
# Nombres reales del catálogo: ninguno debe verse en la experiencia del visitante mientras esté en borrador.
NOMBRES_REALES = ['12 Onzas', 'Artista de Café', 'Komori', 'Siena Luz', 'Fat Cat', 'Alegría Café', 'Coffea', 'Cazador', 'Once Once', 'Hector', 'Nikolo', 'Piña', 'Patio de la Primera',
                  'Parque Central', 'Catedral de San José', 'Palacio de los Capitanes', 'Arco de Santa Catalina', 'La Merced', 'Capuchinas', 'Santa Clara', 'San Francisco el Grande']


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


PUB = {'modo': 'publica', 'fecha_lanzamiento': '', 'mostrar_aliados': True, 'claude_responde': True}
PREV = {'modo': 'vista_previa', 'fecha_lanzamiento': '', 'mostrar_aliados': True, 'claude_responde': True}
GUARDIANES = ["No'j", "Iq'", 'Kej', "E'"]
FRASES_PROHIBIDAS = ['Caminá con respeto', '¿Cómo me porto', 'reglas fijas, sin IA', '¿En qué te ayudo', "Soy No'j", 'Tips para', 'en revisión: todavía no tengo lugares con fuente']


def ruta_norte_publicada():
    base = [('catedral', 'Catedral de San José', 'cultura', 3.6, 4.5), ('cazador', 'El Cazador Italiano', 'comida', 3, 4.4),
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

        # =============== A. VISTA PREVIA con el catálogo real ===============
        ctx, page, errors = new_page(browser, url)
        M = '[vista previa]'
        check(M + ' Carga el catálogo (21), la configuración y las fuentes (2)', page.evaluate("window.NAIHUAL_LUGARES.length === 21 && window.NAIHUAL_CONFIG.modo === 'vista_previa' && window.NAIHUAL_FUENTES.length === 2"))
        check(M + ' Inicio: portada ilustrada, «Quiero un café» y «Recién llegué»', page.locator('.hero-art svg').count() == 1 and page.locator('#cta-cafe').inner_text().strip() == 'Quiero un café' and page.locator('[data-ask="empezar"]').count() == 1)
        g = [page.locator('.guard-strip .gbtn b').nth(i).inner_text() for i in range(page.locator('.guard-strip .gbtn').count())]
        check(M + " Inicio: exactamente 4 guardianes, en orden No'j, Iq', Kej, E'", g == GUARDIANES, g)
        check(M + ' Inicio: retratos, no letras sueltas', page.locator('.guard-strip svg.portrait').count() == 4 and page.locator('.guard-strip .av').count() == 0)
        check(M + ' Inicio: 3 rutas con su mapa', page.locator('.route-card').count() == 3 and page.locator('.route-card svg path.route').count() == 3)
        check(M + ' Inicio: 4 accesos (Lugares, Cultura maya, Costumbres, Guardianes)', page.locator('.tiles .tile').count() == 4)
        biz = page.locator('section.biz')
        check(M + ' Inicio: Aliados como propuesta piloto, sin precio ni contacto', biz.count() == 1 and 'Propuesta piloto' in biz.inner_text() and 'Q250' not in biz.inner_text() and biz.locator('a').count() == 0)
        check(M + ' Botón de emergencias visible', page.locator('#sos').is_visible())
        page.click('#sos')
        check(M + ' Emergencias: «Pendiente de números oficiales», sin números', 'Pendiente de números oficiales' in page.inner_text('#dlg') and not any(ch.isdigit() for ch in page.inner_text('#dlg')))
        page.keyboard.press('Escape')
        check(M + ' 390 px sin desplazamiento horizontal (Inicio)', no_hscroll(page))
        tabs = page.locator('#tabs button').all_inner_texts()
        check(M + ' 4 pestañas: Inicio, Rutas, Guía, Guardados', [x.split('\n')[0].strip() for x in tabs] == ['Inicio', 'Rutas', 'Guía', 'Guardados'], tabs)

        # Café en 1 toque desde Inicio
        page.click('#cta-cafe')
        page.wait_for_timeout(200)
        m = page.locator('.msg').last
        cards = m.locator('.cards.pilot [data-place]')
        check(M + ' «Quiero un café» en 1 toque: abre la Guía con 3 cafés', page.locator('.guide-head').count() == 1 and cards.count() == 3)
        check(M + ' Cafés por verificar marcados una sola vez, con su sello', m.locator('details.seal[data-seal="pending"]').count() == 3 and m.locator('.tag.check').count() == 0)
        hrefs = [cards.nth(i).locator('a.btn').get_attribute('href') for i in range(3)]
        check(M + ' «Cómo llegar» de cada café es un enlace de Google Maps', all(h.startswith('https://www.google.com/maps/search/?api=1&query=') for h in hrefs), hrefs)
        check(M + " La bienvenida la da No'j, sin autopresentación", "No'j · te cuenta el porqué" in page.locator('.msg').first.inner_text() and '¿Qué tenés ganas de hacer en Antigua?' in page.locator('.msg').first.inner_text())
        for chip in ['empezar', 'horas', 'comida', 'dia', 'cultura', 'costumbres']:
            page.click('#chips [data-chip="%s"]' % chip)
            page.wait_for_timeout(60)
        chat = page.inner_text('main')
        check(M + ' Guía: respuestas con tarjetas visuales (fotos provisionales, mapas, costumbres)', page.locator('main .pcard').count() >= 3 and page.locator('main .rcard').count() >= 1 and page.locator('main .tipcard').count() >= 1)
        check(M + ' Guía: sin frases de sermón ni de sistema', not [f for f in FRASES_PROHIBIDAS if f in chat], [f for f in FRASES_PROHIBIDAS if f in chat])
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
        check(M + ' Rutas: nombres de calles y aviso «Esquema · no a escala»', page.locator('.mapframe text.lbl').count() >= 10 and 'ESQUEMA · NO A ESCALA' in page.inner_text('.mapframe').upper())
        page.click('[data-selroute="conventos"]')
        check(M + ' Rutas: elegir otra ruta la dibuja (5 paradas)', page.locator('.mapframe .stop').count() == 5 and page.locator('.stops li').count() == 5)
        h = page.locator('[data-route-detail] a.btn.anil').get_attribute('href')
        check(M + ' «Abrir ruta a pie» arma un enlace de Google Maps con origen, destino y paradas', h.startswith('https://www.google.com/maps/dir/?api=1&travelmode=walking&origin=') and '&destination=' in h and '&waypoints=' in h, h[:90])
        check(M + ' 390 px sin desplazamiento horizontal (Rutas)', no_hscroll(page))
        page.locator('.stops li button').first.click()
        d = page.inner_text('main')
        check(M + ' Ficha desde la ruta: foto provisional, sello «Por verificar» y lo que le falta', page.locator('.d-hero .ph').count() == 1 and page.locator('details.seal[data-seal="pending"]').count() == 1 and 'Le falta:' in d)
        check(M + ' Ficha: mapa chico con el lugar y «Cómo llegar»', page.locator('.minimap .pin').count() == 1 and page.locator('main a.btn[href*="google.com/maps"]').count() >= 1)
        check(M + ' 390 px sin desplazamiento horizontal (Ficha)', no_hscroll(page))
        page.click('[data-back]')
        check(M + ' «Volver» regresa a la ruta', page.locator('.mapframe').count() == 1)

        # Explorar
        page.click('[data-tab="inicio"]')
        page.click('[data-go="explorar"]')
        check(M + ' Explorar: muro visual con lugares, rutas y costumbres', page.locator('.grid [data-pin^="p:"]').count() == 21 and page.locator('.grid [data-pin^="r:"]').count() == 3)
        page.click('[data-filter="cafe"]')
        check(M + ' Explorar · Cafés: 7', page.locator('.grid [data-pin]').count() == 7)
        page.click('[data-filter="all"]')
        page.fill('#fq', 'matcha')
        page.wait_for_timeout(80)
        check(M + ' Buscar «matcha» encuentra Komori', page.locator('.grid [data-pin]').count() == 1 and 'Komori' in page.inner_text('.grid'))
        page.locator('.grid [data-open="p:komori"]').click()
        check(M + ' Ficha sin dirección: sin «Cómo llegar» y sin mapa', page.locator('main a[href*="maps"]').count() == 0 and page.locator('.minimap').count() == 0)
        page.click('[data-back]')
        page.fill('#fq', '')
        check(M + ' 390 px sin desplazamiento horizontal (Explorar)', no_hscroll(page))

        # Guardados
        page.locator('.pin-wrap:has([data-pin="r:norte"]) .heart').click()
        page.click('[data-tab="guardados"]')
        check(M + ' Guardados: arma un plan con mapa y enlace a pie', page.locator('.minimap .stop').count() == 5 and page.locator('main a.btn.anil[href*="/maps/dir/"]').count() == 1)
        check(M + ' La pestaña Guardados cuenta lo guardado', '1' in page.locator('[data-tab="guardados"]').inner_text())
        check(M + ' 390 px sin desplazamiento horizontal (Guardados)', no_hscroll(page))

        # Cultura, nawales, costumbres, guardianes
        page.click('[data-tab="inicio"]')
        page.click('[data-go="cultura"]')
        check(M + ' Cultura maya: consejos con ⓘ y acceso a los nawales', page.locator('.tipcard').count() == 9 and page.locator('.tipcard details.info').count() == 9)
        page.click('[data-go="nawales"]')
        check(M + ' Los 20 nawales, con los 4 guardianes resaltados', page.locator('.nawal').count() == 20 and page.locator('.nawal.guard').count() == 4)
        check(M + ' Aviso: nAIhual no calcula tu nawal', 'no calcula tu nawal' in page.inner_text('main'))
        page.click('[data-nawal="iq"]')
        check(M + " Nawal Iq': ficha y «Hablar con Iq'»", page.locator('.facts div').count() == 4 and page.locator('main [data-guide="iq"]').count() == 1)
        page.click('[data-tab="inicio"]')
        page.click('[data-go="costumbres"]')
        cos = page.inner_text('main')
        check(M + ' Costumbres de aquí: 2, sin sermones', page.locator('.tipcard').count() == 2 and not [f for f in FRASES_PROHIBIDAS if f in cos])
        page.click('[data-tab="inicio"]')
        page.click('[data-go="guardianes"]')
        gs = page.locator('.gfull h2').all_inner_texts()
        check(M + ' Guardianes: 4 en orden, con rumbo y ⓘ', gs == GUARDIANES and 'Oriente · rojo' in page.inner_text('main') and page.locator('details.info[data-info="guard"]').count() == 1, gs)
        check(M + ' 390 px sin desplazamiento horizontal (Guardianes)', no_hscroll(page))

        # Aliados
        page.click('[data-tab="inicio"]')
        page.click('section.biz [data-go="aliados"]')
        al = page.inner_text('main')
        for frase in ['Propuesta piloto, pendiente de aprobación antes de contratar', 'Q250 al mes', 'primeros 3 meses desde la fecha de lanzamiento público',
                      'primeros 6 meses, contados desde tu fecha de ingreso', 'precio de renovación está pendiente de decisión', 'no hay acciones ni participación',
                      'La ventana todavía no empieza: nAIhual está en vista previa', 'La impresión del sticker no está incluida', 'un reel vertical o un carrusel de fotos',
                      'no es mensual', 'No incluye una activación individual garantizada', 'no prueban visitas ni ventas', 'Autorizar por escrito', 'El pago no cambia el orden',
                      'Datos ficticios de demostración', 'Todavía no hay formulario ni contacto']:
            check(M + ' Aliados: «%s»' % frase, frase in al)
        check(M + ' Aliados: sin formularios, campos ni enlaces', page.locator('main form, main input, main textarea, main select, main a').count() == 0)
        check(M + ' Aliados: sin contador ni fechas', page.locator('[data-window="preview"]').count() == 1 and '2026' not in al)
        check(M + ' 390 px sin desplazamiento horizontal (Aliados)', no_hscroll(page))

        # Vista interna
        page.click('[data-tab="inicio"]')
        page.click('footer [data-go="taller"]')
        t = page.inner_text('main')
        check(M + ' Vista interna: aviso y revisión de las 21 fichas', 'no la ve el visitante' in t and 'Publicadas hoy: 0 de 21' in t and page.locator('[data-review]').count() == 21)
        check(M + ' Revisión: Coffea sin la frase sin fuente', 'Afirmación retirada hasta tener fuente' in t and 'Entre las 100 mejores coffee shops del mundo.' not in page.inner_text('body').replace('«Entre las 100 mejores coffee shops del mundo».', ''))
        for sec, sel, n in [('textos', '[data-copy]', 11), ('etapas', '[data-stage]', 4), ('aprendizaje', '.flow li', 7), ('arquitectura', '.layer', 6), ('sistema', '.sw', 18)]:
            page.click('[data-sec="%s"]' % sec)
            check(M + ' Vista interna · %s' % sec, page.locator(sel).count() >= n and no_hscroll(page), page.locator(sel).count())
        page.click('[data-sec="aprendizaje"]')
        a = page.inner_text('main')
        check(M + ' Aprendizaje: «Diseño futuro / no activo» y «Datos ficticios de demostración»', 'Diseño futuro / no activo' in a and 'Datos ficticios de demostración' in a)
        page.click('[data-demo-fb="si"]')
        check(M + ' La demo «¿Te sirvió?» no guarda nada', 'no se guardó ni se envió nada' in page.inner_text('main') and page.evaluate('Object.keys(localStorage).every(k => k === "naihual.app1")'))
        page.click('[data-sec="arquitectura"]')
        r = page.inner_text('main')
        check(M + ' Arquitectura: registro de la última respuesta y fuentes del mapa', 'reglas-fijas 2.0' in r and 'Wikivoyage' in r and 'NotebookLM Enterprise' in r)
        code = open(os.path.join(APP, 'index.html'), encoding='utf-8').read()
        check(M + ' Sin llaves de API ni conexiones a servicios en el código', not any(x in code for x in ['AIza', 'generativelanguage.googleapis', 'apiKey', 'api_key=']))
        check(M + ' Sin datos de lugares escritos dentro del programa', 'Coffea Cafés Especiales' not in code.split('<script>')[1].split('// ===================== CLAUDE')[0] and "name: '12 Onzas'" not in code)
        check(M + ' Red: solo archivos propios y la letra de Google Fonts', {h.split(':')[0] for h in HOSTS[id(ctx)]} <= PERMITIDOS, sorted(HOSTS[id(ctx)]))
        check(M + ' Consola sin errores', not errors, errors)
        ctx.close()

        # =============== B. PÚBLICA con el catálogo real ===============
        M = '[pública]'
        ctx, page, errors = new_page(browser, url, None, 'light', PUB, '', {'texto': 'hola', 'lugares': [], 'consejos': [], 'opciones': []})
        body = page.inner_text('main')
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
        check(M + ' Explorar: solo cultura y costumbres, sin lugares', page.locator('.grid [data-pin^="p:"]').count() == 0 and page.locator('.grid [data-pin^="t:"]').count() == 11 and not sin_nombres(ex))
        page.click('[data-filter="cafe"]')
        check(M + ' Explorar · Cafés: estado vacío diseñado', 'Esta parte todavía la estoy probando.' in page.inner_text('main'))
        page.click('[data-filter="all"]')
        page.locator('.pin-wrap:has([data-pin="t:foto"]) .heart').click()
        page.click('[data-tab="guardados"]')
        check(M + ' Guardados con un consejo: avisa que el plan espera lugares', 'Todavía no hay.' in page.inner_text('main') and page.locator('.grid [data-pin]').count() == 1)
        check(M + ' Consola sin errores', not errors, errors)
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
        check('[vista previa] Los por verificar llevan su sello; el publicado, «Verificado»', m.locator('details.seal[data-seal="ok"]').count() == 1 and m.locator('details.seal[data-seal="pending"]').count() == 2)
        ctx.close()

        # =============== D. Claude responde (vista previa, simulado) ===============
        ok_reply = {'texto': 'Te cuento algo para empezar con calma.', 'consejos': ['foto', 'inventado'], 'lugares': ['doce'], 'cultural': False, 'suficiente': True, 'opciones': ['Contame más']}
        ctx, page, errors = new_page(browser, url, None, 'light', None, '', ok_reply)
        page.wait_for_selector('[data-ai="listo"]')
        check('[Claude] Avisa la prueba privada y que nAIhual no guarda nada', 'nAIhual no lo guarda' in page.inner_text('main'))
        page.click('[data-tab="guia"]')
        page.fill('#q', '¿Qué me recomendás hacer hoy?')
        page.press('#q', 'Enter')
        check('[Claude] Muestra «pensando» y un botón para detener', page.locator('[data-kind="thinking"]').count() == 1 and page.locator('[data-stop]').count() == 1)
        page.wait_for_selector('[data-kind="ai"]')
        last = page.locator('.msg').last
        check('[Claude] Responde el guardián de turno, marcado «con Claude»', 'Te cuento algo para empezar con calma.' in last.inner_text() and 'con Claude' in last.inner_text())
        check('[Claude] Muestra el consejo pedido y descarta ids inventados', last.locator('.tipcard').count() == 1)
        check('[Claude] Un lugar no publicado nunca se muestra aunque Claude lo pida', last.locator('[data-place]').count() == 0)
        check('[Claude] Ofrece sus opciones', last.locator('[data-say="Contame más"]').count() == 1)
        calls = page.evaluate('window.__calls')
        first = calls[0][0]['content'] if calls else ''
        check('[Claude] Recibe reglas, datos y la lista de lugares que no puede nombrar', 'Usá SOLO los DATOS' in first and 'en_revision_no_nombrar' in first and calls[0][-1]['content'] == '¿Qué me recomendás hacer hoy?')
        n = len(calls)
        pedir_cafe(page)
        page.wait_for_timeout(250)
        check('[Claude] «Quiero un café» sigue con reglas fijas', len(page.evaluate('window.__calls')) == n)
        page.evaluate("window.__reply = {texto: 'Andá a Coffea, es buenísimo.', lugares: [], consejos: [], cultural: false, suficiente: true, opciones: []}")
        page.fill('#q', 'Recomendame algo bonito para visitar')
        page.press('#q', 'Enter')
        page.wait_for_timeout(500)
        check('[Claude] Si nombra un lugar por verificar, se descarta', 'Coffea' not in page.locator('.msg').last.inner_text() and 'por verificar; respondí con las reglas fijas' in page.locator('.msg').last.inner_text())
        page.evaluate("window.__reply = {__error: 'not_granted'}")
        page.fill('#q', 'hola de nuevo, contame algo')
        page.press('#q', 'Enter')
        page.wait_for_timeout(500)
        check('[Claude] Si no está permitido, responden las reglas y el pie lo dice', 'no está permitido' in page.locator('.msg').last.inner_text() and page.locator('[data-ai="no-disponible"]').count() == 1)
        check('[Claude] Consola sin errores', not errors, errors)
        ctx.close()

        # =============== E. Ventana de Aliados Fundadores ===============
        for cfg, state, frase in [
            ({'modo': 'publica', 'fecha_lanzamiento': ''}, 'nodate', 'falta configurar la fecha de lanzamiento'),
            ({'modo': 'publica', 'fecha_lanzamiento': '2099-01-01'}, 'future', 'empieza el día del lanzamiento público: 1 ene 2099'),
            ({'modo': 'publica', 'fecha_lanzamiento': '2026-10-01'}, 'open', 'Inscripción abierta del 1 oct 2026 al 31 dic 2026'),
            ({'modo': 'publica', 'fecha_lanzamiento': '2026-01-01'}, 'closed', 'cerró el 31 mar 2026'),
            ({'modo': 'vista_previa', 'fecha_lanzamiento': '2026-10-01'}, 'preview', 'está en vista previa')]:
            ctx, page, errors = new_page(browser, url, None, 'light', dict(cfg, mostrar_aliados=True), '#aliados')
            win = page.locator('[data-window]')
            check('Ventana de Aliados %s: «%s»' % (json.dumps(cfg, ensure_ascii=False), frase), win.count() == 1 and win.get_attribute('data-window') == state and frase in win.inner_text(), win.inner_text() if win.count() else '')
            ctx.close()
        ctx, page, errors = new_page(browser, url, None, 'light', dict(PREV, mostrar_aliados=False))
        check('«mostrar_aliados: false»: sin tarjeta de negocios', page.locator('section.biz').count() == 0)
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
        dup = page.evaluate('() => { const ids = [...document.querySelectorAll("[id]")].map(e => e.id); return ids.filter((x, i) => ids.indexOf(x) !== i); }')
        check('Accesibilidad básica: sin id duplicados', not dup, dup)
        check('Accesibilidad básica: idioma del documento', page.evaluate('document.documentElement.lang') == 'es')
        ctx.close()
        for scheme in ['light', 'dark']:
            c2, p2, e2 = new_page(browser, url, FIX['cuatro'], scheme, PREV)
            vals = {'café': contrast(p2, '#cta-cafe'), 'pestaña activa': contrast(p2, '#tabs [aria-current="page"]'), 'propuesta': contrast(p2, 'section.biz .tag')}
            p2.click('#cta-cafe')
            p2.wait_for_timeout(150)
            vals['sello verificado'] = contrast(p2, 'details.seal.ok summary')
            vals['patrocinado'] = contrast(p2, '.tag.sp')
            vals['por verificar'] = contrast(p2, '.tag.check') if p2.locator('.tag.check').count() else 21
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
        datos = page.evaluate("window.NAIHUAL_LUGARES.map(p => [p.id, p.nombre, p.direccion])")
        page.click('[data-tab="inicio"]')
        page.click('[data-go="explorar"]')
        malos = []
        for pid, nombre, dire in datos:
            page.locator('.grid [data-open="p:%s"]' % pid).click()
            a = page.locator('.actions a.btn[href*="maps"]')
            if dire:
                href = unquote(a.get_attribute('href')) if a.count() else ''
                if not (nombre in href and dire in href and 'Antigua Guatemala' in href):
                    malos.append(pid)
            elif a.count():
                malos.append(pid + ' (sin dirección y con botón)')
            page.click('[data-back]')
        check('Enlaces · los 21 «Cómo llegar» bien armados; sin dirección, sin botón', not malos, malos)
        page.click('[data-tab="rutas"]')
        bad = []
        for rid, n in [('centro', 6), ('conventos', 5), ('norte', 5)]:
            page.click('[data-selroute="%s"]' % rid)
            h = unquote(page.locator('[data-route-detail] a.btn.anil').get_attribute('href'))
            if h.count('Antigua Guatemala') != n or h.split('waypoints=')[1].count('|') != n - 3:
                bad.append(rid)
        check('Enlaces · las 3 rutas llevan origen, destino y todas sus paradas', not bad, bad)
        check('Recorridos · consola sin errores', not errors, errors)
        ctx.close()

        # =============== G. Abrir el archivo directo ===============
        ctx = browser.new_context(viewport={'width': 390, 'height': 844})
        page = ctx.new_page()
        errs = []
        page.on('pageerror', lambda e: errs.append(str(e)))
        page.goto('file://' + os.path.join(APP, 'index.html'))
        page.wait_for_selector('.hero')
        check('Abre directo desde el archivo (file://) con los datos', page.evaluate('window.NAIHUAL_LUGARES.length') == 21 and not errs, errs)
        ctx.close()
        browser.close()
    httpd.shutdown()
    fails = [r for r in RESULTS if not r[1]]
    print('\nResultado: %d de %d pruebas pasan.' % (len(RESULTS) - len(fails), len(RESULTS)))
    return 1 if fails else 0


if __name__ == '__main__':
    sys.exit(main())
