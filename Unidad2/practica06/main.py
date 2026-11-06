"""
Práctica 6: validación estadística de números pseudoaleatorios con Chi-cuadrado y Kolmogorov-Smirnov.

Uso (desde la carpeta del proyecto):
    python3 main.py
"""
from pathlib import Path

import controller as ctl
import view
from model import ALPHA

N = 10_000
OUT = Path(__file__).resolve().parent / "resultados"


def main():
    OUT.mkdir(exist_ok=True)
    ctl.compile_java()
    print("H0: los números siguen una distribución U(0,1)   H1: no la siguen   α =", ALPHA)

    # 1. Generación en Python y Java
    lang = ctl.compare_languages(N, OUT)
    view.print_header(f"1. Secuencia LCG (a = 1664525, c = 1013904223, m = 2^32, semilla = 12345, n = {N})")
    print(f"Valores idénticos entre Python y Java: {lang['iguales']} de {N}")
    print(f"{'n':>3} | {'U Python':>12} | {'U Java':>12} | Igual")
    rows20 = []
    for i, (p, j) in enumerate(zip(lang["python"][:20], lang["java"][:20]), start=1):
        same = f"{p:.10f}" == f"{j:.10f}"
        rows20.append([i, f"{p:.10f}", f"{j:.10f}", "Sí" if same else "No"])
        print(f"{i:>3} | {p:.10f} | {j:.10f} | {'Sí' if same else 'No'}")
    view.save_csv(rows20, ["n", "u_python", "u_java", "coinciden"], OUT / "comparacion_20.csv")

    # 2. Chi-cuadrado
    chi, jt = lang["chi_python"], lang["java_pruebas"]
    view.print_header("2. Prueba Chi-cuadrado (k = 10 intervalos)")
    print(f"{'Intervalo':>12} | {'Oi':>5} | {'Ei':>6} | {'(Oi-Ei)²/Ei':>11}")
    freq_rows = []
    for i, o in enumerate(chi["observadas"]):
        contribution = (o - chi["esperada"]) ** 2 / chi["esperada"]
        freq_rows.append([f"[{i / 10:.1f}, {(i + 1) / 10:.1f})", o, chi["esperada"], f"{contribution:.4f}"])
        print(f"{freq_rows[-1][0]:>12} | {o:>5} | {chi['esperada']:>6.0f} | {contribution:>11.4f}")
    view.save_csv(freq_rows, ["intervalo", "observada", "esperada", "contribucion"], OUT / "frecuencias_chi2.csv")
    print(f"Python: χ² = {chi['estadistico']:.4f}, gl = {chi['gl']}, p = {chi['p']:.6f} → {view.decision(chi['rechaza'])}")
    print(f"Java:   χ² = {jt['chi2']:.4f}, gl = {jt['gl']}, p = {jt['p_chi2']:.6f}")

    # 3. Kolmogorov-Smirnov
    ks = lang["ks_python"]
    view.print_header("3. Prueba Kolmogorov-Smirnov")
    print(f"Python: D+ = {ks['d_mas']:.6f}, D- = {ks['d_menos']:.6f}, D = {ks['estadistico']:.6f}, "
          f"p = {ks['p']:.6f} → {view.decision(ks['rechaza'])}")
    print(f"Java:   D+ = {jt['d_mas']:.6f}, D- = {jt['d_menos']:.6f}, D = {jt['d']:.6f}, p = {jt['p_ks']:.6f}")

    # 4. Configuraciones del generador
    configs = ctl.configurations(N)
    view.print_header(f"4. Configuraciones del generador (n = {N})")
    config_rows = []
    for r in configs:
        same = abs(r["chi"]["estadistico"] - r["java"]["chi2"]) < 1e-6 and \
            abs(r["ks"]["estadistico"] - r["java"]["d"]) < 1e-8
        config_rows.append([r["nombre"], r["a"], r["c"], r["m"], r["seed"], r["distintos"],
                            f"{r['chi']['estadistico']:.3f}", f"{r['chi']['p']:.4g}", view.decision(r["chi"]["rechaza"]),
                            f"{r['ks']['estadistico']:.5f}", f"{r['ks']['p']:.4g}", view.decision(r["ks"]["rechaza"]),
                            "Sí" if same else "No"])
        print(f"{r['nombre']:<32} distintos={r['distintos']:>5}  χ²={r['chi']['estadistico']:>10.3f} "
              f"p={r['chi']['p']:<10.4g} D={r['ks']['estadistico']:.5f} p={r['ks']['p']:<10.4g} Java igual: {config_rows[-1][-1]}")
    view.save_csv(config_rows, ["configuracion", "a", "c", "m", "semilla", "valores_distintos", "chi2", "p_chi2",
                                "decision_chi2", "d_ks", "p_ks", "decision_ks", "python_igual_java"],
                  OUT / "configuraciones.csv")

    # 5. Tamaño de muestra
    sizes = ctl.sample_sizes([100, 1_000, 10_000, 100_000])
    view.print_header("5. Efecto del tamaño de la muestra (configuración de la guía)")
    for r in sizes:
        print(f"n = {r['n']:>7}: χ² = {r['chi']['estadistico']:7.3f} (p = {r['chi']['p']:.4f})   "
              f"D = {r['ks']['estadistico']:.5f} (p = {r['ks']['p']:.4f})")
    view.save_csv([[r["n"], f"{r['chi']['estadistico']:.4f}", f"{r['chi']['p']:.4f}",
                    f"{r['ks']['estadistico']:.6f}", f"{r['ks']['p']:.4f}"] for r in sizes],
                  ["n", "chi2", "p_chi2", "d_ks", "p_ks"], OUT / "tamano_muestra.csv")

    # 6. Pruebas repetidas
    repeated = ctl.repeated_tests(blocks=200, block_size=1_000)
    view.print_header("6. 200 bloques consecutivos de 1000 números")
    for key, name in (("chi", "Chi-cuadrado"), ("ks", "KS")):
        rejected = sum(r[key] < ALPHA for r in repeated)
        print(f"{name}: {rejected} de 200 bloques rechazan H0 ({rejected / 2:.1f} %; esperado ≈ 5 %)")

    # 7. Estimación de π
    pi_rows = ctl.pi_table([1_000, 10_000, 100_000, 1_000_000])
    view.print_header("7. Estimación de π por Monte Carlo con el LCG")
    print(f"{'N':>9} | {'π Python':>10} | {'π Java':>10} | {'Error':>8} | {'T Python (s)':>12} | {'T Java (s)':>10}")
    for r in pi_rows:
        print(f"{r['n']:>9} | {r['pi']:>10.6f} | {r['pi_java']:>10.6f} | {r['error']:>8.6f} | "
              f"{r['tiempo_python']:>12.6f} | {r['tiempo_java']:>10.6f}")
    view.save_csv([[r["n"], f"{r['pi']:.6f}", f"{r['pi_java']:.6f}", f"{r['error']:.6f}",
                    f"{r['tiempo_python']:.6f}", f"{r['tiempo_java']:.6f}"] for r in pi_rows],
                  ["n", "pi_python", "pi_java", "error", "tiempo_python_s", "tiempo_java_s"], OUT / "pi_monte_carlo.csv")

    view.plot_frequencies(chi, OUT / "chi_cuadrado.png")
    view.plot_ecdf(lang["python"], ks, OUT / "kolmogorov_smirnov.png")
    view.plot_configurations(configs, OUT / "configuraciones.png")
    view.plot_triples(configs, OUT / "randu_3d.png")
    view.plot_p_values(repeated, OUT / "valores_p.png")
    view.plot_pi(pi_rows, OUT / "pi_monte_carlo.png")
    print(f"\nArchivos guardados en {OUT}")


if __name__ == "__main__":
    main()
