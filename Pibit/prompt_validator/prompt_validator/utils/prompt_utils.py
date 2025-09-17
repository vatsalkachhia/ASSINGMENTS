from utils.config_utils import load_config
import os 

config = load_config()

def get_prompt(prompt_name):
    prompt_dir = config["app"]["prompt_dir"]
    prompt_path = os.path.join(prompt_dir, prompt_name + ".txt")
    with open(prompt_path, "r") as f:
        prompt = f.read()
    return prompt