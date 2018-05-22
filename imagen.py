from PIL import Image
import urllib, cStringIO

URL = "https://antecedentes.policia.gov.co:7005/WebJudicial/captcha.jpg"
file = cStringIO.StringIO(urllib.urlopen(URL).read())
try:
    imagen = Image.open(file)
    imagen.resize((50, 50))
    imagen.show()
except:
    print ("No ha sido posible cargar la imagen")
