# -*- coding: utf-8 -*-
import mysql, sys, os
import time
from mysql.connector import Error
from ofac import consulta as ofac
from policia import consulta as policia
from procuraduria import consulta as procuraduria

identidad = raw_input('Escriba Numero Identidad: ')
resPoli = policia(identidad)
resOfac = ofac(identidad)
resProcu = procuraduria(identidad)

try:
    cnx1 = mysql.connector.connect(user='root', password='', host='VR-NC-WEB-AP01', port='3307', database='caja')
    insertar = cnx1.cursor()
    insertar.execute("INSERT INTO caja.con_gov(identif,ponal,ofac,procura) VALUES (%s,%s,%s,%s)",
                     (identidad, resPoli, resOfac, resProcu))
    cnx1.commit()
    cnx1.close()
except Error as e:
    print e

print "Resultado Policia: " + resPoli + "\n"
print "Resultado Ofac: " + resOfac + "\n"
print "Resultado Procuraduria: " + resProcu + "\n"
time.sleep(30)
os.system('TASKKILL /F /IM geckodriver.exe')
sys.exit()
