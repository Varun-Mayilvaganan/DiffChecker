"""Column-level statistics validation."""

import pandas as pd

from models.result import ValidationResult, ValidationStatus
from utils.helpers import is_numeric_column


def validate_column_stats(df1: pd.DataFrame, df2: pd.DataFrame) -> ValidationResult:
    """
    Compare column-level statistics.

    Args:
        df1: First dataframe
        df2: Second dataframe

    Returns:
        ValidationResult with column statistics comparison
    """
    common_cols = sorted(set(df1.columns) & set(df2.columns))

    if not common_cols:
        return ValidationResult(
            name="Column Statistics",
            status=ValidationStatus.WARNING,
            summary="No common columns to compare",
            details={"stats": []},
        )

    stats_comparison = []
    mismatches = 0

    for col in common_cols:
        col1 = df1[col]
        col2 = df2[col]

        if is_numeric_column(col1) and is_numeric_column(col2):
            # Numeric column stats
            stats = {
                "column": col,
                "type": "numeric",
                "source_nulls": int(col1.isna().sum()),
                "target_nulls": int(col2.isna().sum()),
                "source_min": float(col1.min()) if not col1.isna().all() else None,
                "target_min": float(col2.min()) if not col2.isna().all() else None,
                "source_max": float(col1.max()) if not col1.isna().all() else None,
                "target_max": float(col2.max()) if not col2.isna().all() else None,
                "source_sum": float(col1.sum()) if not col1.isna().all() else None,
                "target_sum": float(col2.sum()) if not col2.isna().all() else None,
            }
            # Check for mismatches
            if (
                stats["source_nulls"] != stats["target_nulls"]
                or stats["source_min"] != stats["target_min"]
                or stats["source_max"] != stats["target_max"]
                or stats["source_sum"] != stats["target_sum"]
            ):
                stats["match"] = False
                mismatches += 1
            else:
                stats["match"] = True
        else:
            # Non-numeric column stats
            stats = {
                "column": col,
                "type": "non-numeric",
                "source_nulls": int(col1.isna().sum()),
                "target_nulls": int(col2.isna().sum()),
                "source_unique": int(col1.nunique()),
                "target_unique": int(col2.nunique()),
            }
            # Check for mismatches
            if stats["source_nulls"] != stats["target_nulls"] or stats["source_unique"] != stats["target_unique"]:
                stats["match"] = False
                mismatches += 1
            else:
                stats["match"] = True

        stats_comparison.append(stats)

    # Determine overall status
    if mismatches > 0:
        status = ValidationStatus.FAIL
        summary = f"{mismatches} column(s) with statistical differences"
    else:
        status = ValidationStatus.PASS
        summary = "All column statistics match"

    return ValidationResult(
        name="Column Statistics",
        status=status,
        summary=summary,
        details={"stats": stats_comparison, "mismatch_count": mismatches},
    )


