# Práctica 01 — Construcción y simulación computacional de un modelo matemático

## 1. Descripción

Simula el comportamiento de la atmósfera a lo largo de un día y determina en qué horas existe posibilidad de lluvia. Para cada hora combina humedad, nubosidad y temperatura en un **índice de lluvia** y lo clasifica según la tabla de reglas de la guía.

- **Propósito:** comprender cómo se construye un modelo matemático (variables, parámetros y relaciones) y analizar cómo influyen sus parámetros.
- **Problema que resuelve:** a partir de datos atmosféricos crudos, predice el estado del clima hora a hora y compara el modelo original con un modelo ajustado.

### El modelo

```
I = W_H·H + W_N·N + W_TF·Tf
```

| Símbolo | Significado |
|---|---|
| `H` | Humedad normalizada (0–1) |
| `N` | Nubosidad normalizada (0–1) |
| `Tf` | Factor de temperatura, tomado de la tabla de la guía |
| `W_H, W_N, W_TF` | Pesos de cada variable. Suman **1**, porque `I` es un promedio ponderado |

| Índice I | Estado |
|---|---|
| I < 0.40 | Sin lluvia |
| 0.40 ≤ I < 0.60 | Baja posibilidad |
| 0.60 ≤ I < 0.75 | Lluvia probable |
| I ≥ 0.75 | Lluvia |

| Modelo | W_H | W_N | W_TF |
|---|---|---|---|
| Original (guía) | 0.5 | 0.3 | 0.2 |
| Ajustado | 0.4 | 0.3 | 0.3 |

El modelo ajustado no cambia la fórmula ni las variables: solo redistribuye los pesos, dándole más peso a la temperatura.

## 2. Tecnologías utilizadas

| Tecnología | Uso |
|---|---|
| Python 3.12 | Lenguaje de implementación |
| NumPy 1.26 | Cálculo numérico |
| Matplotlib 3.9 | Gráficas |

## 3. Instalación

Desde la raíz del repositorio:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## 4. Configuración

No requiere variables de entorno. Los valores del modelo se editan en el código:

| Qué cambiar | Dónde |
|---|---|
| Pesos del modelo original y ajustado | `WEIGHTS_ORIGINAL`, `WEIGHTS_ADJUSTED` en `model.py` |
| Tabla del factor de temperatura | `TEMPERATURE_TABLE` en `model.py` |
| Datos de entrada (hora, humedad, nubosidad, temperatura) | `BASE_DATA` en `controller.py` |

## 5. Uso

```bash
cd Unidad1/practica01
python3 main.py
```

Imprime en consola la tabla de cada modelo y genera estas gráficas:

| Archivo | Qué muestra |
|---|---|
| `indice_lluvia.png` | Índice original vs. ajustado durante el día, sobre las franjas de la tabla de reglas |
| `factor_temperatura.png` | Influencia de la temperatura en Tf |
| `variables_entrada.png` | Evolución de H, N y Tf a lo largo del día |
| `contribucion_variables.png` | Aporte de cada término (peso × variable) al índice |

Ejemplo de salida:

```
Modelo original (pesos 0.5 / 0.3 / 0.2)
Hora    Humedad  Nubosidad  Temp      H      N     Tf   Indice  Estado
----------------------------------------------------------------------
06:00        65         40    14   0.65   0.40   0.80     0.60  Lluvia probable
...
18:00        92         95    16   0.92   0.95   0.70     0.89  Lluvia
```

## 6. Estructura del proyecto

Arquitectura **MVC (Modelo-Vista-Controlador)**:

```
practica01/
├── model.py        # Fórmula del índice, tabla de Tf y clasificación (sin I/O)
├── controller.py   # Datos de la guía y orquestación del modelo
├── view.py         # Tablas por consola y gráficas
├── main.py         # Punto de entrada: controller → model → view
├── *.png           # Gráficas generadas
├── reporte/        # Fuente HTML del reporte técnico
└── Reporte_Practica_01.pdf
```

## 7. Información adicional

### Resultados principales

| Hora | Índice original | Índice ajustado | Estado |
|---|---|---|---|
| 06:00 | 0.60 | 0.62 | Lluvia probable |
| 12:00 | 0.47 | 0.45 | Baja posibilidad |
| 16:00 | 0.80 | 0.77 | Lluvia |
| 18:00 | 0.89 | 0.86 | Lluvia |

- El modelo predice lluvia desde las 16:00 hasta las 22:00, cuando la humedad y la nubosidad son altas y la temperatura baja.
- Al pasar peso de la humedad a la temperatura, el índice baja levemente, pero la clasificación casi no cambia.

Las tablas completas, la interpretación y las preguntas de control están en el **[reporte técnico](Reporte_Practica_01.pdf)**.

### Notas

- Para temperaturas que no están en la tabla (15 °C, 17 °C) se usa el siguiente escalón igual o mayor.
- La guía también pide una versión en Java; este repositorio contiene solo la implementación en Python.
