"""Vistas: consola, CSV de comparación y gráficas."""
import csv

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402


def print_comparison(py_rows, java_rows, limit=20):
    print(f"{'n':>3} | {'X Python':>11} | {'X Java':>11} | {'U Python':>12} | {'U Java':>12} | Igual")
    print("-" * 70)
    for p, j in zip(py_rows[:limit], java_rows[:limit]):
        same = "Sí" if p[1] == j[1] else "No"
        print(f"{p[0]:>3} | {p[1]:>11} | {j[1]:>11} | {p[2]:>12.10f} | {j[2]:>12.10f} | {same}")


def save_comparison_csv(py_rows, java_rows, path, limit=20):
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["n", "x_python", "x_java", "u_python", "u_java", "coinciden"])
        for p, j in zip(py_rows[:limit], java_rows[:limit]):
            writer.writerow([p[0], p[1], j[1], f"{p[2]:.10f}", f"{j[2]:.10f}", p[1] == j[1]])


def plot_sequence(py_rows, java_rows, path, limit=100):
    n = [r[0] for r in py_rows[:limit]]
    fig, ax = plt.subplots(figsize=(10, 4))
    ax.plot(n, [r[2] for r in py_rows[:limit]], "-o", ms=4, lw=1, label="Python", color="#1f77b4")
    ax.plot(n, [r[2] for r in java_rows[:limit]], "x", ms=7, label="Java", color="#d62728")
    ax.set(xlabel="n", ylabel="U(n)", ylim=(0, 1),
           title=f"Secuencia U(n) = X(n)/m — primeros {limit} valores (semilla 12345)")
    ax.legend(loc="upper right")
    ax.grid(alpha=0.3)
    fig.tight_layout()
    fig.savefig(path, dpi=150)
    plt.close(fig)


def plot_distribution(rows, path):
    u = [r[2] for r in rows]
    fig, (left, right) = plt.subplots(1, 2, figsize=(11, 4.5))
    left.hist(u, bins=10, range=(0, 1), edgecolor="black", color="#1f77b4", alpha=0.8)
    left.axhline(len(u) / 10, color="#d62728", ls="--", label="Frecuencia esperada")
    left.set(xlabel="U", ylabel="Frecuencia", title=f"Histograma de {len(u)} valores")
    left.legend(loc="lower right")
    right.scatter(u[:-1], u[1:], s=1, color="#1f77b4", alpha=0.5)
    right.set(xlabel="U(n)", ylabel="U(n+1)", title="Pares consecutivos", xlim=(0, 1), ylim=(0, 1))
    right.set_aspect("equal")
    fig.tight_layout()
    fig.savefig(path, dpi=150)
    plt.close(fig)


def plot_seeds(sequences, path, limit=50):
    fig, ax = plt.subplots(figsize=(10, 4))
    for seed, rows in sequences.items():
        ax.plot([r[0] for r in rows[:limit]], [r[2] for r in rows[:limit]], "-o", ms=3, lw=1,
                label=f"semilla {seed}")
    ax.set(xlabel="n", ylabel="U(n)", ylim=(0, 1), title=f"Efecto de la semilla — primeros {limit} valores")
    ax.legend(loc="upper right", fontsize=8)
    ax.grid(alpha=0.3)
    fig.tight_layout()
    fig.savefig(path, dpi=150)
    plt.close(fig)


def plot_period_examples(examples, path):
    fig, ax = plt.subplots(figsize=(10, 4.5))
    for i, ex in enumerate(examples):
        label = f"a={ex['a']}, c={ex['c']}, X0={ex['semilla']} → período {ex['periodo']}"
        ax.plot(range(len(ex["secuencia"])), ex["secuencia"], "-o", ms=3, lw=1, label=label)
    ax.set(xlabel="n", ylabel="X(n)", ylim=(-0.5, 15.5), title="Efecto de los parámetros (m = 16)")
    ax.legend(loc="upper left", bbox_to_anchor=(1.01, 1), fontsize=8)
    ax.grid(alpha=0.3)
    fig.tight_layout()
    fig.savefig(path, dpi=150)
    plt.close(fig)
