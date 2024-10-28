import csv
from rich.console import Console
from rich.table import Table
import os



# -----------------------------
# Parte grafica
# Funciones

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

    for proceso in p_nuevos:
        PrintProcesos.add_row(str(proceso[0]), str(proceso[1]), str(proceso[2]), str(proceso[3]), "Nuevo")

    for proceso in listo_suspendido:
        PrintProcesos.add_row(str(proceso[0]), str(proceso[1]), str(proceso[2]), str(proceso[3]), "Listo/Suspendido")

    for proceso in listos:
        PrintProcesos.add_row(str(proceso[0]), str(proceso[1]), str(proceso[2]), str(proceso[3]), "Listo")

    for proceso in ejecucion:
        PrintProcesos.add_row(str(proceso[0]), str(proceso[1]), str(proceso[2]), str(proceso[3]), "Ejecucion")

    for proceso in terminados:
        PrintProcesos.add_row(str(proceso[0]), str(proceso[1]), str(proceso[2]), str(proceso[3]), "Finalizado", style='red')


##################hasta aca es todo grafico


#EJEMPLO PANTALLA PROCESO

#        0              1           2               3
#  | id_proceso  |   Tamaño   |   Arribo    |   Irrupcion   |
# -----------------------------
# Definicion de las funciones
# -----------------------------



# -----------------------------
# PARTE LOGICA
# -----------------------------

# Se ve cuales procesos ya cumplen con el tiempo de arribo y se los lleva a la espera
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
            # y se mueve a la lista de procesos listos para ser suspendidos
            listo_suspendido.append(proceso)

            # Elimina el proceso de la lista de procesos nuevos, ya que ha sido movido
            p_nuevos.remove(proceso)
            
    # no es un evento relevante ya que no hace falta, que solo se agregan de nuevos a listo suspendido


# Si no hay 5 procesos en listos o ejecución, se los pone en listo


def verificar_multiprogramacion():

    global ejecucion
    global listos
    global listo_suspendido

    if ((len(ejecucion) + len(listos)) < 5) and (listo_suspendido):

        procesos_que_entran = 5 - len(ejecucion) - len(listos)

        # Agrega los procesos que pueden entrar en la lista de listos
        listos.extend(listo_suspendido[:procesos_que_entran])

        # Elimina los procesos que se han movido a la lista de listos
        listo_suspendido = listo_suspendido[procesos_que_entran:]

# Si hay un proceso en ejecución, reduce su tiempo restante y el quantum actual


# funcion que lleva un proceso a la lista de ejecucion
def ejecutar_proceso():

    global ejecucion_flag
    global ejecucion
    global terminados
    global quantum_actual
    
    ejecucion_flag = False

    if ejecucion:
        ejecucion[0][3] -= 1
        quantum_actual += 1

        # Verifica si el proceso se haya terminado de ejecutar lo lleva a la lista de terminados
        # Si el proceso termina de ejecutarse se debe retirar de la lista
        if ejecucion[0][3] == 0:
           
            # se habilita la bandera de evento
            ejecucion_flag=True            #cambia el proceso, luego esto genera el evento
            
            terminados.append(ejecucion[0])
            ejecucion.pop(0)
            quantum_actual = 0

            aux_principal.pop(aux_principal.index(terminados[-1]))

            # Parte de la gestion de memoria: libera la memoria reseteando los valores de dicha particion
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
        listos.append(ejecucion[0])
        ejecucion.pop(0)
        quantum_actual = 0


# Si no hay nada ejecutándose, se pone en la lista de ejecución

def verificar_procesos_ejecucion():

    global ejecucion
    global listos

    if not ejecucion and listos:
        ejecucion.append(listos[0])
        listos.pop(0)


# Funcion que pretende parar el simulador ante cada evento importante
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

    p_nuevos = []

    with open('procesos.csv', mode='r') as archivo_csv:

        # Crea un objeto lector CSV
        lector_csv = csv.reader(archivo_csv)

        # Itera a través de las filas del archivo CSV
        for fila in lector_csv:

            # Agrega los valores (con tipo int) a la lista nuevos

            #                | id_proceso  |   Tamaño   |   Arribo    |   Irrupcion   |
            p_nuevos.append([ int(fila[0]), int(fila[1]),int(fila[2]), int(fila[3])])

    print('csv abierto!!')

    # Elimina los elementos con valor > 250 de tamaño de proceso porque nunca van a poder entrar
    # filtra la lista nuevo por tamaño

   
    # Ordena la lista procesos_filtrados por tiempo de arribo (por comodidad nms)
    p_nuevos = sorted(p_nuevos, key=lambda proceso: proceso[2])

    return p_nuevos


def print_memory_state():
    print("-- Estado Actual de la Memoria --")
    
    for mem, mem_map in memory.items():
        print(f'Partición {mem}: {mem_map}')




def worst_fit(proceso):

    global best_partition
    global best_minimal_frag
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



# Parecida a la funcion best fit, la diferencia es que, aqui no se controla si esta ocupada o no
# porque simplemente ese proceso que debe hacer swap_in es porque no esta en memoria y debe ocupar la cpu
# por lo tanto debe reemplazarse en la mejor particion
def swap_in(proceso):

    global best_partition
    global best_minimal_frag
    global memory
    global memoria_secundaria
    global aux_principal

    for mem, mem_map in memory.items():
        # print(f'El proceso {proceso[0]} se encuentra recorriendo la particion {mem}')

        fragmentacion = mem_map["tam"] - proceso[1]

        if fragmentacion >= 0:
            if fragmentacion < best_minimal_frag:
                best_minimal_frag = fragmentacion
                best_partition = mem_map["tam"]

    for mem, mem_map in memory.items():
        if (best_partition == mem_map["tam"]):
            # swap out
            for swapout in aux_principal:
                if swapout[0] == mem_map["busy_for"]:
                    aux_principal.pop(aux_principal.index(swapout))
                    break

            mem_map["frag_int"] = mem_map["tam"] - proceso[1]
            mem_map["busy"] = True
            mem_map["busy_for"] = proceso[0]
            aux_principal.append(proceso)  # Swap in

    best_minimal_frag = 300
    best_partition = 300


# Ejecuta el round robin
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

        # se verifica cuales procesos ya cumplen con el tiempo de arribo y se lo lleva a la cola de espera
        verificar_tiempo_arribo()

        # "Cargar" a memoria secundaria aquellos procesos que esten en listo_suspendido
        for proceso in listo_suspendido:
            # Se fija si se encuentra en en memoria principal o Si está en memoria secundaria
            if (proceso not in aux_principal) or (proceso not in memoria_secundaria):
                memoria_secundaria.append(proceso)

        verificar_multiprogramacion()

        # Intenta aplicar best fit para los 3 primeros de listos (se agarran 3 y no 2 porque puede que no haya nada en ejecucion, para ahorrar)
        # testear que onda con el numero
        for proceso in listos[:3]:
            # Para no cargar un proceso ya cargado
            if not (((proceso[0] == memory["part1"]["busy_for"])) or ((proceso[0] == memory["part2"]["busy_for"])) or ((proceso[0] == memory["part3"]["busy_for"]))):
                worst_fit(proceso)

        ejecutar_proceso()

        # Si proceso termina, eliminarlo
        
        # imprimir tablas
        # se limpia la panatalla        
        #os.system('cls')    # comando windows
        #os.system('clear')  # por si se ejecuta en linux
        
        # como no se puede actualizar campo por campo los datos hacemos que se reimpriman las dos tablas
        resetPrintMemoria()
        resetPrintProcesos()
        
        console.print(PrintMemoria)
        console.print(PrintProcesos)


        verificar_quantum()

        verificar_procesos_ejecucion()

        
        
    
        comprobar_eventos()
        # input()

        # Al cambiar proceso de ejecucion, asegurarse que esté cargado en memoria1 (Swap in / swap out)

        if (ejecucion) and (ejecucion[0] not in aux_principal):
            swap_in(ejecucion[0])

        # Incrementa el tiempo
        print('El tiempo actual ',tiempo_actual)
        tiempo_actual += 1






# PARTE DE ESTRUCTURAS DE DATOS

memory = {
    'part1': {
        'part_id': 1,
        'tam': 110,
        'frag_int': 110,
        'busy': False,
        'busy_for': None
    },

    'part2': {
        'part_id': 2,
        'tam': 160,
        'frag_int': 160,
        'busy': False,
        'busy_for': None
    },

    'part3': {
        'part_id': 3,
        'tam': 300,
        'frag_int': 160,
        'busy': False,
        'busy_for': None
    },
}



# Nombre del archivo CSV
nombre_archivo = 'procesos.csv'

# Lista de listos que no pueden entrar por el maximo de 5
listo_suspendido = []

# Procesos que están listos
listos = []

# Procesos nuevos
p_nuevos = []

# Proceso que se está ejecutando
ejecucion = []

# Proceso terminado
terminados = []

# Memoria secundaria (Solamente la lista)
memoria_secundaria = []
aux_principal = []

# best fist
best_minimal_frag = 300
best_partition = 300


# Se inicializa el tiempo en 0 por si algun proceso arriba en ese momento
tiempo_actual = 0


# Se define el quantum que se desea (2 para el TPI) y se inicia el quantum que se va a ir contandun, un aux
quantum = 2
quantum_actual = 0


console = Console()

PrintMemoria = Table(title="Particiones de memoria")

PrintProcesos = Table(title="Procesos")



