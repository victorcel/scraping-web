# -*- coding: utf-8 -*-
import mechanize
from bs4 import BeautifulSoup
import ssl

try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    # Legacy Python that doesn't verify HTTPS certificates by default
    pass
else:
    # Handle target environment that doesn't support HTTPS verification
    ssl._create_default_https_context = _create_unverified_https_context

url = "https://www.procuraduria.gov.co/CertWEB/Certificado.aspx?tpo=1"
br = mechanize.Browser()
br.set_proxies({"http": "localhost:8888"})
br.set_handle_robots(False)  # ignore robots
br.open(url)



def consulta(ident):
    try:
        html = BeautifulSoup(br.response().read(), "html.parser")
        entradas = html.find_all('div', {'class': 'divContenedorPGN'})
        for i, entrada in enumerate(entradas):
            titulo = entrada.find('span', {'id': 'lblPregunta'}).getText()
            print "%d - %s " % (i + 1, titulo)

        respuesta = raw_input('Escriba respuesta: ')
        identidad = ident#raw_input('Escriba numero ID: ')
        br.select_form(id='form1')
        br.form['ddlTipoID'] = ['1']
        br.form['txtNumID'] = identidad
        br.form['txtRespuestaPregunta'] = respuesta
        br.submit(name="btnConsultar")

        html = BeautifulSoup(br.response().read(), "html.parser")

        entradas = html.find_all('div', {'id': 'divSec'})
        for i, entrada in enumerate(entradas):
            if len(entrada) == 1:
                resl = "EL NÚMERO DE IDENTIFICACIÓN INGRESADO NO SE ENCUENTRA REGISTRADO EN EL SISTEMA."
            else:
                titulo = entrada.find('div', {'class': 'datosConsultado'}).getText()
                spans = entrada.findAll('span')
                lines = [span.getText() for span in spans]
                reporte = entrada.find('h2').getText()
                resl = "%s %s %s %s - %s " % (lines[0], lines[1], lines[2], lines[3], reporte)
        br.close()
    except AttributeError as err:
        print err
    return resl