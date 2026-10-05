"""
Controlador (C de MVC): conecta los datos de entrada con el modelo y
decide que se ejecuta. No calcula nada por si mismo ni dibuja nada:
solo orquesta.
"""
from model import HourRecord

# Datos de la tabla de la guia (Hora, Humedad%, Nubosidad%, Temperatura C).
BASE_DATA = [
    ("06:00", 65, 40, 14),
    ("08:00", 70, 50, 16),
    ("10:00", 68, 45, 18),
    ("12:00", 60, 30, 22),
    ("14:00", 75, 70, 20),
    ("16:00", 85, 85, 18),
    ("18:00", 92, 95, 16),
    ("20:00", 88, 90, 17),
    ("22:00", 80, 75, 15),
]


class RainSimulationController:
    """Recibe los datos crudos y le pide al modelo que procese cada hora."""

    def __init__(self, data):
        self.data = data

    def run(self, weights):
        """Crea un HourRecord por cada fila de BASE_DATA y lo procesa con el set de pesos dado."""
        return [HourRecord(*row).process(weights) for row in self.data]
