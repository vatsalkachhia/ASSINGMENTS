from utils.prompt_utils import get_prompt
from utils.llm_handler import LLM, get_response
from utils.config_utils import load_config
from utils.parser import eval_parser
from utils.logger import get_logger

import numpy as np

config = load_config()
logger = get_logger("Test")

def evaluate_improved_prompt(prompt_to_evaluate):
    prompt = get_prompt("evaluation_prompt")
    prompt = prompt.format(prompt = prompt_to_evaluate)
    llm = LLM
    resp = get_response(llm = llm, 
                        prompt = prompt, 
                        params = config["llm"]["inference_params"], parser=eval_parser)
    return resp

def evaluate_improved_prompts(improved_prompts: dict[str, str]):
    scores_for_each_file: dict[str, float] = {}
    for file_name in improved_prompts:
        resp = evaluate_improved_prompt(improved_prompts[file_name])
        scores_for_each_file[file_name] = resp["score"]
        print(f"Evaluation for {file_name}: {resp}")

    average_score = np.mean(list(scores_for_each_file.values()))
    logger.info(f"Average score: {average_score}")
    return scores_for_each_file