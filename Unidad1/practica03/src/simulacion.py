import simpy
import numpy as np

from src.teoria import es_estable


def simular(lam, mu, tiempo_simulacion=1000, semilla=42):
    """
    Cola M/M/1 con un unico servidor

    Parametros:
        lam: tasa promedio de llegada de clientes.
        mu: tasa promedio de servicio.
        tiempo_simulacion: duracion de la simulacion.
        semilla: semilla para reproducir la simulacion.

    Retorna:
        Diccionario con los resultados de la simulacion.
    """

    # Validar parametros
    if lam <= 0 or mu <= 0:
        raise ValueError("Las tasas deben ser mayores que cero.")

    if tiempo_simulacion <= 0:
        raise ValueError("El tiempo de simulacion debe ser positivo.")

    if not es_estable(lam, mu):
        raise ValueError("El sistema no es estable.") 

    # Generador de numeros aleatorios
    rng = np.random.default_rng(semilla)

    # Crear entorno y servidor
    env = simpy.Environment()
    servidor = simpy.Resource(env, capacity=1)

    # Variables de la simulacion
    tiempos_espera = []
    tiempos_sistema = []
    tamanos_cola = []
    muestras_cola = []

    clientes_llegados = 0
    clientes_atendidos = 0

    def atender_cliente(numero):

        """Llegada, espera y atencion de un cliente."""
        nonlocal clientes_atendidos

        llegada = env.now

        # Registrar cuantos clientes esperan al llegar
        tamanos_cola.append(len(servidor.queue))
        muestras_cola.append((env.now, len(servidor.queue)))
        

        # Solicitar el servidor
        with servidor.request() as solicitud:
            yield solicitud

            # Registrar inicio del servicio y tiempo de espera
            inicio_servicio = env.now
            tiempos_espera.append(inicio_servicio - llegada)

            # Registrar la cola cuando el cliente sale de ella
            muestras_cola.append((env.now, len(servidor.queue)))

            # Generar duracion aleatoria del servicio
            tiempo_servicio = rng.exponential(1 / mu)

            # Atender al cliente
            yield env.timeout(tiempo_servicio)

            # Registrar finalizacion
            tiempos_sistema.append(env.now - llegada)
            clientes_atendidos += 1

    def generar_clientes():
        """Genera clientes segun el proceso de llegadas."""
        nonlocal clientes_llegados

        while True:
            # Tiempo entre llegadas con distribucion exponencial
            intervalo = rng.exponential(1 / lam)

            # Esperar hasta la siguiente llegada
            yield env.timeout(intervalo)

            # No admitir clientes fuera del periodo de simulacion
            if env.now >= tiempo_simulacion:
                break

            clientes_llegados += 1
            env.process(atender_cliente(clientes_llegados))

    # Iniciar la generacion de clientes
    env.process(generar_clientes())

    # Ejecutar la simulacion
    env.run(until=tiempo_simulacion)

    # Devolver estadisticas simuladas
    return {
        "clientes_llegados": clientes_llegados,
        "clientes_atendidos": clientes_atendidos,
        "clientes_pendientes": clientes_llegados - clientes_atendidos,
        "Wq_simulado": (
            float(np.mean(tiempos_espera))
            if tiempos_espera else 0.0
        ),
        "W_simulado": (
            float(np.mean(tiempos_sistema))
            if tiempos_sistema else 0.0
        ),
        "cola_promedio_en_llegadas": (
            float(np.mean(tamanos_cola))
            if tamanos_cola else 0.0
        ),
        "tiempo_simulacion": tiempo_simulacion,
        "tiempos_espera": tiempos_espera,
        "muestras_cola": muestras_cola,
    }

simular_mm1 = simular