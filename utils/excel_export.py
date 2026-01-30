"""Excel report export functionality using XlsxWriter."""

from datetime import datetime
from io import BytesIO
from typing import Any

import pandas as pd
import xlsxwriter

from models.result import ValidationResult, ValidationStatus


class ExcelReportGenerator:
    """Generate professional Excel validation reports using XlsxWriter."""

    def __init__(
        self,
        report_name: str,
        project_name: str = "",
        environment: str = "UAT",
        cognos_report_name: str = "",
        powerbi_report_name: str = "",
    ) -> None:
        """Initialize the report generator.

        Args:
            report_name: Name of the report being validated
            project_name: Name of the project
            environment: Environment (UAT, DEV, SIT, PROD, QA)
            cognos_report_name: Name of the Cognos source report
            powerbi_report_name: Name of the PowerBI target report
        """
        self.report_name = report_name or "Data Validation Report"
        self.project_name = project_name or "DataSure Validation"
        self.environment = environment or "UAT"
        self.cognos_report_name = cognos_report_name or "Cognos_Export"
        self.powerbi_report_name = powerbi_report_name or "PowerBI_Export"
        self.validation_date = datetime.now().strftime("%Y-%m-%d %H:%M")

    def _create_formats(self, workbook: xlsxwriter.Workbook) -> dict[str, Any]:
        """Create all formatting styles for the workbook."""
        formats = {}

        # Title format
        formats["title"] = workbook.add_format({
            "bold": True,
            "font_size": 16,
            "font_color": "#1e3a5f",
            "align": "center",
            "valign": "vcenter",
        })

        # Header format (dark blue background)
        formats["header"] = workbook.add_format({
            "bold": True,
            "font_size": 11,
            "font_color": "white",
            "bg_color": "#1e3a5f",
            "align": "center",
            "valign": "vcenter",
            "border": 1,
            "text_wrap": True,
        })

        # Sub-header format
        formats["sub_header"] = workbook.add_format({
            "bold": True,
            "font_size": 10,
            "font_color": "white",
            "bg_color": "#4472c4",
            "align": "center",
            "valign": "vcenter",
            "border": 1,
        })

        # Field label format (left column in key-value pairs)
        formats["field_label"] = workbook.add_format({
            "bold": True,
            "font_size": 10,
            "bg_color": "#d9e2f3",
            "align": "left",
            "valign": "vcenter",
            "border": 1,
        })

        # Field value format
        formats["field_value"] = workbook.add_format({
            "font_size": 10,
            "align": "left",
            "valign": "vcenter",
            "border": 1,
        })

        # Data cell format
        formats["data"] = workbook.add_format({
            "font_size": 10,
            "align": "center",
            "valign": "vcenter",
            "border": 1,
        })

        # Data cell left-aligned
        formats["data_left"] = workbook.add_format({
            "font_size": 10,
            "align": "left",
            "valign": "vcenter",
            "border": 1,
        })

        # Number format
        formats["number"] = workbook.add_format({
            "font_size": 10,
            "align": "center",
            "valign": "vcenter",
            "border": 1,
            "num_format": "#,##0.00",
        })

        # Integer format
        formats["integer"] = workbook.add_format({
            "font_size": 10,
            "align": "center",
            "valign": "vcenter",
            "border": 1,
            "num_format": "#,##0",
        })

        # Percentage format
        formats["percent"] = workbook.add_format({
            "font_size": 10,
            "align": "center",
            "valign": "vcenter",
            "border": 1,
            "num_format": "0.00%",
        })

        # Status formats
        formats["status_pass"] = workbook.add_format({
            "bold": True,
            "font_size": 10,
            "font_color": "white",
            "bg_color": "#10b981",
            "align": "center",
            "valign": "vcenter",
            "border": 1,
        })

        formats["status_warning"] = workbook.add_format({
            "bold": True,
            "font_size": 10,
            "font_color": "white",
            "bg_color": "#f59e0b",
            "align": "center",
            "valign": "vcenter",
            "border": 1,
        })

        formats["status_fail"] = workbook.add_format({
            "bold": True,
            "font_size": 10,
            "font_color": "white",
            "bg_color": "#ef4444",
            "align": "center",
            "valign": "vcenter",
            "border": 1,
        })

        # Match/Mismatch formats
        formats["match"] = workbook.add_format({
            "font_size": 10,
            "font_color": "#065f46",
            "bg_color": "#d1fae5",
            "align": "center",
            "valign": "vcenter",
            "border": 1,
        })

        formats["mismatch"] = workbook.add_format({
            "font_size": 10,
            "font_color": "#991b1b",
            "bg_color": "#fee2e2",
            "align": "center",
            "valign": "vcenter",
            "border": 1,
        })

        # Alternating row colors
        formats["row_alt"] = workbook.add_format({
            "font_size": 10,
            "align": "center",
            "valign": "vcenter",
            "border": 1,
            "bg_color": "#f8fafc",
        })

        formats["row_alt_left"] = workbook.add_format({
            "font_size": 10,
            "align": "left",
            "valign": "vcenter",
            "border": 1,
            "bg_color": "#f8fafc",
        })

        return formats

    def _get_status_format(
        self, status: ValidationStatus | str, formats: dict[str, Any]
    ) -> Any:
        """Get the appropriate format for a validation status."""
        if isinstance(status, ValidationStatus):
            status_val = status.value
        else:
            status_val = str(status).lower()

        if status_val == "pass" or status_val == "match":
            return formats["status_pass"]
        elif status_val == "warning" or status_val == "accepted":
            return formats["status_warning"]
        else:
            return formats["status_fail"]

    def _write_validation_overview(
        self,
        workbook: xlsxwriter.Workbook,
        formats: dict[str, Any],
        results: list[ValidationResult],
        overall_status: ValidationStatus,
    ) -> None:
        """Write the Validation Overview sheet."""
        sheet = workbook.add_worksheet("Validation_Overview")
        sheet.set_column("A:A", 30)
        sheet.set_column("B:B", 40)

        # Title
        sheet.merge_range("A1:B1", "DATA VALIDATION REPORT", formats["title"])
        sheet.set_row(0, 30)

        # Overview data
        overview_data = [
            ("Field", "Value"),
            ("Project Name", self.project_name),
            ("Report Name", self.report_name),
            ("Cognos Report Name", self.cognos_report_name),
            ("Power BI Report Name", self.powerbi_report_name),
            ("Environment", self.environment),
            ("Validation Date", self.validation_date),
            ("Validated By", "DataSure Platform"),
            ("Date Range Used", "Full Dataset"),
            ("Overall Validation Status", overall_status.value.upper()),
            ("Known Limitations Referenced", "See Known_Limitations sheet"),
        ]

        for row_idx, (field, value) in enumerate(overview_data, start=2):
            if row_idx == 2:  # Header row
                sheet.write(row_idx, 0, field, formats["header"])
                sheet.write(row_idx, 1, value, formats["header"])
            elif field == "Overall Validation Status":
                sheet.write(row_idx, 0, field, formats["field_label"])
                sheet.write(
                    row_idx, 1, value, self._get_status_format(overall_status, formats)
                )
            else:
                sheet.write(row_idx, 0, field, formats["field_label"])
                sheet.write(row_idx, 1, value, formats["field_value"])

        # Add validation summary
        row = len(overview_data) + 4
        sheet.merge_range(row, 0, row, 1, "VALIDATION SUMMARY", formats["sub_header"])
        row += 1

        sheet.write(row, 0, "Validation Check", formats["header"])
        sheet.write(row, 1, "Result", formats["header"])
        row += 1

        for result in results:
            sheet.write(row, 0, result.name, formats["field_label"])
            sheet.write(
                row, 1, result.status.value.upper(),
                self._get_status_format(result.status, formats)
            )
            row += 1

    def _write_data_sheet(
        self,
        workbook: xlsxwriter.Workbook,
        formats: dict[str, Any],
        df: pd.DataFrame,
        sheet_name: str,
        max_rows: int = 100,
    ) -> None:
        """Write a data sample sheet (Cognos or PowerBI data)."""
        sheet = workbook.add_worksheet(sheet_name)

        # Limit rows for display
        df_sample = df.head(max_rows)

        # Set column widths based on content
        for col_idx, col_name in enumerate(df_sample.columns):
            max_len = max(
                len(str(col_name)),
                df_sample[col_name].astype(str).str.len().max() if len(df_sample) > 0 else 0
            )
            sheet.set_column(col_idx, col_idx, min(max_len + 2, 40))

        # Write headers
        for col_idx, col_name in enumerate(df_sample.columns):
            sheet.write(0, col_idx, col_name, formats["header"])

        # Write data
        for row_idx, (_, row) in enumerate(df_sample.iterrows(), start=1):
            for col_idx, value in enumerate(row):
                fmt = formats["row_alt"] if row_idx % 2 == 0 else formats["data"]
                if pd.isna(value):
                    sheet.write(row_idx, col_idx, "", fmt)
                elif isinstance(value, (int, float)):
                    sheet.write_number(row_idx, col_idx, value, fmt)
                else:
                    sheet.write(row_idx, col_idx, str(value), fmt)

        # Add note if truncated
        if len(df) > max_rows:
            note_row = len(df_sample) + 2
            sheet.write(
                note_row, 0,
                f"Note: Showing first {max_rows} of {len(df)} rows",
                formats["field_label"]
            )

    def _write_metric_comparison(
        self,
        workbook: xlsxwriter.Workbook,
        formats: dict[str, Any],
        stats_result: ValidationResult,
    ) -> None:
        """Write the Metric Comparison sheet (Column Statistics)."""
        sheet = workbook.add_worksheet("Metric_Comparison")

        # Set column widths
        sheet.set_column("A:A", 25)  # Metric Name
        sheet.set_column("B:B", 18)  # Column
        sheet.set_column("C:C", 18)  # Cognos Value
        sheet.set_column("D:D", 18)  # PowerBI Value
        sheet.set_column("E:E", 15)  # Difference
        sheet.set_column("F:F", 15)  # % Difference
        sheet.set_column("G:G", 12)  # Status
        sheet.set_column("H:H", 30)  # Comments

        # Headers
        headers = [
            "Column Name", "Metric", "Cognos Value", "Power BI Value",
            "Difference", "% Difference", "Status", "Comments"
        ]
        for col_idx, header in enumerate(headers):
            sheet.write(0, col_idx, header, formats["header"])

        stats = stats_result.details.get("stats", [])
        row = 1

        for col_stats in stats:
            col = col_stats["column"]
            is_numeric = col_stats["type"] == "numeric"

            # Null count comparison
            src_nulls = col_stats["source_nulls"]
            tgt_nulls = col_stats["target_nulls"]
            null_match = src_nulls == tgt_nulls

            sheet.write(row, 0, col, formats["data_left"])
            sheet.write(row, 1, "Null Count", formats["data"])
            sheet.write(row, 2, src_nulls, formats["integer"])
            sheet.write(row, 3, tgt_nulls, formats["integer"])

            diff = tgt_nulls - src_nulls
            pct_diff = (diff / src_nulls * 100) if src_nulls > 0 else 0
            sheet.write(row, 4, diff, formats["integer"])
            sheet.write(row, 5, f"{pct_diff:.2f}%", formats["data"])
            sheet.write(
                row, 6, "Match" if null_match else "Mismatch",
                formats["match"] if null_match else formats["mismatch"]
            )
            sheet.write(row, 7, "" if null_match else "Null count differs", formats["data_left"])
            row += 1

            if is_numeric:
                # Min comparison
                src_min = col_stats.get("source_min", 0)
                tgt_min = col_stats.get("target_min", 0)
                min_match = src_min == tgt_min

                sheet.write(row, 0, col, formats["data_left"])
                sheet.write(row, 1, "Min", formats["data"])
                sheet.write(row, 2, src_min if src_min else 0, formats["number"])
                sheet.write(row, 3, tgt_min if tgt_min else 0, formats["number"])

                diff = (tgt_min or 0) - (src_min or 0)
                pct_diff = (diff / src_min * 100) if src_min else 0
                sheet.write(row, 4, diff, formats["number"])
                sheet.write(row, 5, f"{pct_diff:.2f}%", formats["data"])
                sheet.write(
                    row, 6, "Match" if min_match else "Mismatch",
                    formats["match"] if min_match else formats["mismatch"]
                )
                sheet.write(row, 7, "" if min_match else "Min value differs", formats["data_left"])
                row += 1

                # Max comparison
                src_max = col_stats.get("source_max", 0)
                tgt_max = col_stats.get("target_max", 0)
                max_match = src_max == tgt_max

                sheet.write(row, 0, col, formats["data_left"])
                sheet.write(row, 1, "Max", formats["data"])
                sheet.write(row, 2, src_max if src_max else 0, formats["number"])
                sheet.write(row, 3, tgt_max if tgt_max else 0, formats["number"])

                diff = (tgt_max or 0) - (src_max or 0)
                pct_diff = (diff / src_max * 100) if src_max else 0
                sheet.write(row, 4, diff, formats["number"])
                sheet.write(row, 5, f"{pct_diff:.2f}%", formats["data"])
                sheet.write(
                    row, 6, "Match" if max_match else "Mismatch",
                    formats["match"] if max_match else formats["mismatch"]
                )
                sheet.write(row, 7, "" if max_match else "Max value differs", formats["data_left"])
                row += 1

                # Sum comparison
                src_sum = col_stats.get("source_sum", 0)
                tgt_sum = col_stats.get("target_sum", 0)
                sum_match = src_sum == tgt_sum

                sheet.write(row, 0, col, formats["data_left"])
                sheet.write(row, 1, "Sum", formats["data"])
                sheet.write(row, 2, src_sum if src_sum else 0, formats["number"])
                sheet.write(row, 3, tgt_sum if tgt_sum else 0, formats["number"])

                diff = (tgt_sum or 0) - (src_sum or 0)
                pct_diff = (diff / src_sum * 100) if src_sum else 0
                sheet.write(row, 4, diff, formats["number"])
                sheet.write(row, 5, f"{pct_diff:.2f}%", formats["data"])
                sheet.write(
                    row, 6, "Match" if sum_match else "Mismatch",
                    formats["match"] if sum_match else formats["mismatch"]
                )
                sheet.write(
                    row, 7, "" if sum_match else "Sum differs - investigate",
                    formats["data_left"]
                )
                row += 1
            else:
                # Unique count for non-numeric
                src_unique = col_stats.get("source_unique", 0)
                tgt_unique = col_stats.get("target_unique", 0)
                unique_match = src_unique == tgt_unique

                sheet.write(row, 0, col, formats["data_left"])
                sheet.write(row, 1, "Unique Count", formats["data"])
                sheet.write(row, 2, src_unique, formats["integer"])
                sheet.write(row, 3, tgt_unique, formats["integer"])

                diff = tgt_unique - src_unique
                pct_diff = (diff / src_unique * 100) if src_unique else 0
                sheet.write(row, 4, diff, formats["integer"])
                sheet.write(row, 5, f"{pct_diff:.2f}%", formats["data"])
                sheet.write(
                    row, 6, "Match" if unique_match else "Mismatch",
                    formats["match"] if unique_match else formats["mismatch"]
                )
                sheet.write(
                    row, 7, "" if unique_match else "Cardinality differs",
                    formats["data_left"]
                )
                row += 1

    def _write_schema_validation(
        self,
        workbook: xlsxwriter.Workbook,
        formats: dict[str, Any],
        schema_result: ValidationResult,
    ) -> None:
        """Write the Filter Level Validation sheet (Schema Validation)."""
        sheet = workbook.add_worksheet("Schema_Validation")

        # Set column widths
        sheet.set_column("A:A", 20)
        sheet.set_column("B:B", 25)
        sheet.set_column("C:C", 20)
        sheet.set_column("D:D", 20)
        sheet.set_column("E:E", 12)
        sheet.set_column("F:F", 35)

        details = schema_result.details
        missing = details.get("missing_columns", [])
        extra = details.get("extra_columns", [])
        type_mismatches = details.get("type_mismatches", [])

        # Section 1: Column Existence
        sheet.merge_range("A1:F1", "SCHEMA VALIDATION RESULTS", formats["title"])
        sheet.set_row(0, 25)

        row = 2
        sheet.merge_range(row, 0, row, 5, "Column Existence Check", formats["sub_header"])
        row += 1

        headers = ["Check Type", "Column Name", "In Cognos", "In PowerBI", "Status", "Remarks"]
        for col_idx, header in enumerate(headers):
            sheet.write(row, col_idx, header, formats["header"])
        row += 1

        # Missing columns
        for col in missing:
            sheet.write(row, 0, "Missing Column", formats["data"])
            sheet.write(row, 1, col, formats["data_left"])
            sheet.write(row, 2, "Yes", formats["match"])
            sheet.write(row, 3, "No", formats["mismatch"])
            sheet.write(row, 4, "FAIL", formats["status_fail"])
            sheet.write(row, 5, "Column missing in PowerBI", formats["data_left"])
            row += 1

        # Extra columns
        for col in extra:
            sheet.write(row, 0, "Extra Column", formats["data"])
            sheet.write(row, 1, col, formats["data_left"])
            sheet.write(row, 2, "No", formats["mismatch"])
            sheet.write(row, 3, "Yes", formats["match"])
            sheet.write(row, 4, "WARNING", formats["status_warning"])
            sheet.write(row, 5, "New column in PowerBI", formats["data_left"])
            row += 1

        if not missing and not extra:
            sheet.write(row, 0, "All Columns", formats["data"])
            sheet.write(row, 1, "All columns present", formats["data_left"])
            sheet.write(row, 2, "Yes", formats["match"])
            sheet.write(row, 3, "Yes", formats["match"])
            sheet.write(row, 4, "PASS", formats["status_pass"])
            sheet.write(row, 5, "All columns match", formats["data_left"])
            row += 1

        # Section 2: Data Type Mismatches
        row += 2
        sheet.merge_range(row, 0, row, 5, "Data Type Validation", formats["sub_header"])
        row += 1

        headers = ["Column Name", "Cognos Type", "PowerBI Type", "", "Status", "Remarks"]
        for col_idx, header in enumerate(headers):
            sheet.write(row, col_idx, header, formats["header"])
        row += 1

        if type_mismatches:
            for col_name, cognos_type, powerbi_type in type_mismatches:
                sheet.write(row, 0, col_name, formats["data_left"])
                sheet.write(row, 1, cognos_type, formats["data"])
                sheet.write(row, 2, powerbi_type, formats["data"])
                sheet.write(row, 3, "", formats["data"])
                sheet.write(row, 4, "FAIL", formats["status_fail"])
                sheet.write(row, 5, "Data type mismatch - verify conversion", formats["data_left"])
                row += 1
        else:
            sheet.write(row, 0, "All Columns", formats["data_left"])
            sheet.write(row, 1, "Match", formats["match"])
            sheet.write(row, 2, "Match", formats["match"])
            sheet.write(row, 3, "", formats["data"])
            sheet.write(row, 4, "PASS", formats["status_pass"])
            sheet.write(row, 5, "All data types match", formats["data_left"])

    def _write_record_count_validation(
        self,
        workbook: xlsxwriter.Workbook,
        formats: dict[str, Any],
        file_result: ValidationResult,
    ) -> None:
        """Write the Record Count Validation sheet."""
        sheet = workbook.add_worksheet("Record_Count_Validation")

        # Set column widths
        sheet.set_column("A:A", 25)
        sheet.set_column("B:B", 18)
        sheet.set_column("C:C", 18)
        sheet.set_column("D:D", 15)
        sheet.set_column("E:E", 35)

        details = file_result.details

        # Headers
        headers = ["Metric", "Cognos Count", "Power BI Count", "Status", "Remarks"]
        for col_idx, header in enumerate(headers):
            sheet.write(0, col_idx, header, formats["header"])

        # Row count
        row_match = details["row_match"]
        sheet.write(1, 0, "Total Row Count", formats["data_left"])
        sheet.write(1, 1, details["row_count_1"], formats["integer"])
        sheet.write(1, 2, details["row_count_2"], formats["integer"])
        sheet.write(
            1, 3, "Match" if row_match else "Mismatch",
            formats["status_pass"] if row_match else formats["status_fail"]
        )
        diff = details["row_count_2"] - details["row_count_1"]
        remark = "Row counts match" if row_match else f"Difference: {diff:+d} rows"
        sheet.write(1, 4, remark, formats["data_left"])

        # Column count
        col_match = details["column_match"]
        sheet.write(2, 0, "Total Column Count", formats["data_left"])
        sheet.write(2, 1, details["column_count_1"], formats["integer"])
        sheet.write(2, 2, details["column_count_2"], formats["integer"])
        sheet.write(
            2, 3, "Match" if col_match else "Mismatch",
            formats["status_pass"] if col_match else formats["status_fail"]
        )
        diff = details["column_count_2"] - details["column_count_1"]
        remark = "Column counts match" if col_match else f"Difference: {diff:+d} columns"
        sheet.write(2, 4, remark, formats["data_left"])

    def _write_row_differences(
        self,
        workbook: xlsxwriter.Workbook,
        formats: dict[str, Any],
        row_result: ValidationResult,
    ) -> None:
        """Write the Row Level Differences sheet."""
        sheet = workbook.add_worksheet("Row_Level_Differences")

        # Set column widths
        sheet.set_column("A:A", 12)
        sheet.set_column("B:B", 25)
        sheet.set_column("C:C", 30)
        sheet.set_column("D:D", 30)

        details = row_result.details

        if details.get("skipped"):
            sheet.write(0, 0, "Row-level comparison was skipped", formats["field_label"])
            sheet.write(1, 0, row_result.summary, formats["data_left"])
            return

        differences = details.get("differences", [])
        total = details.get("total_differences", 0)

        # Summary
        sheet.merge_range(
            "A1:D1",
            f"ROW-LEVEL DIFFERENCES: {total} total mismatches found",
            formats["title"] if total == 0 else formats["status_fail"]
        )
        sheet.set_row(0, 25)

        # Headers
        headers = ["Row Number", "Column Name", "Cognos Value", "PowerBI Value"]
        for col_idx, header in enumerate(headers):
            sheet.write(1, col_idx, header, formats["header"])

        if not differences:
            sheet.write(2, 0, "No differences found - perfect match!", formats["match"])
            return

        # Write differences (limit to 500 for performance)
        for row_idx, (row_num, col_name, val1, val2) in enumerate(differences[:500], start=2):
            fmt = formats["row_alt"] if row_idx % 2 == 0 else formats["data"]
            fmt_left = formats["row_alt_left"] if row_idx % 2 == 0 else formats["data_left"]

            sheet.write(row_idx, 0, row_num, fmt)
            sheet.write(row_idx, 1, col_name, fmt_left)
            sheet.write(row_idx, 2, str(val1) if val1 is not None else "", fmt_left)
            sheet.write(row_idx, 3, str(val2) if val2 is not None else "", fmt_left)

        if len(differences) > 500:
            row = len(differences[:500]) + 3
            sheet.write(
                row, 0,
                f"Note: Showing first 500 of {total} differences",
                formats["field_label"]
            )

    def _write_known_limitations(
        self,
        workbook: xlsxwriter.Workbook,
        formats: dict[str, Any],
        results: list[ValidationResult],
    ) -> None:
        """Write the Known Limitations & Assumptions sheet."""
        sheet = workbook.add_worksheet("Known_Limitations")

        # Set column widths
        sheet.set_column("A:A", 15)
        sheet.set_column("B:B", 50)
        sheet.set_column("C:C", 30)
        sheet.set_column("D:D", 12)

        # Headers
        headers = ["Limitation ID", "Description", "Reason", "Impact"]
        for col_idx, header in enumerate(headers):
            sheet.write(0, col_idx, header, formats["header"])

        # Standard limitations
        limitations = [
            ("LIM-01", "Minor rounding differences in decimal values", "Floating-point precision", "Low"),
            ("LIM-02", "Row comparison limited to first 10,000 rows", "Performance optimization", "Low"),
            ("LIM-03", "Column order may differ between systems", "Tool behavior", "None"),
            ("LIM-04", "NULL vs empty string treated as equivalent", "Data normalization", "Low"),
        ]

        for row_idx, (lim_id, desc, reason, impact) in enumerate(limitations, start=1):
            fmt = formats["row_alt"] if row_idx % 2 == 0 else formats["data"]
            fmt_left = formats["row_alt_left"] if row_idx % 2 == 0 else formats["data_left"]

            sheet.write(row_idx, 0, lim_id, fmt)
            sheet.write(row_idx, 1, desc, fmt_left)
            sheet.write(row_idx, 2, reason, fmt_left)
            sheet.write(row_idx, 3, impact, fmt)

    def generate_report(
        self,
        df_cognos: pd.DataFrame,
        df_powerbi: pd.DataFrame,
        results: list[ValidationResult],
        overall_status: ValidationStatus,
    ) -> BytesIO:
        """Generate the complete Excel validation report.

        Args:
            df_cognos: Source DataFrame (Cognos)
            df_powerbi: Target DataFrame (PowerBI)
            results: List of ValidationResult objects
            overall_status: Overall validation status

        Returns:
            BytesIO buffer containing the Excel file
        """
        output = BytesIO()
        workbook = xlsxwriter.Workbook(output, {"in_memory": True})
        formats = self._create_formats(workbook)

        # Find specific results
        file_result = next((r for r in results if r.name == "File Validation"), None)
        schema_result = next((r for r in results if r.name == "Schema Validation"), None)
        stats_result = next((r for r in results if r.name == "Column Statistics"), None)
        row_result = next((r for r in results if r.name == "Row-Level Differences"), None)

        # Write all sheets
        self._write_validation_overview(workbook, formats, results, overall_status)
        self._write_data_sheet(workbook, formats, df_cognos, "Cognos_Data")
        self._write_data_sheet(workbook, formats, df_powerbi, "PowerBI_Data")

        if stats_result:
            self._write_metric_comparison(workbook, formats, stats_result)

        if schema_result:
            self._write_schema_validation(workbook, formats, schema_result)

        if file_result:
            self._write_record_count_validation(workbook, formats, file_result)

        if row_result:
            self._write_row_differences(workbook, formats, row_result)

        self._write_known_limitations(workbook, formats, results)

        workbook.close()
        output.seek(0)
        return output
