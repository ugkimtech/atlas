from rich import print
import subprocess
import sys
import os

def execute(comm):
    command = comm.split(' ')
    print(f"Executing {comm} ...")
    try:
        res = subprocess.run(command, capture_output=True, check=True, text=True)
        print(res.stdout)
        print(f"{comm} executed successfully.")
        return True
    except subprocess.CalledProcessError as e:
        print(f"[red]Error {e.stderr}")
        return False
    except FileNotFoundError:
        print(f"[red]{comm} failed to execute![/red]")
        return False


def run_server(comm):
    """
    Executes  runserver interactively.
    Streams logs directly to the terminal and hands control to the user.
    """
    command = comm.split(' ')
    print(f"\nExecuting {comm} in interractive environment...")
    print("Press Ctrl+C in your terminal to stop the process.\n")

    try:
        subprocess.run(
            command,
            cwd=".",
            check=True
        )
    except KeyboardInterrupt:
        print("\n\n Running process stopped successfully.")
    except subprocess.CalledProcessError as e:
        print(f"[red]Process crashed! {e.returncode}[/red]")