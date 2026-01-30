"""Row-level comparison validation."""

import pandas as pd

from models.result import ValidationResult, ValidationStatus


def validate_row_level(
    df1: pd.DataFrame, df2: pd.DataFrame, max_differences: int = 100
) -> ValidationResult:
    """
    Compare rows by index (strict comparison).

    Args:
        df1: First dataframe
        df2: Second dataframe
        max_differences: Maximum number of differences to return

    Returns:
        ValidationResult with row-level differences
    """
    # Skip if row counts don't match
    if len(df1) != len(df2):
        return ValidationResult(
            name="Row Level Differences",
            status=ValidationStatus.WARNING,
            summary="Cannot compare rows - row counts differ",
            details={"differences": []},
        )

    # Skip if column names don't match
    if set(df1.columns) != set(df2.columns):
        return ValidationResult(
            name="Row Level Differences",
            status=ValidationStatus.WARNING,
            summary="Cannot compare rows - column names differ",
            details={"differences": []},
        )

    # Align columns
    df2_aligned = df2[df1.columns]

    # Find differences
    differences: list[dict[str, str | int]] = []
    for idx in range(len(df1)):
        row1 = df1.iloc[idx]
        row2 = df2_aligned.iloc[idx]

        for col in df1.columns:
            val1 = row1[col]
            val2 = row2[col]

            # Handle NaN comparison
            if pd.isna(val1) and pd.isna(val2):
                continue

            if val1 != val2:
                differences.append(
                    {
                        "row_index": idx,
                        "column": col,
                        "source_value": str(val1),
                        "target_value": str(val2),
                    }
                )

                if len(differences) >= max_differences:
                    break

        if len(differences) >= max_differences:
            break

    # Determine status
    if differences:
        status = ValidationStatus.FAIL
        summary = f"Found {len(differences)} difference(s) (showing first {max_differences})"
    else:
        status = ValidationStatus.PASS
        summary = "All rows match perfectly"

    return ValidationResult(
        name="Row Level Differences",
        status=status,
        summary=summary,
        details={"differences": differences[:max_differences]},
    )


