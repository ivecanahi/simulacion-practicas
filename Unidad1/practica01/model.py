"""
Modelo (M de MVC): logica matematica pura del indice de probabilidad de lluvia.

Formula entregada en la guia:
    I = 0.5*H + 0.3*N + 0.2*Tf

donde H = humedad normalizada, N = nubosidad normalizada y Tf = factor de
temperatura (obtenido de una tabla de referencia). Este modulo no sabe nada
de consola ni de graficas: solo calcula.
"""

# Tabla de factor de temperatura entregada por la guia de la practica.
# Cada fila es (temperatura en C, Tf correspondiente).
TEMPERATURE_TABLE = [
    (10, 1.00),
    (12, 0.90),
    (14, 0.80),
    (16, 0.70),
    (18, 0.60),
    (20, 0.50),
    (22, 0.40),
    (24, 0.30),
    (26, 0.20),
    (28, 0.10),
]

# Pesos fijos de la formula I = W_H*H + W_N*N + W_TF*Tf
W_H, W_N, W_TF = 0.5, 0.3, 0.2


def normalize(value):
    """Convierte un porcentaje (0-100) a proporcion (0-1). Ej: 65 -> 0.65."""
    return value / 100


def temperature_factor_discrete(temp):
    """
    Modelo ORIGINAL: busca Tf recorriendo la tabla tal cual la entrega la guia.
    Si la temperatura cae entre dos filas de la tabla (ej. 17C), se usa el
    siguiente escalon hacia arriba (comportamiento tipo "tabla de reglas").
    """
    if temp <= TEMPERATURE_TABLE[0][0]:
        return TEMPERATURE_TABLE[0][1]
    if temp >= TEMPERATURE_TABLE[-1][0]:
        return TEMPERATURE_TABLE[-1][1]
    for t_table, tf in TEMPERATURE_TABLE:
        if temp <= t_table:
            return tf
    return TEMPERATURE_TABLE[-1][1]


def temperature_factor_continuous(temp):
    """
    Modelo AJUSTADO (punto 5 de la guia: "ajuste el modelo y llene de nuevo
    la tabla"). Se observa que la tabla original es en realidad una recta:
    Tf baja 0.05 por cada grado que sube la temperatura desde 10C.
    Esto permite calcular Tf para CUALQUIER temperatura, no solo las que
    aparecen en la tabla (ej. 15C o 17C), sin perder los valores limite.
    """
    tf = 1.00 - 0.05 * (temp - 10)
    return min(1.00, max(0.10, tf))  # se mantiene dentro de [0.10, 1.00]


def compute_index(humidity, cloudiness, temp, tf_function):
    """
    Aplica la formula del indice para una hora puntual.
    tf_function decide si se usa el modelo discreto o el ajustado.
    Devuelve los 4 valores (H, N, Tf, Indice) para poder mostrarlos despues.
    """
    h = normalize(humidity)
    n = normalize(cloudiness)
    tf = tf_function(temp)
    index = W_H * h + W_N * n + W_TF * tf
    return h, n, tf, index


def classify_state(index):
    """Traduce el indice numerico al estado segun la 'Tabla de reglas' de la guia."""
    if index < 0.40:
        return "Sin lluvia"
    if index < 0.60:
        return "Baja posibilidad"
    if index < 0.75:
        return "Lluvia probable"
    return "Lluvia"


class HourRecord:
    """
    Representa una fila de la tabla de la practica (una hora del dia).
    Guarda los datos crudos (humedad, nubosidad, temp) y, luego de llamar
    a process(), tambien los resultados calculados (H, N, Tf, indice, estado).
    """

    def __init__(self, hour, humidity, cloudiness, temp):
        self.hour = hour
        self.humidity = humidity
        self.cloudiness = cloudiness
        self.temp = temp
        self.h = self.n = self.tf = self.index = self.state = None

    def process(self, tf_function):
        """Calcula H, N, Tf, indice y estado para esta hora y los guarda en el objeto."""
        self.h, self.n, self.tf, self.index = compute_index(
            self.humidity, self.cloudiness, self.temp, tf_function
        )
        self.state = classify_state(self.index)
        return self
