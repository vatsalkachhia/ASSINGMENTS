from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from langchain_huggingface import HuggingFaceEndpoint, ChatHuggingFace
from utils.config_utils import load_config
from utils.logger import get_logger


import os


logger = get_logger("LLMHandler")

LLM = None
config = load_config()


def get_llm():
    if config["llm"].get("provider") == "openai":
        llm = ChatOpenAI(model=config["llm"].get("model"), openai_api_key=config["llm"].get("api_key"))
    # elif config["llm"].get("provider") == "anthropic":
        # llm = ChatAnthropic(model=config["llm"].get("model"), anthropic_api_key=config["llm"].get("api_key"))
    elif config["llm"].get("provider") == "huggingface":
        os.environ["HUGGINGFACEHUB_API_TOKEN"] = config["llm"].get("api_key")
        hf_ep = HuggingFaceEndpoint(repo_id=config["llm"].get("model"), **config["llm"].get("unique_load_params"))
        llm = ChatHuggingFace(llm=hf_ep)
    else:
        raise ValueError(f"Invalid provider: {config['llm']['provider']}")
    
    return llm


def load_llm():
    global LLM
    LLM = get_llm()

load_llm()


def get_response(llm, prompt, params, parser = None):
    response = llm.invoke(prompt, **params)
    if parser is not None:
        logger.info(f"parsing response..") #temp
        response = parser(response.content)
        logger.info(f"response after parsing: {response}") #temp
    else:
        response = response.content
    return response
