# Práctica 6: validación estadística con Chi-cuadrado y Kolmogorov-Smirnov

Evalúa si los números del generador congruencial lineal (LCG) siguen una
distribución uniforme en [0, 1). Las pruebas Chi-cuadrado y Kolmogorov-Smirnov
están implementadas en Python y en Java, con los valores p programados desde
cero, sin bibliotecas estadísticas.

```
H0: U ~ U(0,1)      H1: U no sigue U(0,1)      α = 0.05
```

## Tecnologías

- Python 3.10 o posterior, Matplotlib
- Java (JDK 17 o posterior)
- unittest: pruebas. SciPy es opcional y solo se usa para validar los valores p.

## Ejecución

Desde la carpeta del proyecto:

```bash
python -m pip install -r requirements.txt
python3 main.py              # unos 20 s
python3 -m unittest -v       # 18 pruebas
```

`main.py` compila el código Java en `java/build/` y compara sus resultados con
los de Python. Java también se puede usar solo:

```bash
cd java
javac -d build *.java
java -cp build Main pruebas 1664525 1013904223 4294967296 12345 10000
java -cp build Main pi 1000000 12345
```

## Resultados (LCG de la guía, n = 10 000, semilla 12345)

| Prueba | Estadístico | Valor p | Decisión |
|---|---:|---:|---|
| Chi-cuadrado (k = 10, gl = 9) | χ² = 14.160 | 0.1167 | No se rechaza H0 |
| Kolmogorov-Smirnov | D = 0.00596 | 0.8686 | No se rechaza H0 |

Python y Java producen la misma secuencia (10 000 de 10 000 valores), los mismos
estadísticos y valores p, y la misma estimación de π.

### Configuraciones del generador

| Configuración | χ² p | KS p | Comentario |
|---|---:|---:|---|
| Guía (a = 1664525, c = 1013904223, m = 2³²) | 0.117 | 0.869 | Pasa ambas |
| RANDU (a = 65539, c = 0, m = 2³¹) | 0.455 | 0.813 | Pasa ambas, pero sus ternas caen en 15 planos |
| Módulo pequeño (m = 256) | 0.939 | 0.997 | Pasa ambas con solo 256 valores distintos |
| Incremento fijo (a = 1) | 1.000 | ≈ 0 | χ² = 0, pero KS la rechaza |
| Multiplicador par (a = 1664524) | ≈ 0 | ≈ 0 | Ciclo de 16 valores: falla ambas |

### Estimación de π (tabla de la guía)

| N | π estimado | Error | Python (s) | Java (s) |
|---:|---:|---:|---:|---:|
| 1 000 | 3.172000 | 0.030407 | 0.0021 | 0.0018 |
| 10 000 | 3.158800 | 0.017207 | 0.0201 | 0.0035 |
| 100 000 | 3.141080 | 0.000513 | 0.1746 | 0.0273 |
| 1 000 000 | 3.142656 | 0.001063 | 1.6185 | 0.0435 |

Los tiempos varían entre ejecuciones. El análisis completo y las preguntas de
control están en `Reporte_Practica_06.pdf`, generado desde `reporte/reporte.html`.

## Estructura

```text
model.py                        # LCG, Chi-cuadrado, KS, valores p y Monte Carlo para π
controller.py                   # Experimentos y ejecución del código Java
view.py                         # Tablas, CSV y gráficas
main.py                         # Ejecución del proyecto
java/Lcg.java                   # Generador en Java
java/PruebasEstadisticas.java   # Chi-cuadrado y KS en Java
java/Main.java                  # Modos generar, pruebas y pi
test_model.py                   # Pruebas del modelo (y validación opcional con SciPy)
test_controller.py              # Pruebas de la comparación Python/Java
reporte/                        # Fuente HTML del reporte técnico
resultados/                     # CSV y gráficas generadas
```
