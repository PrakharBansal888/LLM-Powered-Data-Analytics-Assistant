# LLM Agent for data analysis
import requests
import re
import textwrap
from config.settings import OPENROUTER_API_KEY, MODELS, SYSTEM_PROMPT


def ask_llm(schema: str, question: str, history: list, model_key: str) -> dict:
    """
    Call OpenRouter LLM API to generate analysis code.
    
    Args:
        schema: Dataset schema description
        question: User question about the data
        history: Chat history
        model_key: Selected model name from MODELS dict
    
    Returns:
        {
            "code": str,
            "insight": str,
            "raw": str,
            "model_used": str,
            "error": str | None
        }
    """
    model_id = MODELS[model_key]

    # Build message history
    messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    for msg in history:
        messages.append(msg)
    messages.append({
        "role": "user",
        "content": f"Dataset schema:\n{schema}\n\nQuestion: {question}"
    })

    try:
        response = requests.post(
            url="https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {OPENROUTER_API_KEY}",
                "Content-Type": "application/json",
                "HTTP-Referer": "http://localhost:8501",
                "X-Title": "LLM Analytics Assistant",
            },
            json={
                "model": model_id,
                "messages": messages,
            },
            timeout=30
        )

        data = response.json()

        # Handle API errors
        if "error" in data:
            error_msg = data.get("error", {}).get("message", "Unknown API error")
            return {
                "code": "",
                "insight": "",
                "raw": "",
                "model_used": model_key,
                "error": error_msg
            }

        raw = data["choices"][0]["message"]["content"]

        # Extract code block
        code = _extract_code_block(raw)
        # Extract insight
        insight = _extract_insight(raw)

        return {
            "code": code,
            "insight": insight,
            "raw": raw,
            "model_used": model_key,
            "error": None
        }

    except requests.exceptions.RequestException as e:
        return {
            "code": "",
            "insight": "",
            "raw": "",
            "model_used": model_key,
            "error": f"API request failed: {str(e)}"
        }


def _extract_code_block(text: str) -> str:
    """Extract Python code block from markdown."""
    match = re.search(r"```python\s*(.*?)```", text, re.DOTALL)
    if match:
        raw_code = match.group(1)
        # Dedent to remove common leading whitespace
        code = textwrap.dedent(raw_code).strip()
        # Clean up blank lines
        code = '\n'.join(line.rstrip() for line in code.split('\n')).strip()
        return code
    return ""


def _extract_insight(text: str) -> str:
    """Extract insight section from response."""
    match = re.search(r"INSIGHT:(.*?)$", text, re.DOTALL)
    return match.group(1).strip() if match else ""
