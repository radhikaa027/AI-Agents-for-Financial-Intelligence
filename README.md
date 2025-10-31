# Agentic Finance Framework

A sophisticated multi-agent system that automates comprehensive investment analysis reports for publicly traded companies. This project demonstrates advanced AI orchestration through two distinct implementations, simulating a professional financial analyst team where each agent specializes in a specific domain.

## 🎯 Project Overview

This system leverages generative AI to create detailed investment reports by coordinating multiple specialized agents that work together to research, analyze, and synthesize financial data. The project showcases two different approaches to multi-agent systems, highlighting the evolution from high-level frameworks to custom implementations.

## 🚀 Key Features

### 🧩 Multi-Agent Architecture
- **6 Specialized AI Agents**: Portfolio Manager, Quantitative Analyst, Market Researcher, Risk Analyst, Investment Report Writer and Compliance Validator
- **Role-Based Expertise**: Each agent brings domain-specific knowledge and analytical perspectives
- **Collaborative Workflow**: Agents share insights and build upon each other's findings

### Dual Implementation Strategy
- **Phase 1 — CrewAI Workflow:**: Built with the CrewAI orchestration framework for rapid development and modular design.
- **Phase 2 — ADK Workflow:**: Re-engineered using Google’s Agent Development Kit (ADK) and Gemini API for explicit memory management, custom tools, and detailed logging.

### Advanced Capabilities
- **Parallel Processing**: Concurrent execution of data gathering tasks for optimal performance
- **Real-time Data Integration**: Live financial data via `yfinance` and current market news through NewsAPI
- **Custom Analytics**: Proprietary investment scoring algorithm (ADK implementation)
- **State Management**: Centralized memory system for agent coordination (ADK implementation)
- **Quality Assurance**: Built-in hallucination detection and fact-checking mechanisms
- **Comprehensive Logging**: Full workflow transparency and debugging capabilities

## 📁 Project Structure

```
finance-agents-project/
│
├── 📄 README.md
├── 📄 requirements_crewai.txt
├── 📄 requirements_adk.txt
│
├── 📁 crewai_workflow/
│   ├── 📄 main.py
│   ├── 📁 agents/
│   │   └── financial_agents.py
│   ├── 📁 tools/
│   │   └── (market_data_tools.py, etc.)
│   └── 📁 workflows/
│       └── (investment_crew.py, etc.)
│
└── 📁 adk_extension/
    ├── 📄 main.py
    ├── 📄 config.py
    ├── 📁 agents/
    │   └── financial_agent_functions.py
    ├── 📁 tools/
    │   └── (market_data_tools.py, etc.)
    └── 📁 utils/
        └── logging_setup.py
```

## 🛠 Technology Stack

| Component | Assignment 1 (CrewAI) | Assignment 2 (ADK) |
|-----------|------------------------|---------------------|
| **Framework** | CrewAI | Google Agent Development Kit |
| **LLM** | Google Gemini 2.5 Flash | Google Gemini 2.5 Flash |
| **Financial Data** | Yahoo Finance API | Yahoo Finance API |
| **Market News** | NewsAPI | NewsAPI |
| **Processing** | Built-in orchestration | Custom parallel execution |
| **State Management** | Framework-managed | Custom implementation |

## 🔧 Setup & Installation

### Prerequisites
- Python 3.10 or higher
- Google API Key (for Gemini)
- NewsAPI Key (for market news)

### 1. Environment Setup

```bash
# Clone the repository
git clone <your-repo-url>
cd finance-agents-project

# Create environment file
echo "GOOGLE_API_KEY=your_google_api_key_here" > .env
echo "NEWS_API_KEY=your_news_api_key_here" >> .env
```

### 2. Setup for CrewAI (Phase 1)

```bash
# Create virtual environment
python -m venv crewai_env

# Activate environment
# Windows:
.\crewai_env\Scripts\activate
# macOS/Linux:
source crewai_env/bin/activate

# Install dependencies
pip install -r requirements_crewai.txt
```

### 3. Setup for ADK (Phase 2)

```bash
# Create virtual environment
python -m venv adk_env

# Activate environment
# Windows:
.\adk_env\Scripts\activate
# macOS/Linux:
source adk_env/bin/activate

# Install dependencies
pip install -r requirements_adk.txt
```

## 🚀 Usage

### Running CrewAI (Phase 1)

```bash
# Ensure crewai_env is activated
cd crewai_workflow
python main.py

# Follow prompts to enter stock ticker (e.g., AAPL, TSLA, GOOGL)
# Reports will be generated in outputs/ folder
```

### Running ADK (Phase 2)

```bash
# Ensure adk_env is activated
cd adk_extension
python main.py

# Follow prompts to enter stock ticker
# Reports and workflow logs will be generated in outputs/ folder
```

## 📊 Output Examples

Both implementations generate comprehensive investment reports including:

- **Executive Summary**: High-level investment recommendation
- **Financial Analysis**: Key metrics, ratios, and performance indicators
- **Market Context**: Industry trends and competitive positioning
- **Risk Assessment**: Potential risks and mitigation strategies
- **Technical Analysis**: Chart patterns and technical indicators
- **Investment Score**: Quantitative recommendation (ADK implementation)

## 🔍 Key Differences Between Implementations

| Feature | CrewAI | ADK |
|---------|--------|-----|
| **Development Speed** | ✅ Rapid prototyping | ⚡ More development time |
| **Customization** | 🔧 Framework constraints | 🎯 Complete control |
| **Debugging** | 📝 Limited visibility | 🔍 Full transparency |
| **State Management** | 🏢 Framework-handled | 🧠 Custom memory system |
| **Error Handling** | ⚠️ Basic | 🛡️ Advanced validation |
| **Performance** | 🚀 Good | 🚀 Optimized |

## 🧪 Testing

The project includes built-in validation mechanisms:
- **Integration of multiple data sources** : financial metrics from yfinance and market news from NewsAPI.
- **Fact Checking**: Compliance validator agent verifies report accuracy
- **Error Logging**: Comprehensive error tracking and reporting

