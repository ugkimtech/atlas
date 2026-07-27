import os
import sys
import platform
import subprocess
from rich import print


class PackageManager:
    
    def check_package(self, pkg):
        print(f"Checking if {pkg} is installed...")
        try:
            res = subprocess.run([pkg, '--version'], capture_output=True, check=True, text=True)
            print(res.stdout)
            print(f"{pkg} found successfully.")
            return True
        except subprocess.CalledProcessError as e:
            print(f"[red]Error {e.stderr}")
            return False
        except FileNotFoundError:
            print(f"[red]{pkg} not installed![/red]")
            return False# will be changed to call installer