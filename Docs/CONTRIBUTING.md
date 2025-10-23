# Contributing to AI Agent System

Thank you for your interest in contributing to the AI Agent System! This document provides guidelines and best practices for contributing to the project.

## Code of Conduct

By participating in this project, you are expected to uphold our Code of Conduct. Please report unacceptable behavior to the project maintainers.

## How to Contribute

### 1. Reporting Bugs

Before submitting a bug report, please check if the issue has already been reported.

**To report a bug:**
1. Check the [issue tracker](../../issues) for existing reports
2. Create a new issue if one doesn't exist
3. Include the following information:
   - Clear and descriptive title
   - Steps to reproduce the issue
   - Expected vs. actual behavior
   - Screenshots if applicable
   - Environment details (OS, Python version, etc.)

### 2. Suggesting Enhancements

Feature requests and enhancements are welcome! When suggesting an enhancement:

1. Check the [issue tracker](../../issues) for existing suggestions
2. Create a new issue with:
   - Clear and descriptive title
   - Detailed description of the proposed feature
   - Use cases and benefits
   - Potential implementation approach (if known)

### 3. Code Contributions

#### Getting Started

1. Fork the repository
2. Clone your fork:
   ```bash
   git clone https://github.com/your-username/A_I-Agent-master.git
   ```
3. Create a new branch for your feature or bugfix:
   ```bash
   git checkout -b feature/your-feature-name
   ```

#### Development Setup

1. Follow the [Setup Guide](SETUP_GUIDE.md) to configure your development environment
2. Install development dependencies:
   ```bash
   pip install -r requirements-dev.txt
   ```

#### Coding Standards

##### Python Code Style
- Follow [PEP 8](https://pep8.org/) style guide
- Use 4 spaces for indentation (no tabs)
- Limit lines to 88 characters (Black default)
- Use descriptive variable and function names
- Include docstrings for all functions and classes

##### Example:
```python
def calculate_user_progress(user_id: str) -> float:
    """
    Calculate the progress percentage for a user's course.
    
    Args:
        user_id (str): The unique identifier for the user
        
    Returns:
        float: Progress percentage (0.0 to 100.0)
        
    Raises:
        ValueError: If user_id is invalid
    """
    if not user_id:
        raise ValueError("user_id cannot be empty")
    
    # Implementation here
    pass
```

##### HTML/CSS/JavaScript Standards
- Use semantic HTML elements
- Follow Bootstrap 5 best practices
- Maintain consistent class naming conventions
- Comment complex JavaScript logic

#### Testing

##### Unit Tests
- Write unit tests for new functionality
- Place tests in the appropriate test files
- Use pytest for test execution
- Ensure all tests pass before submitting

##### Test Coverage
- Aim for >80% test coverage for new code
- Test both success and failure cases
- Mock external dependencies

##### Running Tests
```bash
# Run all tests
python -m pytest

# Run specific test file
python -m pytest tests/test_user_controller.py

# Run with coverage
python -m pytest --cov=utils
```

#### Documentation

##### Code Documentation
- Update docstrings when modifying functions
- Add comments for complex logic
- Maintain type hints

##### User Documentation
- Update relevant documentation files
- Add new documentation for new features
- Keep README and other docs up to date

#### Commit Messages

Follow the [Conventional Commits](https://www.conventionalcommits.org/) specification:

```
type(scope): description

body (optional)

footer (optional)
```

##### Commit Types
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting, etc.)
- `refactor`: Code refactoring
- `test`: Adding or modifying tests
- `chore`: Maintenance tasks

##### Examples:
```
feat(auth): add two-factor authentication

Implement TOTP-based two-factor authentication for user accounts.
Adds new endpoints for 2FA setup and verification.

fix(database): resolve connection timeout issue

Fix intermittent connection timeouts when connecting to MongoDB.
Improves error handling and retry logic.
```

#### Pull Request Process

1. Ensure your code follows the coding standards
2. Write clear, descriptive commit messages
3. Include tests for new functionality
4. Update documentation as needed
5. Verify all tests pass
6. Submit a pull request with:
   - Clear title and description
   - Reference to related issues
   - Summary of changes

#### Pull Request Review Process

1. Automated checks (CI) must pass
2. Code review by maintainers
3. Address feedback from reviewers
4. Approval from maintainers
5. Merge by maintainers

### 4. Documentation Contributions

#### Improving Documentation
- Fix typos and grammatical errors
- Clarify confusing sections
- Add missing information
- Update outdated content

#### Adding New Documentation
- Follow the existing documentation structure
- Use clear, concise language
- Include examples where appropriate
- Maintain consistent formatting

## Development Workflow

### Branching Strategy

- `main`: Production-ready code
- `develop`: Development branch
- `feature/*`: Feature branches
- `bugfix/*`: Bug fix branches
- `release/*`: Release preparation branches

### Versioning

We follow [Semantic Versioning](https://semver.org/):
- MAJOR version for incompatible API changes
- MINOR version for backward-compatible functionality
- PATCH version for backward-compatible bug fixes

### Release Process

1. Create release branch from `develop`
2. Update version numbers
3. Final testing
4. Merge to `main`
5. Create GitHub release
6. Deploy to production

## Community

### Communication Channels

- **GitHub Issues**: Bug reports and feature requests
- **GitHub Discussions**: General discussion and questions
- **Email**: Direct communication with maintainers

### Getting Help

If you need help with your contribution:
1. Check the documentation
2. Search existing issues
3. Ask in GitHub Discussions
4. Contact maintainers directly

## Recognition

Contributors will be recognized in:
- Release notes
- Contributor list
- Project documentation

Thank you for helping make the AI Agent System better!