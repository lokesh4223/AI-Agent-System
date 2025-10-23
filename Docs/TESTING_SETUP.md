# Testing Setup Guide

## Overview

This document provides instructions for setting up and running tests for the AI Agent System.

## Prerequisites

Before running tests, ensure you have:

1. **Python 3.8 or higher** installed
2. **Virtual environment** set up
3. **Development dependencies** installed

## Installation

### 1. Create and Activate Virtual Environment

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate

# On macOS/Linux:
source venv/bin/activate
```

### 2. Install Development Dependencies

```bash
pip install -r requirements-dev.txt
```

This will install:
- Core application dependencies
- Testing frameworks (pytest, selenium)
- Code quality tools (flake8, black)
- Security scanning tools (bandit, safety)

## Test Structure

The tests are organized in the following structure:

```
tests/
├── __init__.py
├── conftest.py
├── unit/
│   ├── test_user_controller.py
│   ├── test_course_controller.py
│   └── test_database.py
├── integration/
│   ├── test_auth_flow.py
│   └── test_course_enrollment.py
├── functional/
│   └── test_user_journeys.py
└── security/
    └── test_vulnerabilities.py
```

## Running Tests

### 1. Run All Tests

```bash
# Run all tests
python -m pytest

# Run all tests with verbose output
python -m pytest -v
```

### 2. Run Specific Test Categories

```bash
# Run unit tests only
python -m pytest tests/unit/

# Run integration tests only
python -m pytest tests/integration/

# Run functional tests only
python -m pytest tests/functional/
```

### 3. Run Specific Test Files

```bash
# Run a specific test file
python -m pytest tests/unit/test_user_controller.py

# Run a specific test class
python -m pytest tests/unit/test_user_controller.py::TestUserController

# Run a specific test method
python -m pytest tests/unit/test_user_controller.py::TestUserController::test_signup_user_success
```

### 4. Run Tests with Coverage

```bash
# Run tests with coverage report
python -m pytest --cov=.

# Run tests with HTML coverage report
python -m pytest --cov=. --cov-report=html

# Run tests with coverage requirements
python -m pytest --cov=. --cov-fail-under=80
```

## Test Configuration

### pytest.ini

The [pytest.ini](file:///d:/project%202/A_I-Agent-master/pytest.ini) file contains the pytest configuration:

```ini
[tool:pytest]
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
addopts = -v --tb=short
```

### conftest.py

The [conftest.py](file:///d:/project%202/A_I-Agent-master/tests/conftest.py) file contains shared fixtures and configuration:

```python
import sys
from pathlib import Path

# Add the project root to the path so we can import our modules
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))
```

## Writing Tests

### Test Structure

Tests should follow this structure:

```python
import pytest
from unittest.mock import Mock, patch

def test_example_function():
    """Test description"""
    # Arrange
    # Set up test data and mocks
    
    # Act
    # Call the function being tested
    
    # Assert
    # Verify the results
```

### Using Mocks

```python
def test_database_operation(mocker):
    """Test database operation with mocking"""
    # Mock database connection
    mock_db = Mock()
    mock_collection = Mock()
    mock_collection.find_documents.return_value = [{'name': 'John'}]
    
    # Patch the database functions
    mocker.patch('utils.database.get_db_connection', return_value=mock_db)
    mocker.patch('utils.database.get_collection', return_value=mock_collection)
    
    # Test the function
    result = some_function_that_uses_database()
    
    # Verify the results
    assert result == expected_result
```

## Continuous Integration

The project includes GitHub Actions configuration for continuous integration:

```yaml
name: CI Tests
on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v2
    - name: Set up Python
      uses: actions/setup-python@v2
      with:
        python-version: 3.9
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements-dev.txt
    - name: Run tests
      run: python -m pytest
    - name: Security scan
      run: |
        pip install bandit safety
        bandit -r .
        safety check
```

## Best Practices

### 1. Test Organization

- **Unit Tests**: Test individual functions in isolation
- **Integration Tests**: Test interactions between components
- **Functional Tests**: Test complete user workflows
- **Security Tests**: Test for vulnerabilities

### 2. Test Naming

- Use descriptive test names
- Follow the pattern: `test_action_being_tested_expected_result`
- Example: `test_signup_user_with_valid_data_creates_account`

### 3. Test Data

- Use fixtures for reusable test data
- Keep test data minimal and focused
- Use factories for complex test data

### 4. Mocking

- Mock external dependencies
- Use real implementations when possible
- Verify mock calls to ensure correct interactions

## Troubleshooting

### Common Issues

#### 1. Import Errors
```
ModuleNotFoundError: No module named 'pytest'
```
**Solution:** Install development dependencies:
```bash
pip install -r requirements-dev.txt
```

#### 2. Database Connection Errors
```
ConnectionError: Could not connect to test database
```
**Solution:** Ensure MongoDB is running or mock database operations

#### 3. Missing Environment Variables
```
KeyError: 'MONGO_URI'
```
**Solution:** Set required environment variables or mock them in tests

### Debugging Tests

```bash
# Run tests with detailed output
python -m pytest -v -s

# Run tests with debug logging
python -m pytest --log-cli-level=DEBUG

# Run a single test with pdb debugger
python -m pytest -v --pdb test_file.py::test_function
```

## Test Coverage

### Viewing Coverage Reports

```bash
# Generate HTML coverage report
python -m pytest --cov=. --cov-report=html

# Open the report
# On macOS/Linux:
open htmlcov/index.html

# On Windows:
start htmlcov/index.html
```

### Coverage Requirements

The project aims for:
- **Unit Tests**: 90% coverage
- **Integration Tests**: 80% coverage
- **Overall**: 85% coverage

## Security Testing

### Running Security Scans

```bash
# Run bandit security linting
bandit -r .

# Check for vulnerable dependencies
safety check

# Run all security tests
python -m pytest tests/security/
```

## Performance Testing

### Running Load Tests

```bash
# Run locust load tests
locust -f tests/performance/locustfile.py
```

## Conclusion

This testing setup provides a comprehensive framework for ensuring code quality, security, and performance. Regular execution of tests helps maintain a stable and reliable application.