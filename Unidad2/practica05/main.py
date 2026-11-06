"""
Práctica 5: Generador Congruencial Lineal en Python y Java.

Uso (desde la carpeta del proyecto):
    python3 main.py                  # todo, incluido el período completo en Java (10 a 30 s)
    python3 main.py --sin-periodo    # omite el recorrido de 2^32 valores
"""
import sys
from pathlib import Path

import controller as ctl
import view
from model import A, C, M, SEED, hull_dobell

N = 10_000
SEEDS = [SEED, 54321, 2026]
OUT = Path(__file__).resolve().parent / "resultados"


def main(full_period=True):
    OUT.mkdir(exist_ok=True)
    print(f"Parámetros: a = {A}, c = {C}, m = 2^32 = {M}, semilla = {SEED}, n = {N}\n")

    ctl.compile_java()
    sequences = {}
    for seed in SEEDS:
        py_rows = ctl.python_sequence(N, seed)
        ctl.write_csv(py_rows, OUT / f"lcg_python_{seed}.csv")
        java_rows = ctl.java_sequence(N, seed, OUT / f"lcg_java_{seed}.csv")
        equal, total = ctl.compare(py_rows, java_rows)
        print(f"Semilla {seed}: {equal}/{total} valores idénticos entre Python y Java")
        sequences[seed] = (py_rows, java_rows)

    py_rows, java_rows = sequences[SEED]
    print("\nPrimeras 20 observaciones (semilla 12345)")
    view.print_comparison(py_rows, java_rows)
    view.save_comparison_csv(py_rows, java_rows, OUT / "comparacion_20.csv")

    print("\nEstadísticos de U(n) por semilla (esperado: media 0.5, varianza 1/12 = 0.0833)")
    print(f"{'Semilla':>8} | {'Media':>7} | {'Varianza':>8} | {'Chi²':>6} | {'Crítico':>7} | {'r(1)':>7} | Repetidos")
    for seed, (rows, _) in sequences.items():
        s = ctl.statistics(rows)
        print(f"{seed:>8} | {s['media']:.4f} | {s['varianza']:.5f} | {s['chi2']:>6.2f} | "
              f"{s['chi2_critico']:>7.3f} | {s['autocorrelacion']:>7.4f} | {s['repetidos']}")

    print("\nTeorema de Hull-Dobell (a, c, m de la guía):")
    for condition, ok in hull_dobell(A, C, M).items():
        print(f"  [{'✓' if ok else '✗'}] {condition}")
    if full_period:
        length, seconds = ctl.java_full_period(SEED)
        print(f"  Período medido en Java: {length} (= 2^32: {length == M}) en {seconds:.1f} s")

    print("\nPeríodo de los k bits menos significativos:")
    print("  " + ", ".join(f"k={k}: {p}" for k, p in ctl.low_bit_periods(SEED)))

    examples = ctl.small_period_examples()
    print("\nEjemplos con m = 16:")
    for ex in examples:
        print(f"  a={ex['a']:>2} c={ex['c']:>2} X0={ex['semilla']:>2}  período={ex['periodo']:>2}  "
              f"Hull-Dobell={'sí' if ex['hull_dobell'] else 'no'}  {ex['secuencia'][:10]}")

    view.plot_sequence(py_rows, java_rows, OUT / "secuencia.png")
    view.plot_distribution(py_rows, OUT / "distribucion.png")
    view.plot_seeds({s: rows for s, (rows, _) in sequences.items()}, OUT / "semillas.png")
    view.plot_period_examples(examples, OUT / "periodo_parametros.png")
    print(f"\nArchivos guardados en {OUT}")


if __name__ == "__main__":
    main(full_period="--sin-periodo" not in sys.argv)
