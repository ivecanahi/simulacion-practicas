"""
Punto de entrada: orquesta todo el patron MVC.

Flujo:
1. El Controller toma los datos crudos (BASE_DATA) y le pide al modelo que
   calcule H, N, Tf, indice y estado para cada hora, dos veces: con los
   pesos originales de la guia y con los pesos ajustados (misma formula,
   mismas variables, otros pesos que tambien suman 1).
2. La View muestra ambas tablas en consola y genera las graficas en PNG.
"""
from model import WEIGHTS_ORIGINAL, WEIGHTS_ADJUSTED
from controller import RainSimulationController, BASE_DATA
from view import ConsoleView, ChartView


def main():
    controller = RainSimulationController(BASE_DATA)

    original_records = controller.run(WEIGHTS_ORIGINAL)
    adjusted_records = controller.run(WEIGHTS_ADJUSTED)

    ConsoleView.show_table("Modelo original (pesos 0.5 / 0.3 / 0.2)", original_records)
    ConsoleView.show_table("Modelo ajustado (pesos 0.4 / 0.3 / 0.3)", adjusted_records)

    ChartView.plot_index(
        {"Original": original_records, "Ajustado": adjusted_records},
        "indice_lluvia.png",
    )
    ChartView.plot_temperature_factor("factor_temperatura.png")


if __name__ == "__main__":
    main()
