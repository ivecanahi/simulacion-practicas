"""
Punto de entrada: orquesta todo el patron MVC.

Flujo:
1. El Controller estima P0, r y sigma a partir del arreglo de datos y corre
   los cuatro modelos (deterministico, discreto, estocastico y continuo).
2. Ademas corre los escenarios de analisis: distintas r, distintos sigma
   y distintos dt.
3. La View muestra tablas en consola y genera las graficas en PNG.

Uso:
    python3 main.py                       # datos de la guia
    python3 main.py 500 480 470 430 400   # cualquier otro arreglo de datos
"""
import sys

from controller import PopulationSimulationController, BASE_DATA
from model import deterministic_model
from view import ConsoleView, ChartView


def main(data):
    controller = PopulationSimulationController(data)
    params = controller.params

    results = controller.run_all()
    ConsoleView.show_parameters(data, params, controller.dt)
    ConsoleView.show_table(data, results)
    ConsoleView.show_errors(controller.errors(results))

    r = params["r"]
    rates = sorted({round(r, 4), 0.20, 0.05, 0.0, -0.05, -0.10, -0.20})
    sigma = params["sigma"]
    sigmas = [sigma / 2, sigma, sigma * 4]
    dts = [1, 0.5, 0.1, 0.01]

    ChartView.plot_comparison(data, results, params, "comparacion_modelos.png")
    ChartView.plot_rates(controller.rate_scenarios(rates), round(r, 4), "influencia_r.png")
    ChartView.plot_noise(data, controller.noise_scenarios(sigmas), results["Discreto"],
                         "efecto_sigma.png")
    ChartView.plot_dt(controller.dt_scenarios(dts),
                      deterministic_model(params["p0"], r, params["time"]), "efecto_dt.png")
    print("\nGraficas generadas: comparacion_modelos.png, influencia_r.png, "
          "efecto_sigma.png, efecto_dt.png")


if __name__ == "__main__":
    args = sys.argv[1:]
    try:
        main([float(x) for x in args] if args else BASE_DATA)
    except ValueError as error:
        sys.exit(f"Error en los datos de entrada: {error}")
