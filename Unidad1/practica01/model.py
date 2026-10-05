"""
Modelo (M de MVC): logica matematica pura del indice de probabilidad de lluvia.

Formula entregada en la guia:
    I = W_H*H + W_N*N + W_TF*Tf

donde H = humedad normalizada, N = nubosidad normalizada y Tf = factor de
temperatura (obtenido de la tabla de referencia de la guia), y W_H+W_N+W_TF
siempre suma 1 (es un promedio ponderado). Este modulo no sabe nada de
consola ni de graficas: solo calcula.
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

# Modelo ORIGINAL: pesos (W_H, W_N, W_TF) tal cual los da la guia. Suman 1.
WEIGHTS_ORIGINAL = (0.5, 0.3, 0.2)

# Modelo AJUSTADO: misma formula y mismas variables (H, N, Tf), pero con
# otra combinacion de pesos que tambien suma 1. Le da mas peso a la
# temperatura para ver como cambia el indice frente al modelo original.
WEIGHTS_ADJUSTED = (0.4, 0.3, 0.3)


def normalize(value):
    """Convierte un porcentaje (0-100) a proporcion (0-1). Ej: 65 -> 0.65."""
    return value / 100


def temperature_factor(temp):
    """
    Busca Tf en TEMPERATURE_TABLE siguiendo la 'tabla de reglas' de la guia
    (<=10C -> 1.00, >=28C -> 0.10). Para una temperatura que no esta en la
    tabla (ej. 17C), se toma el siguiente escalon igual o mayor, que es como
    esta redactada la tabla de reglas original. Es la misma tabla para
    cualquier set de pesos: lo unico que cambia entre modelos es W_H/W_N/W_TF.
    """
    if temp <= TEMPERATURE_TABLE[0][0]:
        return TEMPERATURE_TABLE[0][1]
    if temp >= TEMPERATURE_TABLE[-1][0]:
        return TEMPERATURE_TABLE[-1][1]
    for t_table, tf in TEMPERATURE_TABLE:
        if temp <= t_table:
            return tf
    return TEMPERATURE_TABLE[-1][1]


def compute_index(humidity, cloudiness, temp, weights):
    """
    Aplica la formula del indice para una hora puntual con el set de pesos
    que se le pase (WEIGHTS_ORIGINAL o WEIGHTS_ADJUSTED).
    Devuelve los 4 valores (H, N, Tf, Indice) para poder mostrarlos despues.
    """
    w_h, w_n, w_tf = weights
    h = normalize(humidity)
    n = normalize(cloudiness)
    tf = temperature_factor(temp)
    index = w_h * h + w_n * n + w_tf * tf
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
    a process(), tambien los resultados calculados (H, N, Tf, indice, estado)
    para el set de pesos con el que se proceso.
    """

    def __init__(self, hour, humidity, cloudiness, temp):
        self.hour = hour
        self.humidity = humidity
        self.cloudiness = cloudiness
        self.temp = temp
        self.h = self.n = self.tf = self.index = self.state = None

    def process(self, weights):
        """Calcula H, N, Tf, indice y estado para esta hora, usando el set de pesos dado."""
        self.h, self.n, self.tf, self.index = compute_index(
            self.humidity, self.cloudiness, self.temp, weights
        )
        self.state = classify_state(self.index)
        return self
