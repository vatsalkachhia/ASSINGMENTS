from utils.prompt_utils import get_prompt
from utils.llm_handler import LLM, get_response
from utils.config_utils import load_config
from utils.parser import report_parser
from utils.file_handler import load_input_prompts
from utils.logger import get_logger
from utils.file_handler import save_reports
from utils.report_generator import display_issues_table


config = load_config()
logger = get_logger("Detector")


def detect_issues(input_doc):
    prompt=get_prompt("report_prompt")
    prompt=prompt.format(input=input_doc)
    llm  =  LLM
    logger.info(f"getting response from llm..") #temp
    resp = get_response(llm = llm, prompt = prompt, 
                            params = config["llm"]["inference_params"], 
                            parser = report_parser)
    logger.info(f"response from llm: {resp}") #temp
    return resp


def detect_issues_all(save_output: bool = False, display_table: bool = False) -> dict[str, dict]:
    logger.info(f"Detecting issues for all prompts...")
    file_and_input_prompts: dict[str, str] = load_input_prompts()
    issues_for_each_file: dict[str, dict] = {}
    for file_name in file_and_input_prompts:
        logger.debug(f"Detecting issues for {file_name}...")
        issues_for_each_file[file_name] = detect_issues(file_and_input_prompts[file_name])
        if display_table:
            display_issues_table(issues_for_each_file[file_name])
    if save_output:
        logger.debug(f"Saving issues for all prompts...")
        save_reports(issues_for_each_file)
    return issues_for_each_file