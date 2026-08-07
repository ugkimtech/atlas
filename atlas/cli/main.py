import typer
from .commands.start import start_atlas
from .commands.docs import atlas_docs
from .commands.sync import sync_requirements, architecture_md
from .commands.proceed import proceed_project
from .commands.api import change_api


app = typer.Typer(help="SDLC Atlas that takes from step 0 to last phase of Software Development Life Cycle", no_args_is_help=True)
#app.add_typer(start_atlas, name="start")

@app.command()
def start():
    """
    Runs Atlas from phase 0 to last phase.
    """
    start_atlas()
    return


@app.command()
def sync():
    """
    Reflects changes made to project_spec.json to requirements.md
    """
    sync_requirements()
    return


@app.command()
def api():
    """
    Continues the project from its current stage to last Continue
    """
    change_api()
    return


@app.command()
def architecture():
    """
    Regenerates architecture.md file
    """
    architecture_md()

@app.command()
def proceed():
    """
    Continues the project from its current stage
    """
    proceed_project()
    return


@app.command()
def docs():
    """
    Atlas help and documentation
    """
    atlas_docs()
    return


def main():
    app()

if __name__ == "__main__":
    main()