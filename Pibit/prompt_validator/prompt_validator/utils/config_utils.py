import os
from typing import Any, Dict, Optional
from .logger import get_logger

logger = get_logger("ConfigLoader")

def load_config(path: Optional[str] = None) -> Dict[str, Any]:
    package_dir = os.path.dirname(os.path.dirname(__file__))
    default_path = os.path.join(package_dir, "configs", "config.yaml")
    cfg_path = path or os.getenv("PROMPT_VALIDATOR_CONFIG", default_path)

    try:
        import yaml  # type: ignore
    except Exception:
        return {}

    if not os.path.isfile(cfg_path):
        return {}

    try:
        with open(cfg_path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f) or {}
        if isinstance(data, dict):
            return data 
        else: 
            logger.error(f"Config is not a dict: {data}")
            return  {}
        
    except Exception:
        logger.error(f"Error loading config from {cfg_path}")
        return {}


