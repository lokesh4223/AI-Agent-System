# AI Agent System - Python Flask Implementation

This project is a complete conversion of a PHP-based web application to Python using the Flask framework. All the functionality from the original PHP implementation has been preserved while following Python best practices and modern coding style.

## Table of Contents

- [Project Overview](#project-overview)
- [Key Features](#key-features)
- [Technology Stack](#technology-stack)
- [Project Structure](#project-structure)
- [Installation and Setup](#installation-and-setup)
- [Configuration](#configuration)
- [Running the Application](#running-the-application)
- [API Endpoints](#api-endpoints)
- [Database Schema](#database-schema)
- [Testing](#testing)
- [Deployment](#deployment)
- [Security Considerations](#security-considerations)
- [Contributing](#contributing)
- [License](#license)

## Project Overview

The AI Agent System is a comprehensive web application that provides users with access to various AI-powered agents for automating tasks, learning new skills, and enhancing productivity. The system features a complete user authentication system, course enrollment functionality, and a marketplace of specialized AI agents.

## Key Features

1. **User Authentication System**
   - User registration with email verification
   - Secure login with password hashing
   - Password recovery system
   - Session management

2. **AI Agent Marketplace**
   - Browse specialized AI agents
   - Course Automation Agent
   - Task Assistant Agent
   - Writing Assistant Agent
   - Data Analysis Agent
   - Customer Support Agent
   - Code Assistant Agent

3. **Course Enrollment System**
   - Personalized learning schedules
   - Notification preferences
   - Duration and pace configuration
   - Progress tracking

4. **User Profile Management**
   - Account information dashboard
   - Enrollment status tracking
   - Activity history

## Technology Stack

- **Backend**: Python 3.8+, Flask 2.3.3
- **Frontend**: HTML5, CSS3, JavaScript, Bootstrap 5
- **Database**: MongoDB 4.4+
- **Email Service**: Brevo (formerly Sendinblue)
- **Security**: Flask-WTF, Werkzeug, python-dotenv
- **Development Tools**: Virtual environment, Git

## Project Structure

```
A_I-Agent-master/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── .env                   # Environment configuration
├── .gitignore             # Git ignore patterns
├── LICENSE                # License information
├── README.md              # Project documentation
├── MONGODB_SCHEMA.md      # Database schema documentation
├── SCHEDULE_DATA_STORAGE.md # Schedule data storage documentation
├── cleanup_test_data.py   # Test data cleanup utility
├── test_schedule_storage.py # Schedule storage tests
├── view_schedule_data.py  # Schedule data viewer
├── static/                # Static files (CSS, JS, images)
│   ├── SignUp_LogIn_Form.css
│   ├── SignUp_LogIn_Form.js
│   └── images/            # Image assets
├── templates/             # HTML templates
│   ├── course-agent-success.html
│   ├── course-agent.html
│   ├── home.html
│   ├── index.html
│   ├── login_signup.html
│   ├── profile.html
│   └── schedule.html
├── utils/                 # Utility modules
│   ├── __init__.py
│   ├── course_controller.py
│   ├── database.py
│   ├── env_loader.py
│   ├── mail.py
│   └── user_controller.py
└── Docs/                  # Documentation folder
    ├── PROJECT_OVERVIEW.md
    ├── ARCHITECTURE.md
    ├── API_SPECS.md
    ├── SETUP_GUIDE.md
    ├── SECURITY_GUIDELINES.md
    ├── CONTRIBUTING.md
    ├── ROADMAP.md
    ├── DEPLOYMENT.md
    ├── FRONTEND_BACKEND_SUMMARY.md
    └── TESTING_STRATEGY.md
```

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

## Configuration

Create a `.env` file in the project root with the following configuration:

```env
# Database Configuration (MongoDB)
DB_HOST=localhost
DB_PORT=27017
DB_NAME=ai_agent_system
DB_USER=
DB_PASSWORD=
MONGO_URI=mongodb://localhost:27017/ai_agent_system

# Email Configuration
SENDER_EMAIL=your-email@example.com
SENDER_NAME=Your Name
BREVO_API_KEY=your-brevo-api-key

# Flask Configuration
SECRET_KEY=your-secret-key-here
JWT_SECRET=your-jwt-secret
PORT=5000
```

## Running the Application

1. **Start MongoDB** (if running locally)

2. **Run the Flask application**:
   ```bash
   python app.py
   ```

3. **Access the application**:
   - Open your browser and go to http://localhost:5000

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Main landing page |
| `/signup-user` | GET/POST | User registration |
| `/login-user` | GET/POST | User login |
| `/user-otp` | GET/POST | Email verification |
| `/forgot-password` | GET/POST | Password recovery initiation |
| `/reset-code` | GET/POST | Password reset code verification |
| `/new-password` | GET/POST | New password creation |
| `/password-changed` | GET/POST | Password change confirmation |
| `/home` | GET | User dashboard |
| `/profile` | GET | User profile |
| `/logout-user` | GET | User logout |
| `/course-agent` | GET | Course agent page |
| `/course-agent/schedule/<course_id>` | GET | Course schedule configuration |
| `/course-agent/schedule/save` | POST | Save course schedule |
| `/course-agent/success` | GET | Course enrollment success |

## Database Schema

See [MONGODB_SCHEMA.md](../MONGODB_SCHEMA.md) for detailed database schema information.

## Testing

See [TESTING_STRATEGY.md](Docs/TESTING_STRATEGY.md) for testing guidelines and procedures.

## Deployment

See [DEPLOYMENT.md](Docs/DEPLOYMENT.md) for deployment instructions and best practices.

## Security Considerations

See [SECURITY_GUIDELINES.md](Docs/SECURITY_GUIDELINES.md) for security best practices and guidelines.

## Contributing

See [CONTRIBUTING.md](Docs/CONTRIBUTING.md) for contribution guidelines.

## License

This project is licensed under the MIT License - see the [LICENSE](../LICENSE) file for details.