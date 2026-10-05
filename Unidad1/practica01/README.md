# Práctica 01 — Construcción y simulación computacional de un modelo matemático

**Objetivo:** comprender el proceso de construcción de un modelo matemático y analizar su comportamiento mediante Python, implementando un modelo de predicción de lluvia a partir de humedad, nubosidad y temperatura.

## El modelo

```
I = W_H*H + W_N*N + W_TF*Tf
```

- `H` = humedad normalizada (0–1)
- `N` = nubosidad normalizada (0–1)
- `Tf` = factor de temperatura, tomado de la tabla de la guía
- `W_H, W_N, W_TF` = pesos de cada variable. Siempre suman **1**, porque `I` es un promedio ponderado.

| Índice I | Estado |
|---|---|
| I < 0.40 | Sin lluvia |
| 0.40 ≤ I < 0.60 | Baja posibilidad |
| 0.60 ≤ I < 0.75 | Lluvia probable |
| I ≥ 0.75 | Lluvia |

Para temperaturas que no están exactamente en la tabla de `Tf` (ej. 15 °C, 17 °C), se usa el siguiente escalón igual o mayor, siguiendo la misma lógica de "tabla de reglas" con la que está redactada la tabla original (`≤10°C`, `≥28°C`).

## Modelo original vs. modelo ajustado

La guía pide ajustar el modelo y volver a llenar la tabla. El ajuste **no** cambia la fórmula ni las variables (siguen siendo H, N, Tf con la misma tabla de temperatura): cambia únicamente los **pesos**, manteniendo que sumen 1.

| | W_H | W_N | W_TF | Suma |
|---|---|---|---|---|
| Original (de la guía) | 0.5 | 0.3 | 0.2 | 1.0 |
| Ajustado | 0.4 | 0.3 | 0.3 | 1.0 |

El modelo ajustado le da más peso a la temperatura (`Tf`) y menos a la humedad, para observar cómo responde el índice ante esa redistribución.

## Arquitectura (MVC)

| Archivo | Rol |
|---|---|
| `model.py` | Fórmula del índice (con los dos sets de pesos), tabla de temperatura y clasificación de estado. Sin I/O. |
| `controller.py` | Datos de entrada (la tabla de la guía) y orquestación: le pide al modelo que procese cada hora con un set de pesos dado. |
| `view.py` | Tablas por consola y gráficas (`matplotlib`). |
| `main.py` | Arma el flujo: controller → model → view, para el modelo original y el ajustado. |

## Cómo correr

```bash
pip install -r ../../requirements.txt
python3 main.py
```

Genera `indice_lluvia.png` (índice original vs. ajustado durante el día) y `factor_temperatura.png` (influencia de la temperatura en Tf).

## Resultados

**Modelo original (pesos 0.5 / 0.3 / 0.2):**

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

**Modelo ajustado (pesos 0.4 / 0.3 / 0.3):**

| Hora | Humedad | Nubosidad | Temp | H | N | Tf | Índice | Estado |
|---|---|---|---|---|---|---|---|---|
| 06:00 | 65 | 40 | 14 | 0.65 | 0.40 | 0.80 | 0.62 | Lluvia probable |
| 08:00 | 70 | 50 | 16 | 0.70 | 0.50 | 0.70 | 0.64 | Lluvia probable |
| 10:00 | 68 | 45 | 18 | 0.68 | 0.45 | 0.60 | 0.59 | Baja posibilidad |
| 12:00 | 60 | 30 | 22 | 0.60 | 0.30 | 0.40 | 0.45 | Baja posibilidad |
| 14:00 | 75 | 70 | 20 | 0.75 | 0.70 | 0.50 | 0.66 | Lluvia probable |
| 16:00 | 85 | 85 | 18 | 0.85 | 0.85 | 0.60 | 0.77 | Lluvia |
| 18:00 | 92 | 95 | 16 | 0.92 | 0.95 | 0.70 | 0.86 | Lluvia |
| 20:00 | 88 | 90 | 17 | 0.88 | 0.90 | 0.60 | 0.80 | Lluvia |
| 22:00 | 80 | 75 | 15 | 0.80 | 0.75 | 0.70 | 0.76 | Lluvia |

Con menos peso en la humedad y más en la temperatura, el índice baja un poco en casi todas las horas (ej. 16:00 pasa de 0.80 a 0.77), aunque el estado final cambia poco porque los datos de este día son consistentemente húmedos y nublados.

## Preguntas de control

> Nota: estas preguntas de la guía corresponden a un modelo de **crecimiento exponencial** (`P(t) = P₀·eʳᵗ`), no al modelo de índice de lluvia de esta práctica. Se responden en términos generales de modelado matemático.

1. **¿Qué es un modelo matemático?** Una representación simplificada de un fenómeno real mediante variables, parámetros y relaciones (ecuaciones) que permite predecir o explicar su comportamiento.
2. **¿Diferencia entre variable y parámetro?** La variable cambia con cada observación (en esta práctica: H, N, Tf, según la hora). El parámetro es un valor fijo que define el modelo (los pesos W_H/W_N/W_TF, o los umbrales 0.40/0.60/0.75).
3. **¿Qué representa P₀?** Es la condición inicial de un modelo de crecimiento/decrecimiento exponencial. No aplica a este modelo porque no es dinámico ni tiene condición inicial: calcula un índice puntual por hora.
4. **¿Qué ocurre cuando r < 0?** En un modelo exponencial, produce decrecimiento en vez de crecimiento.
5. **¿Limitaciones del modelo exponencial?** No tiene techo (crece o decrece sin límite), ignora factores externos que frenan el proceso, y deja de ser realista a largo plazo.
