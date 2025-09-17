# Prompt Validator

A comprehensive tool for detecting, fixing, and evaluating issues in AI prompts. This tool helps ensure your prompts follow best practices by identifying redundancy, conflicts, and completeness gaps.

## Features

- **Issue Detection**: Automatically detect redundant instructions, conflicting requirements, and missing sections
- **Prompt Fixing**: Generate improved versions of your prompts based on detected issues
- **Evaluation**: Score and evaluate prompt quality against structured criteria
- **Coverage Reports**: Generate comprehensive analysis reports
- **CLI Interface**: Easy-to-use command-line interface for batch processing

## Quick Start

### Prerequisites

- Python 3.8 or higher
- pip package manager

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd prompt_validator
   ```

2. **Create and activate virtual environment**
   
   **Windows (Command Prompt):**
   ```bash
   python -m venv venv
   venv\Scripts\activate
   ```
   
   **Windows (PowerShell):**
   ```bash
   python -m venv venv
   venv\Scripts\Activate.ps1
   ```
   
   **Linux/macOS:**
   ```bash
   python -m venv venv
   source venv/bin/activate
   ```

3. **Install the package**
   ```bash
   pip install -e .
   ```

### Configuration

Before using the prompt validator, you need to configure your LLM provider and API keys.

#### 1. Configure API Keys

The tool supports multiple LLM providers. Choose one and configure it in `configs/config.yaml`:

##### Option A: OpenAI (Recommended)
```yaml
llm:
  provider: "openai"
  model: "gpt-4o-mini"  # or gpt-4, gpt-3.5-turbo, etc.
  api_key: "your-openai-api-key-here"  # or leave empty to use environment variable
  api_key_env: "OPENAI_API_KEY"
  inference_params:
    temperature: 0.0
    max_tokens: 2048
    timeout: 30
```

##### Option B: HuggingFace
```yaml
llm:
  provider: "huggingface"
  model: "provider/model" 
  api_key: "your-huggingface-api-token"
  unique_load_params:
    do_sample: false
    task: "text-generation"
    provider: "auto"
  inference_params:
    temperature: 0.0
    max_tokens: 2048
```


## Usage

### Input Setup

Place all your input prompt text files in the `inputs/` folder. The tool will process all `.txt` files in this directory.

### Command Line Interface

```bash
# Detect and report issues in all prompts
python -m prompt_validator.cli --report

# Fix issues in prompts based on generated reports
python -m prompt_validator.cli --fix

# Evaluate improved prompts (coming soon)
python -m prompt_validator.cli --evaluate

# Generate coverage reports (coming soon)
python -m prompt_validator.cli --cov
```

### Output Structure

```
inference/
├── report/          # Issue detection reports (JSON format)
├── fix/             # Fixed/improved prompts
├── evaluation/      # Evaluation scores and feedback
└── coverage/        # Coverage analysis reports
```

## Prompt Quality Criteria

The tool evaluates prompts against these criteria:

### ✅ Required Elements
- **Task**: Clear description of what to do
- **Success Criteria**: Measurable, verifiable completion conditions
- **Examples**: Including at least one edge case (no PII)
- **CoT/ToT Steps**: Chain of Thought guidance for complex reasoning

### ❌ Issues Detected
- **Redundant Instructions**: Repeated guidance that adds no value
- **Conflicting Instructions**: Contradictory requirements
- **Missing Sections**: Incomplete prompt structure
- **Prohibited Content**: PII, secrets, or confidential data

## Example Workflow

1. **Prepare your prompts**: Place `.txt` files in `inputs/`
2. **Run detection**: `python -m prompt_validator.cli --report`
3. **Review reports**: Check `inference/report/` for detailed analysis
4. **Fix issues**: `python -m prompt_validator.cli --fix`
5. **Get improved prompts**: Find results in `inference/fix/`

## Development

### Project Structure

```
prompt_validator/
├── cli.py              # Command-line interface
├── core/
│   ├── detector.py     # Issue detection logic
│   └── updater.py      # Prompt fixing logic
├── utils/              # Utility functions
├── configs/            # Configuration files
├── prompts/            # System prompts
└── tests/              # Test suite
```
