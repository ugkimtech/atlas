import requests
import time
from rich import print

def post(url, headers={}, payload={}):
    delay = 1
    for retry in range(4):
        try:
            # Make the POST request
            print("[yellow]Sending request...[/yellow]")
            response = requests.post(url, json=payload, headers=headers)
            response.raise_for_status() 
            response_data = response.json()
            print("\n[green]✔ Request processed successfully.[/green]\n")
            return response_data
    
        except (KeyError, IndexError):
            print("[red]Unexpected response format.[/red]")
            return
        except Exception as e:
            if "429" in str(e) or "503" in str(e):
                time.sleep(delay)
                delay *= 2
                print("Retrying...")
            else:
                raise