# Práctica 02 — Comparación de modelos determinísticos, estocásticos, discretos y continuos

## 1. Descripción

Simula el **crecimiento poblacional** con cuatro paradigmas de simulación y los compara contra datos observados:

`datos = [1000, 1100, 1250, 1400, 1600, 1850, 2100]`

- **Propósito:** diferenciar los modelos determinísticos, estocásticos, discretos y continuos, y analizar el efecto de la aleatoriedad.
- **Problema que resuelve:** a partir de un arreglo de poblaciones observadas, estima los parámetros del sistema, proyecta su evolución con cada modelo y mide cuál se ajusta mejor.

### Los cuatro modelos

| Modelo | Ecuación | Característica |
|---|---|---|
| Determinístico | `P(t) = P0·e^(rt)` | Sin aleatoriedad: mismos parámetros, mismo resultado |
| Discreto | `P(t+1) = P(t) + r·P(t)` | La población cambia solo en períodos enteros |
| Estocástico | `P(t+1) = P(t) + r·P(t) + ε(t)`, `ε ~ N(0, σ²)` | Discreto más ruido; si queda < 0 se fija en 0 |
| Continuo | `dP/dt = r·P` → Euler: `P(t+Δt) = P(t) + Δt·r·P(t)` | Aproxima la curva continua con pasos `dt` |

### Parámetros estimados de los datos

| Parámetro | Cómo se obtiene | Valor |
|---|---|---|
| `P0` | Primer dato | 1000 |
| `r` | Promedio de `(P(t+1) − P(t)) / P(t)` | 0.1318 |
| `σ` | Desviación estándar del residuo del modelo discreto | 24.50 |
| `tiempo` | Cantidad de datos − 1 | 6 períodos |

## 2. Tecnologías utilizadas

| Tecnología | Uso |
|---|---|
| Python 3.12 | Lenguaje de implementación |
| NumPy 1.26 | Cálculo numérico y números aleatorios |
| Matplotlib 3.9 | Gráficas |
| unittest | Pruebas unitarias de cada fórmula |

## 3. Instalación

Desde la raíz del repositorio:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## 4. Configuración

No requiere variables de entorno. Los valores se editan en el código:

| Qué cambiar | Dónde |
|---|---|
| Datos por defecto | `BASE_DATA` en `controller.py` |
| Paso del modelo continuo | `DEFAULT_DT` en `controller.py` (0.1) |
| Semilla aleatoria (reproducibilidad) | `SEED` en `controller.py` (42) |
| Escenarios de `r`, `σ` y `dt` | `main()` en `main.py` |

## 5. Uso

```bash
cd Unidad1/practica02
python3 main.py                                        # datos de la guía
python3 main.py 2100 1900 1750 1600 1400 1300 1150     # cualquier otro arreglo
python3 -m unittest test_model.py                      # pruebas
```

El arreglo necesita al menos 2 datos y poblaciones mayores que 0. Si no se cumple, el programa muestra un mensaje de error.

Imprime los parámetros, la tabla por período y el error de cada modelo, y genera estas gráficas:

| Archivo | Qué muestra |
|---|---|
| `comparacion_modelos.png` | Los cuatro modelos sobre los datos observados |
| `influencia_r.png` | Crecimiento (r > 0), equilibrio (r = 0) y decrecimiento (r < 0) |
| `efecto_sigma.png` | 30 corridas estocásticas para tres niveles de σ |
| `efecto_dt.png` | Euler con distintos `dt` frente a la solución exacta |

## 6. Estructura del proyecto

Arquitectura **MVC (Modelo-Vista-Controlador)**:

```
practica02/
├── model.py        # Los cuatro modelos, estimación de parámetros y errores (sin I/O)
├── controller.py   # Datos de la guía; ejecuta los modelos y los escenarios r, σ, dt
├── view.py         # Tablas por consola y gráficas
├── main.py         # Punto de entrada; acepta un arreglo por línea de comandos
├── test_model.py   # Pruebas de cada fórmula
├── *.png           # Gráficas generadas
├── reporte/        # Fuente HTML del reporte técnico
└── Reporte_Practica_02.pdf
```

## 7. Información adicional

### Resultados principales

| Modelo | Población en t = 6 | MAE | RMSE |
|---|---|---|---|
| Datos observados | 2100 | — | — |
| Determinístico | 2204.7 | 65.49 | 73.81 |
| **Discreto** | **2101.6** | **23.07** | **29.61** |
| Estocástico | 2043.8 | 33.83 | 40.47 |
| Continuo (Euler) | 2193.4 | 60.85 | 68.22 |

- **El discreto es el que mejor ajusta**, porque los datos son por período y `r` se estimó por período.
- **El determinístico y el continuo sobreestiman**: con la misma `r`, `e^r = 1.1409 > 1 + r = 1.1318`.
- **Euler converge a la solución exacta** al reducir `dt` (error final 103.2 con dt = 1, 1.1 con dt = 0.01).
- **Más `σ` = más incertidumbre**, no otra tendencia: el promedio de las corridas sigue cerca del discreto.

La interpretación completa y las preguntas de control están en el **[reporte técnico](Reporte_Practica_02.pdf)**.

### Notas

- La guía menciona visualizar el sistema en NetLogo mediante `pyNetLogo`. Esa parte requiere tener NetLogo instalado y no está incluida.
