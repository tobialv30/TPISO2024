
from rich.console import Console
from rich.table import Table
import round_robin


console = Console()

PrintMemoria = Table(title="Particiones de memoria")

PrintProcesos = Table(title="Procesos")


p_nuevos = round_robin.open_csv()

round_robin.main_round_robin()



round_robin.Estadisticas()