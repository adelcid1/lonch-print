# -*- coding: utf-8 -*-

from escpos.printer import Usb
from datetime import datetime
import json
import unicodedata
import sys

reload(sys)
sys.setdefaultencoding('utf8')

def removeData(data):
  return ''.join((c for c in unicodedata.normalize('NFD',unicode(data)) if unicodedata.category(c) != 'Mn')).decode() 

def printOrder(data):
  try:
    p = Usb(0x0519,0x000b)
    p.set(align=u'center')
    p.image("/var/www/loncheando/lonch1.png", impl=u'bitImageColumn')
    p.set(align=u'center', font=u'b', height = 2, width = 2)
    p.text(" \n")
    p.text("ORDEN: ")
    p.text(data["billCaiCurrentCaiAssigned"] + " \n")
    p.text(datetime.strptime(data["billDate"], "%Y-%m-%d %H:%M:%S").strftime('%I:%M %p. %b %d,%Y') + " \n")
    p.text("Hora de entrega: ")
    p.text(data["billDeliveryHour"] + " \n")
    p.text("TEL: " + data["billDetailBusinessPhone"] + " \n \n")
    p.set(align=u'left', font=u'a', height = 1, width = 1)
    p.text("CLIENTE: ")
    p.text(removeData(data["billClientCompleteName"] + " \n"))
    p.text("CELULAR: ")
    p.text(data["billClientPhoneNumber"] + " \n \n")
    p.set(align=u'center', font=u'a', height = 1, width = 1)
    p.text("DETALLE DE ORDEN\n")

    for d in data["billDetail"]:
      p.text("__________________________________________\n \n")
      p.set(align=u'left', font=u'a', height = 1, width = 1)
      p.text("PRODUCTO:\n")
      p.set(align=u'right', font=u'a', height = 1, width = 1)
      p.text(removeData(d["billDetailProductName"]) + " \n \n")
      p.set(align=u'left', font=u'a', height = 1, width = 1)
      p.text("CANTIDAD: ")
      p.text(str(d["billDetailQuantity"]) + " \n \n")
      if d["billDetailOrderComments"] != "":
        p.text("DESCRIPCION:\n")
        p.set(align=u'right', font=u'a', height = 1, width = 1)
        p.text(removeData(d["billDetailOrderComments"]) + " \n")  

    p.text("__________________________________________\n \n")
    p.set(align=u'right', font=u'a', height = 1, width = 1)
    p.text("TOTAL DE PRODUCTOS: ")
    p.text(str(data["billDetailQuantity"]) + " \n \n")
    p.set(align=u'left', font=u'b', height = 2, width = 2)
    p.text("DESCRIPCION DE LA ORDEN:\n")
    p.set(align=u'right', font=u'b', height = 2, width = 2)
    p.text(removeData(data["billOrderComments"]) + " \n")
    p.text(" \n")
    p.text(" \n")
    p.text(" \n")
    p.text(" \n")
    p.cut()
  except AssertionError as error:
    print(error)
    print("no se pudo imprimir")

