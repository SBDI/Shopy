# shopy/utils.py
import json
import re
from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel


def clean_llm_output(data):
    cleaned_output = {}
    for key, value in data.items():
        if isinstance(value, str):
            cleaned_value = value.replace('\\\\n', '\\n')
            cleaned_value = cleaned_value.replace('\\\\', '')
            cleaned_value = re.sub(r'\\{\"plan\": \"|\"\\}$', '', cleaned_value)
            cleaned_output[key] = cleaned_value
        elif isinstance(value, dict):
            cleaned_output[key] = clean_llm_output(value)
        else:
            cleaned_output[key] = value
    return cleaned_output