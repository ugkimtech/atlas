from rich import print
from pathlib import Path
import os
from .services import docs_path
from ..workspace.files import read_json, read_file, write_file, write_json
from .blueprint_manager import BluePrint


class Code:
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
        
        
    def write_code(self):
        print(self.blueprint_json["build_stages"])