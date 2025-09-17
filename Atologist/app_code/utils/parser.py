from utils.logger import get_logger
from utils.models import Event

from langchain.output_parsers import PydanticOutputParser

import json
import sys

logger = get_logger("Parser")


def get_event_parser() -> tuple[PydanticOutputParser, str]:
    """
    get the event parser and format instructions
    Args:
     None
    returns: 
        tuple[PydanticOutputParser, str]: event parser and format instructions
    """
    pydantic_parser = PydanticOutputParser(pydantic_object=Event)
    format_instructions = pydantic_parser.get_format_instructions()
    return pydantic_parser, format_instructions



