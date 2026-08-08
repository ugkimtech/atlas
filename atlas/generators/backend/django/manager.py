from rich import print
from pathlib import Path
import os
import sys
from pathlib import Path
import subprocess
from ....core.pipeline import Pipeline
from ....workspace.files import read_json, read_file, write_file, write_json
from ....shell.system import PackageManager
from ....shell.commands import execute, run_server
from ....generators.blueprint_manager import BluePrint


class DjangoManager:
    
    def __init__(self, specs, reqs, arch, erd, api, blueprint):
        self.current_dir = Path(".")
        self.docs_path = Pipeline().docs_path()
        self.specs = specs
        self.reqs =  reqs
        self.arch =  arch
        self.erd =  erd
        self.api =  api
        self.blueprint_json = blueprint
        self.django_files = ['asgi.py', 'wsgi.py', 'manage.py', '__init__.py']
        self.blueprint = BluePrint(self.blueprint_json, self.django_files)
        
        
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
            if not "init-project" in state["completed_states"]:
                state["completed_states"].append("init-project")
                state["current_state"] = "project-skeleton"
                write_json(Path(self.docs_path)/"state.json", state)
        else:
            execute(f"rm -rf {backend_dir}")
            print("Retrying...")
            self.start_django()
        return True