# AI Agent System - Setup Guide

## Prerequisites

Before installing the AI Agent System, ensure you have the following software installed:

1. **Python 3.8 or higher**
   - Download from [python.org](https://www.python.org/downloads/)
   - Verify installation: `python --version` or `python3 --version`

2. **MongoDB 4.4 or higher**
   - Download from [mongodb.com](https://www.mongodb.com/try/download/community)
   - Or use MongoDB Atlas for cloud hosting
   - Verify installation: `mongod --version`

3. **Git (optional but recommended)**
   - Download from [git-scm.com](https://git-scm.com/downloads)
   - Verify installation: `git --version`

## Installation Steps

### 1. Clone or Download the Repository

```bash
# Using Git
git clone <repository-url>
cd A_I-Agent-master

# Or download and extract the ZIP file
```

### 2. Create a Virtual Environment

Creating a virtual environment isolates the project dependencies:

```bash
# On Windows
python -m venv venv
venv\Scripts\activate

# On macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

Install the required Python packages:

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a `.env` file in the project root directory with the following configuration:

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

#### Configuration Details:

- **DB_HOST**: MongoDB host (default: localhost)
- **DB_PORT**: MongoDB port (default: 27017)
- **DB_NAME**: Database name (default: ai_agent_system)
- **DB_USER**: Database username (if authentication enabled)
- **DB_PASSWORD**: Database password (if authentication enabled)
- **MONGO_URI**: Complete MongoDB connection string
- **SENDER_EMAIL**: Email address for sending notifications
- **SENDER_NAME**: Name to appear as the sender
- **BREVO_API_KEY**: API key for Brevo email service
- **SECRET_KEY**: Flask secret key for session encryption
- **JWT_SECRET**: Secret key for JWT tokens
- **PORT**: Port to run the application on (default: 5000)

### 5. Set Up MongoDB

#### Local Installation

1. Start MongoDB service:
   ```bash
   # On Windows (as Administrator)
   net start MongoDB
   
   # On macOS (with Homebrew)
   brew services start mongodb-community
   
   # On Linux
   sudo systemctl start mongod
   ```

2. Connect to MongoDB shell:
   ```bash
   mongo
   ```

3. Create the database and collections:
   ```javascript
   use ai_agent_system
   db.createCollection("usertable")
   db.createCollection("course_enrollments")
   ```

4. Create indexes:
   ```javascript
   db.usertable.createIndex({ "email": 1 }, { unique: true })
   db.usertable.createIndex({ "code": 1 })
   ```

#### MongoDB Atlas (Cloud)

1. Sign up at [mongodb.com/cloud/atlas](https://www.mongodb.com/cloud/atlas)
2. Create a new cluster
3. Configure database access and network access
4. Get your connection string
5. Update the MONGO_URI in your `.env` file

### 6. Configure Email Service

The system uses Brevo (formerly Sendinblue) for email delivery:

1. Sign up at [brevo.com](https://www.brevo.com)
2. Navigate to SMTP & API > SMTP
3. Generate a new API key
4. Update the BREVO_API_KEY in your `.env` file

### 7. Generate Secret Keys

For production, generate secure secret keys:

```python
import secrets
print(secrets.token_hex(16))
```

Update the SECRET_KEY and JWT_SECRET in your `.env` file with the generated values.

## Running the Application

### Development Mode

```bash
# Activate virtual environment
# On Windows
venv\Scripts\activate

# On macOS/Linux
source venv/bin/activate

# Run the application
python app.py
```

The application will be available at `http://localhost:5000`

### Production Mode

For production deployment, use a WSGI server like Gunicorn:

```bash
# Install Gunicorn
pip install gunicorn

# Run with Gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

## Initial Setup Verification

### 1. Database Connection

Check that the application can connect to MongoDB:

1. Start the application
2. Look for the connection success message in the console:
   ```
   ✅ MongoDB connected successfully!
   ```

### 2. Test User Registration

1. Navigate to `http://localhost:5000/signup-user`
2. Fill in the registration form
3. Check that:
   - A verification email is sent (check console output)
   - User is created in the database
   - Redirect to OTP verification page works

### 3. Test User Login

1. Navigate to `http://localhost:5000/login-user`
2. Log in with the registered user
3. Check that:
   - Login is successful
   - Redirect to home page works
   - Session is created

### 4. Test Course Enrollment

1. Navigate to the course agent page
2. Select a course
3. Configure schedule
4. Check that:
   - Enrollment is saved to the database
   - Success page is displayed

## Troubleshooting

### Common Issues

#### 1. Python Import Errors
```
ModuleNotFoundError: No module named 'flask'
```
**Solution:** Ensure virtual environment is activated and dependencies are installed:
```bash
pip install -r requirements.txt
```

#### 2. Database Connection Failed
```
❌ Error connecting to MongoDB: ...
```
**Solution:** 
- Check that MongoDB is running
- Verify database configuration in `.env`
- Check network connectivity

#### 3. Email Sending Failures
```
Error sending email: ...
```
**Solution:**
- Verify BREVO_API_KEY in `.env`
- Check sender email configuration
- Ensure Brevo account is active

#### 4. Port Already in Use
```
OSError: [Errno 98] Address already in use
```
**Solution:**
- Change PORT in `.env`
- Or stop the process using the port:
  ```bash
  # On Linux/macOS
  lsof -i :5000
  kill -9 <PID>
  
  # On Windows
  netstat -ano | findstr :5000
  taskkill /PID <PID> /F
  ```

### Debugging Tips

1. **Enable Debug Mode**: Set `debug=True` in `app.run()` in [app.py](file:///d:/project%202/A_I-Agent-master/app.py)
2. **Check Logs**: Monitor console output for error messages
3. **Database Inspection**: Use MongoDB shell to inspect collections:
   ```javascript
   use ai_agent_system
   db.usertable.find().pretty()
   db.course_enrollments.find().pretty()
   ```
4. **Environment Variables**: Verify all required variables are set:
   ```bash
   # On Linux/macOS
   printenv | grep -E "(MONGO|SECRET|BREVO)"
   
   # On Windows
   echo %MONGO_URI%
   echo %SECRET_KEY%
   echo %BREVO_API_KEY%
   ```

## Development Workflow

### Code Structure

1. **Main Application**: [app.py](file:///d:/project%202/A_I-Agent-master/app.py) - Route definitions and main logic
2. **Templates**: [templates/](file:///d:/project%202/A_I-Agent-master/templates/) - HTML templates
3. **Static Files**: [static/](file:///d:/project%202/A_I-Agent-master/static/) - CSS, JavaScript, images
4. **Utilities**: [utils/](file:///d:/project%202/A_I-Agent-master/utils/) - Business logic modules

### Making Changes

1. **Frontend Changes**: Modify HTML templates in [templates/](file:///d:/project%202/A_I-Agent-master/templates/)
2. **Styling**: Update CSS in [static/](file:///d:/project%202/A_I-Agent-master/static/)
3. **Backend Logic**: Modify utility modules in [utils/](file:///d:/project%202/A_I-Agent-master/utils/)
4. **New Routes**: Add to [app.py](file:///d:/project%202/A_I-Agent-master/app.py)

### Testing Changes

1. Restart the development server after backend changes
2. Refresh the browser for frontend changes
3. Check console for error messages
4. Verify database changes if applicable

## Next Steps

After successful setup, consider:

1. **Customizing the UI**: Modify templates to match your branding
2. **Adding New Agents**: Create new course agents and templates
3. **Enhancing Security**: Implement additional security measures
4. **Performance Optimization**: Add caching and optimize queries
5. **Deployment**: Deploy to a production environment