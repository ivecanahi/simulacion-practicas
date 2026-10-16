"""Theoretical metrics for the M/M/1 queueing model."""


def es_estable(lam, mu):
    """Return True when the arrival rate is lower than the service rate."""
    return lam < mu


def metricas_teoricas(lam, mu):
    """Return the theoretical M/M/1 metrics: rho, L, Lq, W and Wq."""
    if not es_estable(lam, mu):
        raise ValueError("El sistema no es estable")
    return {
        "rho": lam / mu,
        "L": lam / (mu - lam),
        "Lq": lam**2 / (mu * (mu - lam)),
        "W": 1 / (mu - lam),
        "Wq": lam / (mu * (mu - lam)),
    }
