from langchain_openai import ChatOpenAI
from utils.config_utils import load_config
from utils.logger import get_logger


import os

logger = get_logger("LLMHandler")

config = load_config()



def get_llm(model):
    logger.info("Getting LLM...")
    llm = ChatOpenAI(model=model, openai_api_key=config["llm"]["provider"]["openai"].get("api_key"))
    return llm
