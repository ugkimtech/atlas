from .models.gemini import GeminiModel
from pathlib import Path
from rich import print


class LLMManager:
    def __init__(self):
        self.models = {
            "gemini" : GeminiModel,
        }
        # prompts files according to task
        self.tasks = {
            "analyze_requirements":"analyze_requirements.txt",
            "structure_req":"structure_requirements.txt",
            "requirements_md":"requirements_md.txt",
            "architecture":"architecture_md.txt",
            "blueprint":"blueprint.txt",
            "erd":"erd_md.txt",
            "api":"api_md.txt"
        }
        
        
    def _load_model(self):
        #print("Default model")
        #selection menu in future
        model_class = self.models["gemini"]
        return model_class()
        
    #load prompt template
    def _load_prompt_template(self, task):
        filename = self.tasks.get(task)
        if not filename:
            raise ValueError(f"Unkown task: {task}")
        path = Path(__file__).parent/"prompts"/filename
        try:
            template = path.read_text()
            return template
        except NotADirectoryError:
            print("[red]Prompt template load error![/red]")
        
    #render prompt
    def _render_prompt(self, task, variables):
        prompt = self._load_prompt_template(task)
        try:
            prompt = prompt.format(**variables)
            return prompt
        except AttributeError:
            print("[red]Load Prompt template returned no data!")
            return
        """except KeyError as e:
            print(f"[red]Atlas parsing error![/red] {e}")
            return"""
        
    #generate
    # The only called method outside
    def generate(self, task, variables):
        model = self._load_model()
        prompt = self._render_prompt(task, variables)
        return model.generate(prompt)