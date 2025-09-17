

from utils.parser import get_event_parser
from utils.prompt_utils import get_event_prompt_template
from utils.logger import get_logger
from utils.config_utils import load_config
from utils.llm_handler import get_llm
from core.tools import get_add_event_to_calendar_tool, add_event_to_calendar_wrapper

from langchain.agents import initialize_agent, AgentType





logger = get_logger("Event Extractor")
config = load_config()




def extract_event_info_with_agent(event_info: str) -> dict:
    """
    extract event info with agent
    Args:
        event_info (str): event info
    Returns:
        dict: event info
    """
    logger.info("Extracting event info with agent...")
    llm = get_llm()
    add_event_tool = get_add_event_to_calendar_tool()
    agent = initialize_agent(
                tools = [add_event_tool],
                llm = llm,
                agent = AgentType.ZERO_SHOT_REACT_DESCRIPTION,
                verbose = True
            )
    return agent.invoke({"input": event_info})


def extract_event_info_with_chain_mode(event_info: str) -> dict:
    """
    extract event info with chain mode
    Args:
        event_info (str): event info
    Returns:
        dict: event info
    """
    logger.info("Extracting event info with chain mode...")
    llm = get_llm()
    event_parser, event_parser_format_instructions = get_event_parser()
    prompt = get_event_prompt_template()
    extraction_chain = prompt | llm | event_parser
    extracted_event = extraction_chain.invoke({"event_descriptions": event_info, 
                                "format_instructions":event_parser_format_instructions,
                                })    
    logger.info(f"Extracted event: {extracted_event}")
    tool_input = {
        "title": extracted_event.title,
        "date": extracted_event.date,
        "time": extracted_event.time,
        "location": extracted_event.location,
        "attendees": extracted_event.attendees
    }
    

    calendar_result = add_event_to_calendar_wrapper(tool_input)

    return {
        "input": event_info,
        "output": calendar_result
    }

