"""
Punto de entrada: orquesta todo el patron MVC.

Flujo:
1. El Controller toma los datos crudos (BASE_DATA) y le pide al modelo que
   calcule H, N, Tf, indice y estado para cada hora.
2. La View muestra la tabla de resultados en consola y genera las graficas en PNG.
"""
from controller import RainSimulationController, BASE_DATA
from view import ConsoleView, ChartView


def main():
    controller = RainSimulationController(BASE_DATA)
    records = controller.run()

    ConsoleView.show_table("Indice de probabilidad de lluvia por hora", records)

    ChartView.plot_index(records, "indice_lluvia.png")
    ChartView.plot_temperature_factor("factor_temperatura.png")


if __name__ == "__main__":
    main()
