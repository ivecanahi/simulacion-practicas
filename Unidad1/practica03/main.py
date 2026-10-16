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
    os.makedirs("resultados", exist_ok=True)
    resultados = []
    archivos = []

    mostrar_encabezado(ESCENARIOS, TIEMPO_SIM, SEMILLA)

    for esc in ESCENARIOS:
        n = esc["escenario"]
        lam = esc["lam"]
        mu = esc["mu"]

        if not es_estable(lam, mu):
            mostrar_inestable(n, lam, mu)
            continue

        with CONSOLA.status(f"Simulando escenario {n}..."):
            r = ejecutar_escenario(lam, mu)
        r["escenario"] = n
        resultados.append(r)
        mostrar_escenario(esc, r)

        titulo = f"Escenario {n} (lam={lam}, mu={mu})"
        ruta_cola = f"resultados/cola_esc{n}.png"
        ruta_esperas = f"resultados/esperas_esc{n}.png"
        graficar_cola(r["muestras_cola"], titulo, ruta_cola)
        graficar_esperas(r["tiempos_espera"], titulo, ruta_esperas)
        archivos += [ruta_cola, ruta_esperas]

    tabla_comparativa(resultados)
    graficar_comparacion(resultados, "resultados/comparacion.png")
    archivos += ["resultados/comparacion.png", "resultados/tabla.csv"]

    mostrar_tabla(resultados)
    mostrar_archivos(archivos)


if __name__ == "__main__":
    main()
