import os
import json
from rich import print


def create_folder(path):
    try:
        os.makedirs(path, exist_ok=True)
        return True
    except Exception:
        return None


def write_file(filepath, contents):
    try:
        with open(filepath, "w") as f:
            f.write(contents)
        return True
    except Exception as e:
        print(f"[red]File write Error: {e}")
        return None


def read_file(filepath):
    try:
        with open(filepath, "r") as f:
            data = f.read()
        return data
    except Exception as e:
        print(f"[red]File read Error: {e}")
        return None


def write_json(filepath, contents):
    try:
        with open(filepath, "w") as f:
            json.dump(contents, f, indent=4)
        return True
    except Exception as e:
        print(f"[red]File write Error: {e}")
        return None


def read_json(filepath):
    try:
        with open(filepath, "r", encoding='utf-8') as f:
            data = json.load(f)
        return data
    except Exception as e:
        print(f"[red]File read error: {e}[/red]")
        return None