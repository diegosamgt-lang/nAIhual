"""Pruebas controladas. NO verifican teselas, rutas públicas ni GPS físico.
Requiere Python Playwright y Chromium instalados en el entorno.
Uso: npm start (en otro proceso), luego python tests/browser_smoke.py
"""
import base64
import json
import os
from pathlib import Path
from playwright.sync_api import sync_playwright, expect

BASE = os.environ.get('NAIHUAL_TEST_URL', 'http://127.0.0.1:3000')
PIXEL = base64.b64decode('iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mP8/x8AAwMCAO+j3ioAAAAASUVORK5CYII=')
RESULTS = []

def fixture():
    return {'code':'Ok','routes':[{'distance':330,'geometry':{'type':'LineString','coordinates':[[-90.7336,14.5586],[-90.7336,14.5606],[-90.7326,14.5606]]},'legs':[{'steps':[
        {'name':'Tramo de prueba','maneuver':{'location':[-90.7336,14.5586],'type':'depart','modifier':'straight'}},
        {'name':'Segundo tramo de prueba','maneuver':{'location':[-90.7336,14.5606],'type':'turn','modifier':'right'}},
        {'name':'','maneuver':{'location':[-90.7326,14.5606],'type':'arrive'}}]}]}]}

def setup(browser, width=390, height=844, permission=True):
    context = browser.new_context(viewport={'width':width,'height':height}, geolocation={'latitude':14.5586,'longitude':-90.7336,'accuracy':10}, permissions=['geolocation'] if permission else [])
    context.route('https://tile.openstreetmap.org/**',lambda route:route.fulfill(status=200,content_type='image/png',body=PIXEL))
    page=context.new_page()
    errors=[]
    page.on('pageerror',lambda err:errors.append(str(err)))
    return context,page,errors

def destination(page):
    page.locator('#coordinate-form summary').click()
    page.locator('#destination-lat').fill('14.5606')
    page.locator('#destination-lng').fill('-90.7326')
    page.get_by_role('button',name='Usar punto',exact=True).click()

with sync_playwright() as p:
    browser=p.chromium.launch(executable_path='/usr/bin/chromium',headless=True,args=['--no-sandbox'])
    for width,height in [(320,700),(390,844),(768,1024),(1280,800)]:
        context,page,errors=setup(browser,width,height)
        requests=[]
        def route_ok(route):
            requests.append(route.request.url)
            assert '/routed-foot/route/v1/foot/' in route.request.url
            route.fulfill(status=200,content_type='application/json',body=json.dumps(fixture()),headers={'Access-Control-Allow-Origin':'*'})
        context.route('https://routing.openstreetmap.de/**',route_ok)
        page.goto(BASE)
        page.get_by_role('link',name='Abrir el mapa').click()
        expect(page.locator('#catalog-status')).to_contain_text('Todavía no hay puntos')
        assert not requests
        page.get_by_role('button',name='Ver puntos',exact=True).click()
        expect(page.locator('#chat-log')).to_contain_text('No voy a inventar lugares')
        destination(page)
        page.locator('#route-button').click()
        expect(page.locator('#route-status')).to_contain_text('Activá tu ubicación')
        assert not requests
        page.locator('#locate-button').click()
        expect(page.locator('#location-badge')).to_contain_text('Ubicación activa')
        assert not requests
        page.locator('#route-button').click()
        expect(page.locator('#route-panel')).to_be_visible()
        expect(page.locator('#next-instruction')).to_contain_text('derecha')
        assert len(requests)==1
        context.set_geolocation({'latitude':14.5606,'longitude':-90.73265,'accuracy':10})
        expect(page.locator('#next-instruction')).to_contain_text('cerca del destino')
        context.set_geolocation({'latitude':14.57,'longitude':-90.74,'accuracy':10})
        expect(page.locator('#next-instruction')).to_contain_text('se alejó del recorrido')
        assert len(requests)==1, 'El GPS no debe consultar automáticamente el proveedor'
        assert page.evaluate('document.documentElement.scrollWidth <= innerWidth'), f'Overflow {width}'
        page.get_by_role('link',name='Propósito',exact=True).click()
        expect(page.locator('#title-proposito')).to_be_visible()
        expect(page.locator('#location-badge')).to_contain_text('desactivada')
        page.get_by_role('link',name='Explorar',exact=True).click()
        expect(page.locator('#route-panel')).to_be_hidden()
        page.locator('#chat-input').fill('<img src=x onerror="window.inyectado=1">')
        page.locator('#send-button').click()
        expect(page.locator('#chat-log')).to_contain_text('<img src=x')
        assert page.evaluate('window.inyectado === undefined')
        assert not errors,errors
        if width==390:
            Path('/tmp/naihual-validation').mkdir(exist_ok=True)
            page.screenshot(path='/tmp/naihual-validation/mobile.png',full_page=True)
        RESULTS.append(f'{width}x{height}: navegación, chat, permisos, ruta peatonal simulada, progreso, desvío, privacidad y ancho: OK')
        context.close()

    # Permiso rechazado: no geolocalización ni consulta de rutas.
    context,page,errors=setup(browser,permission=False)
    page.add_init_script("Object.defineProperty(navigator,'geolocation',{value:{watchPosition(ok,fail){setTimeout(()=>fail({code:1}),0);return 1},clearWatch(){}}})")
    page.goto(BASE+'/#explorar');page.locator('#locate-button').click()
    expect(page.locator('#map-message')).to_contain_text('No diste permiso')
    expect(page.locator('#locate-button')).to_be_enabled()
    assert not errors;context.close();RESULTS.append('Permiso denegado: error claro y botón disponible: OK')

    # Sin API en hosting estático y sin teselas/rutas: no resultados falsos.
    context,page,errors=setup(browser)
    context.route('**/api/chat',lambda route:route.fulfill(status=404,body='No encontrado'))
    context.route('https://tile.openstreetmap.org/**',lambda route:route.abort())
    context.route('https://routing.openstreetmap.de/**',lambda route:route.abort())
    page.goto(BASE+'/#explorar')
    expect(page.locator('#map-message')).to_contain_text('No pude cargar el fondo')
    page.get_by_role('button',name='Ver puntos',exact=True).click()
    expect(page.locator('#chat-log')).to_contain_text('Todavía no hay puntos curados')
    destination(page);page.locator('#locate-button').click()
    expect(page.locator('#location-badge')).to_contain_text('Ubicación activa')
    page.locator('#route-button').click()
    expect(page.locator('#route-status')).to_contain_text('No pude conectar')
    expect(page.locator('#route-panel')).to_be_hidden()
    assert not errors;context.close();RESULTS.append('Hosting sin backend, teselas bloqueadas y ruta caída: mensajes honestos, sin ruta falsa: OK')

    # Una respuesta atrasada no puede restaurar una ruta de un destino anterior.
    context,page,errors=setup(browser)
    pending=[]
    context.route('https://routing.openstreetmap.de/**',lambda route:pending.append(route))
    page.goto(BASE+'/#explorar');destination(page);page.locator('#locate-button').click()
    expect(page.locator('#location-badge')).to_contain_text('Ubicación activa')
    page.locator('#route-button').click()
    expect(page.locator('#route-status')).to_contain_text('Consultando')
    page.locator('#clear-destination').click()
    expect(page.locator('#destination-panel')).to_be_hidden()
    if pending:
        try: pending[0].fulfill(status=200,content_type='application/json',body=json.dumps(fixture()))
        except Exception: pass  # El navegador puede haber abortado ya la solicitud.
    expect(page.locator('#route-panel')).to_be_hidden()
    assert not errors;context.close();RESULTS.append('Cancelación de destino durante consulta: no reaparece una ruta anterior: OK')

    # GPS con poca precisión: no consultar rutas; datos viejos: pausar indicaciones.
    context,page,errors=setup(browser)
    page.add_init_script("Object.defineProperty(navigator,'geolocation',{value:{watchPosition(ok){window.emitLocation=ok;setTimeout(()=>ok({coords:{latitude:14.5586,longitude:-90.7336,accuracy:200},timestamp:Date.now()}),0);return 1},clearWatch(){}}})")
    calls=[]
    context.route('https://routing.openstreetmap.de/**',lambda route:(calls.append(route.request.url),route.fulfill(status=200,content_type='application/json',body=json.dumps(fixture()))))
    page.goto(BASE+'/#explorar');destination(page);page.locator('#locate-button').click()
    expect(page.locator('#location-badge')).to_contain_text('200 m')
    page.locator('#route-button').click();expect(page.locator('#route-status')).to_contain_text('poca precisión');assert not calls
    page.evaluate('emitLocation({coords:{latitude:14.5586,longitude:-90.7336,accuracy:10},timestamp:Date.now()})')
    page.locator('#route-button').click();expect(page.locator('#route-panel')).to_be_visible()
    page.evaluate('emitLocation({coords:{latitude:14.5586,longitude:-90.7336,accuracy:10},timestamp:Date.now()-60000})')
    expect(page.locator('#next-instruction')).to_contain_text('Seguimiento pausado')
    page.locator('#stop-button').click()
    page.evaluate('emitLocation({coords:{latitude:14.5586,longitude:-90.7336,accuracy:10},timestamp:Date.now()})')
    expect(page.locator('#location-badge')).to_contain_text('desactivada')
    assert not errors;context.close();RESULTS.append('GPS impreciso, posición vencida y callback después de detener: no guía con datos inválidos: OK')
    browser.close()

print('\n'.join(RESULTS))
