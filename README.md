# AI Agent System - Python Flask Conversion

This project is a complete conversion of a PHP-based web application to Python using the Flask framework. All the functionality from the original PHP implementation has been preserved while following Python best practices and modern coding style.

## Project Structure

```
A_I-Agent-master/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── .env                   # Environment configuration
├── .gitignore
├── LICENSE
├── README.md
├── MONGODB_SCHEMA.md      # Database schema documentation
├── SCHEDULE_DATA_STORAGE.md # Schedule data storage documentation
├── cleanup_test_data.py   # Test data cleanup utility
├── test_schedule_storage.py # Schedule storage tests
├── view_schedule_data.py  # Schedule data viewer
├── static/                # Static files (CSS, JS, images)
│   └── style.css
├── templates/             # HTML templates
│   ├── cert.html
│   ├── home.html
│   └── index.html
└── utils/                 # Utility modules (converted from PHP includes)
    ├── __init__.py
    ├── database.py        # Database connectivity (from connection.php)
    ├── mail.py            # Email functionality (from PHPMailer)
    ├── env_loader.py      # Environment loading (from env_loader.php)
    └── user_controller.py # User management (from controllerUserData.php)
```

## Comprehensive Documentation

Detailed documentation is available in the [Docs](Docs/) folder:

- [Project Overview](Docs/PROJECT_OVERVIEW.md) - High-level project description
- [Architecture](Docs/ARCHITECTURE.md) - System architecture and design patterns
- [API Specifications](Docs/API_SPECS.md) - REST API endpoints and usage
- [Setup Guide](Docs/SETUP_GUIDE.md) - Installation and configuration instructions
- [Security Guidelines](Docs/SECURITY_GUIDELINES.md) - Security best practices
- [Contribution Guide](Docs/CONTRIBUTING.md) - How to contribute to the project
- [Roadmap](Docs/ROADMAP.md) - Future development plans
- [Deployment](Docs/DEPLOYMENT.md) - Deployment strategies and procedures
- [Frontend & Backend Summary](Docs/FRONTEND_BACKEND_SUMMARY.md) - Technical implementation details
- [Testing Strategy](Docs/TESTING_STRATEGY.md) - Testing approaches and methodologies

## Key Features Converted

1. **User Authentication System**
   - User signup with email verification
   - Secure login with password hashing
   - Password recovery system
   - Session management

2. **Email Services**
   - OTP generation and email sending
   - Password reset functionality
   - Beautiful email templates

3. **Database Integration**
   - MongoDB connectivity using PyMongo
   - Secure query execution
   - User data management

4. **Security Features**
   - CSRF protection
   - Password hashing with Werkzeug
   - Environment-based configuration

5. **Localization**
   - Pricing displayed in Indian Rupees (₹) instead of US Dollars ($)

## Python vs PHP Implementation

| PHP Component | Python Equivalent | Description |
|---------------|-------------------|-------------|
| index.php | app.py | Main application entry point |
| connection.php | utils/database.py | Database connectivity |
| config.php | Environment variables | Configuration management |
| env_loader.php | utils/env_loader.py | Environment variable loading |
| controllerUserData.php | utils/user_controller.py | User management logic |
| PHPMailer | utils/mail.py | Email sending functionality |

## Installation and Setup

1. **Install Python** (if not already installed):
   - Download from https://www.python.org/downloads/
   - Make sure to check "Add Python to PATH" during installation

2. **Create a virtual environment**:
   ```bash
   python -m venv venv
   ```

3. **Activate the virtual environment**:
   - On Windows:
     ```bash
     venv\Scripts\activate
     ```
   - On macOS/Linux:
     ```bash
     source venv/bin/activate
     ```

4. **Install required packages**:
   ```bash
   pip install -r requirements.txt
   ```

5. **Configure environment variables**:
   - Update the [.env](file:///d:/project%202/A_I-Agent-master/.env) file with your database credentials and email settings
   - Change the SECRET_KEY to a secure random value

6. **Set up MongoDB**:
   - Install MongoDB locally or use a cloud MongoDB service
   - Update the database configuration in the [.env](file:///d:/project%202/A_I-Agent-master/.env) file:
     ```
     MONGO_URI=mongodb://localhost:27017/ai_agent_system
     DB_NAME=ai_agent_system
     DB_USER=
     DB_PASSWORD=
     ```

7. **Run the application**:
   ```bash
   python app.py
   ```

8. **Access the application**:
   - Open your browser and go to http://localhost:5000

## Key Improvements in Python Version

1. **Structured Code Organization**:
   - Modular design with utility modules
   - Clear separation of concerns
   - Better code maintainability

2. **Enhanced Security**:
   - Proper password hashing with Werkzeug
   - CSRF protection with Flask-WTF
   - Environment variables for sensitive data

3. **Modern Python Practices**:
   - Type hints for better code clarity
   - Context managers for resource handling
   - Error handling with try/except blocks

4. **Improved Error Handling**:
   - Comprehensive error handling throughout the application
   - User-friendly error messages
   - Graceful degradation on failures

5. **Localization**:
   - Pricing converted from USD to INR for Indian market

## API Endpoints

- `/` - Main landing page
- `/signup-user` - User registration
- `/login-user` - User login
- `/user-otp` - Email verification
- `/forgot-password` - Password recovery initiation
- `/reset-code` - Password reset code verification
- `/new-password` - New password creation
- `/password-changed` - Password change confirmation
- `/home` - User dashboard
- `/logout-user` - User logout

## Environment Variables

The application uses the following environment variables:

- `MONGO_URI` - MongoDB connection string (default: mongodb://localhost:27017/ai_agent_system)
- `DB_NAME` - Database name (default: ai_agent_system)
- `DB_USER` - Database username (if authentication is enabled)
- `DB_PASSWORD` - Database password (if authentication is enabled)
- `SENDER_EMAIL` - Email address for sending emails (lokeshmannuru2000@gmail.com)
- `SENDER_NAME` - Name to appear as the sender of emails (Lokesh Mannuru)
- `BREVO_API_KEY` - API key for Brevo email service
- `SECRET_KEY` - Flask secret key for session encryption
- `JWT_SECRET` - Secret key for JWT tokens (joblocalsecretkey)
- `PORT` - Port to run the application on (default: 5000)

## Dependencies

All dependencies are listed in [requirements.txt](file:///d:/project%202/A_I-Agent-master/requirements.txt):
- Flask - Web framework
- Flask-WTF - CSRF protection
- PyMongo - MongoDB database connector
- python-dotenv - Environment variable management
- Werkzeug - Password hashing and security utilities

## Troubleshooting

1. **Python not found**: Make sure Python is installed and added to your PATH
2. **Import errors**: Ensure all dependencies are installed with `pip install -r requirements.txt`
3. **Database connection issues**: Verify MongoDB is running and credentials in the [.env](file:///d:/project%202/A_I-Agent-master/.env) file
4. **Email sending failures**: Check email configuration in the [.env](file:///d:/project%202/A_I-Agent-master/.env) file

## License

This project is licensed under the MIT License - see the [LICENSE](file:///d:/project%202/A_I-Agent-master/LICENSE) file for details.