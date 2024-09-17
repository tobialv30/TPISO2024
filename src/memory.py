

# best fist
best_minimal_frag=300
best_partition= 300 # tomo 300 porque quiero evaluar la mejor particion, y necesito tener almacenado por momentos la particion mas grande

memory = {
    'part1': {
        'part_id': 1,
        'tam': 110,
        'frag_int': 0,
        'busy': False,
        'busy_for':None
    },

    'part2': {
        'part_id': 2,
        'tam': 160,
        'frag_int': 0,
        'busy': False,
        'busy_for':None
    },
    
    'part3': {
        'part_id': 3,
        'tam': 300,
        'frag_int': 0,
        'busy': False,
        'busy_for':None
    },
}



def memory1_busy():
    return (memory['part1']['busy']) and (memory['part2']['busy']) and (memory['part3']['busy'])
    

def swap():
    return

def remove_part():
    pass




# formato de los procesos    | pid | inicio | tamaño |

# lista de listos
process = [ [ 1, 0, 100], [ 2,  0,  150], [3,0,150], [4,0,120], [5,0,160], [6,0,250],]


def best_fit_m1():
    
    global best_partition
    global best_minimal_frag
    

    
    for proc_map in process:
        print('--'*32)
        print(f'Ingresa Proceso {proc_map[0]}')


        
        # bucle que hace que un proceso recorra las particiones de memoria y ver la mejor parte
        for mem, mem_map in memory.items():
            print(f'El proceso {proc_map[0]} se encuentra recorriendo la particion {mem}')
            
            # preguntar si la particion esta ocupada, si esta en falso esta libre...
            if mem_map["busy"] == False:
                
                fragmentacion = mem_map["tam"] - proc_map[2]
                # pregunta por si el proceso entra en memoria
                if (fragmentacion) >= 0:     # puede entrar
                                     
                    # es la best?
                    if fragmentacion < best_minimal_frag:  
                        best_minimal_frag=fragmentacion
                        best_partition = mem_map["tam"]


        # una vez obtenido el mejor tamaño, se le asignara a la particion de memoria correspondiente
        
        print(f'Estado actual de memoria: ')
        print('#######'*16)

        for mem, mem_map in memory.items():
            
            # condicional que modifica las particiones si encontro la buena particion
            if (best_partition == mem_map["tam"]) and (not mem_map["busy"]):

                mem_map["frag_int"]= (mem_map["tam"]) - (proc_map[2])
                mem_map["busy"]= True
                mem_map["busy_for"]= proc_map[0]
            
            print(f'Particion: {mem}')
            print(f'Tamaño: {mem_map["tam"]}')
            print(f'Fragmentacion interna: {mem_map["frag_int"]}')
            print(f'Ocupado: {mem_map["busy"]}')
            print(f'Ocupado por: Proceso {mem_map["busy_for"]}')
            
            print('#######'*16)

        if memory1_busy():
            print('Toda la memoria 1 esta ocupada')


        best_minimal_frag = 300
        best_partition=300

        print('--'*32)
        print('- PRESIONE ENTER PARA VER LA SIGUIENTE INSTANCIA -')
        input()    
        


best_fit_m1()