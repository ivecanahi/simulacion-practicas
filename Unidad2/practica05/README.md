# Práctica 5: Generador Congruencial Lineal en Python y Java

Implementación del Generador Congruencial Lineal (LCG) en Python y en Java con
los mismos parámetros. El programa genera 10 000 valores en cada lenguaje,
compara las secuencias, grafica los resultados, analiza el período y repite
todo con otras semillas.

```
X(n+1) = (a · X(n) + c) mod m        U(n) = X(n) / m
```

| Parámetro | Valor |
|---|---:|
| a | 1664525 |
| c | 1013904223 |
| m | 2³² = 4294967296 |
| Semilla | 12345 (también 54321 y 2026) |
| Valores generados | 10 000 |

## Tecnologías

- Python 3.10 o posterior, Matplotlib
- Java (JDK 17 o posterior)
- unittest: pruebas

## Ejecución

Desde la carpeta del proyecto:

```bash
python -m pip install -r requirements.txt
python3 main.py                  # todo, incluido el período completo en Java (10 a 30 s)
python3 main.py --sin-periodo    # omite el recorrido de 2^32 valores
python3 -m unittest -v           # 16 pruebas
```

`main.py` compila el código Java en `java/build/`, lo ejecuta y compara su
salida con la de Python. El código Java también se puede usar solo:

```bash
cd java
javac -d build *.java
java -cp build Main generar 10000 12345 lcg_java.csv
java -cp build Main periodo 12345
```

## Resultados

| Semilla | Python = Java | Media | Varianza | χ² (crítico 16.919) | r(1) |
|---:|---:|---:|---:|---:|---:|
| 12345 | 10000 / 10000 | 0.4988 | 0.08302 | 14.16 | −0.0153 |
| 54321 | 10000 / 10000 | 0.4989 | 0.08360 | 7.23 | −0.0020 |
| 2026 | 10000 / 10000 | 0.4991 | 0.08451 | 7.52 | 0.0021 |

- Python y Java producen exactamente la misma secuencia.
- Los parámetros cumplen el teorema de Hull-Dobell, así que el período es
  completo. Java lo confirmó recorriendo los 4 294 967 296 valores.
- Los k bits menos significativos tienen período 2^k (el último bit alterna).
- Con parámetros inadecuados (m = 16) el período cae a 8, 2 o 1.

Archivos generados en `resultados/`:

- `comparacion_20.csv`: primeras 20 observaciones de Python y Java.
- `lcg_python_<semilla>.csv` y `lcg_java_<semilla>.csv`: los 10 000 valores.
- `secuencia.png`, `distribucion.png`, `semillas.png` y `periodo_parametros.png`.

El análisis completo y las preguntas de control están en
`Reporte_Practica_05.pdf`, generado desde `reporte/reporte.html`.

## Estructura

```text
model.py            # Modelo: clase LCG, período, Hull-Dobell y estadísticos
controller.py       # Controlador: ejecuta Python y Java y compara las secuencias
view.py             # Vistas: tabla en consola, CSV y gráficas
main.py             # Ejecución del proyecto
java/Lcg.java       # Generador en Java
java/Main.java      # Genera el CSV o mide el período
test_model.py       # Pruebas del generador
test_controller.py  # Pruebas de la comparación Python/Java
reporte/            # Fuente HTML del reporte técnico
resultados/         # Archivos generados
```
