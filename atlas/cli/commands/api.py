from rich import print
import typer
from ...core.orchestrator import Orchestrator

orch = Orchestrator()

def change_api():
    print("\nAre you sure you want to make changes to api.md? (y/n)\n")
    opt = typer.prompt("\t")
    if opt.lower() == "y":
        print("[yellow]Synchronizing other documents with api.md...[/yellow]")
        if orch.sub_command("API"):
            print("[green]Synchronized successfully.[/green]")
        else:
            print("Nothing chaged! try again.")
        return
    else:
        return