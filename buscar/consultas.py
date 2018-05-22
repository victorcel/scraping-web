# -*- coding: utf-8 -*-
import mechanize, ssl, time, mysql, os, sys
from bs4 import BeautifulSoup
from python_anticaptcha import AnticaptchaClient, ImageToTextTask
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.common.exceptions import NoSuchElementException
from mysql.connector import Error
from PIL import Image

try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    # Legacy Python that doesn't verify HTTPS certificates by default
    pass
else:
    # Handle target environment that doesn't support HTTPS verification
    ssl._create_default_https_context = _create_unverified_https_context

identidad = raw_input('Escriba Numero Identidad: ')


def policia(ident):
    options = Options()
    fp = webdriver.FirefoxProfile()
    fp.set_preference("network.proxy.type", 0)
    options.add_argument('--headless')
    ## Disable JavaScript
    fp.set_preference('javascript.enabled', False)
    fp.set_preference("permissions.default.image", 3)
    fp.set_preference('permissions.default.stylesheet', 2)
    ## Disable Flash
    fp.set_preference('dom.ipc.plugins.enabled.libflashplayer.so', 'false')
    browser = webdriver.Firefox(firefox_profile=fp, options=options)
    # browser.set_window_size(400, 600)
    identidad = ident  # '1069472297'#raw_input('Escriba Numero Identidad: ')
    browser.get('https://antecedentes.policia.gov.co:7005/WebJudicial')
    browser.implicitly_wait(5)
    elem = browser.find_element_by_id('aceptaOption:0')
    browser.execute_script("arguments[0].click();", elem)
    time.sleep(2)
    elem1 = browser.find_element_by_id('continuarBtn')
    browser.execute_script("arguments[0].click();", elem1)
    time.sleep(2)
    browser.find_element_by_id('cedulaInput').send_keys(identidad)
    time.sleep(2)
    elem2 = browser.find_element_by_id('capimg')
    time.sleep(2)
    elem2.screenshot('./captcha/' + identidad + '.png')
    try:
        imagen = Image.open('./captcha/' + identidad + '.png')
        imagen.resize((50, 20))
        imagen.show()
    except:
        print ("No ha sido posible cargar la imagen")


    captcha = raw_input('Escriba Text Imagen: ')
    os.system('TASKKILL /F /IM dllhost.exe')
    try:
        time.sleep(2)
        browser.find_element_by_id('textcaptcha').send_keys(captcha)
        time.sleep(2)
        elem = browser.find_element_by_id('j_idt20')
        browser.execute_script("arguments[0].click();", elem)
        time.sleep(2)

        # nombres = browser.find_element_by_xpath('/html/body/section[2]/form/div/div/table/tbody/tr[2]/td/span/b[3]')

        detalle = browser.find_element_by_id('form:mensajeCiudadano')
        #detalle.find_elements('<b>')
        dato= detalle.find_elements_by_tag_name('b')
        #print  len(dato)
        if len(dato)==4:
            return dato[1].text
        else:
            return dato[2].text + ' - ' + dato[3].text
        # for da in dato:
        #     print da.text
        # return dato[1].text +' '+dato[2].text
    except NoSuchElementException as err:
        print err.msg
        #print browser.find_element_by_xpath('/html/body/section[2]/form/div/div/table/tbody/tr[2]/td/span/b[2]').is_enabled()
        # if err.msg == 'Unable to locate element: /html/body/section[2]/form/div/div/table/tbody/tr[2]/td/span/b[4]':
        #     #data = browser.find_element_by_xpath(
        #     #   '/html/body/section[2]/form/div/div/table/tbody/tr[2]/td/span/b[2]').text
        #     if browser.find_element_by_xpath(
        #         '/html/body/section[2]/form/div/div/table/tbody/tr[2]/td/span/b[2]').is_displayed():
        #         return browser.find_element_by_xpath('/html/body/section[2]/form/div/div/table/tbody/tr[2]/td/span/b[2]').text
        #     else:
        return browser.find_element_by_xpath('/html/body/section[2]/form/div/div/div[1]/div/ul/li/span').text


    finally:
        browser.close()


def ofac(ident):
    url = "https://sanctionssearch.ofac.treas.gov/"
    br = mechanize.Browser()
    br.set_proxies({"http": "localhost:8888"})
    br.set_handle_robots(False)  # ignore robots
    br.open(url)
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
        resl = "EL NÚMERO DE IDENTIFICACIÓN INGRESADO NO SE ENCUENTRA REGISTRADO EN EL SISTEMA." + "\n"
    return resl


def procuraduria(ident):
    url = "https://www.procuraduria.gov.co/CertWEB/Certificado.aspx?tpo=1"
    br = mechanize.Browser()
    br.set_proxies({"http": "localhost:8888"})
    br.set_handle_robots(False)  # ignore robots
    br.open(url)
    try:
        html = BeautifulSoup(br.response().read(), "html.parser")
        entradas = html.find_all('div', {'class': 'divContenedorPGN'})
        for i, entrada in enumerate(entradas):
            titulo = entrada.find('span', {'id': 'lblPregunta'}).getText()
            print "%d - %s " % (i + 1, titulo)

        respuesta = raw_input('Escriba respuesta: ')
        identidad = ident  # raw_input('Escriba numero ID: ')
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


resPoli = policia(identidad)
resOfac = ofac(identidad)
resProcu = procuraduria(identidad)

try:
    cnx1 = mysql.connector.connect(user='root', password='', host='VR-NC-WEB-AP01', port='3307', database='caja')
    insertar = cnx1.cursor()
    insertar.execute("INSERT INTO caja.con_gov(identif,ponal,ofac,procura) VALUES (%s,%s,%s,%s)",(identidad, resPoli, resOfac, resProcu))
    cnx1.commit()
    cnx1.close()
except Error as e:
    print e
    sys.exit()

print "Resultado Policia: " + resPoli + "\n"
print "Resultado Ofac: " + resOfac + "\n"
print "Resultado Procuraduria: " + resProcu + "\n"
time.sleep(5)
os.system('TASKKILL /F /IM geckodriver.exe')
sys.exit()
