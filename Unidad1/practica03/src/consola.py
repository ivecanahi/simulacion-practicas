"""Console presentation for the M/M/1 simulation results."""

from rich import box
from rich.console import Console, Group
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

CONSOLA = Console()


def color_error(error):
    """Green below 10 %, yellow below 20 %, red otherwise."""
    if error < 10:
        return "green"
    if error < 20:
        return "yellow"
    return "red"


def barra_utilizacion(rho, ancho=30):
    """Text bar showing how busy the server is."""
    llenos = round(rho * ancho)
    color = "green" if rho < 0.8 else "yellow" if rho < 0.95 else "red"
    barra = Text("█" * llenos, style=color)
    barra.append("░" * (ancho - llenos), style="dim")
    barra.append(f" {rho:.1%}", style=f"bold {color}")
    return barra


def mostrar_encabezado(escenarios, tiempo_sim, semilla, consola=CONSOLA):
    tabla = Table(box=box.SIMPLE_HEAVY, header_style="bold cyan", show_edge=False)
    tabla.add_column("Escenario", justify="center")
    tabla.add_column("λ (llegadas)", justify="right")
    tabla.add_column("μ (servicio)", justify="right")
    tabla.add_column("Condición")
    for esc in escenarios:
        tabla.add_row(
            str(esc["escenario"]), f"{esc['lam']:.1f}", f"{esc['mu']:.1f}", esc["condicion"]
        )

    parametros = Text.assemble(
        ("Tiempo de simulación: ", "dim"),
        (str(tiempo_sim), "bold"),
        ("   ·   Semilla: ", "dim"),
        (str(semilla), "bold"),
    )
    consola.print()
    consola.print(
        Panel(
            Group(tabla, Text(), parametros),
            title="[bold]Simulación de una cola M/M/1 con SimPy[/bold]",
            subtitle="APE 3 · Simulación",
            border_style="cyan",
            padding=(1, 2),
            expand=False,
        )
    )


def mostrar_escenario(esc, resultado, consola=CONSOLA):
    tabla = Table(box=box.ROUNDED, header_style="bold")
    tabla.add_column("Métrica")
    tabla.add_column("Teórico", justify="right", style="cyan")
    tabla.add_column("Simulado", justify="right", style="magenta")
    tabla.add_column("Error", justify="right")
    filas = [
        ("Wq · espera en cola", "Wq", "espera_promedio", "error_Wq_%"),
        ("Lq · clientes en cola", "Lq", "cola_promedio", "error_Lq_%"),
    ]
    for nombre, teorico, simulado, error in filas:
        e = resultado[error]
        tabla.add_row(
            nombre,
            f"{resultado[teorico]:.3f}",
            f"{resultado[simulado]:.3f}",
            Text(f"{e:.1f}%", style=color_error(e)),
        )

    resumen = Text.assemble(
        ("Utilización ρ  ", "bold"), barra_utilizacion(resultado["rho"]), "\n",
        ("Clientes atendidos  ", "bold"), (f"{resultado['clientes_atendidos']:,}", ""),
    )
    consola.print()
    consola.print(
        Panel(
            Group(resumen, Text(), tabla),
            title=f"[bold]Escenario {esc['escenario']}[/bold] · {esc['condicion']}",
            subtitle=f"λ = {esc['lam']:.1f}   μ = {esc['mu']:.1f}",
            border_style="blue",
            padding=(1, 2),
            expand=False,
        )
    )


def mostrar_inestable(numero, lam, mu, consola=CONSOLA):
    consola.print(
        Panel(
            f"λ = {lam} ≥ μ = {mu}: el sistema no es estable y la cola crecería sin límite.",
            title=f"[bold]Escenario {numero}[/bold] · omitido",
            border_style="red",
            expand=False,
        )
    )


def mostrar_tabla(resultados, consola=CONSOLA):
    tabla = Table(
        title="[bold]Comparación teórico vs. simulado[/bold]",
        box=box.ROUNDED,
        header_style="bold",
        show_lines=False,
    )
    tabla.add_column("Esc.", justify="center")
    tabla.add_column("λ", justify="right")
    tabla.add_column("ρ", justify="right")
    for columna in ["L", "Lq", "W", "Wq"]:
        tabla.add_column(columna, justify="right", style="cyan")
    tabla.add_column("Wq sim.", justify="right", style="magenta")
    tabla.add_column("Lq sim.", justify="right", style="magenta")
    tabla.add_column("Error Wq", justify="right")
    tabla.add_column("Error Lq", justify="right")

    for r in resultados:
        tabla.add_row(
            str(r["escenario"]),
            f"{r['lam']:.1f}",
            f"{r['rho']:.3f}",
            f"{r['L']:.3f}",
            f"{r['Lq']:.3f}",
            f"{r['W']:.3f}",
            f"{r['Wq']:.3f}",
            f"{r['espera_promedio']:.3f}",
            f"{r['cola_promedio']:.3f}",
            Text(f"{r['error_Wq_%']:.1f}%", style=color_error(r["error_Wq_%"])),
            Text(f"{r['error_Lq_%']:.1f}%", style=color_error(r["error_Lq_%"])),
        )

    consola.print()
    consola.print(tabla)
    consola.print(
        "[cyan]■[/cyan] teórico   [magenta]■[/magenta] simulado   "
        "error: [green]< 10 %[/green]  [yellow]< 20 %[/yellow]  [red]≥ 20 %[/red]"
    )


def mostrar_archivos(rutas, consola=CONSOLA):
    lista = Text("\n").join(Text.assemble(("✔ ", "green"), ruta) for ruta in rutas)
    consola.print()
    consola.print(
        Panel(
            lista,
            title="[bold]Archivos generados[/bold]",
            border_style="green",
            padding=(1, 2),
            expand=False,
        )
    )
