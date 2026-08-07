from rich import print
import typer
from ...core.orchestrator import Orchestrator

orch = Orchestrator()

def sync_requirements():
    print("\nAre you sure you want to make changes to project documents? (y/n)\n")
    opt = typer.prompt("\t")
    if opt.lower() == "y":
        print("[yellow]Synchronizing project_spec.json with other documents...[/yellow]")
        if orch.sub_command("sync"):
            print("[green]Synchronized successfully.[/green]")
        else:
            print("Nothing chaged! try again.")
        return
    else:
        return


def architecture_md():
    print("\nAre you sure you want to make changes to architecture document? (y/n)\n")
    opt = typer.prompt("\t")
    if opt.lower() == "y":
        print("[yellow]Regenerating architecture.md...[/yellow]")
        if orch.sub_command("architecture"):
            print("[green]Regenerated successfully.[/green]")
        else:
            print("Nothing chaged! try again.")
        return
    else:
        return