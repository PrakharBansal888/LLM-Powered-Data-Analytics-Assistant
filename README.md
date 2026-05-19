# LLM-Powered Data Analytics Assistant

## Overview
An intelligent data analytics assistant powered by LLMs (via OpenRouter). Upload any CSV file and ask questions about your data in plain English. The assistant generates Python code to analyze and visualize your data.

## Features
- 📊 Upload CSV files and get instant insights
- 🤖 Free LLM models (NVIDIA Nemotron, OpenAI, DeepSeek, MiniMax)
- 🔄 Natural language queries about your data
- 📈 Automatic chart generation with Plotly
- 🛡️ Secure code execution sandbox
- 💬 Multi-turn conversation support

## Project Structure
```
LLM-Powered Data Analytics Assistant/
├── app.py                  # Main Streamlit application
├── config/                 # Configuration module
│   ├── __init__.py
│   └── settings.py         # Global settings, prompts, API config
├── src/                    # Source code modules
│   ├── __init__.py
│   ├── agent.py           # LLM API integration
│   ├── executor.py        # Safe code execution sandbox
│   └── utils.py           # Utility functions (schema, CSV loading)
├── .env                    # API keys (DO NOT commit)
├── .gitignore              # Git ignore rules
├── requirements.txt        # Python dependencies
└── README.md              # This file
```

## Setup

### 1. Get OpenRouter API Key
- Visit [openrouter.ai](https://openrouter.ai)
- Sign up and get your free API key
- The key enables access to free LLM models

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Configure API Key
Edit `.env` file:
```
OPENROUTER_API_KEY=your-key-here
```

### 4. Run the App
```bash
streamlit run app.py
```

The app will open at `http://localhost:8501`

## Usage

1. **Upload Data**: Click "Upload Data" in the sidebar and select your CSV file
2. **Select Model**: Choose your preferred LLM model
3. **Ask Questions**: Type your question in the chat box
4. **View Results**: See generated charts, tables, and insights

### Example Queries
- "Show me the top 5 items by rating"
- "Create a pie chart of categories"
- "What's the average price by region?"
- "Show me the distribution of reviews"

## Available Models
- NVIDIA Nemotron 3 Nano 30B
- OpenAI GPT-OSS 120B
- DeepSeek V4 Flash
- MiniMax M2.5

All models are completely free via OpenRouter!

## How It Works

1. **Schema Extraction**: Analyzes your CSV structure (columns, types, samples)
2. **LLM Generation**: Sends schema + question to OpenRouter LLM
3. **Code Extraction**: Parses generated Python code from LLM response
4. **Safe Execution**: Runs code in restricted sandbox with:
   - Only pandas, plotly, numpy available
   - No file I/O or external imports
   - Proper error handling and reporting
5. **Results Display**: Shows charts, tables, and insights

## Data Type Handling

The LLM is instructed to properly handle:
- Mixed content strings (e.g., "2509 reviews")
- Missing values (NaN)
- Type conversions with error handling
- Safe numeric extraction using regex

## Safety

- Code runs in an isolated sandbox
- Only approved libraries available (pandas, plotly, numpy)
- No access to file system or external imports
- Automatic error handling with user-friendly messages
- Input validation before execution

## Troubleshooting

### API Key Error
```
ValueError: OPENROUTER_API_KEY not found in .env file
```
Solution: Ensure `.env` file exists and contains your API key

### Module Import Error
```
ImportError: No module named 'streamlit'
```
Solution: Run `pip install -r requirements.txt`

### Execution Errors
If code fails to execute:
1. Check the error message in the UI
2. Try simplifying your question
3. Different models may handle complex queries differently

## Dependencies
- **streamlit**: Web app framework
- **pandas**: Data manipulation
- **plotly**: Interactive charts
- **requests**: API calls
- **python-dotenv**: Environment variables

## License
MIT

## Author
Created as an LLM-powered data analytics assistant
