import time
import sys
import mysql.connector
import platform

arg = sys.argv[1]
time.sleep(5)
logfile = "C:/ProgramData/IperiusBackup/Logs/" + arg + "/LogFile.txt"
conexion = mysql.connector.connect(user="redacted",password="redacted",host="redacted",database="redacted")

def checklog(logfile):
    global Files_copy
    global Files_fail
    global Nombre_Trabajo
    notas = []
    log = open(logfile,"r",encoding="utf-16le",newline="\r\n").readlines()
    cont = 0
    for line in log:
        if line != "\r\n":
            cont= cont + 1
            if cont == 2 :
                Nombre_Trabajo = line
            if "Archivos procesados -" in line:
                L = line.split("-")
                Files_copy = L[0]
                Files_copy = Files_copy[0]
                Files_fail = L[1]
                Files_fail = Files_fail[1:10]
                Files_fail = Files_fail[0]
            elif "!Atención:" in line:
                notas.append(line)
            elif "!Error:" in line:
                notas.append(line)
    for aviso in notas :
        print(aviso)
        if "no existe o no es accesible" in aviso:
            Files_fail = "1"

def sendSQL(Archivos_OK, Archivos_NOK, Nombre_Trabajo):
    Archivos_OK = int(Archivos_OK)
    Archivos_NOK = int(Archivos_NOK)
    cursor = conexion.cursor()
    hostname = platform.node()
    checkSQL = "select hostname, Nombre_Trabajo from `iperious_backup` where hostname = '" + hostname + "'"
    hostnamecheck = cursor.execute(checkSQL)
    hostnamecheck = cursor.fetchall()
    if len(hostnamecheck) > 0 :
        for consulta in hostnamecheck:
            hostnamecheck = consulta[0]
            jobnamecheck = consulta[1]
            jobnamecheck = str(jobnamecheck)
            hostnamecheck = str(hostnamecheck)
    else:
        jobnamecheck = "NADA"
    if hostname not in hostnamecheck and Nombre_Trabajo != jobnamecheck:   
        if Archivos_NOK != 0:  
            addbackupjob = "insert into `iperious_backup`(hostname,Ficheros_Fallidos,Nombre_Trabajo) values ('" + hostname + "', " + "1" + ",'" + Nombre_Trabajo + "')"
            cursor = conexion.cursor()
            cursor.execute(addbackupjob)
            conexion.commit()
            cursor.close()
        else :
            addbackupjob = "insert into `iperious_backup`(hostname,Ficheros_Copiados,Nombre_Trabajo) values ('" + hostname + "', " + "1" + ",'" + Nombre_Trabajo + "')"
            cursor = conexion.cursor()
            cursor.execute(addbackupjob)
            conexion.commit()
            cursor.close()
    elif hostname == hostnamecheck and Nombre_Trabajo != jobnamecheck:
        if Archivos_NOK != 0:  
            addbackupjob = "insert into `iperious_backup`(hostname,Ficheros_Fallidos,Nombre_Trabajo) values ('" + hostname + "', " + "1" + ",'" + Nombre_Trabajo + "')"
            cursor = conexion.cursor()
            cursor.execute(addbackupjob)
            conexion.commit()
            cursor.close()
        else :
            addbackupjob = "insert into `iperious_backup`(hostname,Ficheros_Copiados,Nombre_Trabajo) values ('" + hostname + "', " + "1" + ",'" + Nombre_Trabajo + "')"
            cursor = conexion.cursor()
            cursor.execute(addbackupjob)
            conexion.commit()
            cursor.close()
    else:
        if Archivos_NOK != 0:  
            cursor = conexion.cursor()
            delbackupjob = "delete from iperious_backup where hostname = '" + hostname + "' and Nombre_Trabajo = '" + Nombre_Trabajo + "'"
            cursor.execute(delbackupjob)
            conexion.commit()
            addbackupjob = "insert into `iperious_backup`(hostname,Ficheros_Fallidos,Nombre_Trabajo) values ('" + hostname + "', " + "1" + ",'" + Nombre_Trabajo + "')"
            cursor.execute(addbackupjob)
            conexion.commit()
            cursor.close()
        else :
            cursor = conexion.cursor()
            delbackupjob = "delete from iperious_backup where hostname = '" + hostname + "' and Nombre_Trabajo = '" + Nombre_Trabajo + "'"
            cursor.execute(delbackupjob)
            conexion.commit()
            addbackupjob = "insert into `iperious_backup`(hostname,Ficheros_Copiados,Nombre_Trabajo) values ('" + hostname + "', " + "1" + ",'" + Nombre_Trabajo + "')"
            cursor.execute(addbackupjob)
            conexion.commit()
            cursor.close()

checklog(logfile)
sendSQL(Files_copy,Files_fail,Nombre_Trabajo)