"""
Pytest configuration and fixtures.
"""

import pytest
import sys
from pathlib import Path

# Add the parent directory to sys.path to import modules
sys.path.insert(0, str(Path(__file__).parent.parent))

@pytest.fixture
def sample_prompt():
    """Sample prompt for testing."""
    return "This is a sample prompt for testing purposes."

@pytest.fixture
def mock_config():
    """Mock configuration for testing."""
    return {
        "llm": {
            "provider": "openai",
            "model": "gpt-3.5-turbo",
            "inference_params": {
                "temperature": 0.7,
                "max_tokens": 1000
            }
        },
        "paths": {
            "inputs": "inputs/",
            "outputs": "inference/outputs/",
            "reports": "inference/reports/"
        }
    }

@pytest.fixture
def sample_issues():
    """Sample issues for testing."""
    return [
        {
            "type": "clarity",
            "severity": "medium",
            "description": "Prompt lacks specific instructions",
            "suggestion": "Add more detailed instructions"
        },
        {
            "type": "structure",
            "severity": "low",
            "description": "Missing examples",
            "suggestion": "Include relevant examples"
        }
    ]