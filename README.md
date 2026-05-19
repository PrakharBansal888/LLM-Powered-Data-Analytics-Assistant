# 📊 LLM-Powered Data Analytics Assistant

> Transform your CSV data into actionable insights using natural language queries powered by free LLMs.

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-Latest-red)](https://streamlit.io)
[![License](https://img.shields.io/badge/License-MIT-green)](LICENSE)

## ✨ Overview

**LLM-Powered Data Analytics Assistant** is an intelligent tool that enables non-technical users to analyze any CSV dataset using plain English questions. No coding required! Simply upload your data, ask a question, and the AI generates visualizations and insights automatically.

### 🎯 Key Highlights
- **Zero-Code Analytics**: Ask questions in English, get instant insights
- **100% Free**: Uses OpenRouter's free tier LLM models
- **Secure Execution**: Code runs in an isolated sandbox
- **Multiple Models**: NVIDIA Nemotron, OpenAI, DeepSeek, MiniMax - choose your favorite
- **Rich Visualizations**: Auto-generated charts with Plotly
- **Smart Data Handling**: Handles messy data gracefully (missing values, type conversions, etc.)

---

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- pip package manager
- Internet connection (for API calls)

### Installation (3 steps)

1. **Clone the repository**
   ```bash
   git clone https://github.com/PrakharBansal888/LLM-Powered-Data-Analytics-Assistant.git
   cd LLM-Powered-Data-Analytics-Assistant
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Get free API key** (30 seconds)
   - Visit [openrouter.ai](https://openrouter.ai)
   - Sign up (free)
   - Copy your API key
   - Create `.env` file in project root:
     ```
     OPENROUTER_API_KEY=your-key-here
     ```

4. **Run the app**
   ```bash
   streamlit run app.py
   ```
   App opens at `http://localhost:8501`

---

## 💡 Usage Examples

### 1. Hotel Reviews Analysis
```
Question: "Show me the top 5 hotels by average rating"
↓
AI generates code, executes, returns:
- Bar chart of top hotels
- Rating statistics
- Insight summary
```

### 2. Sales Data Insights
```
Question: "What's the average sales per region?"
↓
- Grouped data by region
- Mean calculation with error handling
- Summary statistics table
```

### 3. Distribution Analysis
```
Question: "Create a pie chart of categories"
↓
- Category distribution visualization
- Count of items per category
- Percentage breakdown
```

---

## 📁 Project Structure

```
LLM-Powered Data Analytics Assistant/
│
├── app.py                          # Main Streamlit UI
│
├── config/
│   ├── __init__.py
│   └── settings.py                 # Global config, prompts, API keys
│
├── src/
│   ├── __init__.py
│   ├── agent.py                    # LLM API integration (OpenRouter)
│   ├── executor.py                 # Secure code execution sandbox
│   └── utils.py                    # Data utilities (CSV, schema extraction)
│
├── .env                            # Your API key (local only, not in git)
├── .env.example                    # Template for setup
├── .gitignore                      # Git ignore rules
├── requirements.txt                # Python dependencies
└── README.md                       # This file
```

---

## 🔧 How It Works

### Architecture Flow

```
1. User Upload CSV
   ↓
2. Schema Extraction (columns, types, samples)
   ↓
3. Natural Language Question
   ↓
4. LLM API Call (OpenRouter)
   → "Generate Python code to answer this"
   ↓
5. Code Extraction & Parsing
   → Extract Python code block from response
   ↓
6. Secure Sandbox Execution
   → No imports allowed (modules pre-injected)
   → Only pandas, plotly, numpy available
   ↓
7. Results Rendering
   → Charts, tables, insights, error handling
```

### Data Processing Pipeline

| Step | What Happens | Security |
|------|--------------|----------|
| **Upload** | CSV loaded with pandas | File size validated |
| **Schema** | Columns, dtypes, samples extracted | No data modifications |
| **LLM** | OpenRouter API call | API key in .env only |
| **Code Gen** | LLM generates Python code | Validated before execution |
| **Execution** | Sandbox with restricted builtins | No file I/O, no imports |
| **Display** | Render results in Streamlit | User-friendly error messages |

---

## 🤖 Available LLM Models

All models are **completely free** via OpenRouter:

| Model | Creator | Tier | Speed |
|-------|---------|------|-------|
| NVIDIA Nemotron 3 Nano 30B | NVIDIA | Free | ⚡ Fast |
| OpenAI GPT-OSS 120B | OpenAI | Free | ⚡ Fast |
| DeepSeek V4 Flash | DeepSeek | Free | ⚡⚡ Very Fast |
| MiniMax M2.5 | MiniMax | Free | ⚡⚡ Very Fast |

**No credit card required. No rate limits. Truly free!**

---

## 📊 Features in Detail

### ✅ Smart Data Handling
- Automatically handles NaN/missing values
- Safely converts mixed-content strings (e.g., "2509 reviews" → 2509)
- Error handling with user-friendly messages
- Type inference and conversion

### ✅ Multi-turn Conversations
- Maintains chat history
- Context-aware follow-up questions
- Display previous queries and results

### ✅ Rich Visualizations
- Automatic chart generation (bar, line, pie, scatter, etc.)
- Interactive Plotly charts
- Responsive design
- Export-ready visualizations

### ✅ Code Transparency
- View generated code for every query
- Understand what the AI did
- Learn data analysis patterns

---

## 🛡️ Security & Safety

### Sandbox Protection
```python
# What's BLOCKED:
❌ import statements
❌ File I/O (open, read, write)
❌ Network calls
❌ System commands
❌ Dangerous builtins

# What's ALLOWED:
✅ pandas operations
✅ Plotly visualizations
✅ NumPy calculations
✅ Python standard functions (len, sum, etc.)
```

### API Security
- API key stored locally in `.env` (never in git)
- `.gitignore` prevents accidental commits
- Environment variables properly scoped

### Data Privacy
- Data stays on your machine (no uploads to AI)
- Only schema sent to LLM (structure, not actual data)
- Generated code executed locally

---

## 📦 Dependencies

| Package | Purpose | Version |
|---------|---------|---------|
| streamlit | Web UI framework | Latest |
| pandas | Data manipulation | Latest |
| plotly | Interactive charts | Latest |
| requests | API calls | Latest |
| python-dotenv | Environment variables | Latest |

All are lightweight and well-maintained.

---

## 🚨 Troubleshooting

### ❌ API Key Error
```
ValueError: OPENROUTER_API_KEY not found in .env file
```
**Solution:**
1. Create `.env` file in project root
2. Add: `OPENROUTER_API_KEY=your-key-here`
3. Get key from [openrouter.ai](https://openrouter.ai)

### ❌ Module Not Found
```
ImportError: No module named 'streamlit'
```
**Solution:**
```bash
pip install -r requirements.txt
```

### ❌ Execution Errors
**Common causes:**
- Column names with typos → Ask more clearly
- Data type mismatch → Try simpler queries
- Memory limit → Use smaller datasets

**Debug:**
1. Click "View generated code"
2. Check what code was generated
3. Try a simpler question

### ❌ Slow Performance
- Try faster models (DeepSeek, MiniMax)
- Use smaller CSV files (<100MB)
- Check internet connection
- OpenRouter API response time varies

---

## 💻 Development

### Local Setup
```bash
# Clone repo
git clone <repo-url>
cd LLM-Powered-Data-Analytics-Assistant

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dev dependencies
pip install -r requirements.txt

# Create .env with your key
echo "OPENROUTER_API_KEY=your-key" > .env

# Run app
streamlit run app.py
```

### Project Architecture
- **Modular design**: Separates concerns (config, agent, executor, utils)
- **Type hints**: Improves code clarity
- **Error handling**: Graceful failure modes
- **Clean code**: Well-documented functions

---

## 📝 Configuration

### System Prompt Customization
Edit `config/settings.py` to modify:
- LLM behavior instructions
- Data handling rules
- Output format preferences

### Model Selection
Change default model in `config/settings.py`:
```python
MODELS = {
    "Your Default": "model-id:free",
    # ... other models
}
```

---

## 🤝 Contributing

Contributions welcome! Areas for improvement:
- [ ] Support for JSON, Excel, SQL databases
- [ ] Advanced visualization templates
- [ ] Custom prompt builder UI
- [ ] Model comparison feature
- [ ] Data quality reports

---

## 📚 Examples

### Example 1: Quick Summary
```
Question: "Give me a summary of the data"
Result: Row count, columns, data types, sample statistics
```

### Example 2: Filtering & Analysis
```
Question: "Show hotels with rating > 7.5 and their review counts"
Result: Filtered table with matching hotels
```

### Example 3: Comparative Analysis
```
Question: "Compare average ratings across different hotel types"
Result: Grouped statistics + bar chart comparison
```

---

## ⚡ Performance Tips

1. **Choose right model**: DeepSeek/MiniMax are faster for simple queries
2. **Ask clear questions**: Specific questions = faster, better results
3. **Smaller datasets**: <10MB CSVs process instantly
4. **Check connection**: Stable internet = reliable API calls
5. **Read error messages**: Detailed feedback helps adjust queries

---

## 📄 License

MIT License - See LICENSE file for details

---

## 🎓 Learn More

- [OpenRouter Docs](https://openrouter.ai/docs)
- [Streamlit Docs](https://docs.streamlit.io)
- [Pandas Tutorial](https://pandas.pydata.org/docs)
- [Plotly Gallery](https://plotly.com/python)

---

## 📞 Support

- 🐛 Found a bug? Open an issue
- 💡 Have ideas? Start a discussion
- ❓ Questions? Check troubleshooting section

---

## ✨ Features Roadmap

- [ ] Support for database connections
- [ ] Custom data cleaning rules
- [ ] Report generation (PDF export)
- [ ] Advanced analytics (ML models, forecasting)
- [ ] Team collaboration features
- [ ] API endpoint for programmatic access

---

**Made with ❤️ for data enthusiasts**

⭐ If you find this useful, please star the repository!
