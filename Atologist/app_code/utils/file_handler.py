from utils.config_utils import load_config
from utils.logger import get_logger

import os
import json

config = load_config()
logger = get_logger("FileHandler")

def filter_for_required_file_type(file_type: str, list_of_files: list[str]) -> list[str]:
    return [file for file in list_of_files if file.endswith(file_type)]
def remove_extension(file_name: str) -> str:
    return file_name.replace("." + file_name.split(".")[-1], "")

def load_input_text_files() -> dict[str, str]:
    input_dir = config["app"]["input_dir"]
    logger.info(f"Loading input prompts from {input_dir}...")
    input_files = os.listdir(input_dir)
    input_prompts = {}
    input_files = filter_for_required_file_type(".txt", input_files)
    input_files = [remove_extension(file) for file in input_files]
    logger.info(f"Found {len(input_files)} input prompts")
    logger.debug(f"Input files: {input_files}")
    for file in input_files:
        with open(os.path.join(input_dir, file + ".txt"), "r") as f:
            input_prompts[file] = f.read()
    logger.info(f"Input prompts loaded from {input_dir}")
    return input_prompts
