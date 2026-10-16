from rich.console import Console

from src.consola import (
    color_error,
    mostrar_encabezado,
    mostrar_escenario,
    mostrar_inestable,
    mostrar_tabla,
)

ESCENARIO = {"escenario": 3, "lam": 2.9, "mu": 3.0, "condicion": "Cerca de saturacion"}
RESULTADO = {
    "escenario": 3,
    "lam": 2.9,
    "mu": 3.0,
    "rho": 0.9667,
    "L": 29.0,
    "Lq": 28.0333,
    "W": 10.0,
    "Wq": 9.6667,
    "espera_promedio": 8.2279,
    "cola_promedio": 23.7584,
    "clientes_atendidos": 28950,
    "error_Wq_%": 14.884,
    "error_Lq_%": 15.249,
}


def consola_de_prueba():
    return Console(record=True, width=140, color_system=None)


def test_color_error_por_rango():
    assert color_error(5.0) == "green"
    assert color_error(14.9) == "yellow"
    assert color_error(25.0) == "red"


def test_encabezado_muestra_escenarios_y_parametros():
    consola = consola_de_prueba()
    mostrar_encabezado([ESCENARIO], 10000, 42, consola)
    texto = consola.export_text()
    assert "M/M/1" in texto
    assert "Cerca de saturacion" in texto
    assert "10000" in texto
    assert "42" in texto


def test_escenario_muestra_teorico_y_simulado():
    consola = consola_de_prueba()
    mostrar_escenario(ESCENARIO, RESULTADO, consola)
    texto = consola.export_text()
    assert "Escenario 3" in texto
    assert "9.667" in texto
    assert "8.228" in texto
    assert "28,950" in texto


def test_tabla_muestra_todas_las_metricas():
    consola = consola_de_prueba()
    mostrar_tabla([RESULTADO], consola)
    texto = consola.export_text()
    for valor in ["0.967", "29.000", "28.033", "10.000", "9.667", "8.228", "23.758", "14.9%", "15.2%"]:
        assert valor in texto


def test_inestable_avisa_al_usuario():
    consola = consola_de_prueba()
    mostrar_inestable(4, 3.5, 3.0, consola)
    assert "no es estable" in consola.export_text()
