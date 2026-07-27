import typer
from rich import print


def run_menu(title, options=[]):
    print(f"\n{title}")
    while True:
        index = 0
        for option in options:
            index += 1
            print(f"\t{index}. {option['item']}")
            
        choice = typer.prompt("\nEnter Choice")
        
        try:
            choice = int(choice)
            if options[choice-1]:
                return options[choice-1]["return"]
        except IndexError:
            print(f"[red]Invalid option: [bold]{choice}[/bold][/red] Choose again.\n")
            
        except Exception:
            print(f"[red]Invalid option: [bold]{choice}[/bold][/red] Choose again.\n")


"""
NOTES

If menu return a function name string tobe executed, use hasattr(obj, fn_name), and getattr(obj, fn_name) Eg.
pipeline = Pipeline()
project = pipeline.load_project()
if hasattr(pipeline, project):
    getattr(pipeline, project)()
    
    
Sample options
[
    {
        "item":"menu item name",
        "return":"return value"
    },
]
"""