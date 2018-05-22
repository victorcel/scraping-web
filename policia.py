# -*- coding: utf-8 -*-
import time

import selenium
from http import server
from pip._internal.req.req_file import break_args_options
from python_anticaptcha import ImageToTextTask, AnticaptchaClient
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.common.exceptions import NoSuchElementException
from PIL import Image
from win32com.server import exception

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
identidad = '1069472297'#raw_input('Escriba Numero Identidad: ')
browser.get('https://antecedentes.policia.gov.co:7005/WebJudicial')
browser.implicitly_wait(3)
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
elem2.screenshot('captcha/' + identidad + '.png')
try:
    imagen = Image.open('captcha/' + identidad + '.png')
    imagen.resize((50, 50))
    imagen.show()
except:
    print ("No ha sido posible cargar la imagen")
captcha = raw_input('Escriba Text Imagen: ')


try:
    time.sleep(2)# captcha_fp = open('captcha.png', 'rb')
# client = AnticaptchaClient(api_key)
# task = ImageToTextTask(captcha_fp)
# job = client.createTask(task)
# job.join()
# captcha=job.get_captcha_text()
# print job.get_captcha_text()
    browser.find_element_by_id('textcaptcha').send_keys(captcha)
    time.sleep(2)
    elem = browser.find_element_by_id('j_idt20')
    browser.execute_script("arguments[0].click();", elem)
    time.sleep(2)

    time.sleep(2)
    nombres = browser.find_element_by_xpath('/html/body/section[2]/form/div/div/table/tbody/tr[2]/td/span/b[3]')
    print  nombres.text + "\n"
    detalle = browser.find_element_by_xpath('/html/body/section[2]/form/div/div/table/tbody/tr[2]/td/span/b[4]')
    print detalle.text
except NoSuchElementException as err:
    msj = browser.find_element_by_xpath('/html/body/section[2]/form/div/div/div[1]/div/ul/li/span')
    print msj.text
browser.close()
# elem.send_keys(Keys.ESCAPE)
# elem.send_keys(Keys.RETURN)
# elem.click().perform()
