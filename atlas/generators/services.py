from pathlib import Path
import os


def docs_path():
    current_dir = Path(os.getcwd())
    for folder in current_dir.iterdir():
        if not folder.is_file() and folder.name == "atlas-docs":
            return Path(current_dir)/"atlas-docs"
    print("[red]Not in project root folder! run [bold]cd <path/to/project>[/bold] To proceed.[/red]")
    return None