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

def load_input_prompts() -> dict[str, str]:
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

def load_reports() -> dict[str, dict]:
    report_dir = config["app"]["report_dir"]
    logger.info(f"Loading reports from {report_dir}...")
    report_files = os.listdir(report_dir)
    reports = {}
    report_files = filter_for_required_file_type(".json", report_files)
    report_files = [remove_extension(file) for file in report_files]
    logger.info(f"Found {len(report_files)} reports")
    logger.debug(f"Report files: {report_files}")
    for file in report_files:
        logger.debug(f"Loading report {file}...")
        with open(os.path.join(report_dir, file + ".json"), "r") as f:
            reports[file] = json.load(f)
    logger.info(f"Reports loaded from {report_dir}")
    return reports

def save_reports(reports_json: dict[str, dict]) -> None:
    logger.info(f"Saving reports to {config['app']['report_dir']}...")
    report_dir = config["app"]["report_dir"]
    for file_name in reports_json:
        try:
            with open(os.path.join(report_dir, file_name + ".json"), "w") as f:
                json.dump(reports_json[file_name], f, indent=4)
        except Exception as e:
            logger.error(f"Error saving report {file_name}: {e}")
    logger.info(f"Reports saved to {report_dir}")

def save_improved_prompts(improved_prompts: dict[str, str]) -> None:
    logger.info(f"Saving improved prompts to {config['app']['output_dir']}...")
    output_dir = config["app"]["output_dir"]
    for file_name in improved_prompts:
        try:
            with open(os.path.join(output_dir, file_name + ".txt"), "w") as f:
                f.write(improved_prompts[file_name])
        except Exception as e:
            logger.error(f"Error saving improved prompt {file_name}: {e}")
    logger.info(f"Improved prompts saved to {output_dir}")