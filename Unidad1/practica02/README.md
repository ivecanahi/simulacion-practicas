# Práctica 02 — Comparación de modelos determinísticos, estocásticos, discretos y continuos

**Objetivo:** diferenciar los principales paradigmas de simulación construyendo cuatro modelos de crecimiento poblacional en Python, comparando discreto vs. continuo y analizando el efecto de la aleatoriedad.

**Datos de la guía:** `datos = [1000, 1100, 1250, 1400, 1600, 1850, 2100]`

## Los cuatro modelos

| Modelo | Ecuación | Característica |
|---|---|---|
| Determinístico | `P(t) = P0·e^(rt)` | Sin aleatoriedad: mismos parámetros → mismo resultado |
| Discreto | `P(t+1) = P(t) + r·P(t)` | La población cambia solo en períodos enteros |
| Estocástico | `P(t+1) = P(t) + r·P(t) + ε(t)`, `ε(t) ~ N(0, σ²)` | Discreto + ruido; si queda < 0 se corta en 0 |
| Continuo | `dP/dt = r·P` → Euler: `P(t+Δt) = P(t) + Δt·(r·P(t))` | Aproxima la curva continua con pasos `dt` |

## Parámetros estimados a partir de los datos

| Parámetro | Cómo se obtiene | Valor |
|---|---|---|
| `P0` | Primer dato del arreglo | 1000 |
| `r` | Promedio de `(P(t+1) − P(t)) / P(t)` | 0.1318 |
| `σ` | Desviación estándar del residuo `dato real − predicción del discreto` | 24.50 |
| `tiempo` | Cantidad de datos − 1 | 6 períodos |
| `dt` | Paso de Euler (fijo) | 0.1 |

Las corridas estocásticas usan semilla fija (`42`) para que sean reproducibles.

## Resultados

| t | Datos | Determinístico | Discreto | Estocástico | Continuo (Euler) |
|---|---|---|---|---|---|
| 0 | 1000 | 1000.0 | 1000.0 | 1000.0 | 1000.0 |
| 1 | 1100 | 1140.8 | 1131.8 | 1139.2 | 1139.9 |
| 2 | 1250 | 1301.5 | 1280.9 | 1263.9 | 1299.3 |
| 3 | 1400 | 1484.8 | 1449.7 | 1448.8 | 1481.0 |
| 4 | 1600 | 1694.0 | 1640.7 | 1662.7 | 1688.1 |
| 5 | 1850 | 1932.5 | 1856.9 | 1834.0 | 1924.2 |
| 6 | 2100 | 2204.7 | 2101.6 | 2043.8 | 2193.4 |

| Modelo | MAE | RMSE |
|---|---|---|
| Determinístico | 65.49 | 73.81 |
| **Discreto** | **23.07** | **29.61** |
| Estocástico | 33.83 | 40.47 |
| Continuo (Euler) | 60.85 | 68.22 |

### Gráficas

| Archivo | Qué muestra |
|---|---|
| `comparacion_modelos.png` | Los cuatro modelos sobre los datos observados |
| `influencia_r.png` | Crecimiento (r > 0), equilibrio (r = 0) y decrecimiento (r < 0) |
| `efecto_sigma.png` | 30 corridas estocásticas para σ = 12.3, 24.5 y 98.0 |
| `efecto_dt.png` | Euler con dt = 1, 0.5, 0.1, 0.01 contra la solución exacta |

## Interpretación matemática

- **El discreto es el que mejor ajusta** (MAE 23). Tiene sentido: los datos son observaciones por período y `r` se estimó como tasa *por período*, que es exactamente lo que usa `P(t+1) = (1 + r)·P(t)`. Su solución cerrada es `P(t) = P0·(1 + r)^t`.
- **El determinístico y el continuo sobreestiman** (≈ 2200 vs. 2100 en t = 6). Con la misma `r`, `e^r = 1.1409 > 1 + r = 1.1318`: el crecimiento continuo "capitaliza" a cada instante. La tasa continua equivalente sería `ln(1 + r) ≈ 0.1238`; con ella ambos modelos coincidirían con el discreto en los períodos enteros.
- **El continuo con Euler converge al determinístico** cuando `dt → 0` (error final 103.2 con dt = 1, 1.1 con dt = 0.01). Con `dt = 1` Euler es *idéntico* al modelo discreto.
- **El estocástico** se mueve alrededor del discreto: con σ pequeño las corridas casi no se separan; con σ grande la dispersión crece con el tiempo (desv. final 28 → 84 → 381), pero el **promedio** de muchas corridas sigue cerca del discreto, porque el ruido tiene media 0.
- **Influencia de r:** r > 0 → crecimiento exponencial (más rápido cuanto mayor es r); r = 0 → población constante; r < 0 → decrecimiento exponencial hacia 0, sin llegar a valores negativos si r > −1.

## Arquitectura (MVC)

| Archivo | Rol |
|---|---|
| `model.py` | Los cuatro modelos, estimación de parámetros y métricas de error. Sin I/O. |
| `controller.py` | Datos de la guía; estima parámetros y ejecuta los modelos y escenarios (r, σ, dt). |
| `view.py` | Tablas por consola y gráficas (`matplotlib`). |
| `main.py` | Arma el flujo controller → model → view. |
| `test_model.py` | Pruebas de cada fórmula. |

## Cómo correr

```bash
pip install -r ../../requirements.txt
python3 main.py                                   # datos de la guía
python3 main.py 2100 1900 1750 1600 1400 1300 1150   # otro arreglo
python3 -m unittest test_model.py                 # pruebas
```

> La guía menciona visualizar en NetLogo vía `pyNetLogo`. Esa parte requiere tener NetLogo instalado y no está incluida; toda la simulación y las gráficas se hacen en Python.
