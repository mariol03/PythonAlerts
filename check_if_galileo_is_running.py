#!/usr/bin/python3
import sys
import time
from datetime import datetime
import subprocess
import platform
import mysql.connector
from threading import Thread, Event
import pystray
import PIL.Image

# Argumento
arg = sys.argv[1]
arg = arg.lower()

# Evento de salida
salida = Event()

# Conexion con el servidor MySQL
conexion = mysql.connector.connect(user="redacted",password="redacted",host="redacted",database="redacted")

# Importar imagen, crear funcion para poder cerrar el programa y crear el icono
imagen = PIL.Image.open("triangulo.png")
def on_clicked(icon, item):
    if str(item) == "Salir":
        salida.set()
        icon.stop()
icono = pystray.Icon("Agente comprobador de servicio", imagen, "Agente comprobador de servicio",menu=pystray.Menu(
    pystray.MenuItem("Salir", on_clicked)
    ))

# Obtiene la fecha de hoy y devuele la fecha de hoy en el formato que galileo lo escribe en el log.
def getdiahoy():
    # Obtener la fecha y hora actual en formato epoch
    fecha_actual = time.time()
    # Convertir la fecha y hora actual a una estructura de tiempo
    fecha_actual = datetime.fromtimestamp(fecha_actual)
    fecha_actual = datetime.date(fecha_actual)
    fecha_actual = datetime.strftime(fecha_actual,"%d %b %Y")
    return fecha_actual

def sendMessagetoSQL(servicio):
    hostname = platform.node()
    msg = "En el equipo " + hostname + " se ha parado el servicio " + servicio
    parametros = [time.time(),msg]
    # SQL que comprueba que no haya una alerta similar
    checksql = "select mensaje from alertas where mensaje = '" + msg + "'"
    checkcursor = conexion.cursor()
    checkcursor.execute(checksql)
    listalertas = checkcursor.fetchall()
    listalertas_fix = []
    for mensaje in listalertas:
        listalertas_fix.append(str(mensaje[0]))
    if msg not in listalertas_fix:
        # SQL para insertar la alerta de nivel 3
        sql = "insert into alertas(nivel,fecha,mensaje) values (3,from_unixtime(%s),%s)"
        cursor = conexion.cursor()
        cursor.execute(sql,parametros)
        conexion.commit()

def delMessagefromSQL(servicio):
    hostname = platform.node()
    msg = "En el equipo " + hostname + " se ha parado el servicio " + servicio
    # SQL que comprueba que no haya una alerta similar
    checksql = "select id from alertas where mensaje = '" + msg + "'"
    checkcursor = conexion.cursor()
    checkcursor.execute(checksql)
    listalertas = checkcursor.fetchall()
    for id in listalertas:
        id=str(id[0])
        # SQL que borra la alerta
        sql = "delete from alertas where id = " + id
        cursor = conexion.cursor()
        cursor.execute(sql)
        conexion.commit()

def getinfofromservices(servicio):
    # Funcion que envia el mensaje por SQL
    comando = 'sc query "' + servicio + '"'
    info = subprocess.check_output(comando)
    info = info.decode("Windows-1252")
    info = info.split("\r\n")
    for line in info:
        if "STOPPED" in line:
            sendMessagetoSQL(servicio)
        elif "RUNNING" in line:
            delMessagefromSQL(servicio)

def getinfoevery2s():
    while True:
        if salida.is_set():
            break
        getinfofromservices("Galileo Control System AWS")
        time.sleep(3)

def crearicon():
    icono.run()

if arg == "servicios":
    print("servicios")
    # thread1 = Thread(target=getinfoevery2s)
    # thread2 = Thread(target=crearicon)
    # thread1.start()
    # thread2.start()
elif arg == "copia":
    print("copia")