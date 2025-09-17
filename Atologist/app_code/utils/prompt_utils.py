from utils.config_utils import load_config

from langchain.prompts import ChatPromptTemplate

import os 

config = load_config()

def get_prompt(prompt_name) -> str:
    """
    load the prompt from the prompt directory and return it as a string
    Args:
        prompt_name (str): name of the prompt to load
    returns: 
        str: prompt
    """
    prompt_dir = config["app"]["prompt_dir"]
    prompt_path = os.path.join(prompt_dir, prompt_name + ".txt")
    with open(prompt_path, "r") as f:
        prompt = f.read()
    return prompt

def get_event_prompt_template() -> ChatPromptTemplate:
    """
    load the event prompt and return it as a ChatPromptTemplate
    Args:
     None
    returns: 
        ChatPromptTemplate: prompt template
    """
    prompt = get_prompt("data_extract_prompt")
    prompt_template = ChatPromptTemplate.from_template(template=prompt)
    return prompt_template
    
