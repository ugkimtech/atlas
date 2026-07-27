import typer
from rich import print
from ...core.orchestrator import Orchestrator


def start_atlas():
    print("\n[bold blue] Welcome to Atlas, let's dive into the full SDLC [/bold blue]\n")
    Orchestrator().start()