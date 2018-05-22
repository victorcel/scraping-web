# -*- coding: utf-8 -*-
import time
from distutils.command.bdist_rpm import bdist_rpm

from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.common.exceptions import NoSuchElementException
from PIL import Image

options = Options()
fp = webdriver.FirefoxProfile()
fp.set_preference("network.proxy.type", 0)
#options.add_argument('--headless')
## Disable JavaScript
fp.set_preference('javascript.enabled', False)
fp.set_preference("permissions.default.image", 3)
fp.set_preference('permissions.default.stylesheet', 2)
## Disable Flash
fp.set_preference('dom.ipc.plugins.enabled.libflashplayer.so', 'false')

browser = webdriver.Firefox(firefox_profile=fp, options=options)
browser.set_window_size(300,600)
browser.get('https://aplicaciones.adres.gov.co/BDUA_Internet/Pages/ConsultarAfiliadoWeb.aspx')
browser.implicitly_wait(3)
browser.find_element_by_id('txtNumDoc').send_keys('1128058866')
time.sleep(2)
elem2 = browser.find_element_by_id('Capcha_CaptchaImageUP')
time.sleep(2)
elem2.screenshot('./captcha/Capcha_CaptchaImageUP.png')
try:
    imagen = Image.open('./captcha/Capcha_CaptchaImageUP.png')
    imagen.resize((50, 50))
    imagen.show()
except:
    print ("No ha sido posible cargar la imagen")

captcha = raw_input('Escriba Text Imagen: ')
browser.find_element_by_id('Capcha_CaptchaTextBox').send_keys(captcha)
time.sleep(2)
browser.find_element_by_id('btnConsultar').click()
time.sleep(2)

window_after = browser.window_handles[1]
browser.close()
browser.switch_to.window(window_after)
print browser.find_element_by_id('GridViewBasica').text

browser.close()
#print browser.switch_to_alert().accept()
#print browser.current_url
#browser.execute_script("arguments[0].click();", elem1)