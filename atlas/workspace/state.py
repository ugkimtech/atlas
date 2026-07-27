from pathlib import Path
import os
from rich import print
from .files import write_json

def init_state(state_path):
    state = {
        "current_state":"requirements",
        "completed_states":[],
        "states":[
                'requirements', 
                'architecture', 
                'ERD',
                'API'
                'init project', 
                'project skeleton', 
                'code',
            ]
    }
    print("[yellow]Finalizing initial stage...[/yellow]")
    # save file
    if write_json(state_path, state):
        return True
    return None