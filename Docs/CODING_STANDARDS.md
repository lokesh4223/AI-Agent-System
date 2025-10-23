# AI Agent System - Coding Standards

## Overview

This document outlines the coding standards and best practices for the AI Agent System. Following these standards ensures code consistency, maintainability, and quality across the project.

## Python Coding Standards

### 1. Style Guide

The project follows [PEP 8](https://pep8.org/) - the official Python style guide with some additional conventions.

#### Naming Conventions

- **Variables**: `snake_case`
  ```python
  user_name = "John"
  total_count = 0
  ```

- **Functions**: `snake_case`
  ```python
  def calculate_total():
      pass
      
  def get_user_data(user_id):
      pass
  ```

- **Classes**: `PascalCase`
  ```python
  class UserController:
      pass
      
  class DatabaseConnection:
      pass
  ```

- **Constants**: `UPPER_SNAKE_CASE`
  ```python
  MAX_RETRY_ATTEMPTS = 3
  DEFAULT_TIMEOUT = 30
  ```

- **Modules**: `snake_case`
  ```python
  # user_controller.py
  # database_utils.py
  ```

#### Line Length and Formatting

- Maximum line length: 88 characters (Black default)
- Use 4 spaces for indentation (no tabs)
- Use blank lines to separate logical sections
- Use spaces around operators

```python
# Good
def calculate_sum(a, b):
    result = a + b
    return result

# Bad
def calculate_sum(a,b):
    result=a+b
    return result
```

### 2. Documentation and Comments

#### Docstrings

Use docstrings for all public modules, classes, and functions following the Google Python Style Guide:

```python
def calculate_user_progress(user_id: str, completed_tasks: int, total_tasks: int) -> float:
    """
    Calculate the progress percentage for a user's course.
    
    Args:
        user_id (str): The unique identifier for the user
        completed_tasks (int): Number of completed tasks
        total_tasks (int): Total number of tasks
        
    Returns:
        float: Progress percentage (0.0 to 100.0)
        
    Raises:
        ValueError: If user_id is invalid or total_tasks is zero
        TypeError: If parameters are not of expected types
        
    Example:
        >>> calculate_user_progress("user123", 5, 10)
        50.0
    """
    if not user_id:
        raise ValueError("user_id cannot be empty")
    
    if total_tasks == 0:
        raise ValueError("total_tasks cannot be zero")
        
    return (completed_tasks / total_tasks) * 100.0
```

#### Inline Comments

Use inline comments sparingly and only when necessary to explain complex logic:

```python
# Good - explaining complex logic
def process_data(data):
    # Apply exponential backoff for retry mechanism
    retry_delay = min(1000 * (2 ** retry_count), 30000)
    time.sleep(retry_delay / 1000.0)

# Bad - stating the obvious
def get_user_name(user):
    name = user['name']  # Get the user's name
    return name
```

### 3. Type Hints

Use type hints for function parameters and return values:

```python
from typing import List, Dict, Optional, Tuple

def get_user_courses(user_id: str) -> List[Dict[str, str]]:
    """Get all courses for a user."""
    pass

def find_user(email: str) -> Optional[Dict[str, str]]:
    """Find user by email, return None if not found."""
    pass

def process_enrollment(user_id: str, course_id: str) -> Tuple[bool, List[str]]:
    """Process course enrollment, return success status and errors."""
    pass
```

### 4. Error Handling

#### Exception Handling

- Catch specific exceptions rather than using bare `except:`
- Provide meaningful error messages
- Log errors appropriately
- Don't ignore exceptions silently

```python
# Good
try:
    user = find_user(email)
    if user is None:
        raise ValueError(f"User with email {email} not found")
except ValueError as e:
    logger.error(f"User lookup failed: {e}")
    raise
except DatabaseError as e:
    logger.error(f"Database error during user lookup: {e}")
    raise ServiceUnavailableError("Unable to access user data")

# Bad
try:
    user = find_user(email)
except:
    pass  # Silent failure
```

#### Custom Exceptions

Create custom exceptions for application-specific errors:

```python
class UserNotFoundError(Exception):
    """Raised when a user is not found in the system."""
    pass

class InvalidCredentialsError(Exception):
    """Raised when user credentials are invalid."""
    pass

class CourseEnrollmentError(Exception):
    """Raised when course enrollment fails."""
    pass
```

### 5. Code Organization

#### Imports

- Group imports in the following order:
  1. Standard library imports
  2. Third-party imports
  3. Local application imports
- Use absolute imports when possible
- Avoid wildcard imports

```python
# Good
import os
import sys
from typing import List, Dict

import flask
import pymongo
from flask import request, session

from utils.database import get_db_connection
from utils.mail import send_email

# Bad
from utils import *  # Wildcard import
import sys, os  # Multiple imports on one line
```

#### Module Structure

Organize modules with this structure:
1. Module docstring
2. Import statements
3. Constants
4. Classes
5. Functions
6. Main execution code (if applicable)

```python
"""
User management utilities for the AI Agent System.
"""

import hashlib
from typing import Dict, Optional

from flask import session
from werkzeug.security import generate_password_hash

# Constants
MIN_PASSWORD_LENGTH = 8
MAX_LOGIN_ATTEMPTS = 3

class UserManager:
    """Manages user authentication and account operations."""
    pass

def validate_email(email: str) -> bool:
    """Validate email format."""
    pass

def hash_password(password: str) -> str:
    """Hash user password."""
    pass
```

## HTML/CSS/JavaScript Standards

### 1. HTML Standards

#### Semantic Markup

Use semantic HTML elements appropriately:

```html
<!-- Good -->
<header>
    <nav>Navigation content</nav>
</header>
<main>
    <article>Article content</article>
    <aside>Related content</aside>
</main>
<footer>Footer content</footer>

<!-- Bad -->
<div class="header">
    <div class="nav">Navigation content</div>
</div>
<div class="main">
    <div class="article">Article content</div>
    <div class="sidebar">Related content</div>
</div>
<div class="footer">Footer content</div>
```

#### Accessibility

- Use proper heading hierarchy (h1, h2, h3, etc.)
- Include alt text for images
- Ensure sufficient color contrast
- Use ARIA attributes when necessary

```html
<!-- Good -->
<img src="profile.jpg" alt="Profile picture of John Doe">
<h1>Main Heading</h1>
<h2>Subsection Heading</h2>

<!-- Bad -->
<img src="profile.jpg">  <!-- Missing alt text -->
<font size="7">Main Heading</font>  <!-- Non-semantic styling -->
```

### 2. CSS Standards

#### Naming Conventions

Use BEM (Block Element Modifier) methodology:

```css
/* Good */
.user-card { }
.user-card__header { }
.user-card__title { }
.user-card--featured { }

/* Bad */
.userCard { }  /* Inconsistent naming */
.uc-header { }  /* Unclear abbreviation */
```

#### Organization

- Use consistent indentation
- Group related styles
- Use comments for complex sections
- Prefer classes over IDs for styling

```css
/* Navigation styles */
.navbar {
    background-color: #0d6efd;
}

.navbar__brand {
    font-weight: bold;
}

.navbar__link {
    color: white;
    text-decoration: none;
}

.navbar__link:hover {
    text-decoration: underline;
}

/* User profile styles */
.user-profile {
    padding: 20px;
    border-radius: 10px;
}
```

### 3. JavaScript Standards

#### Variables and Functions

- Use `const` and `let` instead of `var`
- Use arrow functions for callbacks
- Use template literals for string concatenation

```javascript
// Good
const userName = "John";
const greeting = `Hello, ${userName}!`;

const numbers = [1, 2, 3, 4, 5];
const doubled = numbers.map(num => num * 2);

// Bad
var userName = "John";
var greeting = "Hello, " + userName + "!";

var numbers = [1, 2, 3, 4, 5];
var doubled = numbers.map(function(num) {
    return num * 2;
});
```

#### Event Handling

Use modern event handling:

```javascript
// Good
document.addEventListener('DOMContentLoaded', function() {
    const button = document.getElementById('submit-btn');
    button.addEventListener('click', handleSubmit);
});

// Bad
window.onload = function() {
    document.getElementById('submit-btn').onclick = handleSubmit;
};
```

## Testing Standards

### 1. Test Naming

Use descriptive test names that follow the pattern:
`test_action_being_tested_expected_result`

```python
# Good
def test_signup_user_with_valid_data_creates_account():
    pass

def test_login_user_with_invalid_credentials_returns_error():
    pass

# Bad
def test_signup():
    pass

def test_1():
    pass
```

### 2. Test Structure

Follow the AAA pattern (Arrange, Act, Assert):

```python
def test_calculate_user_progress_with_valid_data_returns_percentage():
    """Test that calculate_user_progress returns correct percentage."""
    # Arrange
    user_id = "user123"
    completed_tasks = 5
    total_tasks = 10
    
    # Act
    result = calculate_user_progress(user_id, completed_tasks, total_tasks)
    
    # Assert
    assert result == 50.0
```

### 3. Mocking

Use mocks appropriately:

```python
def test_send_welcome_email_calls_email_service(mocker):
    """Test that send_welcome_email calls the email service."""
    # Arrange
    mock_email_service = mocker.patch('utils.mail.send_email')
    user_email = "test@example.com"
    user_name = "John Doe"
    
    # Act
    send_welcome_email(user_email, user_name)
    
    # Assert
    mock_email_service.assert_called_once_with(
        user_email,
        "Welcome to AI Agent System",
        mocker.ANY
    )
```

## Security Standards

### 1. Input Validation

Always validate and sanitize user input:

```python
import re

def validate_email(email: str) -> bool:
    """Validate email format."""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def sanitize_input(text: str) -> str:
    """Remove potentially dangerous characters."""
    # Remove HTML tags
    sanitized = re.sub(r'<[^>]*>', '', text)
    # Escape special characters
    sanitized = sanitized.replace('"', '&quot;').replace("'", '&#x27;')
    return sanitized
```

### 2. Password Security

- Use strong password hashing (Werkzeug)
- Enforce password complexity
- Implement rate limiting for authentication

```python
from werkzeug.security import generate_password_hash, check_password_hash

def hash_password(password: str) -> str:
    """Hash user password with strong algorithm."""
    return generate_password_hash(password, method='pbkdf2:sha256', salt_length=12)

def verify_password(hashed: str, password: str) -> bool:
    """Verify password against hash."""
    return check_password_hash(hashed, password)
```

### 3. Session Security

- Use secure session configuration
- Implement session timeout
- Regenerate session IDs after login

```python
from flask import session
import secrets

def create_secure_session(user_id: str):
    """Create a secure user session."""
    session['user_id'] = user_id
    session['csrf_token'] = secrets.token_hex(16)
    session.permanent = True
```

## Performance Standards

### 1. Database Queries

- Use indexes appropriately
- Limit query results when possible
- Avoid N+1 query problems

```python
# Good - Single query with projection
users = db.users.find(
    {'status': 'active'}, 
    {'name': 1, 'email': 1, '_id': 0}
).limit(100)

# Bad - Multiple queries in a loop
users = []
for user_id in user_ids:
    user = db.users.find_one({'_id': user_id})  # N queries
    users.append(user)
```

### 2. Caching

Implement caching for expensive operations:

```python
from functools import lru_cache

@lru_cache(maxsize=128)
def get_course_info(course_id: str) -> Dict:
    """Get course information with caching."""
    return db.courses.find_one({'_id': course_id})
```

## Code Review Standards

### 1. Review Checklist

When reviewing code, check for:

- [ ] Follows coding standards
- [ ] Includes appropriate tests
- [ ] Has clear documentation
- [ ] Handles errors appropriately
- [ ] Is secure against common vulnerabilities
- [ ] Is performant and efficient
- [ ] Is readable and maintainable

### 2. Review Process

1. **Self-Review**: Authors review their own code before submission
2. **Peer Review**: At least one other developer reviews the code
3. **Automated Checks**: CI pipeline runs tests and linting
4. **Security Review**: Security-sensitive changes get additional review

## Tools and Automation

### 1. Code Formatting

Use Black for automatic code formatting:

```bash
# Format all Python files
black .

# Check formatting without changes
black --check .
```

### 2. Import Sorting

Use isort for consistent import organization:

```bash
# Sort imports in all files
isort .

# Check import order without changes
isort --check-only .
```

### 3. Linting

Use flake8 for code quality checks:

```bash
# Run linting
flake8 .

# Run with specific configuration
flake8 --config=.flake8
```

### 4. Security Scanning

Use bandit for security linting:

```bash
# Run security scan
bandit -r .

# Run with specific severity level
bandit -r . -ll
```

## Conclusion

Following these coding standards helps maintain a consistent, secure, and maintainable codebase. Regular code reviews and automated tooling help enforce these standards and improve overall code quality.

Remember to:
- Keep learning and updating standards
- Adapt standards based on team feedback
- Use automation to enforce standards where possible
- Document any deviations from these standards with clear reasoning