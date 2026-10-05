"""
Vista (V de MVC): se encarga de mostrar los resultados, ya sea como tabla
de texto en consola o como graficas (matplotlib). No calcula nada: solo
recibe los HourRecord ya procesados y los presenta.
"""
import matplotlib.pyplot as plt
import numpy as np

from model import temperature_factor


class ConsoleView:
    """Imprime la tabla de resultados en la terminal, igual a la tabla de la guia."""

    @staticmethod
    def show_table(title, records):
        print(f"\n{title}")
        header = (f"{'Hora':<6}{'Humedad':>9}{'Nubosidad':>11}{'Temp':>6}"
                  f"{'H':>7}{'N':>7}{'Tf':>7}{'Indice':>9}  Estado")
        print(header)
        print("-" * len(header))
        for r in records:
            print(f"{r.hour:<6}{r.humidity:>9}{r.cloudiness:>11}{r.temp:>6}"
                  f"{r.h:>7.2f}{r.n:>7.2f}{r.tf:>7.2f}{r.index:>9.2f}  {r.state}")


class ChartView:
    """Genera las graficas que pide la guia (punto 6)."""

    @staticmethod
    def plot_index(records_by_label, output_file):
        """
        Grafica la evolucion del indice I a lo largo del dia, comparando el
        modelo original contra el ajustado (mismos H/N/Tf, distintos pesos),
        con los umbrales de la tabla de reglas de referencia.
        """
        plt.figure(figsize=(9, 5))
        for label, records in records_by_label.items():
            hours = [r.hour for r in records]
            indices = [r.index for r in records]
            plt.plot(hours, indices, marker="o", label=label)
        plt.axhline(0.40, linestyle="--", linewidth=0.8, color="gray", label="Umbral 0.40")
        plt.axhline(0.60, linestyle="--", linewidth=0.8, color="gray", label="Umbral 0.60")
        plt.axhline(0.75, linestyle="--", linewidth=0.8, color="gray", label="Umbral 0.75")
        plt.xlabel("Hora")
        plt.ylabel("Indice I")
        plt.title("Evolucion del indice de probabilidad de lluvia")
        plt.legend(fontsize=8)
        plt.tight_layout()
        plt.savefig(output_file)
        plt.close()

    @staticmethod
    def plot_temperature_factor(output_file):
        """Grafica Tf en funcion de la temperatura, para ver la influencia de este parametro en el indice."""
        temps = np.arange(8, 32, 0.5)
        tf_values = [temperature_factor(t) for t in temps]

        plt.figure(figsize=(9, 5))
        plt.step(temps, tf_values, where="post", color="tab:orange")
        plt.xlabel("Temperatura (C)")
        plt.ylabel("Factor de temperatura Tf")
        plt.title("Influencia de la temperatura en Tf")
        plt.tight_layout()
        plt.savefig(output_file)
        plt.close()
