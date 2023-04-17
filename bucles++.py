#!/usr/bin/python3
import platform
import tkinter as tk
from tkinter import ttk
import time
import schedule
import mysql.connector
from getpass import getuser

# Conexion sql (dato externo)
conexion = mysql.connector.connect(user="redacted",password="redacted",host="redacted",database="redacted")

direccion = "abajo"
visto = 0

# Añadir a la BBDD el equipo donde se esta ejecutando
hostname = platform.node()
user_equipo = getuser()
checkcomputer = "select * from equipos where NombreEquipo = '" + hostname + "' AND NombreUsuario = '" + user_equipo + "'"
checkcursor = conexion.cursor()
checkcursor.execute(checkcomputer)
listcomputer = checkcursor.fetchall()
if len(listcomputer) :
    listcomputer = listcomputer[0]
if hostname not in listcomputer:
    addcomputer = "insert into equipos(NombreEquipo,NombreUsuario) values ('" + hostname + "', '" + user_equipo + "')"
    cursor = conexion.cursor()
    cursor.execute(addcomputer)
    conexion.commit()
query = "SELECT id, nivel, fecha, mensaje, color FROM alertas where resuelto = 0 and nivel = (select max(nivel) from alertas where resuelto = 0) and (equipo = '" + user_equipo + "' or equipo = 'Todos') order by Fecha desc limit 1"

def principal():

    def conexionSQL():
        cursor = conexion.cursor()
        cursor.execute(query)
        resultados = cursor.fetchall()
        conexion.commit()
        cursor.close()
        return resultados
    
    if len(conexionSQL()):
        resultados = conexionSQL()
        resultados = resultados[0]
        idproblema = resultados[0]
        nivel = resultados[1]
        texto = resultados[3]
        colorSQL = resultados[4]
        if nivel == 0 : nivel = 5
    else:
        nivel = len(conexionSQL())
    
    if nivel:
        root = tk.Tk()
        root.title("¡¡¡Alerta!!!")
        # pantalla
        anchoPantalla = root.winfo_screenwidth()
        altoPantalla = root.winfo_screenheight()

        # ventana
        anchoVentana = anchoPantalla
        larguraVentana = altoPantalla / 4
        tamañoLetra = 30
        posicionTexto = (larguraVentana / 2) - (tamañoLetra )
        addTamañoTexto = 15

        # Deshabilitar la opción de cambiar el tamaño de la ventana
        root.resizable(False, False)

        # Crear la ventana con la anchura de la pantalla pero con un alto de X
        root.geometry("%dx%d+%d+%d" % (larguraVentana, anchoVentana, 0, 0))

        # Color predeterminado de fondo
        color = "white"
        root.configure(bg=color)

        # Configuración del movimiento
        
        movimiento = 1
        tiempoEspera = 2

        # Movimiento de la ventana
        def mover_window():
            global direccion 
            # direccion = "abajo"
            # Obtiene las coordenadas actuales de la ventana
            x = root.winfo_x()
            y = root.winfo_y()

            # Cambia la dirección si la ventana ha llegado al borde de la pantalla
            if direccion == "abajo" and y + larguraVentana > altoPantalla:
                direccion = "arriba"
            elif direccion == "arriba" and y <= 0:
                direccion = "abajo"

            # Mueve la ventana hacia arriba o hacia abajo dependiendo de la dirección actual
            if direccion == "abajo":
                y += movimiento
            else:
                y -= movimiento

            # Actualiza la posición de la ventana
            root.geometry("%dx%d+%d+%d" % (anchoVentana, larguraVentana, x, y))

            # Llama la función de nuevo después de un tiempo de espera
            root.after(tiempoEspera, mover_window)

        def color_ventana(nivel):
            global visto
            
            if nivel == 1:
                aumento = 6 #Aumento Personalizado (El maximo es 5, entonces esto hace que a la variable visto se le sume 5 y asi solo se muestre 1 vez)
                visto += aumento
                color = "orange"
                pos_x = (anchoPantalla // 2) - (anchoVentana // 2) # Calcula la posicion horizontal donde se situara la ventana # // indica division entera , es decir , se redondea
                pos_y = (altoPantalla // 2) - (larguraVentana // 2) # Calcula la posicion vertical donde se situara la ventana
                root.geometry("%dx%d+%d+%d" % (anchoVentana, larguraVentana, pos_x, pos_y)) # ventana.geometry se utiliza para establecer la geometría de la ventana, es decir, su tamaño y posición en la pantalla.
                root.after(20000,lambda:destruir()) # Muestra la ventana de nivel 1, 20 sengundos (20000 ms)
            elif nivel == 2:
                aumento = 3 #Aumento Personalizado (El maximo es 5, entonces esto hace que a la variable visto se le sume 2 y asi solo se muestre 2 veces)
                visto += aumento
                color = "brown"
                root.after(15000,lambda:destruir()) # Muestra la ventana de nivel 2, 15 sengundos (15000 ms)
                mover_window()
            elif nivel == 3:
                aumento = 2 #Aumento Personalizado (El maximo es 5, entonces esto hace que a la variable visto se le sume 3 y asi solo se muestre 2 veces)
                visto += aumento
                color = "red"
                root.after(12000,lambda:destruir()) # Muestra la ventana de nivel 3, 12 sengundos (12000 ms)
                mover_window()
            elif nivel == 4:
                aumento = 1 #Aumento Personalizado (El maximo es 5, entonces esto hace que a la variable visto se le sume 1 y asi solo se muestre 5 veces)
                visto += aumento
                color = "black"
                root.after(10000,lambda:destruir()) # Muestra la ventana de nivel 4, 10 sengundos (10000 ms)
                mover_window()
            elif nivel == 5:
                aumento = 6 #Aumento Personalizado (El maximo es 5, entonces esto hace que a la variable visto se le sume 6 y asi solo se muestre 1 vez)
                visto += aumento
                color = colorSQL #Color_Personalizado
                pos_x = (anchoPantalla // 2) - (anchoVentana // 2) # Calcula la posicion horizontal donde se situara la ventana # // indica division entera , es decir , se redondea
                pos_y = (altoPantalla // 2) - (larguraVentana // 2) # Calcula la posicion vertical donde se situara la ventana
                root.geometry("%dx%d+%d+%d" % (anchoVentana, larguraVentana, pos_x, pos_y)) # ventana.geometry se utiliza para establecer la geometría de la ventana, es decir, su tamaño y posición en la pantalla.
                root.after(8000,lambda:destruir()) # Muestra la ventana de nivel 5 (personalizada), 8 sengundos (8000 ms)

            

            root.configure(bg=color)
        # Animación del texto
            mensaje = tk.Label(root, text=texto, font=("Impact", 30), foreground="white", background=color,padx=30, pady=posicionTexto+9) #,wraplength=1500, bd=4, relief="sunken" 
            mensaje.pack(pady=posicionTexto - addTamañoTexto , anchor="center")
            mensaje.place(relx=0, rely=10)
            x, y = 1, 0
            def scroll():
                nonlocal x, y
                mensaje.place(relx=x, rely=y)
                x -= 0.0015
                if x < -1:
                    x = 1
                root.after(5, scroll)
            root.after(0, scroll)

        # Crear botón
        nose = tk.Tk()

        def destruir():
            global visto
            root.destroy()
            nose.destroy()
            if visto <= 5:
                print(visto)
                print("Es menor que 5")
            else:
                print(visto)
                visto = 0
                actualizarresuelto = "UPDATE alertas SET resuelto = 1 WHERE id = " + str(idproblema)
                update = conexion.cursor()
                update.execute(actualizarresuelto)
                conexion.commit()
                update.close()
                print("Es mayor que 5")

        boton = ttk.Button(nose, text="Cerrar ventana", command=destruir, width=20, cursor="hand2")
        boton.pack(side="bottom", padx=0, pady=0, anchor="center")

        # El boton se sobreponga a la ventana
        nose.grab_set()
        nose.focus_force()
        nose.wm_attributes("-topmost", True)

        # HAcer que la ventana se sobreponga
        root.wm_attributes("-topmost", True)

        # Ocultar botones tanto de la ventana principal como de la secundaria
        root.overrideredirect(True)
        nose.overrideredirect(True)

        # Añadir transparencia a la ventana
        root.attributes("-alpha", 0.7)

        color_ventana(nivel)
        
        root.mainloop()
        

schedule.every(2).seconds.do(principal)
while True:
    schedule.run_pending()
    time.sleep(1)