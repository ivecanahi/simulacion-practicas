"""
Vista (V de MVC): se encarga de mostrar los resultados, ya sea como tabla
de texto en consola o como graficas (matplotlib). No calcula nada: solo
recibe los HourRecord ya procesados y los presenta.
"""
import matplotlib.pyplot as plt
import numpy as np

from model import TEMPERATURE_TABLE, temperature_factor

# Paleta comun a todas las graficas (fondo, tintas y series en orden fijo).
SURFACE = "#fcfcfb"
INK_PRIMARY = "#0b0b0b"
INK_SECONDARY = "#52514e"
INK_MUTED = "#898781"
GRID = "#e1e0d9"
BASELINE = "#c3c2b7"
SERIES = ["#2a78d6", "#eb6834", "#1baf7a"]  # azul, naranja, aqua

# Umbrales y estados de la 'Tabla de reglas' de la guia.
THRESHOLDS = [
    (0.00, 0.40, "Sin lluvia"),
    (0.40, 0.60, "Baja posibilidad"),
    (0.60, 0.75, "Lluvia probable"),
    (0.75, 1.00, "Lluvia"),
]


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


def _apply_style():
    """Estilo comun: fondo claro, ejes discretos y grilla horizontal suave."""
    plt.rcParams.update({
        "figure.facecolor": SURFACE,
        "axes.facecolor": SURFACE,
        "axes.edgecolor": BASELINE,
        "axes.labelcolor": INK_SECONDARY,
        "axes.titlecolor": INK_PRIMARY,
        "axes.titlesize": 14,
        "axes.titleweight": "bold",
        "axes.titlelocation": "left",
        "axes.titlepad": 28,
        "axes.axisbelow": True,
        "axes.labelsize": 10,
        "axes.spines.top": False,
        "axes.spines.right": False,
        "axes.grid": True,
        "axes.grid.axis": "y",
        "grid.color": GRID,
        "grid.linewidth": 0.8,
        "xtick.color": INK_MUTED,
        "ytick.color": INK_MUTED,
        "xtick.labelsize": 9,
        "ytick.labelsize": 9,
        "legend.frameon": False,
        "legend.fontsize": 9,
        "legend.labelcolor": INK_SECONDARY,
        "font.family": "DejaVu Sans",
        "savefig.dpi": 150,
    })


def _subtitle(ax, text):
    """Linea secundaria debajo del titulo, en tinta gris."""
    ax.text(0, 1.025, text, transform=ax.transAxes, fontsize=9.5,
            color=INK_SECONDARY, va="bottom")


def _save(fig, output_file):
    fig.tight_layout()
    fig.savefig(output_file, facecolor=SURFACE)
    plt.close(fig)


class ChartView:
    """Genera las graficas que pide la guia (punto 6) y dos de apoyo al analisis."""

    _apply_style()

    @staticmethod
    def plot_index(records_by_label, output_file):
        """
        Evolucion del indice I a lo largo del dia, comparando el modelo
        original contra el ajustado, sobre las franjas de la tabla de reglas.
        """
        fig, ax = plt.subplots(figsize=(10, 5.5))

        # Franjas de estado: grises alternados muy suaves + etiqueta a la derecha.
        for i, (low, high, name) in enumerate(THRESHOLDS):
            if i % 2:
                ax.axhspan(low, high, color="#f0efec", zorder=0, linewidth=0)
            ax.axhline(low, color=BASELINE, linewidth=0.8, linestyle=(0, (4, 3)), zorder=1)
            ax.text(1.01, (max(low, 0.3) + high) / 2, name, transform=ax.get_yaxis_transform(),
                    fontsize=8.5, color=INK_MUTED, va="center")

        for i, (color, (label, records)) in enumerate(zip(SERIES, records_by_label.items())):
            hours = [r.hour for r in records]
            indices = [r.index for r in records]
            ax.plot(hours, indices, color=color, linewidth=2.2, marker="o", markersize=7,
                    markeredgecolor=SURFACE, markeredgewidth=1.5, label=label, zorder=3)
            # Etiqueta directa solo en el pico del dia.
            peak = int(np.argmax(indices))
            ax.annotate(f"{indices[peak]:.2f}", (hours[peak], indices[peak]),
                        textcoords="offset points", xytext=(0, 12 if i == 0 else -20),
                        ha="center", fontsize=9, color=INK_PRIMARY, fontweight="bold")

        ax.set_ylim(0.3, 1.0)
        ax.set_ylabel("Indice I")
        ax.set_xlabel("Hora del dia")
        ax.set_title("Evolucion del indice de probabilidad de lluvia")
        _subtitle(ax, "Modelo original (0.5 / 0.3 / 0.2) vs. ajustado (0.4 / 0.3 / 0.3)")
        ax.legend(loc="upper left", ncols=2)
        _save(fig, output_file)

    @staticmethod
    def plot_temperature_factor(output_file):
        """Tf en funcion de la temperatura: como la temperatura influye en el indice."""
        temps = np.arange(8, 31, 0.1)
        tf_values = [temperature_factor(t) for t in temps]

        fig, ax = plt.subplots(figsize=(10, 5.5))
        ax.fill_between(temps, tf_values, step="pre", color=SERIES[1], alpha=0.12, linewidth=0)
        ax.step(temps, tf_values, where="pre", color=SERIES[1], linewidth=2.2)

        table_t = [t for t, _ in TEMPERATURE_TABLE]
        table_tf = [tf for _, tf in TEMPERATURE_TABLE]
        ax.scatter(table_t, table_tf, s=55, color=SERIES[1], edgecolor=SURFACE,
                   linewidth=1.5, zorder=3, label="Valores de la tabla de la guia")
        for t, tf in (TEMPERATURE_TABLE[0], TEMPERATURE_TABLE[-1]):
            ax.annotate(f"{tf:.2f}", (t, tf), textcoords="offset points", xytext=(8, 6),
                        fontsize=9, color=INK_PRIMARY, fontweight="bold")

        ax.set_xlim(8, 30)
        ax.set_ylim(0, 1.1)
        ax.set_xticks(range(8, 31, 2))
        ax.set_xlabel("Temperatura (°C)")
        ax.set_ylabel("Factor de temperatura Tf")
        ax.set_title("Influencia de la temperatura en Tf")
        _subtitle(ax, "A menor temperatura, mayor factor: el frio favorece la lluvia")
        ax.legend(loc="upper right")
        _save(fig, output_file)

    @staticmethod
    def plot_input_variables(records, output_file):
        """Las tres variables normalizadas (H, N, Tf) que alimentan la formula, hora a hora."""
        hours = [r.hour for r in records]
        series = [
            ("Humedad H", [r.h for r in records]),
            ("Nubosidad N", [r.n for r in records]),
            ("Factor de temperatura Tf", [r.tf for r in records]),
        ]

        fig, ax = plt.subplots(figsize=(10, 5.5))
        for color, (label, values) in zip(SERIES, series):
            ax.plot(hours, values, color=color, linewidth=2.2, marker="o", markersize=7,
                    markeredgecolor=SURFACE, markeredgewidth=1.5, label=label)
            # Etiqueta directa al final de cada linea.
            ax.annotate(label.split()[-1], (len(hours) - 1, values[-1]),
                        textcoords="offset points", xytext=(10, 0), va="center",
                        fontsize=9, color=INK_SECONDARY, fontweight="bold")

        ax.set_ylim(0, 1.05)
        ax.set_ylabel("Valor normalizado (0 - 1)")
        ax.set_xlabel("Hora del dia")
        ax.set_title("Variables de entrada del modelo")
        _subtitle(ax, "Humedad y nubosidad suben hacia la tarde; Tf baja con el calor del mediodia")
        ax.legend(loc="lower left", ncols=3)
        _save(fig, output_file)

    @staticmethod
    def plot_contributions(records_by_label, weights_by_label, output_file):
        """
        Aporte de cada termino (W_H*H, W_N*N, W_TF*Tf) al indice, en barras
        apiladas: un panel por modelo, misma escala para poder compararlos.
        """
        labels = list(records_by_label)
        fig, axes = plt.subplots(1, len(labels), figsize=(12, 5.5), sharey=True)

        for ax, label in zip(axes, labels):
            records = records_by_label[label]
            w_h, w_n, w_tf = weights_by_label[label]
            hours = [r.hour for r in records]
            parts = [
                (f"Humedad  ({w_h} x H)", np.array([w_h * r.h for r in records])),
                (f"Nubosidad  ({w_n} x N)", np.array([w_n * r.n for r in records])),
                (f"Temperatura  ({w_tf} x Tf)", np.array([w_tf * r.tf for r in records])),
            ]
            bottom = np.zeros(len(records))
            for color, (name, values) in zip(SERIES, parts):
                ax.bar(hours, values, bottom=bottom, color=color, width=0.68,
                       edgecolor=SURFACE, linewidth=1.5, label=name)
                bottom += values
            for x, total in enumerate(bottom):
                ax.text(x, total + 0.015, f"{total:.2f}", ha="center", fontsize=8,
                        color=INK_SECONDARY)

            ax.set_ylim(0, 1.05)
            ax.set_title(f"Modelo {label.lower()}", fontsize=12)
            ax.tick_params(axis="x", labelsize=8)
            ax.legend(loc="upper left", fontsize=8)

        axes[0].set_ylabel("Aporte al indice I")
        fig.suptitle("Cuanto aporta cada variable al indice", x=0.01, ha="left",
                     fontsize=14, fontweight="bold", color=INK_PRIMARY)
        _save(fig, output_file)
