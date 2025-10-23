"""
Script to view schedule data stored in MongoDB
"""
import os
from utils.database import get_db_connection, get_collection, find_documents

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

def view_schedule_data():
    """View all course enrollment data"""
    try:
        # Connect to database
        db = get_db_connection()
        if db is None:
            print("Failed to connect to database")
            return
            
        # Get course enrollments collection
        collection = get_collection(db, 'course_enrollments')
        enrollments = find_documents(collection, {})
        
        if enrollments:
            print("Course Enrollments:")
            print("=" * 50)
            for enrollment in enrollments:
                print(f"User ID: {enrollment.get('user_id', 'N/A')}")
                print(f"Course ID: {enrollment.get('course_id', 'N/A')}")
                print(f"Course Name: {enrollment.get('course_name', 'N/A')}")
                print(f"Status: {enrollment.get('status', 'N/A')}")
                
                # Print schedule details
                schedule = enrollment.get('schedule', {})
                print("Schedule:")
                for key, value in schedule.items():
                    print(f"  {key}: {value}")
                print("-" * 30)
        else:
            print("No course enrollments found")
            
        # Also check users
        print("\nUsers:")
        print("=" * 50)
        user_collection = get_collection(db, 'usertable')
        users = find_documents(user_collection, {})
        
        if users:
            for user in users:
                print(f"Name: {user.get('name', 'N/A')}")
                print(f"Email: {user.get('email', 'N/A')}")
                print(f"Status: {user.get('status', 'N/A')}")
                print("-" * 30)
        else:
            print("No users found")
            
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    view_schedule_data()