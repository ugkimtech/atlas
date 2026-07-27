from ...core.orchestrator import Orchestrator

orch = Orchestrator()

def proceed_project():
    print("Let's proceed from exactly where we stoped😋😋")
    orch.existing_project()
    return