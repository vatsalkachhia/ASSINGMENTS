from utils.parser import fix_parser
from utils.llm_handler import LLM, get_response
from utils.config_utils import load_config
from utils.prompt_utils import get_prompt
from utils.file_handler import load_reports, load_input_prompts, save_improved_prompts
from utils.logger import get_logger

config = load_config()
logger = get_logger("Updater")

def fix_issues(report_json, original_prompt):
    prompt = get_prompt("fix_prompt")
    prompt = prompt.format(report_json =report_json, prompt = original_prompt)
    llm = LLM
    resp = get_response(llm = llm, 
                            prompt = prompt, 
                            params = config["llm"]["inference_params"], 
                            parser = fix_parser)

    return resp

def fix_issues_all(save_output: bool = False) -> dict[str, dict]:
    logger.info(f"Fixing issues for all prompts...")
    file_and_input_prompts: dict[str, str] = load_input_prompts()
    issues_for_each_file: dict[str, dict] = load_reports()
    improved_prompts_for_each_file: dict[str, str] = {}
    for file_name in issues_for_each_file:
        logger.debug(f"Fixing issues for {file_name}...")
        improved_prompts_for_each_file[file_name] = fix_issues(report_json = issues_for_each_file[file_name], 
                                                                original_prompt = file_and_input_prompts[file_name])
    if save_output:
        logger.debug(f"Saving improved prompts for all prompts...")
        save_improved_prompts(improved_prompts_for_each_file)
    return improved_prompts_for_each_file