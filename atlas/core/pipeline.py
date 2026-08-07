from pathlib import Path
import os
import json
from rich import print
import typer
from ..generators.menu_list.menu import run_menu
from ..agents.requirements_agent import Requirements, StructureRequirements
from ..workspace.files import create_folder, write_file, read_file, write_json, read_json
from ..workspace.state import init_state
from ..llm.manager import LLMManager


class Pipeline:
    def __init__(self):
        self.current_dir = Path(".")
    
    # Load/start project
    def load_project(self):
        menu_title = "Please select project\n"
        items = [
            {"item":"New Project",
                "return":"new"}, {"item":"Existing Project", "return":"existing"}
            ]
        return run_menu(menu_title, items)

    
    # get requirements
    def get_requirements(self):
        # gather requirements
        requirements = Requirements()
        specs = requirements.project_requirements()
        # polish requirements
        analyzer = StructureRequirements()
        polished_specs = analyzer.analyze_requirements(specs)
        if polished_specs:
            # structure requirements
            structured_specs = analyzer.structure(polished_specs)
            if structured_specs:
                return structured_specs
        print("[red]An error has occured during requirements analysis![/red]")
        return None
    
    
    # create project root folder
    def project_root(self, project_name):
        path = Path(self.current_dir)/project_name.replace(" ", "-").strip()
        print(f"[yellow]Creating project workspace...[bold]{path}[/bold]...[/yellow]")
        if create_folder(path):
            create_folder(Path(self.current_dir)/project_name.replace(" ", "-").strip()/"atlas-docs")
            print("[green]Workspace created.[/green]")
            os.chdir(path)##
            return True
        return None
        
        
    # get path to atlas documents
    def docs_path(self):
        for folder in self.current_dir.iterdir():
            if not folder.is_file() and folder.name == "atlas-docs":
                return Path(self.current_dir)/"atlas-docs"
        print("[red]Not in project root folder! run [bold]cd <path/to/project>[/bold] To proceed.[/red]")
        return None
        
        
    # create peoject specs
    def create_spec(self, specs):
        docs_path = self.docs_path()
        print("[yellow]Creating [bold]project_spec.json[/bold] file...[/yellow]")
        if not write_json(Path(docs_path)/"project_spec.json", specs):
            print("[red]An error has occured during creating project_spec.json![/red]")
            return None
        print("[green]project_spec.json created successfully.[/green]")
        return True
    
    
    # project status
    def create_state(self):
        docs_path = self.docs_path()
        if not docs_path:
            return False
        if not init_state(Path(docs_path)/"state.json"):
            return None
        return True
        
    
    # create requirements md
    def create_requirements_md(self):
        docs_path = self.docs_path()
        if not docs_path:
            return None
        specs = read_json(Path(docs_path)/"project_spec.json")
                
        print("[yellow]Preparing requirements.md file...[/yellow]")
        llm = LLMManager()
        prompt_var = {
            "project_specs":json.dumps(specs, indent=2)
        }
        req_md = llm.generate("requirements_md", prompt_var)
        req_md_path = Path(docs_path)/"requirements.md"
        state_path = Path(docs_path)/"state.json"
        
        if req_md:
            write_file(Path(docs_path)/"requirements.md", req_md)
            state = read_json(Path(docs_path)/"state.json")
            if not "requirements" in state["completed_states"]:
                state["completed_states"].append("requirements")
                state["current_state"] = "architecture"
                write_json(Path(docs_path)/"state.json", state)
                
            print("[green]requirements.md file created successfully.[/green]")
            project_name = specs["project_name"].replace(' ', '-')
            print("\n[green]Initial setup completed successfully! we are now ready to work.[/green]")
            print(f"\n\t[bold]ATTENTION\nPlease Check {os.getcwd()}/{project_name}/atlas-docs folder, read through [green]requirements.md[/green], verify if it meets well with your project requirements.")
            print("\n[pink]If something is missing, eddit [green]project_spec.json[/green] and then run [bold]\tatlas sync[/bold] to reflect changes to requirements.md\n")
            print("Let's pause a moment as you review.")
            print(f"\nATTENTION:\n\tMake sure on comming back to this project any time from now, change your command line interface working folder to {project_name} by running [green]cd {project_name}[/green] or maybe open new command interface with in {project_name} folder, then run [green]atlas proceed[/green] to proceed with the project.")
            return True
        else:
            return False
    
    
    # create architecture md
    def create_architecture_md(self):
        docs_path = self.docs_path()
        if not docs_path:
            return None
        specs = read_json(Path(docs_path)/"project_spec.json")
        requirements_md = read_file(Path(docs_path)/"requirements.md")
        
        print("[yellow]Preparing architecture.md file...[/yellow]")
        llm = LLMManager()
        prompt_var = {
            "project_specs":json.dumps(specs, indent=2),
            "requirements_md":requirements_md
        }
        arch = llm.generate("architecture", prompt_var)
        
        if arch:
            write_file(Path(docs_path)/"architecture.md", arch)
            
            state = read_json(Path(docs_path)/"state.json")
            if not "architecture" in state["completed_states"]:
                state["completed_states"].append("architecture")
                state["current_state"] = "ERD"
                write_json(Path(docs_path)/"state.json", state)
            print("[green]architecture.md file created successfully.[/green]")
            return True
        else:
            return False
    
    
    # create project blueprint
    def create_blueprint(self):
        docs_path = self.docs_path()
        if not docs_path:
            return None
        specs = read_json(Path(docs_path)/"project_spec.json")
        requirements_md = read_file(Path(docs_path)/"requirements.md")
        architecture_md = read_file(Path(docs_path)/"architecture.md")
        
        print("[yellow]Preparing project_blueprint.json file...[/yellow]")
        
        llm = LLMManager()
        blue_var = {
            "project_specs":json.dumps(specs, indent=2),
            "requirements_md":requirements_md,
            "architecture":architecture_md
        }
        blueprint = llm.generate("blueprint", blue_var)
        
        try:
            blueprint = json.loads(blueprint)
        except TypeError:
            print(f"[red]Response can't be structured! {blueprint}")
        
        if blueprint:
            write_json(Path(docs_path)/"project_blueprint.json", blueprint)
            
            state = read_json(Path(docs_path)/"state.json")
            if not "blueprint" in state["completed_states"]:
                state["completed_states"].append("blueprint")
                state["current_state"] = "ERD"
                write_json(Path(docs_path)/"state.json", state)
            print("[green]project_blueprint.json created successfully.[/green]")
            return True
        else:
            return False
            
            
    # create ERD md
    def create_erd(self):
        docs_path = self.docs_path()
        if not docs_path:
            return False
        specs = read_json(Path(docs_path)/"project_spec.json")
        reqs = read_file(Path(docs_path)/"requirements.md")
        arch = read_file(Path(docs_path)/"architecture.md")
        
        print("[yellow]Preparing erd.md file...[/yellow]")
        llm = LLMManager()
        prompt_var = {
            "project_specs":json.dumps(specs, indent=2),
            "requirements_md":reqs,
            "architecture_md":arch
        }
        erd_md = llm.generate("erd", prompt_var)
        
        if erd_md:
            write_file(Path(docs_path)/"erd.md", erd_md)
            state = read_json(Path(docs_path)/"state.json")
            if not "API" in state["completed_states"]:
                state["completed_states"].append("ERD")
                state["current_state"] = "API"
                write_json(Path(docs_path)/"state.json", state)
            print("[green]erd.md file created successfully.[/green]")
            return True
        else:
            return False
    
    # create api md
    def create_api_md(self):
        docs_path = self.docs_path()
        if not docs_path:
            return False
        specs = read_json(Path(docs_path)/"project_spec.json")
        reqs = read_file(Path(docs_path)/"requirements.md")
        arch = read_file(Path(docs_path)/"architecture.md")
        erd_md = read_file(Path(docs_path)/"erd.md")
        
        print("[yellow]Preparing api.md file...[/yellow]")
        llm = LLMManager()
        prompt_var = {
            "project_specs":json.dumps(specs, indent=2),
            "requirements_md":reqs,
            "architecture_md":arch,
            "erd_md":erd_md
        }
        api_md = llm.generate("api", prompt_var)
        
        if api_md:
            write_file(Path(docs_path)/"api.md", api_md)
            state = read_json(Path(docs_path)/"state.json")
            if not "API" in state["completed_states"]:
                state["completed_states"].append("API")
                state["current_state"] = "init-project"
                write_json(Path(docs_path)/"state.json", state)
            print("[green]api.md file created successfully.[/green]")
            return True
        else:
            return False
    
    # initialize the project
    
    # create project skeleton
    
    # code
    
    # test
    
    # deploy