# Safe code execution sandbox
import pandas as pd
import traceback

def run_code(code: str, df: pd.DataFrame) -> dict:
    """
    Executes LLM-generated code with `df` in scope.
    Returns: {"fig": Plotly fig | None, "result_df": DataFrame | None, "error": str | None}
    """
    local_vars = {"df": df.copy(), "fig": None, "result_df": None}

    # Minimal allowlist — block dangerous builtins
    safe_globals = {
        "__builtins__": {
            "print": print, "len": len, "range": range,
            "list": list, "dict": dict, "str": str, "int": int,
            "float": float, "bool": bool, "round": round,
            "min": min, "max": max, "sum": sum, "abs": abs,
            "enumerate": enumerate, "zip": zip, "sorted": sorted,
        }
    }

    # Allow pandas and plotly imports inside exec
    import plotly.express as px
    import plotly.graph_objects as go
    import numpy as np

    safe_globals["pd"]  = pd
    safe_globals["px"]  = px
    safe_globals["go"]  = go
    safe_globals["np"]  = np

    try:
        exec(code, safe_globals, local_vars)
        return {
            "fig":       local_vars.get("fig"),
            "result_df": local_vars.get("result_df"),
            "error":     None
        }
    except Exception:
        return {
            "fig":       None,
            "result_df": None,
            "error":     traceback.format_exc()
        }