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

    records_by_label = {"Original": original_records, "Ajustado": adjusted_records}
    weights_by_label = {"Original": WEIGHTS_ORIGINAL, "Ajustado": WEIGHTS_ADJUSTED}

    ChartView.plot_index(records_by_label, "indice_lluvia.png")
    ChartView.plot_temperature_factor("factor_temperatura.png")
    ChartView.plot_input_variables(original_records, "variables_entrada.png")
    ChartView.plot_contributions(records_by_label, weights_by_label, "contribucion_variables.png")


if __name__ == "__main__":
    main()
