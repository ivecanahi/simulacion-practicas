# Simulación — Prácticas

Repositorio de prácticas de la asignatura **Simulación** (Ciclo 5, Carrera de Computación, UNL). Organizado por unidad del sílabo, una carpeta por unidad y una subcarpeta por práctica.

## Estructura

```
.
├── Unidad1/
│   ├── practica01/   # Construcción y simulación computacional de un modelo matemático
│   └── practica02/   # Comparación de modelos determinísticos, estocásticos, discretos y continuos
├── Unidad2/
├── Unidad3/
├── assets/           # Logo y estilo compartidos por los reportes técnicos
├── tools/            # build_reports.sh: genera los reportes PDF
├── requirements.txt
└── .gitignore
```

Cada práctica es un proyecto Python independiente (su propio `main.py`), construido con arquitectura **MVC (Modelo-Vista-Controlador)**:

- **model.py** — lógica matemática pura (sin I/O).
- **controller.py** — datos de entrada y orquestación entre modelo y vista.
- **view.py** — salida en consola y gráficas (matplotlib).
- **main.py** — punto de entrada que arma el flujo completo.

## Requisitos

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Cómo correr una práctica

```bash
cd Unidad1/practica01
python3 main.py
```

Cada práctica tiene su propio `README.md` (descripción, tecnologías, instalación, configuración, uso, estructura e información adicional) y su reporte técnico `Reporte_Practica_NN.pdf`, basado en la plantilla de la carrera.

## Reportes técnicos

El reporte de cada práctica se escribe en `reporte/reporte.html` y se genera en PDF con Chrome:

```bash
tools/build_reports.sh
```
