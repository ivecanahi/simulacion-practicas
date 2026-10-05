"""
Punto de entrada: orquesta todo el patron MVC.

Flujo:
1. El Controller toma los datos crudos (BASE_DATA) y los procesa dos veces:
   una con el modelo original (tabla discreta) y otra con el ajustado
   (formula lineal continua).
2. La View muestra ambas tablas en consola y genera las graficas en PNG.
"""
from model import temperature_factor_discrete, temperature_factor_continuous
from controller import RainSimulationController, BASE_DATA
from view import ConsoleView, ChartView


def main():
    controller = RainSimulationController(BASE_DATA)

    # Primera pasada: Tf tomado tal cual de la tabla de la guia (discreto).
    original_records = controller.run(temperature_factor_discrete)
    # Segunda pasada: Tf calculado con la formula lineal ajustada.
    adjusted_records = controller.run(temperature_factor_continuous)

    ConsoleView.show_table("Modelo original (Tf por tabla discreta)", original_records)
    ConsoleView.show_table("Modelo ajustado (Tf por interpolacion lineal)", adjusted_records)

    ChartView.plot_index(
        {"Original": original_records, "Ajustado": adjusted_records},
        "indice_lluvia.png",
    )
    ChartView.plot_temperature_factor("factor_temperatura.png")


if __name__ == "__main__":
    main()
