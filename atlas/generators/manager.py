from rich import print
from pathlib import Path
from ..workspase.files import read_json
from .backend.django.manager import DjangoManager
from .frontend.reactjs.manager import ReactjsManager

class ProjectManager:
    def __init__(self):
        self.current_dir = Path(".")
        self.docs_path = None
        for folder in self.current_dir.iterdir():
            if not folder.is_file() and folder.name == "atlas-docs":
                self.docs_path = Path(self.current_dir)/"atlas-docs"
            else:
                print("[red]You are not within the project folder. please first run [green]cd <your project folder>[/green] to proceed[/red]")
    
    
    def start_peoject(self):
        backend = ''
        frontend = ''
        specs = read_json(Path(docs_path)/"project_spec.json")
        if specs["backend"]:
            backend = specs["backend"]
            
            match(backend):
                case "django":
                    DjangoManager()
            
        if specs["frontend"]:
            frontend = specs["frontend"]
            match(frontend):
                case "reactjs":
                    ReactjsManager()
            # call frontend manager