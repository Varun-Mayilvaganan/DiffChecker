"""Validation result data structures."""

from dataclasses import dataclass
from enum import Enum
from typing import Any


class ValidationStatus(Enum):
    """Status of a validation check."""

    PASS = "pass"
    WARNING = "warning"
    FAIL = "fail"


@dataclass
class ValidationResult:
    """Standard result structure for all validators."""

    name: str
    status: ValidationStatus
    summary: str
    details: dict[str, Any]


def compute_overall_status(results: list[ValidationResult]) -> ValidationStatus:
    """
    Compute overall status from multiple validation results.

    Logic:
    - If any FAIL → overall FAIL
    - If any WARNING (but no FAIL) → overall WARNING
    - If all PASS → overall PASS
    """
    statuses = [r.status for r in results]

    if ValidationStatus.FAIL in statuses:
        return ValidationStatus.FAIL
    if ValidationStatus.WARNING in statuses:
        return ValidationStatus.WARNING
    return ValidationStatus.PASS


