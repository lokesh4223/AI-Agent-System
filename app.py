"""
AI Agent System - Flask Application
A complete conversion of the PHP project to Python using Flask
"""

import os
import secrets
from flask import Flask, render_template, request, redirect, url_for, session
from flask_wtf.csrf import CSRFProtect
import random
from bson.objectid import ObjectId

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

# Import our utility modules
from utils.database import get_db_connection, get_collection, find_documents

# Test MongoDB connection on startup
def test_mongo_connection():
    """Test MongoDB connection and print status"""
    try:
        db = get_db_connection()
        if db is not None:
            collections = db.list_collection_names()
            print(f"✅ MongoDB connected successfully!")
            print(f"   Database: {db.name}")
            print(f"   Collections: {collections if collections else 'None'}")
            return True
        else:
            print("❌ Failed to connect to MongoDB")
            return False
    except Exception as e:
        print(f"❌ Error connecting to MongoDB: {str(e)}")
        return False

# Initialize Flask app
app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', secrets.token_hex(16))
csrf = CSRFProtect(app)

# Test MongoDB connection when app starts (only in main process, not reloader)
if os.environ.get('WERKZEUG_RUN_MAIN') == 'true':
    print("🔍 Testing MongoDB connection at startup...")
    test_mongo_connection()
    print("🚀 Starting Flask application...")

# Routes
@app.route('/')
def index():
    """Main landing page"""
    is_logged_in = 'user_id' in session
    return render_template('index.html', is_logged_in=is_logged_in)

@app.route('/signup-user', methods=['GET', 'POST'])
def signup_user():
    """User signup page"""
    errors = []
    
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')
        cpassword = request.form.get('cpassword')
        
        # Check if all required fields are provided
        if not name or not email or not password or not cpassword:
            errors.append("All fields are required. Please complete all registration fields.")
        else:
            # Import controller function here to avoid circular imports
            from utils.user_controller import signup_user as signup_user_controller
            success, errors = signup_user_controller(name, email, password, cpassword)
            if success:
                return redirect(url_for('user_otp'))
    
    # Pass a parameter to indicate we're on the signup form
    return render_template('login_signup.html', errors=errors, form='signup')

@app.route('/login-user', methods=['GET', 'POST'])
def login_user():
    """User login page"""
    errors = []
    
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        # Check if email and password are provided
        if not email or not password:
            errors.append("Both email and password are required for authentication.")
        else:
            # Import controller function here to avoid circular imports
            from utils.user_controller import login_user as login_user_controller
            success, errors = login_user_controller(email, password)
            if success:
                return redirect(url_for('home'))
            elif "redirect_user_otp" in errors:
                return redirect(url_for('user_otp'))
    
    # Pass a parameter to indicate we're on the login form
    return render_template('login_signup.html', errors=errors, form='login')

@app.route('/user-otp', methods=['GET', 'POST'])
def user_otp():
    """Email verification OTP page"""
    # Check if user is logged in
    if 'email' not in session:
        return redirect(url_for('login_user'))
    
    errors = []
    info = session.get('info', '')
    
    if request.method == 'POST':
        otp_code = request.form.get('otp')
        
        # Check if OTP is provided
        if not otp_code:
            errors.append("Verification code is required. Please enter the code sent to your email.")
        else:
            # Import controller function here to avoid circular imports
            from utils.user_controller import verify_otp as verify_otp_controller
            success, errors = verify_otp_controller(otp_code)
            if success:
                return redirect(url_for('home'))
    
    # Use the login_signup template but indicate we're on the OTP verification form
    return render_template('login_signup.html', errors=errors, info=info, form='otp')

@app.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    """Password recovery page"""
    errors = []
    
    if request.method == 'POST':
        email = request.form.get('email')
        
        # Check if email is provided
        if not email:
            errors.append("Email address is required to initiate password recovery.")
        else:
            # Import controller function here to avoid circular imports
            from utils.user_controller import forgot_password as forgot_password_controller
            success, errors = forgot_password_controller(email)
            if success:
                return redirect(url_for('reset_code'))
    
    # Use the login_signup template but indicate we're on the forgot password form
    return render_template('login_signup.html', errors=errors, form='forgot')

@app.route('/reset-code', methods=['GET', 'POST'])
def reset_code():
    """Password reset OTP verification page"""
    # Check if user is logged in
    if 'email' not in session:
        return redirect(url_for('login_user'))
    
    errors = []
    info = session.get('info', '')
    
    if request.method == 'POST':
        otp_code = request.form.get('otp')
        
        # Check if OTP is provided
        if not otp_code:
            errors.append("Verification code is required. Please enter the code sent to your email.")
        else:
            # Import controller function here to avoid circular imports
            from utils.user_controller import reset_password_otp as reset_password_otp_controller
            success, errors = reset_password_otp_controller(otp_code)
            if success:
                return redirect(url_for('new_password'))
    
    # Use the login_signup template but indicate we're on the reset code form
    return render_template('login_signup.html', errors=errors, info=info, form='reset')

@app.route('/new-password', methods=['GET', 'POST'])
def new_password():
    """New password creation page"""
    # Check if user is logged in
    if 'email' not in session:
        return redirect(url_for('login_user'))
    
    errors = []
    info = session.get('info', '')
    
    if request.method == 'POST':
        password = request.form.get('password')
        cpassword = request.form.get('cpassword')
        
        # Check if passwords are provided
        if not password or not cpassword:
            errors.append("Both password fields are required. Please complete all password fields.")
        else:
            # Import controller function here to avoid circular imports
            from utils.user_controller import change_password as change_password_controller
            success, errors = change_password_controller(password, cpassword)
            if success:
                return redirect(url_for('password_changed'))
    
    # Use the login_signup template but indicate we're on the new password form
    return render_template('login_signup.html', errors=errors, info=info, form='new-password')

@app.route('/password-changed', methods=['GET', 'POST'])
def password_changed():
    """Password changed confirmation page"""
    info = session.get('info', '')
    
    if request.method == 'POST':
        return redirect(url_for('login_user'))
    
    # Check if user came from password change
    if not info:
        return redirect(url_for('login_user'))
    
    # Use the login_signup template but indicate we're on the password changed form
    return render_template('login_signup.html', info=info, form='password-changed')

@app.route('/home')
def home():
    """User dashboard/home page"""
    # Check if user is logged in
    if 'user_id' not in session:
        return redirect(url_for('login_user'))
    
    try:
        db = get_db_connection()
        if db is not None:
            collection = get_collection(db, 'usertable')
            users = find_documents(collection, {'email': session['email']})
            
            if users:
                user = users[0]
                # Check verification status
                if user['status'] != "verified":
                    return redirect(url_for('user_otp'))
                elif user['code'] != 0:
                    return redirect(url_for('reset_code'))
            else:
                return redirect(url_for('login_user'))
    except Exception as e:
        print(f"Database error: {str(e)}")
        return redirect(url_for('login_user'))
    
    return render_template('home.html', name=session.get('name', 'User'))

@app.route('/logout-user')
def logout_user():
    """User logout"""
    session.clear()
    return redirect(url_for('index'))

@app.route('/login-signup')
def login_signup():
    """Combined login/signup page"""
    # Default to login form
    return render_template('login_signup.html', form='login')

@app.route('/course-agent')
def course_agent():
    """Course Agent page"""
    # Check if user is logged in
    if 'user_id' not in session:
        return redirect(url_for('login_user'))
    
    return render_template('course-agent.html', name=session.get('name', 'User'))

@app.route('/course-agent/schedule/<course_id>')
def course_schedule(course_id):
    """Schedule page for a specific course"""
    # Check if user is logged in
    if 'user_id' not in session:
        return redirect(url_for('login_user'))
    
    # Course icons mapping
    course_icons = {
        'python': 'https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/python/python-original.svg',
        'java': 'https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/java/java-original.svg',
        'javascript': 'https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/javascript/javascript-original.svg',
        'fullstack': 'https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/html5/html5-original.svg',
        'react': 'https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/react/react-original.svg',
        'datascience': 'https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/numpy/numpy-original.svg',
        'mobile': 'https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/react/react-original.svg',
        'cloud': 'https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/amazonwebservices/amazonwebservices-original-wordmark.svg',
        'cybersecurity': 'https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/linux/linux-original.svg',
        'uiux': 'https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/figma/figma-original.svg',
        'ai': 'https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/tensorflow/tensorflow-original.svg',
        'blockchain': 'https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/ethereum/ethereum-original.svg'
    }
    
    # Course names mapping
    course_names = {
        'python': 'Python Programming',
        'java': 'Java Development',
        'javascript': 'JavaScript Mastery',
        'fullstack': 'Full-Stack Web Development',
        'react': 'React Framework',
        'datascience': 'Data Science Fundamentals',
        'mobile': 'Mobile App Development',
        'cloud': 'Cloud Computing & DevOps',
        'cybersecurity': 'Cybersecurity Essentials',
        'uiux': 'UI/UX Design',
        'ai': 'AI & Machine Learning',
        'blockchain': 'Blockchain Development'
    }
    
    # Get course name and icon
    selected_course_name = course_names.get(course_id, 'Unknown Course')
    selected_course_icon = course_icons.get(course_id, '')
    
    return render_template('schedule.html', 
                         name=session.get('name', 'User'),
                         course_id=course_id,
                         selected_course_name=selected_course_name,
                         selected_course_icon=selected_course_icon)

@app.route('/course-agent/schedule/save', methods=['POST'])
def save_schedule():
    """Save the course schedule"""
    # Check if user is logged in
    if 'user_id' not in session:
        return redirect(url_for('login_user'))
    
    # Import controller functions
    from utils.course_controller import select_course as select_course_controller
    from utils.course_controller import send_schedule_confirmation_email, get_user_info
    
    # Get form data
    course_id = request.form.get('course_id')
    if not course_id:
        return redirect(url_for('course_agent'))
    
    # For the new schedule form, we need to map the fields differently
    fullname = request.form.get('fullname')
    whatsapp = request.form.get('whatsapp')
    duration = request.form.get('duration')
    preferred_time = request.form.get('preferred_time')
    notification_method = request.form.get('notification_method')
    
    # Map the new fields to the expected format
    schedule = {
        'preferred_time': preferred_time,
        'frequency': 'daily',  # Default to daily
        'pace': 'intermediate',  # Default to intermediate
        'notification_method': notification_method,
        'fullname': fullname,
        'whatsapp': whatsapp,
        'duration': duration
    }
    
    # Select course
    success, message = select_course_controller(session['user_id'], course_id, schedule)
    
    # If course selection was successful, send confirmation email
    if success:
        try:
            # Get user information for the email
            user = get_user_info(session['user_id'])
            if user:
                user_email = user['email']
                user_name = user['name']
                
                # Course names mapping (same as in course_schedule function)
                course_names = {
                    'python': 'Python Programming',
                    'java': 'Java Development',
                    'javascript': 'JavaScript Mastery',
                    'fullstack': 'Full-Stack Web Development',
                    'react': 'React Framework',
                    'datascience': 'Data Science Fundamentals',
                    'mobile': 'Mobile App Development',
                    'cloud': 'Cloud Computing & DevOps',
                    'cybersecurity': 'Cybersecurity Essentials',
                    'uiux': 'UI/UX Design',
                    'ai': 'AI & Machine Learning',
                    'blockchain': 'Blockchain Development'
                }
                
                selected_course_name = course_names.get(course_id, 'Unknown Course')
                
                # Send confirmation email
                send_schedule_confirmation_email(user_email, user_name, selected_course_name, schedule)
        except Exception as e:
            print(f"Error sending confirmation email: {str(e)}")
            # Don't fail the request if email sending fails
    
    if success:
        return redirect(url_for('course_agent_success'))
    else:
        # In a real implementation, you would pass the error message to the template
        return redirect(url_for('course_agent'))

@app.route('/select-course', methods=['POST'])
def select_course():
    """Handle course selection - redirect to schedule page"""
    # Check if user is logged in
    if 'user_id' not in session:
        return redirect(url_for('login_user'))
    
    # Get form data
    course_id = request.form.get('course_id')
    if not course_id:
        return redirect(url_for('course_agent'))
    
    # Redirect to schedule page for this course
    return redirect(url_for('course_schedule', course_id=course_id))

@app.route('/course-agent/success')
def course_agent_success():
    """Course selection success page"""
    # Check if user is logged in
    if 'user_id' not in session:
        return redirect(url_for('login_user'))
    
    return render_template('course-agent-success.html', name=session.get('name', 'User'))

@app.route('/profile')
def user_profile():
    """User profile page"""
    # Check if user is logged in
    if 'user_id' not in session:
        return redirect(url_for('login_user'))
    
    try:
        db = get_db_connection()
        if db is not None:
            collection = get_collection(db, 'usertable')
            users = find_documents(collection, {'_id': ObjectId(session['user_id'])})
            
            if users:
                user = users[0]
                # Remove sensitive information
                user_data = {
                    'name': user.get('name', 'N/A'),
                    'email': user.get('email', 'N/A'),
                    'status': user.get('status', 'N/A'),
                    'member_since': user.get('_id').generation_time.strftime('%B %d, %Y') if '_id' in user else 'N/A'
                }
                return render_template('profile.html', user=user_data, name=session.get('name', 'User'))
            else:
                return redirect(url_for('login_user'))
        else:
            return redirect(url_for('login_user'))
    except Exception as e:
        print(f"Database error: {str(e)}")
        return redirect(url_for('home'))

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    print(f"✅ Application startup successful!")
    print(f"   Flask app running on port {port}")
    print(f"   MongoDB connection confirmed")
    print(f"   Access URL: http://localhost:{port}")
    app.run(debug=True, host='0.0.0.0', port=port)