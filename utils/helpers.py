"""Helper functions for data analysis."""

import pandas as pd


def is_numeric_column(series: pd.Series) -> bool:
    """Check if a column is numeric."""
    return pd.api.types.is_numeric_dtype(series)


def get_column_type(series: pd.Series) -> str:
    """Get human-readable column type."""
    if pd.api.types.is_integer_dtype(series):
        return "integer"
    elif pd.api.types.is_float_dtype(series):
        return "float"
    elif pd.api.types.is_datetime64_any_dtype(series):
        return "datetime"
    elif pd.api.types.is_bool_dtype(series):
        return "boolean"
    else:
        return "string"

