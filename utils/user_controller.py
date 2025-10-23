"""
User controller utilities for the AI Agent System
Provides functionality equivalent to controllerUserData.php in the original PHP implementation
"""

import random
import os
from flask import session
from werkzeug.security import generate_password_hash, check_password_hash
from typing import List, Dict, Optional, Tuple
from .database import get_db_connection, get_collection, find_documents, insert_document, update_document
from .mail import send_email_brevo, get_otp_email_template

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

# Brevo API Configuration - Use environment variables
BREVO_API_KEY = os.environ.get('BREVO_API_KEY')
BREVO_SENDER_EMAIL = os.environ.get('SENDER_EMAIL')
BREVO_SENDER_NAME = os.environ.get('SENDER_NAME', 'AI Agent System')

def signup_user(name: str, email: str, password: str, cpassword: str) -> Tuple[bool, List[str]]:
    """
    Handle user signup
    Equivalent to the signup section in controllerUserData.php
    """
    errors = []
    
    # Validation
    if password != cpassword:
        errors.append("Password confirmation does not match. Please ensure both password fields contain identical values.")
        return False, errors
    
    # Check if email already exists
    try:
        db = get_db_connection()
        if db is None:
            errors.append("Unable to establish database connection. Please try again in a few moments.")
            return False, errors
            
        collection = get_collection(db, 'usertable')
        existing_user = find_documents(collection, {'email': email})
        if existing_user:
            errors.append("This email address is already associated with an account. Please sign in or use a different email address.")
            return False, errors
        
        # Hash password
        hashed_password = generate_password_hash(password)
        code = random.randint(111111, 999999)
        status = "notverified"
        
        # Create user document
        user_document = {
            'name': name,
            'email': email,
            'password': hashed_password,
            'code': code,
            'status': status
        }
        
        # Insert user
        result = insert_document(collection, user_document)
        
        if result:
            # Send verification email
            subject = "AI Agent System - Email Verification Code"
            message = get_otp_email_template(code, 'verification')
            
            if send_email_brevo(email, subject, message, BREVO_API_KEY, BREVO_SENDER_EMAIL, BREVO_SENDER_NAME):
                session['info'] = f"A verification code has been sent to {email}. Please check your inbox and enter the code to complete registration."
                session['email'] = email
                session['password'] = password
                return True, []
            else:
                # More specific error message for email failure
                errors.append("Unable to send verification email. Please verify your email address is correct and try again.")
        else:
            errors.append("Account creation failed. Please try again or contact support if the issue persists.")
            
        return False, errors

    except Exception as e:
        errors.append("An unexpected error occurred during account creation. Please try again or contact support for assistance.")
        print(f"Database error: {str(e)}")
        return False, errors

def verify_otp(otp_code: str) -> Tuple[bool, List[str]]:
    """
    Verify OTP code
    Equivalent to the OTP verification section in controllerUserData.php
    """
    errors = []
    
    try:
        db = get_db_connection()
        if db is None:
            errors.append("Unable to establish database connection. Please try again in a few moments.")
            return False, errors
            
        collection = get_collection(db, 'usertable')
        user = find_documents(collection, {'code': int(otp_code)})
        
        if user:
            # Update user status
            success = update_document(
                collection,
                {'code': int(otp_code)},
                {'$set': {'code': 0, 'status': 'verified'}}
            )
            
            if success:
                session['name'] = user[0]['name']
                session['user_id'] = str(user[0]['_id'])
                return True, []
            else:
                errors.append("Account verification failed. Please try again or contact support for assistance.")
        else:
            errors.append("Invalid verification code provided. Please check the code and try again.")
            
        return False, errors
        
    except Exception as e:
        errors.append("An error occurred during verification. Please try again or contact support for assistance.")
        print(f"Database error: {str(e)}")
        return False, errors

def login_user(email: str, password: str) -> Tuple[bool, List[str]]:
    """
    Handle user login
    Equivalent to the login section in controllerUserData.php
    """
    errors = []
    
    try:
        db = get_db_connection()
        if db is None:
            errors.append("Unable to establish database connection. Please try again in a few moments.")
            return False, errors
            
        collection = get_collection(db, 'usertable')
        users = find_documents(collection, {'email': email})
        
        if users:
            user = users[0]
            # Check password
            if check_password_hash(user['password'], password):
                session['email'] = email
                session['name'] = user['name']
                
                # Check verification status
                if user['status'] == "verified":
                    session['user_id'] = str(user['_id'])
                    return True, []
                else:
                    session['info'] = f"Email verification required for {email}. Please complete verification to access your account."
                    return False, ["redirect_user_otp"]
            else:
                errors.append("Invalid email or password. Please verify your credentials and try again.")
        else:
            errors.append("No account found with this email address. Please register for a new account.")
            
        return False, errors
        
    except Exception as e:
        errors.append("An error occurred during login. Please try again or contact support for assistance.")
        print(f"Database error: {str(e)}")
        return False, errors

def forgot_password(email: str) -> Tuple[bool, List[str]]:
    """
    Handle forgot password request
    Equivalent to the forgot password section in controllerUserData.php
    """
    errors = []
    
    try:
        db = get_db_connection()
        if db is None:
            errors.append("Unable to establish database connection. Please try again in a few moments.")
            return False, errors
            
        collection = get_collection(db, 'usertable')
        users = find_documents(collection, {'email': email})
        
        if users:
            user = users[0]
            code = random.randint(111111, 999999)
            
            # Update user code
            success = update_document(
                collection,
                {'email': email},
                {'$set': {'code': code}}
            )
            
            if success:
                # Send reset email
                subject = "AI Agent System - Password Reset Code"
                message = get_otp_email_template(code, 'reset')
                
                if send_email_brevo(email, subject, message, BREVO_API_KEY, BREVO_SENDER_EMAIL, BREVO_SENDER_NAME):
                    session['info'] = f"A password reset code has been sent to {email}. Please check your inbox."
                    session['email'] = email
                    return True, []
                else:
                    errors.append("Unable to send password reset email. Please try again in a few moments.")
            else:
                errors.append("Unable to process your request. Please try again or contact support for assistance.")
        else:
            errors.append("No account found with this email address. Please verify the email or register for a new account.")
            
        return False, errors
        
    except Exception as e:
        errors.append("An error occurred while processing your request. Please try again or contact support for assistance.")
        print(f"Database error: {str(e)}")
        return False, errors

def reset_password_otp(otp_code: str) -> Tuple[bool, List[str]]:
    """
    Verify reset password OTP
    Equivalent to the reset OTP section in controllerUserData.php
    """
    errors = []
    
    try:
        db = get_db_connection()
        if db is None:
            errors.append("Unable to establish database connection. Please try again in a few moments.")
            return False, errors
            
        collection = get_collection(db, 'usertable')
        users = find_documents(collection, {'code': int(otp_code)})
        
        if users:
            user = users[0]
            session['email'] = user['email']
            session['info'] = "Please create a new password for your account."
            return True, []
        else:
            errors.append("Invalid reset code provided. Please verify the code and try again.")
            
        return False, errors
        
    except Exception as e:
        errors.append("An error occurred during password reset. Please try again or contact support for assistance.")
        print(f"Database error: {str(e)}")
        return False, errors

def change_password(password: str, cpassword: str) -> Tuple[bool, List[str]]:
    """
    Change user password
    Equivalent to the change password section in controllerUserData.php
    """
    errors = []
    
    if password != cpassword:
        errors.append("Password confirmation does not match. Please ensure both password fields contain identical values.")
        return False, errors
    else:
        try:
            email = session.get('email', '')
            if not email:
                errors.append("Session has expired. Please initiate a new password reset process.")
                return False, errors
                
            hashed_password = generate_password_hash(password)
            
            db = get_db_connection()
            if db is None:
                errors.append("Unable to establish database connection. Please try again in a few moments.")
                return False, errors
                
            collection = get_collection(db, 'usertable')
            success = update_document(
                collection,
                {'email': email},
                {'$set': {'code': 0, 'password': hashed_password}}
            )
            
            if success:
                session['info'] = "Your password has been successfully updated. You may now sign in with your new credentials."
                return True, []
            else:
                errors.append("Unable to update your password. Please try again or contact support for assistance.")
                
            return False, errors
            
        except Exception as e:
            errors.append("An error occurred while changing your password. Please try again or contact support for assistance.")
            print(f"Database error: {str(e)}")
            return False, errors

def login_now() -> str:
    """
    Handle login now button click
    Equivalent to the login now section in controllerUserData.php
    """
    return "login-user"