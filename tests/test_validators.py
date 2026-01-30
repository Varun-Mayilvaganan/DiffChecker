"""Unit tests for validation functions."""

import numpy as np
import pandas as pd

from models.result import ValidationStatus
from validation.file_checks import validate_file_level
from validation.row_checks import validate_row_level
from validation.schema_checks import validate_schema
from validation.stats_checks import validate_column_stats


class TestFileValidation:
    """Test file-level validation."""

    def test_matching_files(self):
        df1 = pd.DataFrame({"a": [1, 2], "b": [3, 4]})
        df2 = pd.DataFrame({"a": [1, 2], "b": [3, 4]})

        result = validate_file_level(df1, df2)
        assert result.status == ValidationStatus.PASS

    def test_row_count_mismatch(self):
        df1 = pd.DataFrame({"a": [1, 2, 3]})
        df2 = pd.DataFrame({"a": [1, 2]})

        result = validate_file_level(df1, df2)
        assert result.status == ValidationStatus.FAIL

    def test_column_count_mismatch(self):
        df1 = pd.DataFrame({"a": [1], "b": [2], "c": [3]})
        df2 = pd.DataFrame({"a": [1], "b": [2]})

        result = validate_file_level(df1, df2)
        assert result.status == ValidationStatus.FAIL


class TestSchemaValidation:
    """Test schema-level validation."""

    def test_matching_schema(self):
        df1 = pd.DataFrame({"a": [1, 2], "b": ["x", "y"]})
        df2 = pd.DataFrame({"a": [3, 4], "b": ["z", "w"]})

        result = validate_schema(df1, df2)
        assert result.status == ValidationStatus.PASS

    def test_missing_columns(self):
        df1 = pd.DataFrame({"a": [1], "b": [2], "c": [3]})
        df2 = pd.DataFrame({"a": [1], "b": [2]})

        result = validate_schema(df1, df2)
        assert result.status == ValidationStatus.FAIL
        assert "c" in result.details["missing_columns"]

    def test_extra_columns(self):
        df1 = pd.DataFrame({"a": [1], "b": [2]})
        df2 = pd.DataFrame({"a": [1], "b": [2], "c": [3]})

        result = validate_schema(df1, df2)
        assert result.status == ValidationStatus.FAIL
        assert "c" in result.details["extra_columns"]

    def test_type_mismatch(self):
        df1 = pd.DataFrame({"a": [1, 2, 3]})
        df2 = pd.DataFrame({"a": ["1", "2", "3"]})

        result = validate_schema(df1, df2)
        assert result.status == ValidationStatus.FAIL
        assert len(result.details["type_mismatches"]) > 0


class TestColumnStats:
    """Test column-level statistics."""

    def test_matching_stats(self):
        df1 = pd.DataFrame({"a": [1, 2, 3], "b": ["x", "y", "z"]})
        df2 = pd.DataFrame({"a": [1, 2, 3], "b": ["x", "y", "z"]})

        result = validate_column_stats(df1, df2)
        assert result.status == ValidationStatus.PASS

    def test_stat_mismatch(self):
        df1 = pd.DataFrame({"a": [1, 2, 3]})
        df2 = pd.DataFrame({"a": [1, 2, 4]})

        result = validate_column_stats(df1, df2)
        assert result.status == ValidationStatus.FAIL

    def test_no_common_columns(self):
        df1 = pd.DataFrame({"a": [1, 2]})
        df2 = pd.DataFrame({"b": [3, 4]})

        result = validate_column_stats(df1, df2)
        assert result.status == ValidationStatus.WARNING


class TestRowComparison:
    """Test row-level comparison."""

    def test_matching_rows(self):
        df1 = pd.DataFrame({"a": [1, 2], "b": [3, 4]})
        df2 = pd.DataFrame({"a": [1, 2], "b": [3, 4]})

        result = validate_row_level(df1, df2)
        assert result.status == ValidationStatus.PASS

    def test_row_differences(self):
        df1 = pd.DataFrame({"a": [1, 2], "b": [3, 4]})
        df2 = pd.DataFrame({"a": [1, 2], "b": [3, 5]})

        result = validate_row_level(df1, df2)
        assert result.status == ValidationStatus.FAIL
        assert len(result.details["differences"]) > 0

    def test_skip_on_row_count_mismatch(self):
        df1 = pd.DataFrame({"a": [1, 2, 3]})
        df2 = pd.DataFrame({"a": [1, 2]})

        result = validate_row_level(df1, df2)
        assert result.status == ValidationStatus.WARNING

    def test_skip_on_schema_mismatch(self):
        df1 = pd.DataFrame({"a": [1], "b": [2]})
        df2 = pd.DataFrame({"a": [1], "c": [3]})

        result = validate_row_level(df1, df2)
        assert result.status == ValidationStatus.WARNING

    def test_nan_handling(self):
        df1 = pd.DataFrame({"a": [1, np.nan, 3]})
        df2 = pd.DataFrame({"a": [1, np.nan, 3]})

        result = validate_row_level(df1, df2)
        assert result.status == ValidationStatus.PASS

