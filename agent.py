import requests
import re
import os
from dotenv import load_dotenv
import textwrap

load_dotenv()

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

if not OPENROUTER_API_KEY:
    raise ValueError("OPENROUTER_API_KEY not found in .env file. Please add it.")


MODELS = {
    "NVIDIA Nemotron 3 Nano 30B":  "nvidia/nemotron-3-nano-30b-a3b:free",
    "OpenAI GPT-OSS 120B":         "openai/gpt-oss-120b:free",
    "DeepSeek V4 Flash":           "deepseek/deepseek-v4-flash:free",
    "MiniMax M2.5":                "minimax/minimax-m2.5:free",
}

SYSTEM_PROMPT = """
You are a data analytics assistant. The user will give you a dataset schema
and ask a question about it. Your job is to:

1. Write a Python code block that uses `df` (a pandas DataFrame already in scope)
   to answer the question. Use Plotly Express for any charts — assign the figure to `fig`.
   If the answer is tabular, assign a DataFrame to `result_df`.
   If there is no chart, set fig = None. If there is no table, set result_df = None.

2. After the code block, write a SHORT plain-English summary (2-4 sentences)
   of what the code does and what insight the user should take from it.
   Start this section with "INSIGHT:" on its own line.

Rules:
- Only use: pandas, plotly.express, plotly.graph_objects, numpy.
- Do NOT import anything else. Do NOT read files or use open().
- Do NOT use st.* or any Streamlit calls inside the code block.
- Always wrap code in ```python ... ``` fences.
- NEVER use .astype() to convert strings to numeric types if they contain non-numeric characters

Data Handling Guidelines - CRITICAL:
1. ALWAYS inspect data first: print df.dtypes and df.head() mentally before processing
2. NEVER use .astype(float) or .astype(int) directly - strings like '2509 reviews' will fail!
3. For string columns with mixed content (text+numbers), use regex to extract numbers:
   - Example: df['col'].str.extract(r'(\d+)')[0].astype(float) to extract the numeric part
4. Use pd.to_numeric(df['col'].str.replace(...), errors='coerce') for safe conversions
5. Always handle NaN/invalid values: filter with dropna() or use errors='coerce'
6. For calculations, explicitly handle missing values and type errors
7. Test your logic mentally: if a value can't be converted, the code will fail

Example of correct approach:
- BAD: df['reviews'].astype(float)  # ❌ Fails on '2509 reviews'
- GOOD: pd.to_numeric(df['reviews'].str.extract(r'(\d+)')[0], errors='coerce')  # ✓
"""

def ask_llm(schema: str, question: str, history: list, model_key: str) -> dict:
    """
    model_key: one of the keys from MODELS dict
    Returns: {"code": str, "insight": str, "raw": str, "model_used": str}
    """
    model_id = MODELS[model_key]

    messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    for msg in history:
        messages.append(msg)
    messages.append({
        "role": "user",
        "content": f"Dataset schema:\n{schema}\n\nQuestion: {question}"
    })

    response = requests.post(
        url="https://openrouter.ai/api/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "Content-Type":  "application/json",
            "HTTP-Referer":  "http://localhost:8501",   # your app URL
            "X-Title":       "LLM Analytics Assistant",
        },
        json={
            "model":    model_id,
            "messages": messages,
        }
    )

    data = response.json()

    # Handle API errors gracefully
    if "error" in data:
        return {
            "code":       "",
            "insight":    "",
            "raw":        "",
            "model_used": model_key,
            "error":      data["error"].get("message", "Unknown API error")
        }

    raw = data["choices"][0]["message"]["content"]

    # Extract code block - more robust extraction
    code_match = re.search(r"```python\s*(.*?)```", raw, re.DOTALL)
    if code_match:
        raw_code = code_match.group(1)
        # First, dedent to remove common leading whitespace
        code = textwrap.dedent(raw_code).strip()
        # Remove any leading/trailing blank lines
        code = '\n'.join(line.rstrip() for line in code.split('\n')).strip()
    else:
        code = ""

    # Extract insight
    insight_match = re.search(r"INSIGHT:(.*?)$", raw, re.DOTALL)
    insight = insight_match.group(1).strip() if insight_match else ""

    return {
        "code":       code,
        "insight":    insight,
        "raw":        raw,
        "model_used": model_key,
        "error":      None
    }