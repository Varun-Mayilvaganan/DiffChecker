"""FastAPI backend for DataSure validation platform."""

import sys
from datetime import datetime
from io import BytesIO
from pathlib import Path
from typing import Any

from fastapi import FastAPI, File, Form, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
import pandas as pd

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from models.result import ValidationResult, ValidationStatus, compute_overall_status
from utils.excel_export import ExcelReportGenerator
from validation.file_checks import validate_file_level
from validation.row_checks import validate_row_level
from validation.schema_checks import validate_schema
from validation.stats_checks import validate_column_stats

app = FastAPI(
    title="DataSure API",
    description="Data validation API for BI migration projects",
    version="1.0.0",
)

# CORS configuration for React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def result_to_dict(result: ValidationResult) -> dict[str, Any]:
    """Convert ValidationResult to dictionary for JSON response."""
    return {
        "name": result.name,
        "status": result.status.value,
        "summary": result.summary,
        "details": result.details,
    }


@app.get("/")
async def root() -> dict[str, str]:
    """Health check endpoint."""
    return {"status": "healthy", "service": "DataSure API"}


@app.post("/api/validate")
async def validate_files(
    cognos_file: UploadFile = File(...),
    powerbi_file: UploadFile = File(...),
    project_name: str = Form(""),
    report_name: str = Form(""),
    environment: str = Form("UAT"),
) -> dict[str, Any]:
    """Validate two CSV files and return comparison results."""
    try:
        # Read CSV files
        cognos_content = await cognos_file.read()
        powerbi_content = await powerbi_file.read()

        df_cognos = pd.read_csv(BytesIO(cognos_content))
        df_powerbi = pd.read_csv(BytesIO(powerbi_content))

        # Run all validators
        results: list[ValidationResult] = [
            validate_file_level(df_cognos, df_powerbi),
            validate_schema(df_cognos, df_powerbi),
            validate_column_stats(df_cognos, df_powerbi),
            validate_row_level(df_cognos, df_powerbi),
        ]

        # Compute overall status
        overall_status = compute_overall_status(results)

        # Prepare response
        return {
            "success": True,
            "overall_status": overall_status.value,
            "validation_date": datetime.now().isoformat(),
            "project_name": project_name or "DataSure Validation",
            "report_name": report_name or "Data Validation Report",
            "environment": environment,
            "cognos_file": cognos_file.filename,
            "powerbi_file": powerbi_file.filename,
            "cognos_shape": {"rows": len(df_cognos), "columns": len(df_cognos.columns)},
            "powerbi_shape": {"rows": len(df_powerbi), "columns": len(df_powerbi.columns)},
            "results": [result_to_dict(r) for r in results],
        }

    except pd.errors.EmptyDataError:
        raise HTTPException(status_code=400, detail="One or both CSV files are empty")
    except pd.errors.ParserError as e:
        raise HTTPException(status_code=400, detail=f"CSV parsing error: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Validation error: {str(e)}")


@app.post("/api/export-excel")
async def export_excel(
    cognos_file: UploadFile = File(...),
    powerbi_file: UploadFile = File(...),
    project_name: str = Form(""),
    report_name: str = Form(""),
    environment: str = Form("UAT"),
) -> StreamingResponse:
    """Generate and download Excel validation report."""
    try:
        # Read CSV files
        cognos_content = await cognos_file.read()
        powerbi_content = await powerbi_file.read()

        df_cognos = pd.read_csv(BytesIO(cognos_content))
        df_powerbi = pd.read_csv(BytesIO(powerbi_content))

        # Run all validators
        results: list[ValidationResult] = [
            validate_file_level(df_cognos, df_powerbi),
            validate_schema(df_cognos, df_powerbi),
            validate_column_stats(df_cognos, df_powerbi),
            validate_row_level(df_cognos, df_powerbi),
        ]

        overall_status = compute_overall_status(results)

        # Generate Excel report
        generator = ExcelReportGenerator(
            report_name=report_name or "Data Validation Report",
            project_name=project_name or "DataSure Validation",
            environment=environment,
            cognos_report_name=cognos_file.filename or "Cognos_Export",
            powerbi_report_name=powerbi_file.filename or "PowerBI_Export",
        )

        excel_buffer = generator.generate_report(
            df_cognos=df_cognos,
            df_powerbi=df_powerbi,
            results=results,
            overall_status=overall_status,
        )

        # Generate filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"DataSure_Validation_Report_{timestamp}.xlsx"

        return StreamingResponse(
            excel_buffer,
            media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            headers={"Content-Disposition": f"attachment; filename={filename}"},
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Export error: {str(e)}")


@app.get("/api/health")
async def health_check() -> dict[str, str]:
    """API health check."""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
