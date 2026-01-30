# DataSure - Data Validation Platform

Professional CSV validation tool for BI migration projects.

## Features

- **File-level validation**: Compare row and column counts
- **Schema validation**: Detect missing columns, extra columns, and data type mismatches
- **Column statistics**: Compare null counts, min/max values, sums, and unique counts
- **Row-level comparison**: Identify specific data differences
- **Encoding support**: Automatically handles multiple CSV encodings (UTF-8, Latin-1, CP1252, etc.)

## Installation

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install package in editable mode
pip install -e .
```

## Usage

```bash
streamlit run app.py
```

## Running Tests

```bash
# Run all tests
pytest

# Run with verbose output
pytest -v

# Run specific test file
pytest tests/test_validators.py
```

## Code Quality

```bash
# Type checking
mypy .

# Linting
ruff check .

# Auto-fix linting issues
ruff check --fix .
```

## Project Structure

```
.
├── app.py                      # Main Streamlit application
├── models/
│   └── result.py              # Validation result structures
├── validators/
│   ├── file_checks.py         # File-level validation
│   ├── schema_checks.py       # Schema validation
│   ├── stats_checks.py        # Column statistics
│   └── row_checks.py          # Row-level comparison
├── utils/
│   ├── loader.py              # CSV loading with encoding support
│   └── helpers.py             # Utility functions
├── tests/
│   └── test_validators.py    # Unit tests
└── sample_data/               # Sample CSV files
```

## License

Internal use only.


