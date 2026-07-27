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


class DjangoManager:
    
    def __init__(self, specs, reqs, arch, erd, api):
        self.current_dir = Path(".")
        self.docs_path = Pipeline().docs_path()
        self.specs = specs
        self.reqs =  reqs
        self.arch =  arch
        self.erd =  erd
        self.api =  api
        
        
    def start_django(self):
        pkg = PackageManager()
        if not pkg.check_package("django-admin"):
            return None
        # init 
        project_name = self.specs['project_name'].replace(' ', '_').replace('-', '_').strip() + "_backend"
        command = f"django-admin startproject {project_name}"
        if execute(command):
            print("[green]Django project initialized successfully. lets test it now...")
            state = read_json(Path(self.docs_path)/"state.json")
            if not "init-project" in state["completed_states"]:
                state["completed_states"].append("init-project")
                state["current_state"] = "project-skeleton"
                write_json(Path(self.docs_path)/"state.json", state)
            os.chdir(project_name)
            # Use the current Python interpreter (works cleanly inside virtual environments)
            python_bin = sys.executable
            run_server(f"{python_bin} manage.py runserver")
        else:
            execute(f"rm -rf {project_name}")
            print("Retrying...")
            self.start_django()
        return True