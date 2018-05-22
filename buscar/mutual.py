# -*- coding: utf-8 -*-
import time

import os

import sys
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.firefox.options import Options
from selenium.common.exceptions import NoSuchElementException
from PIL import Image

options = Options()
fp = webdriver.FirefoxProfile()
fp.set_preference("network.proxy.type", 0)
# options.add_argument('--headless')
## Disable JavaScript
fp.set_preference('javascript.enabled', False)
fp.set_preference("permissions.default.image", 3)
fp.set_preference('permissions.default.stylesheet', 2)
## Disable Flash
fp.set_preference('dom.ipc.plugins.enabled.libflashplayer.so', 'false')

browser = webdriver.Firefox(firefox_profile=fp, options=options)
browser.set_window_size(400, 500)
browser.get('http://www.mutualser.com/app/consulta_afiliados_form.php')
browser.implicitly_wait(3)
estado = True
while estado:
    identidad = raw_input('Escriba Numero Identidad: ')
    browser.find_element_by_name('CodEmp').send_keys(identidad)
    time.sleep(1)
    # browser.execute_script("document.getElementById('g-recaptcha-response').style.display='enable';")
    elem2 = browser.find_element_by_id('g-recaptcha-response')
    browser.execute_script("arguments[0].setAttribute('style','display:enable;');", elem2)
    time.sleep(1)
    browser.find_element_by_id('g-recaptcha-response').send_keys('332432432edwed')
    elem = browser.find_element_by_name('Submit').click()

    msj = browser.find_element_by_xpath('/html/body/table[1]/tbody/tr[2]')
    print msj.text

    identidad=''
    time.sleep(1)
    element =browser.find_element_by_link_text('Volver a la Consulta de Afiliados')
    element.location_once_scrolled_into_view
    element.click()
dato = os.system('TASKKILL /F /IM geckodriver.exe /IM firefox.exe')
sys.exit()
