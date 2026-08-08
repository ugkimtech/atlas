from rich import print
from pathlib import Path
from ..workspace.files import read_json, read_file
from .backend.django.manager import DjangoManager
from .frontend.reactjs.manager import ReactjsManager
from ..core.pipeline import Pipeline

class ProjectManager:
    def __init__(self):
        self.current_dir = Path(".")
        self.docs_path = Pipeline().docs_path()
        self.specs = read_json(Path(self.docs_path)/"project_spec.json")
        self.reqs =  read_file(Path(self.docs_path)/"requirements.md")
        self.arch =  read_file(Path(self.docs_path)/"architecture.md")
        self.erd =  read_file(Path(self.docs_path)/"erd.md")
        self.api =  read_file(Path(self.docs_path)/"api.md")
        self.blueprint = read_json(Path(self.docs_path)/"project_blueprint.json")
    
    
    def start_project(self):
        backend = ''
        frontend = ''
        specs = read_json(Path(self.docs_path)/"project_spec.json")
        try:
            if specs["backend"]:
                backend = specs["backend"]
                
                match(backend):
                    case "django":
                        django = DjangoManager(self.specs, self.reqs, self.arch, self.erd, self.api, self.blueprint)
                        django.start_django()
                        
        except KeyError:
            print("Continuing without backend...")
        
        try:
            if specs["frontend"]:
                frontend = specs["frontend"]
                
                match(frontend):
                    case "reactjs":
                        ReactjsManager()
                        
        except KeyError:
            print("Continuing without frontend...")