# 🎨 Fractal: AI-Powered Paint Defect Detection & Analysis System

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Status](https://img.shields.io/badge/status-active-brightgreen.svg)]()

> An intelligent multi-layered system for real-time paint defect detection, root cause analysis, and automated corrective actions in industrial painting processes.

## 🚀 Overview

Fractal is a comprehensive AI-powered solution designed for industrial paint quality control. The system combines computer vision, machine learning, and process automation to detect paint defects, analyze their root causes, and automatically implement corrective actions.

### 🎯 Key Features

- **🔍 Real-time Defect Detection** - Identifies various paint defects (orange peel, fisheye, overspray, etc.)
- **🧠 Intelligent Root Cause Analysis** - Uses historical data and environmental conditions
- **⚡ Automated Actions** - Adjusts spray parameters and triggers maintenance workflows
- **📊 Continuous Learning** - Improves accuracy through feedback loops
- **🔧 PLC Integration** - Direct integration with industrial control systems
- **📈 Data Analytics** - Comprehensive logging and analysis capabilities

---

## 🏗️ System Architecture

The system is built on a **4-layer architecture** that processes defects through multiple stages:

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│  Perception     │───▶│   Reasoning     │───▶│     Action      │───▶│    Learning     │
│     Layer       │    │     Layer       │    │     Layer       │    │     Layer       │
└─────────────────┘    └─────────────────┘    └─────────────────┘    └─────────────────┘
```

### Layer Details

| Layer | Purpose | Technology |
|-------|---------|------------|
| **🔍 Perception Layer** | Classifies defect types from images | CNN, Computer Vision, Deep Learning |
| **🧠 Reasoning Layer** | Determines root causes using historical data | LLM, Statistical Analysis, Rule-based Systems |
| **⚡ Action Layer** | Executes corrective actions via PLC integration | Process Control, Automation APIs |
| **📊 Learning Layer** | Collects feedback and improves system accuracy | Feedback Loops, Data Analytics |

---

## 📋 Prerequisites

- **Python 3.8+**
- **pip** (Python package manager)
- **OpenAI API Key** (for LLM-based reasoning)
- **Industrial PLC connection** (for action layer - optional for testing)

---

## 🛠️ Installation

### 1. Clone the Repository
```bash
git clone https://github.com/your-username/fractal.git
cd fractal
```

### 2. Create Virtual Environment

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

### 3. Install Dependencies
```bash
pip install -e .
```

### 4. Configure Environment

update the API key in `configs/config.yaml`:
```yaml
llm:
  provider:
    openai:
      api_key: "your_api_key_here"
```

---

## 🚀 Quick Start

### Basic Usage

```bash
python main.py
```

The system will process the sample input defined in `main.py` and output the analysis results.

### Sample Input Format

```json
{
    "schema_version": "1.0",
    "message_id": "uuid",
    "trace_id": "uuid",
    "created_at": "timestamp",
    "panel_id": "string",
    "defect_type": "string",
    "issue_critical": "bool",
    "work_order": { 
        "order_id": "string", 
        "vin": "string (optional)"
        },
    "source": {
        "edge_id": "string", 
        "camera_id": "string", 
        "model_version": "string"
    },
    "environment": {
        "temperature_c": "number",
        "humidity_pct": "number",
        "spray_pressure_bar": "number (optional)",
        "other_sensors": { "type": "object" }
    },
    "image":{ 
        "image_id": "uuid", 
        "uri": "string (s3/orb://) or base64 (only for sync)", "camera_pose": "object (extrinsics)", 
        "timestamp": "timestamp" },
    ,
    "processing_latency_ms": "number",
    "reasoning_layer_messages": [],
        "reasoning_layer_output": "",
        "action_layer_messages": [],
        "action_layer_output": ""
}
```

---

## 📁 Project Structure

```
fractal/
├── 📁 core/                    # Core system components
│   ├── agentic_system.py      # Main system orchestrator
│   ├── components.py          # Layer implementations
│   ├── pydentic_models.py     # Data models and schemas
│   ├── tools.py              # Analysis tools and functions
│   └── dummy.py              # Mock implementations for testing
├── 📁 configs/               # Configuration files
│   └── config.yaml           # System configuration
├── 📁 utils/                 # Utility modules
│   ├── config_utils.py       # Configuration management
│   ├── llm.py               # LLM integration utilities
│   └── logger.py            # Logging utilities
├── 📁 data/                  # Data storage
│   └── upload_data.json      # Training/feedback data
├── 📁 temp/                  # Development notebooks
├── main.py                   # Main application entry point
├── setup.py                  # Package setup
├── requirements.txt          # Python dependencies
├── Perception_Layer.md       # Detailed perception layer docs
└── readme.md                 # This file
```

---

## 🔧 Configuration

### System Configuration (`configs/config.yaml`)

```yaml
agent:
  reasoning_layer:
    llm:
      provider: "openai"
      model: "gpt-4o-mini"
      inference_params:
        temperature: 0.0
        max_tokens: 2048
        timeout: 30

  action_layer:
    llm:
      provider: "openai" 
      model: "gpt-4o-mini"
```

### Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `OPENAI_API_KEY` | OpenAI API key for LLM services | Yes |
| `DATA_PATH` | Path to data storage directory | Yes |

---

## 💡 Usage Examples

### 1. Basic Defect Analysis

```python
from core.agentic_system import app

# Define your input data
input_data = {
    "defect_type": "orange_peel",
    "environment": {
        "temperature_c": 22.5,
        "humidity_pct": 65.0,
        "spray_pressure_bar": 2.1
    },
    # ... other required fields
}

# Process the defect
result = app.invoke(input_data)
print(f"Root Cause: {result['reasoning_layer_output']}")
print(f"Recommended Action: {result['action_layer_output']}")
```

### 2. Batch Processing

```python
import json
from core.agentic_system import app

# Load multiple defect cases
with open('defect_cases.json', 'r') as f:
    cases = json.load(f)

results = []
for case in cases:
    result = app.invoke(case)
    results.append(result)

# Analyze results
for i, result in enumerate(results):
    print(f"Case {i+1}: {result['reasoning_layer_output']}")
```



---

## 📊 Data Management

### Feedback Data Storage

The system automatically stores analysis results and feedback in:
- **JSON Format**: `data/upload_data.json` - Structured data for ML training

### Data Schema

```json
{
    "timestamp": "ISO 8601 timestamp",
    "defect_analysis": {
        "detected_type": "string",
        "confidence": "float",
        "root_cause": "string"
    },
    "feedback": {
        "correct_type": "string", 
        "correct_cause": "string",
        "issue_resolved": "boolean"
    },
    "environment": {
        "temperature_c": "float",
        "humidity_pct": "float",
        "spray_pressure_bar": "float"
    }
}
```

---

## 👥 Author

- **Your Name** - *Vatsal*

