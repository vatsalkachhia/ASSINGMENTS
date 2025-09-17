from utils.logger import get_logger

import json
import sys

logger = get_logger("Parser")

def report_parser(text):
    if "---BEGIN JSON_OUTPUT---" in text:
        text = text.split("---BEGIN JSON_OUTPUT---")[1].split("---END JSON_OUTPUT---")[0]
        text = text.replace("```json", "").replace("```", "")
        json_output = json.loads(text)
    else:
        logger.error(f"No JSON output found in the response")
        sys.exit(1)
    return json_output


def fix_parser(text):
    json_output = None
    for jsn in text.split("--- BEGIN OUTPUT ---"):
        if not jsn.strip():
            continue
        jsn = jsn.split("--- END OUTPUT ---")[0]
        jsn = jsn.replace("```json", "").replace("```", "")
        jsn = json.loads(jsn)

        if jsn["is_fixed"] == True:
            json_output = jsn["fixed_prompt"]
            break
    return json_output


def eval_parser(resp):
    resp = resp.split("```json")[1].split("```")[0]
    resp = json.loads(resp)
    return resp