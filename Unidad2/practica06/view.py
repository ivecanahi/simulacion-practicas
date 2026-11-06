"""Vistas: tablas en consola, CSV y gráficas."""
import csv

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

BLUE, RED, GRAY = "#1f77b4", "#d62728", "#7f7f7f"


def decision(rechaza):
    return "Se rechaza H0" if rechaza else "No se rechaza H0"


def print_header(title):
    print(f"\n{title}\n" + "-" * len(title))


def save_csv(rows, header, path):
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerows(rows)


def plot_frequencies(chi, path):
    k = len(chi["observadas"])
    labels = [f"[{i / k:.1f}, {(i + 1) / k:.1f})" for i in range(k)]
    fig, ax = plt.subplots(figsize=(10, 4))
    ax.bar(labels, chi["observadas"], color=BLUE, edgecolor="black", label="Observada (Oᵢ)")
    ax.axhline(chi["esperada"], color=RED, ls="--", label=f"Esperada (Eᵢ = {chi['esperada']:.0f})")
    ax.set(xlabel="Intervalo", ylabel="Frecuencia",
           title=f"Chi-cuadrado: χ² = {chi['estadistico']:.2f}, gl = {chi['gl']}, p = {chi['p']:.4f}")
    ax.set_ylim(0, chi["esperada"] * 1.25)
    ax.tick_params(axis="x", labelsize=8)
    ax.legend(loc="lower right")
    fig.tight_layout()
    fig.savefig(path, dpi=150)
    plt.close(fig)


def _ecdf(values):
    ordered = sorted(values)
    n = len(ordered)
    return ordered, [(i + 1) / n for i in range(n)]


def plot_ecdf(values, ks, path, zoom_points=50):
    x, y = _ecdf(values)
    fig, (left, right) = plt.subplots(1, 2, figsize=(11, 4.5))
    left.step(x, y, where="post", color=BLUE, label="Fₙ(x) empírica")
    left.plot([0, 1], [0, 1], color=RED, ls="--", label="F(x) = x teórica")
    left.set(xlabel="x", ylabel="Probabilidad acumulada", xlim=(0, 1), ylim=(0, 1),
             title=f"KS: D = {ks['estadistico']:.5f}, p = {ks['p']:.4f}")
    left.legend(loc="upper left")

    # Primeros valores de la muestra: se ven las diferencias entre las dos curvas.
    sample = values[:zoom_points]
    xs, ys = _ecdf(sample)
    right.step(xs, ys, where="post", color=BLUE, label=f"Fₙ(x), primeros {zoom_points} valores")
    right.plot([0, 1], [0, 1], color=RED, ls="--", label="F(x) = x")
    # Segmento donde ocurre D: arriba de la diagonal (D+) o debajo (D-).
    n = len(xs)
    gaps = []
    for i, xi in enumerate(xs):
        gaps.append(((i + 1) / n - xi, xi, xi, (i + 1) / n))   # D+: de F(x) a Fn(x)
        gaps.append((xi - i / n, xi, i / n, xi))               # D-: de Fn(x-) a F(x)
    d, x_at, low, high = max(gaps)
    right.vlines(x_at, low, high, color="black", lw=2, label=f"D (n = {zoom_points}) = {d:.3f}")
    right.set(xlabel="x", xlim=(0, 1), ylim=(0, 1), title="Detalle con una muestra pequeña")
    right.legend(loc="upper left", fontsize=8)
    fig.tight_layout()
    fig.savefig(path, dpi=150)
    plt.close(fig)


def plot_configurations(results, path):
    fig, axes = plt.subplots(2, len(results), figsize=(3.2 * len(results), 6))
    for col, r in enumerate(results):
        hist, ecdf = axes[0, col], axes[1, col]
        hist.hist(r["valores"], bins=10, range=(0, 1), color=BLUE, edgecolor="black")
        hist.axhline(len(r["valores"]) / 10, color=RED, ls="--")
        hist.set_title(f"{r['nombre']}\nχ² p = {r['chi']['p']:.3g}", fontsize=8)
        hist.tick_params(labelsize=7)
        x, y = _ecdf(r["valores"])
        ecdf.step(x, y, where="post", color=BLUE)
        ecdf.plot([0, 1], [0, 1], color=RED, ls="--")
        ecdf.set_title(f"KS p = {r['ks']['p']:.3g}", fontsize=8)
        ecdf.set(xlim=(0, 1), ylim=(0, 1))
        ecdf.tick_params(labelsize=7)
    axes[0, 0].set_ylabel("Frecuencia")
    axes[1, 0].set_ylabel("Fₙ(x)")
    fig.tight_layout()
    fig.savefig(path, dpi=150)
    plt.close(fig)


def plot_triples(results, path, names=("Guía (Numerical Recipes)", "RANDU (IBM, 1960s)")):
    fig = plt.figure(figsize=(11, 5))
    for i, name in enumerate(names, start=1):
        u = next(r["valores"] for r in results if r["nombre"] == name)
        ax = fig.add_subplot(1, 2, i, projection="3d")
        ax.scatter(u[:-2], u[1:-1], u[2:], s=0.5, color=BLUE, alpha=0.6)
        ax.set(xlabel="Uₙ", ylabel="Uₙ₊₁", zlabel="Uₙ₊₂", title=name)
        # Los planos de RANDU cumplen 9x - 6y + z = k; vistos en la dirección (2, 3, 0) quedan de canto.
        ax.view_init(elev=0, azim=56.31)
    fig.tight_layout()
    fig.savefig(path, dpi=150)
    plt.close(fig)


def plot_p_values(repeated, path):
    fig, axes = plt.subplots(1, 2, figsize=(11, 4))
    for ax, key, title in zip(axes, ("chi", "ks"), ("Chi-cuadrado", "Kolmogorov-Smirnov")):
        p = [r[key] for r in repeated]
        rejected = sum(v < 0.05 for v in p)
        ax.hist(p, bins=20, range=(0, 1), color=BLUE, edgecolor="black")
        ax.axvline(0.05, color=RED, ls="--", label="α = 0.05")
        ax.axhline(len(p) / 20, color=GRAY, ls=":", label="Esperado si H0 es cierta")
        ax.set(xlabel="Valor p", ylabel="Bloques",
               title=f"{title}: {rejected} de {len(p)} bloques rechazan H0")
        ax.legend(loc="upper right", fontsize=8)
    fig.tight_layout()
    fig.savefig(path, dpi=150)
    plt.close(fig)


def plot_pi(rows, path):
    import math
    n = [r["n"] for r in rows]
    fig, (left, right) = plt.subplots(1, 2, figsize=(11, 4))
    left.semilogx(n, [r["pi"] for r in rows], "o-", color=BLUE, label="π estimado")
    left.axhline(math.pi, color=RED, ls="--", label="π real")
    left.set(xlabel="N (escala log)", ylabel="Estimación", title="Convergencia de π por Monte Carlo")
    left.legend()
    right.loglog(n, [r["tiempo_python"] for r in rows], "o-", color=BLUE, label="Python")
    right.loglog(n, [r["tiempo_java"] for r in rows], "s-", color=RED, label="Java")
    right.set(xlabel="N (escala log)", ylabel="Tiempo (s, escala log)", title="Tiempo de ejecución")
    right.legend()
    fig.tight_layout()
    fig.savefig(path, dpi=150)
    plt.close(fig)
