"""Punto de entrada: simula los tres escenarios de la práctica M/M/1.

Uso: python main.py
Imprime los resultados en la consola y guarda las gráficas y la tabla
comparativa en la carpeta resultados/.
"""

import os

from src.consola import (
    CONSOLA,
    mostrar_archivos,
    mostrar_encabezado,
    mostrar_escenario,
    mostrar_inestable,
    mostrar_tabla,
)
from src.experimentos import (
    ESCENARIOS,
    SEMILLA,
    TIEMPO_SIM,
    ejecutar_escenario,
    tabla_comparativa,
)
from src.graficas import graficar_cola, graficar_comparacion, graficar_esperas
from src.teoria import es_estable


def main():
    """Ejecuta todos los escenarios, muestra los resultados y genera los archivos."""
    os.makedirs("resultados", exist_ok=True)
    resultados = []  # un diccionario por escenario simulado
    archivos = []    # rutas generadas, para listarlas al final

    mostrar_encabezado(ESCENARIOS, TIEMPO_SIM, SEMILLA)

    for esc in ESCENARIOS:
        n = esc["escenario"]
        lam = esc["lam"]
        mu = esc["mu"]

        # Si lam >= mu la cola crece sin límite: el escenario no se simula
        if not es_estable(lam, mu):
            mostrar_inestable(n, lam, mu)
            continue

        # Muestra una animación de carga mientras corre la simulación
        with CONSOLA.status(f"Simulando escenario {n}..."):
            r = ejecutar_escenario(lam, mu)
        r["escenario"] = n
        resultados.append(r)
        mostrar_escenario(esc, r)

        # Gráficas propias de cada escenario
        titulo = f"Escenario {n} (lam={lam}, mu={mu})"
        ruta_cola = f"resultados/cola_esc{n}.png"
        ruta_esperas = f"resultados/esperas_esc{n}.png"
        graficar_cola(r["muestras_cola"], titulo, ruta_cola)
        graficar_esperas(r["tiempos_espera"], titulo, ruta_esperas)
        archivos += [ruta_cola, ruta_esperas]

    # Resultados que comparan los tres escenarios juntos
    tabla_comparativa(resultados)
    graficar_comparacion(resultados, "resultados/comparacion.png")
    archivos += ["resultados/comparacion.png", "resultados/tabla.csv"]

    mostrar_tabla(resultados)
    mostrar_archivos(archivos)


# Solo se ejecuta al correr "python main.py", no al importar este archivo
if __name__ == "__main__":
    main()
