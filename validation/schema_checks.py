"""Schema-level validation checks."""

import pandas as pd

from models.result import ValidationResult, ValidationStatus
from utils.helpers import get_column_type


def validate_schema(df1: pd.DataFrame, df2: pd.DataFrame) -> ValidationResult:
    """
    Validate column names and data types.

    Args:
        df1: First dataframe
        df2: Second dataframe

    Returns:
        ValidationResult with schema comparison
    """
    cols1 = set(df1.columns)
    cols2 = set(df2.columns)

    missing = sorted(cols1 - cols2)
    extra = sorted(cols2 - cols1)
    common = sorted(cols1 & cols2)

    # Check data type mismatches
    type_mismatches = []
    for col in common:
        type1 = get_column_type(df1[col])
        type2 = get_column_type(df2[col])
        if type1 != type2:
            type_mismatches.append({"column": col, "source_type": type1, "target_type": type2})

    # Determine status
    if missing or extra or type_mismatches:
        status = ValidationStatus.FAIL
        issues = []
        if missing:
            issues.append(f"{len(missing)} missing column(s)")
        if extra:
            issues.append(f"{len(extra)} extra column(s)")
        if type_mismatches:
            issues.append(f"{len(type_mismatches)} type mismatch(es)")
        summary = ", ".join(issues)
    else:
        status = ValidationStatus.PASS
        summary = "Schema matches perfectly"

    return ValidationResult(
        name="Schema Validation",
        status=status,
        summary=summary,
        details={
            "missing_columns": missing,
            "extra_columns": extra,
            "common_columns": common,
            "type_mismatches": type_mismatches,
        },
    )


