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

url = "https://sanctionssearch.ofac.treas.gov/"
br = mechanize.Browser()
br.set_proxies({"http": "localhost:8888"})
br.set_handle_robots(False)  # ignore robots
br.open(url)


def consulta(ident):
    identidad = ident
    br.select_form(name='aspnetForm')
    br.form['ctl00$MainContent$txtID'] = identidad  # '16820602'
    res = br.submit(name="ctl00$MainContent$btnSearch")
    # content = res.read()
    html = BeautifulSoup(br.response().read(), "html.parser")
    entradas = html.find_all('table', {'id': 'gvSearchResults'})
    if len(entradas) != 0:
        for i, entrada in enumerate(entradas):
            titulo = entrada.find('a', {'id': 'btnDetails'}).getText()
            resl = "%s " % (titulo)
    else:
            resl= "EL NÚMERO DE IDENTIFICACIÓN INGRESADO NO SE ENCUENTRA REGISTRADO EN EL SISTEMA."+"\n"
    return resl
