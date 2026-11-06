"""Controlador: experimentos de la práctica y ejecución del código Java."""
import csv
import re
import shutil
import subprocess
import time
from pathlib import Path

from model import CONFIGURATIONS, LCG, chi_square_test, ks_test, monte_carlo_pi

PROJECT_DIR = Path(__file__).resolve().parent
JAVA_SRC = PROJECT_DIR / "java"
JAVA_BUILD = JAVA_SRC / "build"
GUIDE = CONFIGURATIONS["Guía (Numerical Recipes)"]


# ---------------------------------------------------------------- Java

def compile_java():
    if shutil.which("javac") is None or shutil.which("java") is None:
        raise RuntimeError("No se encontró el JDK (javac/java) en el PATH")
    JAVA_BUILD.mkdir(exist_ok=True)
    subprocess.run(["javac", "-d", str(JAVA_BUILD), *map(str, sorted(JAVA_SRC.glob("*.java")))], check=True)


def _java(*args):
    return subprocess.run(["java", "-cp", str(JAVA_BUILD), "Main", *map(str, args)],
                          check=True, capture_output=True, text=True).stdout


def java_sequence(n, seed, path):
    _java("generar", n, seed, path)
    with open(path, encoding="utf-8") as f:
        return [float(row["u"]) for row in csv.DictReader(f)]


def java_tests(config, n):
    out = _java("pruebas", config["a"], config["c"], config["m"], config["seed"], n)
    values = dict(pair.split("=") for pair in out.split())
    return {key: (int(v) if key == "gl" else float(v)) for key, v in values.items()}


def java_pi(n, seed):
    match = re.search(r"pi=([\d.]+) segundos=([\d.]+)", _java("pi", n, seed))
    return float(match.group(1)), float(match.group(2))


# ---------------------------------------------------------------- experimentos

def write_sequence_csv(values, path):
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["n", "u"])
        writer.writerows((i, f"{u:.10f}") for i, u in enumerate(values, start=1))


def compare_languages(n, out_dir):
    """Secuencia y pruebas en Python y Java con la configuración de la guía."""
    py_values = LCG(**GUIDE).uniforms(n)
    write_sequence_csv(py_values, out_dir / "lcg_python.csv")
    java_values = java_sequence(n, GUIDE["seed"], out_dir / "lcg_java.csv")
    equal = sum(1 for p, j in zip(py_values, java_values) if f"{p:.10f}" == f"{j:.10f}")
    return {
        "python": py_values,
        "java": java_values,
        "iguales": equal,
        "chi_python": chi_square_test(py_values),
        "ks_python": ks_test(py_values),
        "java_pruebas": java_tests(GUIDE, n),
    }


def configurations(n):
    results = []
    for name, config in CONFIGURATIONS.items():
        values = LCG(**config).uniforms(n)
        results.append({"nombre": name, **config, "valores": values,
                        "distintos": len(set(values)),
                        "chi": chi_square_test(values), "ks": ks_test(values),
                        "java": java_tests(config, n)})
    return results


def sample_sizes(sizes):
    return [{"n": n, "chi": chi_square_test(v), "ks": ks_test(v)}
            for n in sizes for v in [LCG(**GUIDE).uniforms(n)]]


def repeated_tests(blocks, block_size):
    """Aplica ambas pruebas a bloques consecutivos e independientes de la misma secuencia."""
    gen = LCG(**GUIDE)
    results = []
    for _ in range(blocks):
        values = gen.uniforms(block_size)
        results.append({"chi": chi_square_test(values)["p"], "ks": ks_test(values)["p"]})
    return results


def pi_table(sizes, seed=GUIDE["seed"]):
    import math
    rows = []
    for n in sizes:
        start = time.perf_counter()
        py_estimate = monte_carlo_pi(n, seed)
        py_time = time.perf_counter() - start
        java_estimate, java_time = java_pi(n, seed)
        rows.append({"n": n, "pi": py_estimate, "pi_java": java_estimate,
                     "error": abs(py_estimate - math.pi),
                     "tiempo_python": py_time, "tiempo_java": java_time})
    return rows
