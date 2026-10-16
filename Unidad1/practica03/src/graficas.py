import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np


def graficar_cola(muestras_cola, titulo, ruta, hasta=200):
    """Queue length over time as a step plot."""
    visibles = [(t, n) for t, n in muestras_cola if t <= hasta]
    tiempos = [t for t, _ in visibles]
    tamanos = [n for _, n in visibles]
    plt.figure(figsize=(10, 4))
    plt.step(tiempos, tamanos, where="post")
    plt.title(titulo)
    plt.xlabel("Tiempo")
    plt.ylabel("Clientes en cola")
    plt.grid(alpha=0.3)
    plt.tight_layout()
    plt.savefig(ruta)
    plt.close()


def graficar_esperas(tiempos_espera, titulo, ruta):
    """Histogram of waiting times with the mean marked."""
    plt.figure(figsize=(8, 4))
    plt.hist(tiempos_espera, bins=30, edgecolor="black")
    plt.axvline(np.mean(tiempos_espera), color="red", linestyle="--", label="Promedio")
    plt.title(titulo)
    plt.xlabel("Tiempo de espera")
    plt.ylabel("Cantidad de clientes")
    plt.legend()
    plt.tight_layout()
    plt.savefig(ruta)
    plt.close()


def graficar_comparacion(tabla, ruta):
    """Grouped bars: theoretical vs simulated Wq and Lq per scenario."""
    etiquetas = [f"Esc. {fila['escenario']}" for fila in tabla]
    x = np.arange(len(tabla))
    ancho = 0.35
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 4))
    ax1.bar(x - ancho / 2, [f["Wq"] for f in tabla], ancho, label="Teórico")
    ax1.bar(x + ancho / 2, [f["espera_promedio"] for f in tabla], ancho, label="Simulado")
    ax1.set_title("Tiempo promedio en cola (Wq)")
    ax2.bar(x - ancho / 2, [f["Lq"] for f in tabla], ancho, label="Teórico")
    ax2.bar(x + ancho / 2, [f["cola_promedio"] for f in tabla], ancho, label="Simulado")
    ax2.set_title("Clientes promedio en cola (Lq)")
    for ax in (ax1, ax2):
        ax.set_xticks(x)
        ax.set_xticklabels(etiquetas)
        ax.legend()
        ax.grid(axis="y", alpha=0.3)
    fig.tight_layout()
    fig.savefig(ruta)
    plt.close(fig)