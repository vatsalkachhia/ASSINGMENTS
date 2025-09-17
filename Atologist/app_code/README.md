# Event Extractor

Event Extractor is a tool designed to process natural language event descriptions and extract structured information. It then simulates adding these events into a calendar system.

The application supports **two execution modes**:

1. **Agent Mode** – Uses an agent-based approach to complete tasks. More robust with retries on failure, but slower.
2. **Chain Mode** – Executes faster but only attempts the task once.

Both modes perform the following:

* Extract structured event details from natural language descriptions
* Add the event into a simulated calendar system

---

## Features

* Two modes of execution: **Agent** and **Chain**
* Structured event information extraction
* Calendar system integration (simulation)
* Configurable LLM provider (OpenAI or HuggingFace)
* Easy setup with Python virtual environment

---

## Quick Start

### Prerequisites

* Python **3.8+**
* pip (Python package manager)

### Installation
1. **Create and activate a virtual environment**

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

2. **Install dependencies**

   ```bash
   pip install -e .
   ```

---

## Configuration

Before running the application, configure your preferred **LLM provider** and **API keys**.

### 1. Configure API Keys

Edit `configs/config.yaml` to specify your provider.

#### Option A: OpenAI (Recommended)

```yaml
llm:
  provider: "openai"
  model: "gpt-4o-mini"  # or gpt-4, gpt-3.5-turbo, etc.
  api_key: "your-openai-api-key-here"  # leave empty to use environment variable
  api_key_env: "OPENAI_API_KEY"
  inference_params:
    temperature: 0.0
    max_tokens: 2048
    timeout: 30
```

#### Option B: HuggingFace

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

---

## Running the Application

You can run the application interactively using the provided **Jupyter notebook**:

```bash
Run_app.ipynb
```

---

⚡ That’s it! You’re ready to start extracting events.

