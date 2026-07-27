import os
from dotenv import load_dotenv
import json
from ...core.api_requests import post
from rich import print

load_dotenv()
class GeminiModel:
    def __init__(self):
        self.api_key = os.getenv("GEMINI_API_KEY")
        self.url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent"
        self.headers = {
            "Content-Type": "application/json",
            "x-goog-api-key": self.api_key
        }
        
        
    def generate(self, prompt):
        payload = {
            "contents": [
                {
                    "parts": [
                        {"text": prompt}
                    ]
                }
            ]
        }
        
        try:
            response = post(self.url, self.headers, payload)
            if response is None:
                print("[bold red]❌ Error[/bold red] The server returned an empty response (Service Unavailable).")
                return
                
            if "error" in response:
                print(f"[bold red]❌ API Error:[/bold red] {response.get('error', 'Unknown error structure')}")
                return
            # Safely extract text string from response structure
            gemini_text = response['candidates'][0]['content']['parts'][0]['text'].strip()
            # Strip code fences if the model included them anyway
            if gemini_text.startswith("```"):
                lines = gemini_text.splitlines()
                if lines[0].startswith("```"):
                    lines = lines[1:]
                if lines and lines[-1].startswith("```"):
                    lines = lines[:-1]
                gemini_text = "\n".join(lines).strip()
                return gemini_text
            return gemini_text
            
        except (KeyError, IndexError) as e:
            print(f"[bold red]❌ Structure Error:[/bold red] The API returned a response layout that couldn't be parsed.")
            print("[yellow]Raw API output payload response was:[/yellow]", response)
            return
            
        except Exception as e:
            print(f"[bold red]❌ Unexpected System Connection Error:[/bold red] {e}")
            return
