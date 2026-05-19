# Utility functions
import pandas as pd


def extract_schema(df: pd.DataFrame) -> str:
    """
    Returns a compact schema string the LLM can read:
    column name, dtype, and 3 sample values per column.
    """
    lines = [f"Shape: {df.shape[0]} rows × {df.shape[1]} columns\n"]
    for col in df.columns:
        dtype = str(df[col].dtype)
        samples = df[col].dropna().head(3).tolist()
        lines.append(f"  - {col} ({dtype}): {samples}")
    return "\n".join(lines)


def load_csv(uploaded_file) -> pd.DataFrame:
    """Load CSV file and return DataFrame"""
    return pd.read_csv(uploaded_file)
