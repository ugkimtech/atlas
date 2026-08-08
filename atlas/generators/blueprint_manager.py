from pathlib import Path
#import os
#import json
#from ..workspace.files import read_json


class BluePrint:
    def __init__(self, blueprint, no_edit_files=[]):
        self.blueprint = blueprint
        self.no_edit_files = no_edit_files
        
        
    def project_tree(self):
        tree = self.blueprint["project_tree"]
        files = []
        for file in tree:
            f = file["path"].lstrip().split('/')[::-1][0]
            if f not in self.no_edit_files:
                files.append(file["path"])
                #print(file["path"], '-->', file["type"])
        return files