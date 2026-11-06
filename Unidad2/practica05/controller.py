"""Controlador: genera las secuencias en Python y Java y las compara."""
import csv
import re
import shutil
import subprocess
from pathlib import Path

from model import (A, C, M, LCG, chi_square_uniformity, hull_dobell,
                   lag1_autocorrelation, mean, period, variance)

PROJECT_DIR = Path(__file__).resolve().parent
JAVA_SRC = PROJECT_DIR / "java"
JAVA_BUILD = JAVA_SRC / "build"


def python_sequence(n, seed):
    return [(i, x, u) for i, (x, u) in enumerate(LCG(seed=seed).generate(n), start=1)]


def write_csv(rows, path):
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["n", "x", "u"])
        for i, x, u in rows:
            writer.writerow([i, x, f"{u:.10f}"])


def read_csv(path):
    with open(path, encoding="utf-8") as f:
        return [(int(r["n"]), int(r["x"]), float(r["u"])) for r in csv.DictReader(f)]


def compile_java():
    if shutil.which("javac") is None or shutil.which("java") is None:
        raise RuntimeError("No se encontró el JDK (javac/java) en el PATH")
    JAVA_BUILD.mkdir(exist_ok=True)
    sources = [str(p) for p in sorted(JAVA_SRC.glob("*.java"))]
    subprocess.run(["javac", "-d", str(JAVA_BUILD), *sources], check=True)


def java_sequence(n, seed, path):
    subprocess.run(["java", "-cp", str(JAVA_BUILD), "Main", "generar", str(n), str(seed), str(path)],
                   check=True, capture_output=True, text=True)
    return read_csv(path)


def java_full_period(seed):
    out = subprocess.run(["java", "-cp", str(JAVA_BUILD), "Main", "periodo", str(seed)],
                         check=True, capture_output=True, text=True).stdout
    match = re.search(r"periodo=(\d+) segundos=([\d.]+)", out)
    return int(match.group(1)), float(match.group(2))


def compare(py_rows, java_rows):
    """Número de filas donde X coincide exactamente entre ambos lenguajes."""
    equal = sum(1 for p, j in zip(py_rows, java_rows) if p[1] == j[1])
    return equal, len(py_rows)


def statistics(rows):
    uniforms = [u for _, _, u in rows]
    chi2, critical = chi_square_uniformity(uniforms)
    return {
        "media": mean(uniforms),
        "varianza": variance(uniforms),
        "chi2": chi2,
        "chi2_critico": critical,
        "autocorrelacion": lag1_autocorrelation(uniforms),
        "repetidos": len(uniforms) - len({x for _, x, _ in rows}),
    }


def small_period_examples():
    """Ejemplos con m = 16 que muestran el efecto de los parámetros sobre el período."""
    cases = [(5, 3, 16, 7), (5, 4, 16, 1), (4, 2, 16, 1), (3, 3, 16, 1), (1, 0, 16, 5)]
    results = []
    for a, c, m, seed in cases:
        sequence, x = [], seed
        for _ in range(18):
            sequence.append(x)
            x = (a * x + c) % m
        results.append({"a": a, "c": c, "m": m, "semilla": seed,
                        "periodo": period(a, c, m, seed),
                        "hull_dobell": all(hull_dobell(a, c, m).values()),
                        "secuencia": sequence})
    return results


def low_bit_periods(seed, max_bits=8):
    """Período del bit k menos significativo: x mod 2^k sigue el mismo LCG con m = 2^k."""
    return [(k, period(A % 2**k, C % 2**k, 2**k, seed % 2**k)) for k in range(1, max_bits + 1)]
