from .pipeline import Pipeline
from rich import print
import typer
import os
from pathlib import Path
from ..workspace.files import read_json, read_file
from ..generators.manager import ProjectManager


class Orchestrator:
    def __init__(self):
        self.current_dir = Path(".")
        self.pipeline = Pipeline()
    
    def start(self):
        # Load project
        project = self.pipeline.load_project()
        if project == "new":
            requirements = self.pipeline.get_requirements()
            if not requirements:
                return False
            if not self.pipeline.project_root(requirements["project_name"]):
                return False
            if not self.pipeline.create_spec(requirements):
                return False
            if not self.pipeline.create_state():
                return False
            if not self.pipeline.create_requirements_md():
                return False
            
            print("\nInitial stage completed, do you want to proceed right from here without changing working folder? [bold]Nonte:[/bold] This only works for this session. change to project folder the next time you come back\n")
            opt = typer.prompt("Proceed from here? (y/n)")
            if opt.lower() == 'y':
                return self.existing_project()
            return True
        else:
            self.existing_project()
        
        
    def existing_project(self):
        
        while True:
            # get state
            state = read_json(Path(self.pipeline.docs_path())/"state.json")
            print(f"Current state: {state['current_state']}")
            if not self.sub_command(state["current_state"]):
                break
        
        # initialize the project
        
        # create project skeleton
        
        # code
        
        # test
        
        # deploy
        
        
    def sub_command(self, command):
        
        match(command):
            case "sync":
                req_md = self.pipeline.create_requirements_md()
                arc = self.pipeline.create_architecture_md()
                erd =self.pipeline.create_erd()
                api = self.pipeline.create_api_md()
                if req_md and arc and erd and api:
                    return True
                else:
                    return False
                    
            case "architecture":
                if self.pipeline.create_architecture_md():
                    return True
                return False
            
            case "ERD":
                if self.pipeline.create_erd():
                    return True
                return False
            
            case "API":
                if self.pipeline.create_api_md():
                    return True
                return False
                
            case "init-project":
                ProjectManager().start_project()
            
            case _:
                print(f"[red]Unknown command: {command}[/red]")
                return None