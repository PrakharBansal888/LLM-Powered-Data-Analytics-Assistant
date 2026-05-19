# Code executor with proper sandbox
import pandas as pd
import traceback
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import re


def _clean_code(code: str) -> str:
    """Remove import statements and other dangerous code."""
    lines = []
    for line in code.split('\n'):
        stripped = line.strip()
        # Skip import statements
        if stripped.startswith('import ') or stripped.startswith('from '):
            continue
        lines.append(line)
    return '\n'.join(lines).strip()


def run_code(code: str, df: pd.DataFrame) -> dict:
    """
    Executes LLM-generated code in a controlled sandbox.
    Returns: {"fig": Plotly fig | None, "result_df": DataFrame | None, "error": str | None, "success": bool}
    """
    # Clean the code first (remove imports)
    code = _clean_code(code)
    
    # Pre-define all variables available to the user
    local_vars = {
        "df": df.copy(), 
        "fig": None, 
        "result_df": None
    }

    # Safe globals with only allowed modules/functions
    safe_globals = {
        "pd": pd,
        "px": px,
        "go": go,
        "np": np,
        "__builtins__": {
            "print": print,
            "len": len,
            "range": range,
            "list": list,
            "dict": dict,
            "tuple": tuple,
            "set": set,
            "str": str,
            "int": int,
            "float": float,
            "bool": bool,
            "round": round,
            "min": min,
            "max": max,
            "sum": sum,
            "abs": abs,
            "enumerate": enumerate,
            "zip": zip,
            "sorted": sorted,
            "reversed": reversed,
            "map": map,
            "filter": filter,
            "all": all,
            "any": any,
            "isinstance": isinstance,
            "type": type,
        }
    }

    try:
        # Execute the code with restricted globals and local variables
        exec(code, safe_globals, local_vars)
        
        return {
            "fig": local_vars.get("fig"),
            "result_df": local_vars.get("result_df"),
            "error": None,
            "success": True
        }
    except Exception as e:
        error_msg = traceback.format_exc()
        # Clean up traceback for better readability
        return {
            "fig": None,
            "result_df": None,
            "error": error_msg,
            "success": False
        }


def validate_code(code: str) -> tuple[bool, str]:
    """
    Validates that code doesn't contain dangerous operations.
    Returns: (is_safe: bool, message: str)
    """
    dangerous_patterns = [
        r'__import__',
        r'eval\(',
        r'open\(',
        r'__',
    ]
    
    for pattern in dangerous_patterns:
        if re.search(pattern, code):
            return False, f"Code contains restricted operation: {pattern}"
    
    return True, "Code is safe"
