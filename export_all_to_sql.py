#!/usr/bin/python3

# Importacion de los modulos
import requests
import json
import time
import schedule
from decimal import *
import mysql.connector

# Lectura del fichero de credenciales
env_file = open(".env", "r")
username=env_file.readline()
username=username.rstrip("\n")
password=env_file.readline()
password=password.rstrip("\n")

# Conexion e inicio de sesion en el servidor
url= "http://172.16.0.99/zabbix/api_jsonrpc.php"
loginjson = {"jsonrpc":"2.0","method":"user.login","params":{"username":username,"password":password},"id":1}
datos = requests.post(url,json=loginjson)
getauth = json.loads(datos.text)
conexion = mysql.connector.connect(user="sistemascn",password="Congelados1",host="172.16.0.88",database="protoinventorywebv2")

# Definicion de funciones
# Creacion de la lista de host
def gethostlist() :
    hosts = []
    get_host = {"jsonrpc":"2.0","method":"host.get","params":{"output":["hostid"],"groupids":["22"]},"auth":getauth["result"],"id":2}
    getinfo = requests.post(url,json=get_host)
    parseinfo = json.loads(getinfo.text)
    countinfo = json.dumps(parseinfo["result"], indent=2, separators=(" , "," = "))
    for line in countinfo.split('\n'):
        if "hostid" in line:
            line = line.split("=")
            line = line[1]
            line = line[2:-1]
            hosts.append(line)
    return(hosts)

# A partir del ID del host pregunta por el nombre
def gethostname(hostid):
    gethostid = {"jsonrpc":"2.0","method":"host.get","params":{"hostids":hostid,"output":["host"]},"auth":getauth["result"],"id":3}
    execgethostid = requests.post(url,json=gethostid)
    loadhostid = json.loads(execgethostid.text)
    for dato in loadhostid["result"]:
        return(dato["host"])

# Lectura de las peticiones ICMP que realiza el serividor zabbix y las exporta al servidor SQL
def exportpingtoSQL():
    cursor= conexion.cursor()
    checkmessage = "SELECT id FROM alertas"
    cursor.execute(checkmessage)
    idalert = cursor.fetchall()
    idalert_fix = []
    for id in idalert:
        idalert_fix.append(str(id[0]))
    for host_ind in gethostlist():
        get_pings = {"jsonrpc":"2.0","method":"item.get","params":{"hostids":host_ind,"search":{"name":"PING"}},"auth":getauth["result"],"id":3}
        exec_pings = requests.post(url,json=get_pings)
        loadping = json.loads(exec_pings.text)
        for dato in loadping["result"]:
            cursor= conexion.cursor()
            idproblema = dato["itemid"]
            fechaproblema = int(time.time())
            mensaje = dato["lastvalue"]
            if mensaje == "" :
                mensaje = "Nombre de host: " + str(gethostname(host_ind)) + " --> Desconectado"
            elif mensaje == "0":
                mensaje = "Nombre de host: " + str(gethostname(host_ind)) + " --> Desconectado"
            else:
                checkcursor= conexion.cursor()
                checkmessage = "SELECT id FROM alertas"
                checkcursor.execute(checkmessage)
                listalertas = checkcursor.fetchall()
                listalertas_fix = []
                for id in listalertas:
                    listalertas_fix.append(str(id[0]))
                if idproblema in listalertas_fix:
                    delcursor= conexion.cursor()
                    borraralertaSQL = "DELETE FROM alertas where id = " + idproblema
                    delcursor.execute(borraralertaSQL)
                    conexion.commit()
                    delcursor.close()
                else:
                    continue
            if idproblema in idalert_fix:
                continue
            query = 'insert into alertas(id,nivel,fecha,mensaje) values (%s,%s,from_unixtime(%s),%s)'
            parametros = (idproblema,3,fechaproblema,mensaje)
            cursor.execute(query, parametros)
            conexion.commit()
            cursor.close()

def exportalertstoSQL():
    # Exportar los erres que han saltado en zabbix
    cursor= conexion.cursor()
    items = {"jsonrpc":"2.0","method":"problem.get","params":{"time_from":fecha2,"time_till":fecha},"auth":getauth["result"],"id":2}
    datos = requests.post(url,json=items)
    datos = json.loads(datos.text)
    listadatos = datos["result"]
    checkmessage = "SELECT id FROM alertas"
    cursor.execute(checkmessage)
    idalert = cursor.fetchall()
    idalert_fix = []
    for id in idalert:
        idalert_fix.append(str(id[0]))
    for dato in datos["result"]:
        idproblema = dato["objectid"]
        fechaproblema = dato["clock"]
        mensaje = dato["name"]
        cursor= conexion.cursor()
        if idproblema in idalert_fix:
            continue
        else:
            if "Temperature of HDD" in mensaje:
                nivelerta = "1"
                query = 'insert into alertas(id,nivel,fecha,mensaje) values (%s,%s,from_unixtime(%s),%s)'
                parametros = (idproblema,nivelerta,fechaproblema,mensaje)
                cursor.execute(query, parametros)
                conexion.commit()
                cursor.close()
            elif "(startup type automatic delayed)" in mensaje:
                nivelerta = "1"
                query = 'insert into alertas(id,nivel,fecha,mensaje) values (%s,%s,from_unixtime(%s),%s)'
                parametros = (idproblema,nivelerta,fechaproblema,mensaje)
                cursor.execute(query, parametros)
                conexion.commit()
                cursor.close()
            elif "Faulty state of volume" in mensaje:
                nivelerta = "4"
                query = 'insert into alertas(id,nivel,fecha,mensaje) values (%s,%s,from_unixtime(%s),%s)'
                parametros = (idproblema,nivelerta,fechaproblema,mensaje)
                cursor.execute(query, parametros)
                conexion.commit()
                cursor.close()
            elif "Faulty state of Pool" in mensaje:
                nivelerta = "4"
                query = 'insert into alertas(id,nivel,fecha,mensaje) values (%s,%s,from_unixtime(%s),%s)'
                parametros = (idproblema,nivelerta,fechaproblema,mensaje)
                cursor.execute(query, parametros)
                conexion.commit()
                cursor.close()
            elif "Faulty state of HDD" in mensaje:
                nivelerta = "4"
                query = 'insert into alertas(id,nivel,fecha,mensaje) values (%s,%s,from_unixtime(%s),%s)'
                parametros = (idproblema,nivelerta,fechaproblema,mensaje)
                cursor.execute(query, parametros)
                conexion.commit()
                cursor.close()
            elif "SMART failure" in mensaje:
                nivelerta = "4"
                query = 'insert into alertas(id,nivel,fecha,mensaje) values (%s,%s,from_unixtime(%s),%s)'
                parametros = (idproblema,nivelerta,fechaproblema,mensaje)
                cursor.execute(query, parametros)
                conexion.commit()
                cursor.close()
            elif "Zabbix agent" in mensaje:
                print("Agente de zabbix")
            elif "Free space is less" in mensaje:
                nivelerta = "2"
                query = 'insert into alertas(id,nivel,fecha,mensaje) values (%s,%s,from_unixtime(%s),%s)'
                parametros = (idproblema,nivelerta,fechaproblema,mensaje)
                cursor.execute(query, parametros)
                conexion.commit()
                cursor.close()
            elif "Free disk space is less" in mensaje:
                nivelerta = "2"
                query = 'insert into alertas(id,nivel,fecha,mensaje) values (%s,%s,from_unixtime(%s),%s)'
                parametros = (idproblema,nivelerta,fechaproblema,mensaje)
                cursor.execute(query, parametros)
                conexion.commit()
                cursor.close()
            elif "Reaching threshold" in mensaje:
                nivelerta = "2"
                query = 'insert into alertas(id,nivel,fecha,mensaje) values (%s,%s,from_unixtime(%s),%s)'
                parametros = (idproblema,nivelerta,fechaproblema,mensaje)
                cursor.execute(query, parametros)
                conexion.commit()
                cursor.close()
            elif "(startup type automatic)" in mensaje:
                nivelerta = "3"
                query = 'insert into alertas(id,nivel,fecha,mensaje) values (%s,%s,from_unixtime(%s),%s)'
                parametros = (idproblema,nivelerta,fechaproblema,mensaje)
                cursor.execute(query, parametros)
                conexion.commit()
                cursor.close()
            elif "unavailable by ICMP" in mensaje:
                print("No hace ping")
            else:
                print("Otra cosa")


# Consegir la fecha y hora actual y el dia de hoy en formato epoch
fecha = time.time()
fecha = int(fecha)
fecha2 = fecha - 3600

schedule.every(5).seconds.do(exportalertstoSQL)
schedule.every(5).seconds.do(exportpingtoSQL)

while True:
    schedule.run_pending()
    time.sleep(1)