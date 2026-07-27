import requests
from rich import print

def post(url, headers={}, payload={}):
    try:
        # Make the POST request
        print("[yellow]Sending request...[/yellow]")
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status() 
        response_data = response.json()
        print("\n[green]✔ Request processed successfully.[/green]\n")
        return response_data

    except requests.exceptions.RequestException as e:
        print(f"[red]Network error![/red]")
        return
    except (KeyError, IndexError):
        print("[red]Unexpected response format.[/red]")
        return