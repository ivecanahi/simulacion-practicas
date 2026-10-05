# Simulación — Prácticas

Repositorio de prácticas de la asignatura **Simulación** (Ciclo 5, Carrera de Computación, UNL). Organizado por unidad del sílabo, una carpeta por unidad y una subcarpeta por práctica.

## Estructura

```
.
├── Unidad1/
│   └── practica01/   # Construcción y simulación computacional de un modelo matemático
├── Unidad2/
├── Unidad3/
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

Cada práctica tiene su propio `README.md` con el objetivo, el modelo usado y la interpretación de resultados.
