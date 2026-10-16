import csv

from src.simulacion import simular_mm1
from src.teoria import metricas_teoricas

ESCENARIOS = [
    {"escenario": 1, "lam": 2.0, "mu": 3.0, "condicion": "Sistema estable"},
    {"escenario": 2, "lam": 2.5, "mu": 3.0, "condicion": "Mayor utilizacion"},
    {"escenario": 3, "lam": 2.9, "mu": 3.0, "condicion": "Cerca de saturacion"},
]

TIEMPO_SIM = 10000
SEMILLA = 42
COLUMNAS = [
    "escenario", "lam", "mu", "rho", "L", "Lq", "W", "Wq",
    "espera_promedio", "cola_promedio", "error_Wq_%", "error_Lq_%",
]

def error_porcentual(teorico, simulado):
    return abs(teorico - simulado) / teorico * 100 
    
def ejecutar_escenario(lam, mu):
    teoria = metricas_teoricas(lam,mu)
    sim = simular_mm1(lam,mu,TIEMPO_SIM,SEMILLA)
    return {
        "lam": lam,
        "mu": mu,
        **teoria,
        "espera_promedio": sim["Wq_simulado"],
        "cola_promedio": sim["cola_promedio_en_llegadas"],
        "clientes_atendidos": sim["clientes_atendidos"],
        "tiempos_espera": sim["tiempos_espera"],
        "muestras_cola": sim["muestras_cola"],
        "error_Wq_%": error_porcentual(teoria["Wq"], sim["Wq_simulado"]),
        "error_Lq_%": error_porcentual(teoria["Lq"], sim["cola_promedio_en_llegadas"]),
    }

def tabla_comparativa(resultados, ruta="resultados/tabla.csv"):
    """Save the comparison table as CSV (console output lives in src/consola.py)."""
    with open(ruta, "w", newline="") as archivo:
        escritor = csv.DictWriter(archivo, fieldnames=COLUMNAS, extrasaction="ignore")
        escritor.writeheader()
        escritor.writerows(resultados)  