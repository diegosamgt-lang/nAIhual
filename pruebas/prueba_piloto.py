"""Pruebas automáticas de nAIhual App 1.2 (app/index.html + app/data/*.js).

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
    page.wait_for_selector('main *')
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


def main():
    httpd, url = serve()
    with sync_playwright() as pw:
        browser = pw.chromium.launch(executable_path=EXE) if os.path.exists(EXE) else pw.chromium.launch()

        # ---------- 1. Catálogo real del proyecto ----------
        ctx, page, errors = new_page(browser, url)
        check('La app carga el catálogo real (21), la configuración y las fuentes (2)', page.evaluate('window.NAIHUAL_LUGARES.length === 21 && !!window.NAIHUAL_CONFIG && window.NAIHUAL_FUENTES.length === 2'))
        names = page.locator('#wheel .wg small').all_inner_texts()
        check("Exactamente 4 guardianes, en orden No'j, Iq', Kej, E'", names == ["No'j", "Iq'", 'Kej', "E'"], names)
        check("Empieza guiando No'j", page.locator('#wheel .wg[aria-current="true"] small').inner_text() == "No'j")
        check('La bienvenida nombra a los otros tres', "Iq', Kej o E'" in page.locator('.msg').first.inner_text())
        body = page.inner_text('body')
        check("B'atz' y Ajpu no aparecen como guardianes en la Guía", "B'atz'" not in body and 'Ajpu' not in body)
        first = page.locator('#chips .chip').first
        check('Primer chip = «Quiero un café», resaltado', first.inner_text() == 'Quiero un café' and 'pilot' in first.get_attribute('class'))
        check('390 px sin desplazamiento horizontal (Guía)', no_hscroll(page))
        page.click('[data-who]')
        cards = page.locator('#dlg .gcard b').all_inner_texts()
        check('Panel de guardianes: 4 en orden', cards == ["No'j", "Iq'", 'Kej', "E'"], cards)
        dlg = page.inner_text('#dlg')
        check('Rumbo y color con * y aviso de validación cultural', 'Oriente · rojo *' in dlg and 'Pendiente de validación cultural' in dlg)
        page.keyboard.press('Escape')

        m = pedir_cafe(page)
        check('«Quiero un café» con catálogo real: «Selección en revisión»', m.locator('.pilot-empty').count() == 1 and 'Selección en revisión' in m.inner_text())
        check('El estado vacío no ofrece enlaces', m.locator('a').count() == 0)
        for chip in ['empezar', 'horas', 'comida', 'dia', 'cultura', 'respeto']:
            page.click('#chips [data-chip="%s"]' % chip)
            page.wait_for_timeout(60)
        chat = page.inner_text('main')
        check('Guía: ningún borrador aparece como recomendación (ni fichas ni nombres)', page.locator('main [data-place]').count() == 0 and not sin_nombres(chat), sin_nombres(chat))
        check('Guía: sin enlaces de Maps mientras no haya lugares publicados', page.locator('main a[href*="google.com/maps"]').count() == 0)
        check('Guía: avisa «en revisión» donde antes recomendaba lugares', 'Esa selección está en revisión' in chat)
        check('Guía: los consejos culturales siguen, con *', 'Popol Wuj' in chat and '* Información cultural por confirmar' in chat)

        page.fill('#q', 'xyz qwerty')
        page.press('#q', 'Enter')
        page.wait_for_timeout(80)
        last = page.locator('.msg').last
        opts = last.locator('.choices .chip').all_inner_texts()
        check('Pregunta no entendida: aclaración breve con 4 opciones', opts == ['Un café', 'Cultura maya', 'Moverme con respeto', 'Por dónde empiezo'], opts)
        last.locator('.choices .chip').first.click()
        page.wait_for_timeout(80)
        check('Elegir una opción de la aclaración responde esa intención', page.locator('.msg').last.locator('.pilot-empty').count() == 1)

        seq = []
        for _ in range(4):
            page.click('#chips [data-next]')
            page.wait_for_timeout(40)
            seq.append(page.locator('#wheel .wg[aria-current="true"] small').inner_text())
        check("«Otro guía» recorre Iq' → Kej → E' → No'j", seq == ["Iq'", 'Kej', "E'", "No'j"], seq)
        for txt, want in [("quiero hablar con E'", "E'"), ("Iq'", "Iq'"), ('kej por favor', 'Kej'), ("No'j", "No'j")]:
            page.fill('#q', txt)
            page.press('#q', 'Enter')
            page.wait_for_timeout(40)
            got = page.locator('#wheel .wg[aria-current="true"] small').inner_text()
            check('Pedir por nombre: «%s»' % txt, got == want, got)
        page.fill('#q', 'quiero hablar con batz')
        page.press('#q', 'Enter')
        check("Pedir a B'atz' no lo convierte en guardián", page.locator('#wheel .wg[aria-current="true"] small').inner_text() == "No'j")

        # Explorar
        page.click('#tab-feed')
        feed = page.inner_text('main')
        check('Explorar carga', page.locator('.pagehead h1').inner_text() == 'Antigua, a tu manera')
        check('Explorar: ningún lugar ni ruta en borrador', page.locator('.pin[data-open^="p:"], .pin[data-open^="r:"]').count() == 0 and not sin_nombres(feed), sin_nombres(feed))
        check('Explorar: consejos y colección de nawales siguen', page.locator('.pin[data-open^="t:"]').count() >= 10 and page.locator('.pin[data-open="c:nawales"]').count() == 1)
        check('390 px sin desplazamiento horizontal (Explorar)', no_hscroll(page))
        page.click('[data-filter="cafe"]')
        check('Explorar · Cafés: estado «Selección en revisión»', page.locator('main .emptybox').count() == 1 and 'Selección en revisión' in page.inner_text('main'))
        page.click('[data-filter="nawal"]')
        check('Los 20 nawales siguen en Explorar', page.locator('.pin').count() == 20)
        page.click('[data-filter="all"]')
        biz = page.locator('section.biz')
        check('Tarjeta para negocios: «Círculo de Aliados Fundadores» como propuesta piloto, sin Q250 ni contacto', biz.count() == 1 and 'Propuesta piloto' in biz.inner_text() and 'Q250' not in biz.inner_text() and biz.locator('a').count() == 0)

        # Aliados Fundadores
        biz.locator('[data-go="aliados"]').click()
        al = page.inner_text('main')
        for frase in ['Propuesta piloto, pendiente de aprobación antes de contratar', 'Q250 al mes', 'primeros 3 meses desde la fecha de lanzamiento público',
                      'primeros 6 meses, contados desde tu fecha de ingreso', 'precio de renovación está pendiente de decisión', 'no hay acciones ni participación',
                      'La ventana todavía no empieza: nAIhual está en vista previa', 'La impresión del sticker no está incluida', 'un reel vertical o un carrusel de fotos',
                      'no es mensual', 'No incluye una activación individual garantizada', 'no prueban visitas ni ventas', 'Autorizar por escrito', 'El pago no cambia el orden',
                      'Datos ficticios de demostración', 'Todavía no hay formulario ni contacto']:
            check('Aliados: «%s»' % frase, frase in al)
        check('Aliados: distintivo y «Patrocinado» juntos en el ejemplo', page.locator('[data-demo="aliado"] .tag.ally').count() == 1 and page.locator('[data-demo="aliado"] .tag.sp').count() == 1)
        check('Aliados: sin formularios, campos ni enlaces de contacto o pago', page.locator('main form, main input, main textarea, main select, main a').count() == 0)
        check('Aliados: sin contador ni fechas inventadas', page.locator('[data-window="preview"]').count() == 1 and 'restan' not in al.lower() and '2026' not in al)
        check('390 px sin desplazamiento horizontal (Aliados)', no_hscroll(page))
        page.click('[data-back]')
        check('Volver desde Aliados regresa a Explorar', page.locator('.pagehead h1').inner_text() == 'Antigua, a tu manera')

        # Para vos
        page.locator('.pin[data-open="t:foto"] .heart').click()
        page.click('#tab-para')
        check('Para vos: guarda un consejo y avisa que el plan espera lugares comprobados', page.locator('.grid .pin').count() == 1 and 'Todavía no hay ninguno publicado' in page.inner_text('main') and page.locator('.plan').count() == 0)
        check('Para vos: el contador de la pestaña cuenta lo visible', page.locator('#tab-para').inner_text().endswith('· 1'))
        check('390 px sin desplazamiento horizontal (Para vos)', no_hscroll(page))

        # Vista interna
        page.click('#tab-guia')
        check('Vista interna: enlace en el pie (vista previa)', page.locator('main [data-go="taller"]').count() == 1)
        page.click('main [data-go="taller"]')
        t = page.inner_text('main')
        check('Vista interna: aviso «no la ve el visitante»', 'Vista interna del equipo · no la ve el visitante' in t)
        check('Revisión: 0 publicadas de 21 y la lista completa', 'Publicadas hoy: 0 de 21' in t and page.locator('[data-review]').count() == 21)
        check('Revisión: Coffea sin la afirmación «100 mejores», con nota interna', 'Afirmación retirada hasta tener fuente' in t)
        check('Revisión: fuentes con título, fecha, responsable, tema, versión y estado', page.locator('#taller-revision .panel').count() == 2 and 'pendiente de validación cultural' in t)
        check('390 px sin desplazamiento horizontal (Revisión)', no_hscroll(page))
        page.click('[data-review="komori"]')
        d = page.inner_text('main')
        check('Ficha interna de un borrador: aviso, «En revisión», sin Maps (sin dirección)', 'Vista interna: esta ficha está en revisión' in d and 'En revisión' in d and page.locator('main a[href*="maps"]').count() == 0)
        page.click('[data-back]')
        check('Volver desde la ficha interna regresa a Revisión', page.locator('#taller-revision').count() == 1)
        page.click('[data-sec="etapas"]')
        e = page.inner_text('main')
        check('Etapas: 4, todas «Hipótesis · sin ingresos»', page.locator('[data-stage]').count() == 4 and e.count('Hipótesis · sin ingresos') == 4)
        check('Etapas: evidencia por etapa y sin porcentajes ni tarifas inventadas', e.count('Evidencia que necesita') == 4 and '%' not in e and 'Porcentaje (no se inventa)' in e)
        check('390 px sin desplazamiento horizontal (Etapas)', no_hscroll(page))
        page.click('[data-sec="aprendizaje"]')
        a = page.inner_text('main')
        check('Aprendizaje: «Diseño futuro / no activo» y 7 pasos', 'Diseño futuro / no activo' in a and page.locator('.flow li').count() == 7)
        check('Aprendizaje: distingue contexto, patrones, base de conocimiento y reentrenamiento', all(x in a for x in ['Contexto de la conversación actual', 'Patrones entre conversaciones', 'Actualizar la base de conocimiento', 'Reentrenar un modelo']))
        check('Aprendizaje: ejemplo marcado «Datos ficticios de demostración»', 'Datos ficticios de demostración' in a)
        page.click('[data-demo-fb="si"]')
        check('Aprendizaje: la demo «¿Te sirvió?» no guarda nada', 'no se guardó ni se envió nada' in page.inner_text('main') and 'naihual.app1' not in page.evaluate('JSON.stringify(Object.keys(localStorage).filter(k => k !== "naihual.app1"))'))
        page.click('[data-sec="arquitectura"]')
        r = page.inner_text('main')
        check('Arquitectura: «sin servicios externos conectados» y 6 capas', 'sin servicios externos conectados' in r and page.locator('.layer').count() == 6)
        check('Arquitectura: registro de la última respuesta (proveedor, versión, fuentes)', 'Reglas fijas (sin IA)' in r and 'reglas-fijas 1.2' in r)
        check('Arquitectura: NotebookLM y Gemini con lo verificado y lo pendiente', 'NotebookLM Enterprise' in r and 'No confirmé' in r and 'servidor propio' in r)
        page.click('[data-sec="sistema"]')
        check('Sistema visual: colores, tipografía, botones, etiquetas, tarjeta, vacío y navegación', page.locator('.sw').count() >= 16 and page.locator('.scale').count() == 2 and page.locator('[data-demo="tarjeta"]').count() == 1 and page.locator('.mininav').count() == 1)
        check('Sistema visual: ejemplos marcados como ficticios', 'ficticios' in page.inner_text('main'))
        for sec in ['aprendizaje', 'arquitectura', 'sistema']:
            page.click('[data-sec="%s"]' % sec)
            check('390 px sin desplazamiento horizontal (%s)' % sec, no_hscroll(page))
        check('Sin llaves de API ni conexiones a servicios en el código', not any(x in open(os.path.join(APP, 'index.html'), encoding='utf-8').read() for x in ['AIza', 'generativelanguage.googleapis', 'apiKey', 'api_key=']))
        check('Red: solo archivos propios y la letra de Google Fonts', {h.split(':')[0] for h in HOSTS[id(ctx)]} <= PERMITIDOS, sorted(HOSTS[id(ctx)]))
        check('Consola sin errores (catálogo real)', not errors, errors)
        ctx.close()

        # ---------- 2. Catálogos de prueba ----------
        for name, want in [('cero', 0), ('uno', 1), ('cuatro', 3)]:
            ctx, page, errors = new_page(browser, url, FIX[name])
            m = pedir_cafe(page)
            shown = m.locator('.cards.pilot [data-place]')
            ids = [shown.nth(i).get_attribute('data-place') for i in range(shown.count())]
            check('Prueba «%s»: muestra %d café(s)' % (name, want), len(ids) == want, ids)
            if want == 0:
                check('Prueba «cero»: estado vacío claro', m.locator('.pilot-empty').count() == 1)
            bad = [i for i in ids if i in {r['id'] for r in INCOMPLETAS}]
            check('Prueba «%s»: ninguna ficha incompleta en el recorrido' % name, not bad, bad)
            for i in range(shown.count()):
                c = shown.nth(i)
                txt = c.inner_text()
                check('Prueba «%s» · %s: fuente y fecha visibles' % (name, ids[i]), 'Fuente: ' in txt and 'Comprobado el 20 oct 2026 por Persona de prueba' in txt)
                a = c.locator('a.btn')
                href = a.get_attribute('href') if a.count() else ''
                label = a.get_attribute('aria-label') if a.count() else ''
                ok = href.startswith('https://www.google.com/maps/search/?api=1&query=') and ('Calle de Prueba ' + ids[i]) in unquote(href) or href == 'https://maps.app.goo.gl/prueba'
                check('Prueba «%s» · %s: «Cómo llegar» con enlace de Maps usable y nombre accesible' % (name, ids[i]), a.count() == 1 and ok and label.startswith('Cómo llegar a '), href)
            if name == 'uno':
                check('Horario solo aparece con su fuente', 'Horario: 7:00 a 18:00' in m.inner_text())
            if name == 'cuatro':
                check('Orden = orden del catálogo (el patrocinio no lo cambia)', ids == ['a', 'b', 'c'], ids)
                check('El patrocinado se identifica', 'Patrocinado' in shown.nth(1).inner_text() and 'Patrocinado' not in shown.nth(0).inner_text())
                check('La fuente con enlace se puede abrir', shown.nth(0).locator('.trust a[href="https://example.com/fuente-a"]').count() == 1)
                check('Enlace propio de Maps se respeta', shown.nth(2).locator('a.btn').get_attribute('href') == 'https://maps.app.goo.gl/prueba')
                check('390 px sin desplazamiento horizontal (3 fichas)', no_hscroll(page))
                page.click('#lang-en')
                check('Inglés: fuente y fecha visibles', 'Checked on Oct 20, 2026 by Persona de prueba' in page.locator('.cards.pilot').last.inner_text())
                page.click('#lang-es')
                shown.nth(0).locator('.heart').click()
                page.click('#tab-para')
                check('Para vos arma un plan con un café publicado guardado', page.locator('.plan li').count() >= 1 and 'Café A' in page.inner_text('.plan'))
            page.click('#tab-feed')
            page.click('[data-filter="cafe"]')
            feed = page.inner_text('main')
            pub = page.locator('.pin[data-open^="p:"]').count()
            check('Prueba «%s»: Explorar muestra solo los publicados (%d)' % (name, {'cero': 0, 'uno': 1, 'cuatro': 4}[name]), pub == {'cero': 0, 'uno': 1, 'cuatro': 4}[name] and 'Café Sin Fuente' not in feed and 'Café Borrador' not in feed, pub)
            page.click('main [data-go="taller"]') if page.locator('main [data-go="taller"]').count() else None
            rev = page.inner_text('main')
            check('Prueba «%s»: pausado y retirado no se cargan en ninguna parte' % name, 'Café Pausado' not in rev + feed and 'Café Retirado' not in rev + feed)
            if name == 'uno':
                check('Prueba «uno»: la revisión interna lista lo que falta', 'Publicadas hoy: 1 de 10' in rev and 'Falta:' in rev and 'enlace de Maps válido' in rev and 'fecha de verificación' in rev)
            check('Prueba «%s»: consola sin errores' % name, not errors, errors)
            ctx.close()

        # ---------- 3. Configuración ----------
        casos = [
            ('vista interna apagada', {'vista_previa': True, 'vista_interna': False, 'mostrar_aliados': True, 'fecha_lanzamiento': ''}, '#revision'),
            ('sin archivo de configuración', 'sin', '#revision'),
        ]
        for nombre, cfg, h in casos:
            ctx, page, errors = new_page(browser, url, None, 'light', cfg, h)
            check('Config «%s»: no hay enlace ni acceso a la vista interna' % nombre, page.locator('[data-go="taller"]').count() == 0 and page.locator('[id^="taller-"]').count() == 0 and page.locator('.msg').count() == 1)
            check('Config «%s»: consola sin errores' % nombre, not errors, errors)
            ctx.close()
        ctx, page, errors = new_page(browser, url, None, 'light', {'vista_previa': True, 'vista_interna': True, 'mostrar_aliados': False, 'fecha_lanzamiento': ''})
        page.click('#tab-feed')
        check('Config «mostrar_aliados: false»: sin tarjeta de negocios', page.locator('section.biz').count() == 0)
        ctx.close()
        ventanas = [
            ({'vista_previa': False, 'fecha_lanzamiento': ''}, 'nodate', 'falta configurar la fecha de lanzamiento'),
            ({'vista_previa': False, 'fecha_lanzamiento': '2099-01-01'}, 'future', 'empieza el día del lanzamiento público: 1 ene 2099'),
            ({'vista_previa': False, 'fecha_lanzamiento': '2026-10-01'}, 'open', 'Inscripción abierta del 1 oct 2026 al 31 dic 2026'),
            ({'vista_previa': False, 'fecha_lanzamiento': '2026-01-01'}, 'closed', 'cerró el 31 mar 2026'),
            ({'vista_previa': True, 'fecha_lanzamiento': '2026-10-01'}, 'preview', 'está en vista previa'),
        ]
        for cfg, state, frase in ventanas:
            ctx, page, errors = new_page(browser, url, None, 'light', dict(cfg, vista_interna=True, mostrar_aliados=True), '#aliados')
            win = page.locator('[data-window]')
            check('Ventana de Aliados con %s: «%s»' % (json.dumps(cfg, ensure_ascii=False), frase), win.count() == 1 and win.get_attribute('data-window') == state and frase in win.inner_text(), win.inner_text() if win.count() else '')
            ctx.close()

        # ---------- 3b. Claude responde (simulado; no llama a Claude de verdad) ----------
        ok_reply = {'texto': 'Te cuento algo para empezar con respeto.', 'consejos': ['foto', 'inventado'], 'lugares': ['doce'], 'cultural': False, 'suficiente': True, 'opciones': ['Contame más']}
        ctx, page, errors = new_page(browser, url, None, 'light', None, '', ok_reply)
        page.wait_for_selector('[data-ai="listo"]')
        check('Claude: el pie avisa la prueba privada y que nAIhual no guarda nada', 'nAIhual no lo guarda' in page.inner_text('main'))
        page.fill('#q', '¿Qué me recomendás hacer hoy?')
        page.press('#q', 'Enter')
        check('Claude: muestra «Pensando…» y un botón para detener', page.locator('[data-kind="thinking"]').count() == 1 and page.locator('[data-stop]').count() == 1)
        page.wait_for_selector('[data-kind="ai"]')
        last = page.locator('.msg').last
        check('Claude: responde el guardián de turno con su texto', "No'j" in last.inner_text() and 'Te cuento algo para empezar con respeto.' in last.inner_text() and 'responde Claude' in last.inner_text())
        check('Claude: muestra el consejo pedido y descarta ids inventados', last.locator('.tipcard').count() == 1)
        check('Claude: un lugar en borrador nunca se muestra aunque Claude lo pida', last.locator('[data-place]').count() == 0)
        check('Claude: ofrece las opciones que propone', last.locator('[data-say="Contame más"]').count() == 1)
        calls = page.evaluate('window.__calls')
        first = calls[0][0]['content'] if calls else ''
        check('Claude: recibe las reglas, los datos y la lista de lugares que no puede nombrar', 'Usá SOLO los DATOS' in first and 'en_revision_no_nombrar' in first and '12 Onzas' in first and calls[0][-1]['content'] == '¿Qué me recomendás hacer hoy?')
        n = len(calls)
        pedir_cafe(page)
        page.wait_for_timeout(300)
        check('Claude: «Quiero un café» sigue con las reglas del piloto (no llama a Claude)', len(page.evaluate('window.__calls')) == n and page.locator('.msg').last.locator('.pilot-empty').count() == 1)
        page.fill('#q', "quiero hablar con Iq'")
        page.press('#q', 'Enter')
        page.wait_for_timeout(300)
        check('Claude: el cambio de guardián lo deciden las reglas', page.locator('#wheel .wg[aria-current="true"] small').inner_text() == "Iq'" and len(page.evaluate('window.__calls')) == n)
        page.evaluate("window.__reply = {texto: 'Andá a Coffea, es buenísimo.', lugares: [], consejos: [], cultural: false, suficiente: true, opciones: []}")
        page.fill('#q', 'Recomendame algo bonito para visitar')
        page.press('#q', 'Enter')
        page.wait_for_timeout(500)
        last = page.locator('.msg').last
        check('Claude: si nombra un lugar en revisión, se descarta y responden las reglas', 'Coffea' not in last.inner_text() and 'todavía está en revisión' in last.inner_text())
        page.evaluate("window.__reply = {__error: 'not_granted'}")
        page.fill('#q', 'hola de nuevo, contame algo')
        page.press('#q', 'Enter')
        page.wait_for_timeout(500)
        check('Claude: si no está permitido, responden las reglas y el pie lo dice', 'no está permitido' in page.locator('.msg').last.inner_text() and page.locator('[data-ai="no-disponible"]').count() == 1)
        check('Claude: consola sin errores', not errors, errors)
        ctx.close()

        # ---------- 4. Teclado y accesibilidad básica ----------
        ctx, page, errors = new_page(browser, url, FIX['cuatro'])
        reached = False
        for _ in range(30):
            page.keyboard.press('Tab')
            if page.evaluate('document.activeElement && document.activeElement.dataset.chip') == 'cafe':
                reached = True
                break
        check('Teclado: Tab llega a «Quiero un café»', reached)
        page.keyboard.press('Enter')
        page.wait_for_timeout(150)
        check('Teclado: Enter abre el recorrido', page.locator('.cards.pilot [data-place]').count() == 3)
        page.locator('.cards.pilot a.btn').first.focus()
        check('Teclado: «Cómo llegar» recibe foco y es un enlace', page.evaluate('document.activeElement.tagName') == 'A')
        def unnamed():
            return page.evaluate('''() => [...document.querySelectorAll('button, a[href], input')].filter(e => e.offsetParent !== null || e.closest('dialog[open]'))
              .filter(e => !((e.getAttribute('aria-label') || '').trim() || (e.innerText || '').trim() || (e.placeholder || '').trim())).map(e => e.outerHTML.slice(0, 80))''')
        check('Accesibilidad básica: controles con nombre (Guía)', not unnamed(), unnamed())
        page.click('main [data-go="taller"]')
        page.locator('[data-sec="aprendizaje"]').focus()
        page.keyboard.press('Enter')
        check('Teclado: las secciones internas se abren con Enter', page.locator('#taller-aprendizaje').count() == 1)
        check('Accesibilidad básica: controles con nombre (vista interna)', not unnamed(), unnamed())
        dup = page.evaluate('() => { const ids = [...document.querySelectorAll("[id]")].map(e => e.id); return ids.filter((x, i) => ids.indexOf(x) !== i); }')
        check('Accesibilidad básica: sin id duplicados', not dup, dup)
        check('Accesibilidad básica: idioma del documento', page.evaluate('document.documentElement.lang') == 'es')
        check('Consola sin errores (teclado)', not errors, errors)
        ctx.close()
        for scheme in ['light', 'dark']:
            c2, p2, e2 = new_page(browser, url, FIX['cero'], scheme)
            vals = {g: round(contrast(p2, '#wheel .wg.g-%s .av' % g), 2) for g in ['noj', 'iq', 'kej', 'e']}
            check('Contraste de los íconos de guardián ≥ 4.5 (%s)' % scheme, all(v >= 4.5 for v in vals.values()), vals)
            check('Contraste del chip «Quiero un café» ≥ 4.5 (%s)' % scheme, contrast(p2, '#chips .chip.pilot') >= 4.5)
            p2.click('main [data-go="taller"]')
            p2.click('[data-sec="etapas"]')
            check('Contraste de etiquetas «Hipótesis» y avisos ≥ 4.5 (%s)' % scheme, contrast(p2, '.tag.future') >= 4.5 and contrast(p2, '.status') >= 4.5)
            p2.click('#tab-feed')
            p2.click('[data-go="aliados"]')
            check('Contraste de «Patrocinado» y «Aliado Fundador» ≥ 4.5 (%s)' % scheme, contrast(p2, '.tag.sp') >= 4.5 and contrast(p2, '.tag.ally') >= 4.5)
            c2.close()

        # ---------- 5. Abrir el archivo directo (sin servidor) ----------
        ctx = browser.new_context(viewport={'width': 390, 'height': 844})
        page = ctx.new_page()
        errs = []
        page.on('pageerror', lambda e: errs.append(str(e)))
        page.goto('file://' + os.path.join(APP, 'index.html'))
        page.wait_for_selector('.msg')
        check('Abre directo desde el archivo (file://) con los datos', page.evaluate('window.NAIHUAL_LUGARES.length') == 21 and not errs, errs)
        ctx.close()
        browser.close()
    httpd.shutdown()
    fails = [r for r in RESULTS if not r[1]]
    print('\nResultado: %d de %d pruebas pasan.' % (len(RESULTS) - len(fails), len(RESULTS)))
    return 1 if fails else 0


if __name__ == '__main__':
    sys.exit(main())
