# shopy/utils.py
import re
from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel
import logging

def clean_llm_output(data, console=None):
    """Cleans the LLM output and prints it with Rich."""
    if console is None:
        console = Console()

    cleaned_output = {}
    for key, value in data.items():
        if isinstance(value, str):
            cleaned_value = value.replace('\\\\n', '\\n')
            cleaned_value = cleaned_value.replace('\\\\', '')
            cleaned_value = re.sub(r'\\{\"plan\": \"|\"\\}$', '', cleaned_value)
            cleaned_output[key] = cleaned_value
            # Use rich.print for styled output
            console.print(f"[bold]{key}:[/bold] {cleaned_value}")
        elif isinstance(value, dict):
            cleaned_output[key] = clean_llm_output(value, console)
        else:
            cleaned_output[key] = value
    return cleaned_output