# Lab 05: Debugging, Data & Organization - Gemini Mandates

This document outlines the foundational mandates and standards for Lab 05. These instructions take absolute precedence over general workflows.

## 1. Core Mandates
- **Educational Integrity:** When fixing bugs in the `code/` directory, provide clear, concise explanations of the root cause and the logic behind the fix.
- **Data Privacy:** Never expose or log full student names or IDs from `data/student_grades.csv`. Use aggregate metrics or anonymized identifiers if needed.
- **Surgical Organization:** When organizing the `messy/` folder, prioritize clear, descriptive naming and logical categorization (e.g., by date or file type).

## 2. Project Structure
- `code/`: Contains Python scripts for algorithmic exercises and utility tools.
- `data/`: CSV and other data files for analysis.
- `messy/`: Sandbox for file management and organization tasks.
- `papers/`: Research papers and documentation for summarization tasks.

## 3. Coding Standards
- **Language:** Use Python for all logic and scripting.
- **Documentation:** Ensure all functions have docstrings explaining their parameters and return values.
- **Error Handling:** Use explicit exception handling (e.g., `ValueError` for invalid inputs) as seen in `calculator.py`.

## 4. Maintenance of the `messy/` folder
- **Cleanup Strategy:** When asked to clean up this folder, propose a renaming and folder structure scheme before execution.
- **Preservation:** Do not delete files in `messy/` unless explicitly instructed; prefer moving them to an `archive/` or `deprecated/` sub-folder.

## 5. Testing & Validation
- **Unit Tests:** Always create a corresponding `test_*.py` file in the `code/` folder when fixing bugs in `buggy_sort.py` or expanding `calculator.py`.
- **Validation:** Use `pytest` for running and validating tests if the framework is present; otherwise, use the `unittest` library.
