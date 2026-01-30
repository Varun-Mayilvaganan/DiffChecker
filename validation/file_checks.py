"""File-level validation checks."""

import pandas as pd

from models.result import ValidationResult, ValidationStatus


def validate_file_level(df1: pd.DataFrame, df2: pd.DataFrame) -> ValidationResult:
    """
    Validate row and column counts.

    Args:
        df1: First dataframe
        df2: Second dataframe

    Returns:
        ValidationResult with file-level comparison
    """
    row_match = len(df1) == len(df2)
    col_match = len(df1.columns) == len(df2.columns)

    if row_match and col_match:
        status = ValidationStatus.PASS
        summary = "File structure matches"
    else:
        status = ValidationStatus.FAIL
        issues = []
        if not row_match:
            issues.append(f"row count mismatch ({len(df1)} vs {len(df2)})")
        if not col_match:
            issues.append(f"column count mismatch ({len(df1.columns)} vs {len(df2.columns)})")
        summary = ", ".join(issues)

    return ValidationResult(
        name="File Validation",
        status=status,
        summary=summary,
        details={
            "row_count_1": len(df1),
            "row_count_2": len(df2),
            "column_count_1": len(df1.columns),
            "column_count_2": len(df2.columns),
            "row_match": row_match,
            "column_match": col_match,
        },
    )

