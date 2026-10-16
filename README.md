# Simulación — Prácticas

Repositorio de prácticas de la asignatura **Simulación** (Ciclo 5, Carrera de Computación, UNL). Organizado por unidad del sílabo, una carpeta por unidad y una subcarpeta por práctica.

## Estructura

```
.
├── Unidad1/
│   ├── practica01/   # Construcción y simulación computacional de un modelo matemático
│   ├── practica02/   # Comparación de modelos determinísticos, estocásticos, discretos y continuos
│   └── practica03/   # Simulación de un sistema de líneas de espera M/M/1 mediante SimPy
├── Unidad2/
├── Unidad3/
├── assets/           # Logo y estilo compartidos por los reportes técnicos
├── tools/            # build_reports.sh: genera los reportes PDF
├── requirements.txt
└── .gitignore
```

Cada práctica es un proyecto Python independiente, con su propio `main.py` como punto de entrada. La organización interna del código (archivos y módulos) se describe en el `README.md` de cada práctica.

## Requisitos

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Si una práctica tiene su propio `requirements.txt` (por ejemplo, `practica03` usa SimPy y rich), se instala también desde su carpeta:

```bash
pip install -r Unidad1/practica03/requirements.txt
```

## Cómo correr una práctica

```bash
cd Unidad1/practica01
python3 main.py
```

Cada práctica tiene su propio `README.md` (descripción, tecnologías, instalación, configuración, uso, estructura e información adicional) y su reporte técnico `Reporte_Practica_NN.pdf`, basado en la plantilla de la carrera.

## Reportes técnicos

En `practica01` y `practica02`, el reporte se escribe en `reporte/reporte.html` y se genera en PDF con Chrome:

```bash
tools/build_reports.sh
```
