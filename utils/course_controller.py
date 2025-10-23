"""
Course controller utilities for the AI Agent System
Provides functionality for course selection and scheduling
"""

import os
from flask import session
from typing import Dict, List, Optional, Tuple
from bson.objectid import ObjectId
from .database import get_db_connection, get_collection, find_documents, insert_document, update_document
from .mail import send_email_brevo, get_schedule_confirmation_email_template
from .user_controller import BREVO_API_KEY, BREVO_SENDER_EMAIL, BREVO_SENDER_NAME

# Course definitions
COURSES = {
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

def get_available_courses() -> Dict[str, str]:
    """
    Get all available courses
    """
    return COURSES

def select_course(user_id: str, course_id: str, schedule: Dict) -> Tuple[bool, str]:
    """
    Select a course for a user and save their schedule preferences
    """
    try:
        # Validate course ID
        if course_id not in COURSES:
            return False, "The selected course is not available. Please choose a valid course from the catalog."
        
        db = get_db_connection()
        if db is None:
            return False, "Unable to establish database connection. Please try again in a few moments."
        
        # Create course enrollment document
        enrollment = {
            'user_id': user_id,
            'course_id': course_id,
            'course_name': COURSES[course_id],
            'schedule': schedule,
            'status': 'active'
        }
        
        # Insert enrollment
        collection = get_collection(db, 'course_enrollments')
        result = insert_document(collection, enrollment)
        
        if result:
            return True, "Course enrollment successful. Your learning journey is about to begin!"
        else:
            return False, "Course enrollment failed. Please try again or contact support for assistance."
            
    except Exception as e:
        print(f"Error selecting course: {str(e)}")
        return False, "An unexpected error occurred during course enrollment. Please try again or contact support for assistance."

def get_user_courses(user_id: str) -> Optional[List[Dict]]:
    """
    Get all courses for a user
    """
    try:
        db = get_db_connection()
        if db is None:
            return None
            
        collection = get_collection(db, 'course_enrollments')
        enrollments = find_documents(collection, {'user_id': user_id})
        
        return enrollments
        
    except Exception as e:
        print(f"Error retrieving user courses: {str(e)}")
        return None

def update_course_schedule(user_id: str, course_id: str, schedule: Dict) -> Tuple[bool, str]:
    """
    Update a user's course schedule
    """
    try:
        db = get_db_connection()
        if db is None:
            return False, "Unable to establish database connection. Please try again in a few moments."
            
        collection = get_collection(db, 'course_enrollments')
        result = update_document(
            collection,
            {'user_id': user_id, 'course_id': course_id},
            {'$set': {'schedule': schedule}}
        )
        
        if result:
            return True, "Learning schedule updated successfully."
        else:
            return False, "Unable to update learning schedule. Please try again or contact support for assistance."
            
    except Exception as e:
        print(f"Error updating course schedule: {str(e)}")
        return False, "An error occurred while updating your schedule. Please try again or contact support for assistance."

def get_user_info(user_id: str) -> Optional[Dict]:
    """
    Get user information by user ID
    """
    try:
        db = get_db_connection()
        if db is None:
            return None
            
        collection = get_collection(db, 'usertable')
        users = find_documents(collection, {'_id': ObjectId(user_id)})
        
        if users:
            return users[0]
        return None
        
    except Exception as e:
        print(f"Error retrieving user info: {str(e)}")
        return None

def send_schedule_confirmation_email(user_email: str, user_name: str, course_name: str, schedule: Dict) -> bool:
    """
    Send a schedule confirmation email to the user
    """
    try:
        # Format schedule details for the email
        schedule_details = ""
        if 'fullname' in schedule:
            schedule_details += f"<div class='detail-item'><span class='detail-label'>Full Name:</span> {schedule['fullname']}</div>"
        if 'duration' in schedule:
            schedule_details += f"<div class='detail-item'><span class='detail-label'>Learning Duration:</span> {schedule['duration']} days</div>"
        if 'preferred_time' in schedule:
            schedule_details += f"<div class='detail-item'><span class='detail-label'>Preferred Time:</span> {schedule['preferred_time']}</div>"
        if 'notification_method' in schedule:
            method = schedule['notification_method'].replace('_', ' ').title()
            schedule_details += f"<div class='detail-item'><span class='detail-label'>Notification Method:</span> {method}</div>"
        if 'whatsapp' in schedule:
            schedule_details += f"<div class='detail-item'><span class='detail-label'>WhatsApp:</span> {schedule['whatsapp']}</div>"
        
        # Generate email content
        subject = f"AI Agent System - {course_name} Learning Schedule Confirmation"
        html_content = get_schedule_confirmation_email_template(user_name, course_name, schedule_details)
        
        # Send email
        return send_email_brevo(user_email, subject, html_content, BREVO_API_KEY, BREVO_SENDER_EMAIL, BREVO_SENDER_NAME)
        
    except Exception as e:
        print(f"Error sending schedule confirmation email: {str(e)}")
        return False
