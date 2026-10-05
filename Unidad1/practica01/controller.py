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
    """Recibe los datos crudos y los procesa con la funcion Tf que se le indique."""

    def __init__(self, data):
        self.data = data

    def run(self, tf_function):
        """
        Crea un HourRecord por cada fila y lo procesa.
        tf_function = temperature_factor_discrete o temperature_factor_continuous,
        segun que version del modelo se quiera correr.
        """
        return [HourRecord(*row).process(tf_function) for row in self.data]
