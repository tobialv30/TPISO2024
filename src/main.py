
from rich.console import Console
from rich.table import Table
import round_robin


console = Console()

PrintMemoria = Table(title="Particiones de memoria")

PrintProcesos = Table(title="Procesos")

# -------------------------------------
# Ejecucion principal del planificador
# -------------------------------------

# A p_nuevos le asignamos el archivo csv
p_nuevos = round_robin.open_csv()
print(p_nuevos)

# # Una vez cargado, se ejecuta el round robin
round_robin.main_round_robin()
print(round_robin.terminados)
round_robin.print_memory_state()
round_robin.Estadisticas()