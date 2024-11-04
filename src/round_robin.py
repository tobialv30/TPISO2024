import csv
from rich.console import Console
from rich.table import Table
import os



#Tablas

def resetPrintMemoria():
    global PrintMemoria

    PrintMemoria = Table(title="Particiones de memoria")

    PrintMemoria.add_column("ID", justify="right", style="cyan", no_wrap=True)
    PrintMemoria.add_column("Tamaño", style="magenta")
    PrintMemoria.add_column("Frag. Interna", style="magenta")
    PrintMemoria.add_column("En Uso", justify="right", style="green")
    PrintMemoria.add_column("Usado Por Proceso", justify="right", style="green")

    part1 = memory["part1"]
    PrintMemoria.add_row(
        str(part1["part_id"]),
        str(part1["tam"]),
        str(part1["frag_int"]),
        str(part1["busy"]),
        str(part1["busy_for"])
    )

    part2 = memory["part2"]
    PrintMemoria.add_row(
        str(part2["part_id"]),
        str(part2["tam"]),
        str(part2["frag_int"]),
        str(part2["busy"]),
        str(part2["busy_for"])
    )

    part3 = memory["part3"]
    PrintMemoria.add_row(
        str(part3["part_id"]),
        str(part3["tam"]),
        str(part3["frag_int"]),
        str(part3["busy"]),
        str(part3["busy_for"])
    )



def resetPrintProcesos():
    global PrintProcesos

    PrintProcesos = Table(title="Procesos")

    PrintProcesos.add_column("ID", justify="right", style="cyan", no_wrap=True)
    PrintProcesos.add_column("Tamaño", style="magenta")
    PrintProcesos.add_column("T. Arribo", justify="right", style="green")
    PrintProcesos.add_column("T. Irrupcion", justify="right", style="green")
    PrintProcesos.add_column("Estado", justify="right", style="green")
    PrintProcesos.add_column("Tiempo salida CPU", justify="right", style="green")

    for proceso in p_nuevos:
        PrintProcesos.add_row(str(proceso[0]), str(proceso[1]), str(proceso[2]), str(proceso[3]), "Nuevo")

    for proceso in listo_suspendido:
        PrintProcesos.add_row(str(proceso[0]), str(proceso[1]), str(proceso[2]), str(proceso[3]), "Listo/Suspendido")

    for proceso in listos:
        PrintProcesos.add_row(str(proceso[0]), str(proceso[1]), str(proceso[2]), str(proceso[3]), "Listo")

    for proceso in ejecucion:
        PrintProcesos.add_row(str(proceso[0]), str(proceso[1]), str(proceso[2]), str(proceso[3]), "Ejecucion")

    for proceso in terminados:
        PrintProcesos.add_row(str(proceso[0]), str(proceso[1]), str(proceso[2]), str(proceso[3]), "Finalizado",str(proceso[5]))







# Se carga aquellos procesos que arribaron
def verificar_tiempo_arribo():

    # Se utilizan las variables globales para acceder y modificar las listas y variables definidas fuera de la función
    global p_nuevos
    global tiempo_actual
    global listo_suspendido

    # Itera sobre cada proceso en la lista de procesos nuevos
    for proceso in p_nuevos:

        # Comprueba si el tiempo de arribo del proceso es menor o igual al tiempo actual
        if proceso[2] <= tiempo_actual:
            # Si cumple la condición, se considera que ha llegado al tiempo de arribo 
            # y se mueve a la lista de procesos listos suspendidos
            listo_suspendido.append(proceso)

            # Elimina el proceso de la lista de procesos nuevos, ya que ha sido movido
            p_nuevos.remove(proceso)
            



# Si no hay 5 procesos en listos o ejecución, se los pone en listo
def verificar_multiprogramacion():
    global ejecucion
    global listos
    global listo_suspendido
    global tiempo_actual  # Asegúrate de que este es el tiempo de CPU actual

    if (len(ejecucion) + len(listos) < 5) and listo_suspendido:    #Multiprogramacion grado 5
        procesos_que_entran = 5 - len(ejecucion) - len(listos)

        # Agrega los procesos que pueden entrar en la lista de listos
        for i in range(min(procesos_que_entran, len(listo_suspendido))):
            proceso = listo_suspendido[i]
            proceso[6] = tiempo_actual  # Guardar tiempo de CPU actual para tiempo de espera
            listos.append(proceso)

        # Elimina los procesos que se han movido a la lista de listos
        listo_suspendido = listo_suspendido[procesos_que_entran:]


# Ejecutar un proceso
def ejecutar_proceso():
    global tiempo_actual
    global ejecucion_flag
    global ejecucion
    global terminados
    global quantum_actual
    
    ejecucion_flag = False           #Bandera que sirve en caso que un proceso termine

    if ejecucion:
        ejecucion[0][3] -= 1
        quantum_actual += 1

        # Verifica si el proceso se haya terminado de ejecutar lo lleva a la lista de terminados
        if ejecucion[0][3] == 0:
           

            ejecucion_flag=True            #Para el evento de cambio
            
            terminados.append(ejecucion[0])
            terminados[-1][5]= tiempo_actual     #Para el calculo de tiempo de retorno
            ejecucion.pop(0)
            quantum_actual = 0

            aux_principal.pop(aux_principal.index(terminados[-1]))   #Saca de la lista aux MP al proceso que termino

            # Libera la memoria
            for mem, mem_map in memory.items():
                if (terminados[-1][0] == mem_map["busy_for"]):
                    mem_map["frag_int"] = mem_map["tam"]
                    mem_map["busy"] = False
                    mem_map["busy_for"] = None


# Verifica si es necesario cambiar el proceso en ejecución debido al quantum

def verificar_quantum():

    global ejecucion
    global quantum
    global quantum_actual
    global listos

    if quantum_actual == quantum and ejecucion:
        listos.append(ejecucion[0])                          #Lo pasa a listo
        ejecucion.pop(0)
        quantum_actual = 0


# Si no hay nada ejecutándose, se pone en la lista de ejecución

def verificar_procesos_ejecucion():

    global ejecucion
    global listos

    if not ejecucion and listos:
        ejecucion.append(listos[0])
        listos.pop(0)


# Detiene el simulador cuando termina un proceso
def comprobar_eventos():
    global ejecucion_flag
    global tiempo_actual
    
    # Estas condiciones van a ser de retroalimentacion al usuario, se debe parar el simulador cuando haya:
    
    if (ejecucion_flag):    # Nuevo proceso en ejecucion
        print(f'Tiempo {tiempo_actual}: Ejecucion de un Nuevo proceso')
        input()
    elif(): # 
        pass


# Abre el archivo CSV en modo lectura, filtra los primeros 10 y ordena
def open_csv():
    global p_nuevos
    global nombre_archivo
    p_nuevos = []

    with open(nombre_archivo, mode='r') as archivo_csv:

        lector_csv = csv.reader(archivo_csv)

        # Itera a través de las filas del archivo CSV
        for fila in lector_csv:

            # Agrega los valores (con tipo int) a la lista nuevos

            #                | id_proceso  |   Tamaño   |   Arribo    |   Irrupcion   | I fantasma
            p_nuevos.append([ int(fila[0]), int(fila[1]),int(fila[2]), int(fila[3]),int(fila[3]),None,None])

    print('csv abierto!!')


   
    # Ordena la lista procesos_filtrados por tiempo de arribo
    p_nuevos = sorted(p_nuevos, key=lambda proceso: proceso[2])

    return p_nuevos




def worst_fit(proceso):

    global memory
    global memoria_secundaria
    global aux_principal

    # Inicializamos la variable que almacenará el tamaño de la partición más grande disponible
    worst_partition = None
    worst_fragmentation = -1  # Fragmentación negativa para asegurar que cualquier valor positivo lo reemplace

    # Iteramos sobre las particiones de memoria
    for mem, mem_map in memory.items():

        # Si la partición no está ocupada
        if not mem_map["busy"]:
            # Calculamos el espacio que quedaría después de asignar el proceso
            fragmentacion = mem_map["tam"] - proceso[1]

            # Si la partición es suficiente para el proceso y es más grande que la anterior
            if fragmentacion >= 0 and fragmentacion > worst_fragmentation:
                worst_fragmentation = fragmentacion
                worst_partition = mem_map

    # Si encontramos una partición adecuada (la más grande)
    if worst_partition:
        # Actualizamos los datos de la partición, asignando el proceso
        worst_partition["frag_int"] = worst_partition["tam"] - proceso[1]
        worst_partition["busy"] = True
        worst_partition["busy_for"] = proceso[0]

        # Añadimos el proceso a la memoria principal
        aux_principal.append(proceso)

        # Si el proceso estaba en la memoria secundaria, lo eliminamos de ahí
        if proceso in memoria_secundaria:
            memoria_secundaria.pop(memoria_secundaria.index(proceso))

    # Reiniciamos los valores para la siguiente llamada
    worst_fragmentation = -1
    worst_partition = None



# En caso que un proceso deba hacer swapin swapout, sin importar si la mem esta ocupada

def swap_in(proceso):
    global memory
    global memoria_secundaria
    global aux_principal

    worst_partition = None
    worst_fragmentation = -1 

    #Igual a worstfit
    for mem, mem_map in memory.items():
        fragmentacion = mem_map["tam"] - proceso[1]

        if fragmentacion >= 0 and fragmentacion > worst_fragmentation:
            worst_fragmentation = fragmentacion
            worst_partition = mem


    if worst_partition is not None:
        # Realizamos el swap-out si la partición ya está ocupada
        mem_map = memory[worst_partition]
        if mem_map["busy"]:
            # Eliminamos el proceso actualmente en la partición de la memoria principal
            for swapout in aux_principal:
                if swapout[0] == mem_map["busy_for"]:
                    aux_principal.remove(swapout)
                    break

        # Asignamos el nuevo proceso a la partición seleccionada
        mem_map["frag_int"] = mem_map["tam"] - proceso[1]
        mem_map["busy"] = True
        mem_map["busy_for"] = proceso[0]
        aux_principal.append(proceso)  # Swap-in del nuevo proceso




def main_round_robin():

    global tiempo_actual
    global p_nuevos
    global listo_suspendido
    global ejecucion
    global listos
    global terminados
    global memoria_secundaria
    global aux_principal
    global memory

    # mientras haya procesos en nuevos o listo_suspendido o en ejecucion o listos se ejecuta el bucle
    while (p_nuevos) or (listo_suspendido) or (ejecucion) or (listos):

       
        verificar_tiempo_arribo()  #Procesos a cola de espera

        # Cargamos a memoria secundaria
        for proceso in listo_suspendido:
            # Se fija si se encuentra en en memoria principal o Si está en memoria secundaria
            if (proceso not in aux_principal) or (proceso not in memoria_secundaria):
                memoria_secundaria.append(proceso)

        verificar_multiprogramacion() # Hasta 5
        
        for proceso in listos[:3]:    #Parte de asignacion de memoria
            # Para no cargar un proceso ya cargado
            if not (((proceso[0] == memory["part1"]["busy_for"])) or ((proceso[0] == memory["part2"]["busy_for"])) or ((proceso[0] == memory["part3"]["busy_for"]))):
                worst_fit(proceso)


        ejecutar_proceso() #El tiempo se incrementa segundo a segundo




        #os.system('cls')    Limpiar pantalla
        

        resetPrintMemoria()                  #tabla actualizada
        resetPrintProcesos()                 #tabla actualizada
        
        console.print(PrintMemoria)
        console.print(PrintProcesos)


        verificar_quantum()                #Cambiamos de proceso si Q igual a 3

        verificar_procesos_ejecucion()     #Pasamos a ejecucion 

        
        
    
        comprobar_eventos()
       

        if (ejecucion) and (ejecucion[0] not in aux_principal):
            swap_in(ejecucion[0])                             # Como cambiamos de procesos, nos fijamos si esta en mem principal aux

    
        print('El tiempo actual ',tiempo_actual)
        tiempo_actual += 1                       # Incrementa el tiempo CPU


def Estadisticas():
    global PrintEstadisticas
    global PromRet
    global PromEsp
    
    PrintEstadisticas = Table(title="Estadisticas")
    PrintEstadisticas.add_column("ID PROCESO", justify="center", style="cyan", no_wrap=True)
    PrintEstadisticas.add_column("Tiempo de retorno", justify="center", style="magenta")
    PrintEstadisticas.add_column("Tiempo de espera", justify="center", style="green")
    
    for proceso in terminados:
        retorno = proceso[5] - proceso[2]
        PromRet = PromRet + retorno 
        Espera = retorno - proceso[6]
        PromEsp = PromEsp +  Espera
        PrintEstadisticas.add_row(str(proceso[0]),str(retorno),str(Espera))
    
    console.print(PrintEstadisticas)
    
    print('El tiempo de retorno promedio ',  PromRet/len(terminados))
    print('El tiempo de espera promedio ', PromEsp/len(terminados))




    









# Memoria

memory = {
    'part1': {
        'part_id': 1,
        'tam': 50,
        'frag_int': 50,
        'busy': False,
        'busy_for': None
    },

    'part2': {
        'part_id': 2,
        'tam': 150,
        'frag_int': 150,
        'busy': False,
        'busy_for': None
    },

    'part3': {
        'part_id': 3,
        'tam': 250,
        'frag_int': 250,
        'busy': False,
        'busy_for': None
    },
}



#Definicion de datos


nombre_archivo = 'procesos.csv'


listo_suspendido = []


listos = []


p_nuevos = []


ejecucion = []


terminados = []


memoria_secundaria = []
aux_principal = []

PromRet = 0

PromEsp = 0


tiempo_actual = 0



quantum = 3
quantum_actual = 0


console = Console()

PrintMemoria = Table(title="Particiones de memoria")

PrintProcesos = Table(title="Procesos")

PrintEstadisticas = Table(title="Estadisticas")



