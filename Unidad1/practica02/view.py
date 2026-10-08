"""
Vista (V de MVC): muestra los resultados como tablas en consola y como
graficas (matplotlib). No calcula nada: solo recibe resultados ya listos.
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

# Misma paleta que la practica 01 (fondo, tintas y series en orden fijo).
SURFACE = "#fcfcfb"
INK_PRIMARY = "#0b0b0b"
INK_SECONDARY = "#52514e"
INK_MUTED = "#898781"
GRID = "#e1e0d9"
BASELINE = "#c3c2b7"
SERIES = ["#2a78d6", "#eb6834", "#1baf7a", "#8a5cd6"]  # azul, naranja, aqua, violeta
DATA_COLOR = INK_PRIMARY


class ConsoleView:
    """Imprime parametros, tabla de valores por periodo y errores de cada modelo."""

    @staticmethod
    def show_parameters(data, params, dt):
        print("\nDatos de entrada:", data)
        print("Parametros estimados a partir de los datos:")
        print(f"  P0    = {params['p0']:.0f}")
        print(f"  r     = {params['r']:.4f}  (promedio de (P(t+1)-P(t))/P(t))")
        print(f"  sigma = {params['sigma']:.2f}  (desv. estandar del residuo del modelo discreto)")
        print(f"  tiempo = {params['time']} periodos, dt = {dt}")

    @staticmethod
    def show_table(data, results):
        print("\nPoblacion por periodo")
        names = list(results)
        header = f"{'t':>3}{'Datos':>9}" + "".join(f"{n:>18}" for n in names)
        print(header)
        print("-" * len(header))
        for t, real in enumerate(data):
            values = "".join(f"{np.interp(t, *results[n]):>18.1f}" for n in names)
            print(f"{t:>3}{real:>9}{values}")

    @staticmethod
    def show_errors(errors):
        print("\nError frente a los datos")
        print(f"{'Modelo':<20}{'MAE':>10}{'RMSE':>10}")
        print("-" * 40)
        for name, (mae, rmse) in errors.items():
            print(f"{name:<20}{mae:>10.2f}{rmse:>10.2f}")


def _apply_style():
    """Estilo comun: fondo claro, ejes discretos y grilla suave."""
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


def _plot_data(ax, data):
    """Datos observados como puntos negros, para comparar contra los modelos."""
    ax.scatter(range(len(data)), data, s=50, color=DATA_COLOR, zorder=5,
               edgecolor=SURFACE, linewidth=1.2, label="Datos observados")


def _labels(ax):
    ax.set_xlabel("Tiempo (periodos)")
    ax.set_ylabel("Poblacion")


def _save(fig, output_file):
    fig.tight_layout()
    fig.savefig(output_file, facecolor=SURFACE)
    plt.close(fig)


class ChartView:
    """Genera las graficas que pide la guia (comparacion, r, sigma y dt)."""

    _apply_style()

    @staticmethod
    def plot_comparison(data, results, params, output_file):
        """Los cuatro modelos sobre los datos observados."""
        fig, ax = plt.subplots(figsize=(10, 5.5))
        styles = {
            "Deterministico": dict(linewidth=2.4),
            "Discreto": dict(linewidth=0, marker="s", markersize=7, drawstyle="steps-post"),
            "Estocastico": dict(linewidth=1.8, marker="o", markersize=5, linestyle="--"),
            "Continuo (Euler)": dict(linewidth=2.0, linestyle=":"),
        }
        for color, (name, (t, p)) in zip(SERIES, results.items()):
            style = styles[name]
            if name == "Discreto":
                ax.step(t, p, where="post", color=color, linewidth=1.4, alpha=0.6)
                ax.plot(t, p, color=color, linestyle="none", marker="s", markersize=7, label=name)
            else:
                ax.plot(t, p, color=color, label=name, **style)
        _plot_data(ax, data)

        _labels(ax)
        ax.set_title("Comparacion de los cuatro modelos de crecimiento")
        _subtitle(ax, f"P0 = {params['p0']:.0f}, r = {params['r']:.4f}, "
                      f"sigma = {params['sigma']:.1f} (estimados de los datos)")
        ax.legend(loc="upper left")
        _save(fig, output_file)

    @staticmethod
    def plot_rates(scenarios, estimated_r, output_file):
        """Influencia de r: crecimiento (r > 0), equilibrio (r = 0) y decrecimiento (r < 0)."""
        fig, ax = plt.subplots(figsize=(10, 5.5))
        max_abs = max(abs(r) for r in scenarios) or 1
        for r, (t, p) in sorted(scenarios.items(), reverse=True):
            if r > 0:
                color = SERIES[0]
            elif r < 0:
                color = SERIES[1]
            else:
                color = INK_MUTED
            alpha = 0.35 + 0.65 * abs(r) / max_abs if r else 1
            width = 3 if np.isclose(r, estimated_r) else 1.8
            label = f"r = {r:+.4f} (estimado)" if np.isclose(r, estimated_r) else f"r = {r:+.2f}"
            ax.plot(t, p, color=color, alpha=alpha, linewidth=width, marker="o", markersize=4,
                    label=label)
            ax.annotate(f"{p[-1]:.0f}", (t[-1], p[-1]), textcoords="offset points",
                        xytext=(8, 0), va="center", fontsize=8.5, color=INK_SECONDARY)

        _labels(ax)
        ax.set_title("Influencia de la tasa r: crecimiento y decrecimiento")
        _subtitle(ax, "Modelo discreto. r > 0 crece, r = 0 se mantiene, r < 0 decrece")
        ax.legend(loc="upper left", ncols=2)
        _save(fig, output_file)

    @staticmethod
    def plot_noise(data, scenarios, base, output_file):
        """Efecto de sigma: varias corridas estocasticas por nivel de ruido."""
        sigmas = list(scenarios)
        fig, axes = plt.subplots(1, len(sigmas), figsize=(14, 5.2), sharey=True)
        t_base, p_base = base
        for ax, sigma in zip(axes, sigmas):
            runs = scenarios[sigma]
            for t, p in runs:
                ax.plot(t, p, color=SERIES[1], alpha=0.18, linewidth=1)
            stacked = np.array([p for _, p in runs])
            ax.plot(runs[0][0], stacked.mean(axis=0), color=SERIES[1], linewidth=2.2,
                    label="Promedio de las corridas")
            ax.plot(t_base, p_base, color=SERIES[0], linewidth=2, linestyle="--",
                    label="Discreto (sin ruido)")
            _plot_data(ax, data)
            spread = stacked[:, -1].std()
            ax.set_title(f"sigma = {sigma:.1f}", fontsize=12, pad=10)
            ax.text(0.03, 0.80, f"desv. final = {spread:.0f}", transform=ax.transAxes,
                    fontsize=9, color=INK_SECONDARY)
            ax.set_xlabel("Tiempo (periodos)")
        axes[0].set_ylabel("Poblacion")
        axes[0].legend(loc="upper left", fontsize=8)
        fig.suptitle(f"Efecto del nivel de ruido sigma ({len(scenarios[sigmas[0]])} corridas por panel)",
                     x=0.01, ha="left", fontsize=14, fontweight="bold", color=INK_PRIMARY)
        _save(fig, output_file)

    @staticmethod
    def plot_dt(scenarios, exact, output_file):
        """Efecto de dt: Euler con distintos pasos contra la solucion exacta P0*e^(rt)."""
        fig, ax = plt.subplots(figsize=(10, 5.5))
        t_exact, p_exact = exact
        ax.plot(t_exact, p_exact, color=DATA_COLOR, linewidth=2.6, label="Exacta P0*e^(rt)")
        for color, (dt, (t, p)) in zip(SERIES, sorted(scenarios.items(), reverse=True)):
            error = abs(p[-1] - p_exact[-1])
            ax.plot(t, p, color=color, linewidth=1.8, marker="o" if dt >= 0.5 else None,
                    markersize=4, label=f"Euler dt = {dt}  (error final = {error:.1f})")

        _labels(ax)
        ax.set_title("Efecto del tamano de paso dt en el modelo continuo")
        _subtitle(ax, "Mientras mas pequeno es dt, Euler se acerca mas a la solucion exacta")
        ax.legend(loc="upper left")
        _save(fig, output_file)
