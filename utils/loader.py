"""CSV loading utilities with proper error handling."""

from typing import Any

import pandas as pd


class CSVLoadError(Exception):
    """Raised when CSV cannot be loaded."""

    pass


def load_csv(file_path: Any, file_name: str) -> pd.DataFrame:
    """
    Load CSV file with robust error handling and encoding detection.

    Args:
        file_path: Path to CSV file or file-like object (string path or UploadedFile)
        file_name: Human-readable file name for error messages

    Returns:
        pandas DataFrame

    Raises:
        CSVLoadError: If file cannot be loaded
    """
    try:
        # Try multiple encodings for CSV files
        encodings = ['utf-8', 'latin-1', 'cp1252', 'iso-8859-1', 'utf-16']

        for encoding in encodings:
            try:
                # Reset file pointer if possible
                if hasattr(file_path, 'seek'):
                    file_path.seek(0)

                df = pd.read_csv(file_path, low_memory=False, encoding=encoding)
                break  # Success, exit loop
            except (UnicodeDecodeError, UnicodeError):
                continue
        else:
            # All encodings failed
            raise CSVLoadError(
                f"{file_name} has encoding issues. Tried: {', '.join(encodings)}"
            )

        if df.empty:
            raise CSVLoadError(f"{file_name} is empty")
        return df
    except CSVLoadError:
        raise
    except pd.errors.EmptyDataError as e:
        raise CSVLoadError(f"{file_name} is empty or has no data") from e
    except Exception as e:
        raise CSVLoadError(f"Failed to load {file_name}: {str(e)}") from e


