"""
Test script to verify schedule data storage in MongoDB
"""
import os
from utils.database import get_db_connection, get_collection, find_documents, insert_document
from utils.course_controller import select_course
from bson.objectid import ObjectId

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

def test_schedule_storage():
    """Test that schedule data is properly stored in MongoDB"""
    try:
        # Connect to database
        db = get_db_connection()
        if db is None:
            print("Failed to connect to database")
            return False
            
        # Test data
        test_user_id = "68e5163fef8bfd666eca5332"  # Using existing user ID from our data
        test_course_id = "python"
        test_schedule = {
            'preferred_time': '2:00 PM',
            'frequency': 'daily',
            'pace': 'intermediate',
            'notification_method': 'both',
            'fullname': 'Test User',
            'whatsapp': '+1234567890',
            'duration': '45'
        }
        
        # Test the select_course function
        success, message = select_course(test_user_id, test_course_id, test_schedule)
        
        if success:
            print("✓ Course enrollment created successfully")
            print(f"Message: {message}")
            
            # Verify the data was stored
            collection = get_collection(db, 'course_enrollments')
            enrollments = find_documents(collection, {
                'user_id': test_user_id,
                'course_id': test_course_id
            })
            
            if enrollments:
                # Get the most recent enrollment (should be the one we just created)
                enrollment = enrollments[-1]  # Last one should be the newest
                print("\nStored Enrollment Data:")
                print(f"User ID: {enrollment.get('user_id')}")
                print(f"Course ID: {enrollment.get('course_id')}")
                print(f"Course Name: {enrollment.get('course_name')}")
                print(f"Status: {enrollment.get('status')}")
                
                # Check schedule data
                stored_schedule = enrollment.get('schedule', {})
                print("\nStored Schedule:")
                for key, value in stored_schedule.items():
                    print(f"  {key}: {value}")
                
                # Verify all expected fields are present
                expected_fields = ['preferred_time', 'frequency', 'pace', 'notification_method', 
                                 'fullname', 'whatsapp', 'duration']
                missing_fields = [field for field in expected_fields if field not in stored_schedule]
                
                if not missing_fields:
                    print("\n✓ All schedule fields stored correctly")
                    return True
                else:
                    print(f"\n✗ Missing fields: {missing_fields}")
                    return False
            else:
                print("✗ Failed to find stored enrollment")
                return False
        else:
            print(f"✗ Failed to create enrollment: {message}")
            return False
            
    except Exception as e:
        print(f"Error during test: {str(e)}")
        return False

if __name__ == "__main__":
    print("Testing schedule data storage in MongoDB...")
    print("=" * 50)
    success = test_schedule_storage()
    if success:
        print("\n✓ Test PASSED: Schedule data is being stored correctly")
    else:
        print("\n✗ Test FAILED: Schedule data storage issue")