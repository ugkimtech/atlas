from rich import print
import typer
import json
from ..generators.menu_list.menu import run_menu
from ..llm.manager import LLMManager


class Requirements:
    # gather project requirements
    def project_requirements(self):
        # Collect requirements
        print("\nLet Atlas understand your Project idea by answering a few questions below")
        
        specs = {}
        specs["project_name"] = self.project_name()
        specs["description"] = self.description()
        specs["project_type"] = self.project_type()
        if specs["project_type"] == "webapp":
            specs["frontend"] = self.frontend()
            specs["backend"] = self.backend()
            if specs["frontend"] != "reactjs":
                specs["api"] = self.api()
            specs["database"] = self.database()
            specs["authentication"] = self.authentication()
            specs["roles"] = self.roles()
            specs["entities"] = self.entities()
        return specs
        
    
    def project_name(self):
        project_name = typer.prompt("\nProject Name")
        return project_name
    
    
    def description(self):
        print("\nDescribe your project in full details")
        description = typer.prompt("\n==>")
        return description
        
    
    def project_type(self):
        title = "\nSelect project type."
        
        items = [
            {"item":"Website", "return":"website"}, {"item":"Web App","return":"webapp"}, {"item":"Mobil App", "return":"mobileapp"}
            ]
        return run_menu(title, items)
    
    
    def frontend(self):
        title = "\nSelect frontend technology"
        items = [
            {"item":"React js", "return":"reactjs"}, {"item":"Flutter", "return":"flutter"}, {"item":"HTML, CSS & JavaScript", "return":"vanilla"}
            ]
        
        return run_menu(title, items)
    
    
    def backend(self):
        title = "\nSelect backend technology"
        items = [
            {"item":"Django", "return":"django"}, {"item":"ASP.NET Core", "return":"asp.net"}, {"item":"Flask", "return":"flask"}, {"item":"No Framework", "return":"vanilla"},
            ]
        
        return run_menu(title, items)
    
        
    def api(self):
        title = "\nAre APIs included?"
        items = [
            {"item":"Yes", "return":"yes"},{"item":"No", "return":"no"},  
            ]
        return run_menu(title, items)
    
    
    def database(self):
        title = "\nSelect database engine."
        items = [
            {"item":"SQLite", "return":"sqli"}, {"item":"PostgreSQL", "return":"postgresql"}, {"item":"MySQL", "return":"mysql"}
            ]
        return run_menu(title, items)
        
    
    def authentication(self):
        print("\n[pink]>>>[/pink] JWT Authentication will be used")
        return "jwt"
        
        
    def roles(self):
        print("\nEnter your user required roles (separated by comma ',')\nExample: Admin, Teller, Borrower")
        inputs = input("Roles: ")
        roles = list(item.strip() for item in inputs.split(','))
        return roles
        
        
    def entities(self):
        print("\nEnter your system required entities (separated by comma ',')\nExample: Loan, Lender, Repayments")
        inputs = input("Entities: ")
        entities = list(item.strip() for item in inputs.split(','))
        return entities


class StructureRequirements:
    def __init__(self):
        self.llm = LLMManager()
        self.req_obj = Requirements()
        
        
    def analyze_requirements(self, raw_req):
        prompt_var = {
            "raw_specs":raw_req
        }
        polished_req = self.llm.generate("analyze_requirements", prompt_var)
        # decode into standard python dictionary
        try:
            project_specs = json.loads(polished_req)
            print("\n[green]✔ Requirements analyzed successfully.[/green]\n")
            return project_specs
            
        except json.JSONDecodeError:
            print("[red]Could not parse string output into JSON.[/red]")
            return
        except TypeError:
            print("[red]Server returned unsupported response format[/red]")
            return
        
    
    
    def structure(self, polished_reqs):
        prompt_var = {
            "raw_specs":json.dumps(polished_reqs, indent=2)
        }
        print("[yellow]Structuring requirements...")
        structured_reqs = self.llm.generate("structure_req", prompt_var)
        try:
            project_specs = json.loads(structured_reqs)
            print("\n[green]✔ Requirements structured successfully.[/green]\n")
            return project_specs
            
        except json.JSONDecodeError:
            print("[red]Could not parse string output into JSON.[/red]")
            return
        except TypeError:
            print("[red]Atlas received unsupported response type!![/red]")
    
    def validate():
        # will ask user to validate project spec json
        pass