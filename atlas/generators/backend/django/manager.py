from rich import print
from pathlib import Path
import os
import sys
import subprocess
from ...services import docs_path
from ....workspace.files import read_json, read_file, write_file, write_json
from ....shell.system import PackageManager
from ....shell.commands import execute, run_server
from ....generators.blueprint_manager import BluePrint


class DjangoManager:
    
    def __init__(self, specs, reqs, arch, erd, api, blueprint):
        self.current_dir = Path(".")
        self.docs_path = docs_path()
        self.specs = specs
        self.reqs =  reqs
        self.arch =  arch
        self.erd =  erd
        self.api =  api
        self.blueprint_json = blueprint
        self.django_files = ['asgi.py', 'wsgi.py', 'manage.py', '__init__.py']
        self.blueprint = BluePrint(self.blueprint_json, self.django_files)
        
        
    def dj_pipeline(self):
        while True:
            state = read_json(Path(self.docs_path)/"django_state.json")
            print(f"Current django state is {state["current_state"]}.")
            
            match(state["current_state"]):
                case "init":
                    if self.start_django():
                        if "init" not in state["completed_states"]:
                            state["completed_states"].append("init")
                            state["current_state"] = "skeleton"
                            write_json(Path(self.docs_path)/"django_state.json", state)
                        
                case "skeleton":
                    if self.dj_skeleton():
                        if "skeleton" not in state["completed_states"]:
                            state["completed_states"].append("skeleton")
                            state["current_state"] = "code"
                            write_json(Path(self.docs_path)/"django_state.json", state)
                        
                case _:
                    break
        
    
    def init_dj_state(self):
        state = {
            "current_state":"init",
            "completed_states":[],
            "states":[
                "init","skeleton","code","test"
                ]
        }
        write_json(Path(self.docs_path)/"django_state.json", state)
        return True
        
        
    def start_django(self):
        pkg = PackageManager()
        #check Django installation
        if not pkg.check_package("django-admin"):
            return None
        # init project
        print("initializing django project...")
        tree = self.blueprint.project_tree()
        dirs = []
        for element in tree:
            if 'backend' in element and element.endswith('/'):
                # removing trailing /
                el_list = element.split('/')
                el_list.pop()
                if len(el_list) <= 2:
                    dirs.append('/'.join(el_list))
                
        dirs = dirs[::-1]
        backend_dir = dirs.pop().strip()
        Path(backend_dir).mkdir(exist_ok=True, parents=True)
        project_name = dirs.pop()
        
        command = f"django-admin startproject {project_name.split('/')[1]} {backend_dir}"
        if execute(command):
            print(f"[green]Django project initialized successfully inside {backend_dir} folder.")
            state = read_json(Path(self.docs_path)/"state.json")
            dj_state = read_json(Path(self.docs_path)/"django_state.json")
            if not "init-project" in state["completed_states"]:
                state["completed_states"].append("init-project")
                state["current_state"] = "project-skeleton"
                write_json(Path(self.docs_path)/"state.json", state)
        else:
            execute(f"rm -rf {backend_dir}")
            print("Retrying...")
            self.start_django()
        return True
        
        
    def dj_skeleton(self):
        tree = self.blueprint.project_tree()
        apps = []
        backend_dir = None
        for element in tree:
            if 'backend' in element and element.endswith('/'):
                element = element.split('/')
                element.pop()
                if len(element) == 2:
                    apps.append('/'.join(element))
        # removing project core
        apps = apps[::-1]
        apps.pop()
        # start apps
        backend_dir = apps[0].split('/')[0]
        os.chdir(backend_dir)
        
        for app in apps:
            app = app.split('/')
            print(f"Creating {app[1]} app...\n")
            command = f"python manage.py startapp {app[1]}"
            if execute(command):
                write_file(Path(app[1])/"urls.py", f"# {Path('/'.join(app))}/urls.py")
                print(f"[green]{app[1]} app & {app[1]}/urls.py created successfully.")
        os.chdir('..')
        
        gen_files = [
            "settings.py", "apps.py", 
            "urls.py", "views.py", 
            "models.py", "admin.py"]
        files = []
        for element in tree:
            if 'backend' in element and not element.endswith('/'):
                element = element.split('/')
                if not element[len(element)-1] in gen_files:
                    write_file(Path('/'.join(element)), f"# {'/'.join(element)}")
                    print(f"[green]File {'/'.join(element)} created successfully")
        return True