# Práctica 01 — Construcción y simulación computacional de un modelo matemático

**Objetivo:** comprender el proceso de construcción de un modelo matemático y analizar su comportamiento mediante Python, implementando un modelo de predicción de lluvia a partir de humedad, nubosidad y temperatura.

## El modelo

```
I = 0.5*H + 0.3*N + 0.2*Tf
```

- `H` = humedad normalizada (0–1)
- `N` = nubosidad normalizada (0–1)
- `Tf` = factor de temperatura, tomado de la tabla de la guía

| Índice I | Estado |
|---|---|
| I < 0.40 | Sin lluvia |
| 0.40 ≤ I < 0.60 | Baja posibilidad |
| 0.60 ≤ I < 0.75 | Lluvia probable |
| I ≥ 0.75 | Lluvia |

La guía pide calcular la tabla dos veces: una con el modelo original y otra con el modelo "ajustado". Se observó que la tabla de `Tf` de la guía es en realidad una recta (`Tf = 1.00 - 0.05*(T-10)`), así que:

- **Modelo original** (`temperature_factor_discrete`): usa la tabla tal cual, por escalones.
- **Modelo ajustado** (`temperature_factor_continuous`): usa la fórmula lineal, lo que permite calcular `Tf` para cualquier temperatura (incluidas las que no están en la tabla, como 15 °C o 17 °C).

## Arquitectura (MVC)

| Archivo | Rol |
|---|---|
| `model.py` | Fórmula del índice, tabla de temperatura y clasificación de estado. Sin I/O. |
| `controller.py` | Datos de entrada (la tabla de la guía) y orquestación: le pide al modelo que procese cada hora. |
| `view.py` | Tabla por consola y gráficas (`matplotlib`). |
| `main.py` | Arma el flujo: controller → model → view, para el modelo original y el ajustado. |

## Cómo correr

```bash
pip install -r ../../requirements.txt
python3 main.py
```

Genera `indice_lluvia.png` (evolución del índice durante el día) y `factor_temperatura.png` (Tf discreto vs. ajustado).

## Resultados

**Modelo original (Tf por tabla discreta):**

| Hora | Humedad | Nubosidad | Temp | H | N | Tf | Índice | Estado |
|---|---|---|---|---|---|---|---|---|
| 06:00 | 65 | 40 | 14 | 0.65 | 0.40 | 0.80 | 0.60 | Lluvia probable |
| 08:00 | 70 | 50 | 16 | 0.70 | 0.50 | 0.70 | 0.64 | Lluvia probable |
| 10:00 | 68 | 45 | 18 | 0.68 | 0.45 | 0.60 | 0.59 | Baja posibilidad |
| 12:00 | 60 | 30 | 22 | 0.60 | 0.30 | 0.40 | 0.47 | Baja posibilidad |
| 14:00 | 75 | 70 | 20 | 0.75 | 0.70 | 0.50 | 0.68 | Lluvia probable |
| 16:00 | 85 | 85 | 18 | 0.85 | 0.85 | 0.60 | 0.80 | Lluvia |
| 18:00 | 92 | 95 | 16 | 0.92 | 0.95 | 0.70 | 0.89 | Lluvia |
| 20:00 | 88 | 90 | 17 | 0.88 | 0.90 | 0.60 | 0.83 | Lluvia |
| 22:00 | 80 | 75 | 15 | 0.80 | 0.75 | 0.70 | 0.77 | Lluvia |

**Modelo ajustado (Tf por interpolación lineal):**

| Hora | Humedad | Nubosidad | Temp | H | N | Tf | Índice | Estado |
|---|---|---|---|---|---|---|---|---|
| 06:00 | 65 | 40 | 14 | 0.65 | 0.40 | 0.80 | 0.60 | Lluvia probable |
| 08:00 | 70 | 50 | 16 | 0.70 | 0.50 | 0.70 | 0.64 | Lluvia probable |
| 10:00 | 68 | 45 | 18 | 0.68 | 0.45 | 0.60 | 0.59 | Baja posibilidad |
| 12:00 | 60 | 30 | 22 | 0.60 | 0.30 | 0.40 | 0.47 | Baja posibilidad |
| 14:00 | 75 | 70 | 20 | 0.75 | 0.70 | 0.50 | 0.68 | Lluvia probable |
| 16:00 | 85 | 85 | 18 | 0.85 | 0.85 | 0.60 | 0.80 | Lluvia |
| 18:00 | 92 | 95 | 16 | 0.92 | 0.95 | 0.70 | 0.89 | Lluvia |
| 20:00 | 88 | 90 | 17 | 0.88 | 0.90 | 0.65 | 0.84 | Lluvia |
| 22:00 | 80 | 75 | 15 | 0.80 | 0.75 | 0.75 | 0.78 | Lluvia |

La única diferencia está en 20:00 y 22:00, horas con temperaturas (17 °C, 15 °C) que no estaban en la tabla original: el modelo discreto las redondea hacia el siguiente escalón, el ajustado las calcula de forma exacta.

## Preguntas de control

> Nota: estas preguntas de la guía corresponden a un modelo de **crecimiento exponencial** (`P(t) = P₀·eʳᵗ`), no al modelo de índice de lluvia de esta práctica. Se responden en términos generales de modelado matemático.

1. **¿Qué es un modelo matemático?** Una representación simplificada de un fenómeno real mediante variables, parámetros y relaciones (ecuaciones) que permite predecir o explicar su comportamiento.
2. **¿Diferencia entre variable y parámetro?** La variable cambia con cada observación (en esta práctica: H, N, Tf, según la hora). El parámetro es un valor fijo que define el modelo (los pesos 0.5/0.3/0.2, o los umbrales 0.40/0.60/0.75).
3. **¿Qué representa P₀?** Es la condición inicial de un modelo de crecimiento/decrecimiento exponencial. No aplica a este modelo porque no es dinámico ni tiene condición inicial: calcula un índice puntual por hora.
4. **¿Qué ocurre cuando r < 0?** En un modelo exponencial, produce decrecimiento en vez de crecimiento.
5. **¿Limitaciones del modelo exponencial?** No tiene techo (crece o decrece sin límite), ignora factores externos que frenan el proceso, y deja de ser realista a largo plazo.
