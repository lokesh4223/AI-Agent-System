"""
Script to clean up test data from MongoDB
"""
import os
from utils.database import get_db_connection, get_collection, find_documents, delete_document

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

def cleanup_test_data():
    """Remove test enrollment data from MongoDB"""
    try:
        # Connect to database
        db = get_db_connection()
        if db is None:
            print("Failed to connect to database")
            return False
            
        # Find test enrollment (with Test User fullname)
        collection = get_collection(db, 'course_enrollments')
        enrollments = find_documents(collection, {
            'schedule.fullname': 'Test User'
        })
        
        if enrollments:
            # Delete the test enrollment
            for enrollment in enrollments:
                enrollment_id = enrollment['_id']
                result = collection.delete_one({'_id': enrollment_id})
                if result.deleted_count > 0:
                    print(f"✓ Deleted test enrollment: {enrollment_id}")
                else:
                    print(f"✗ Failed to delete test enrollment: {enrollment_id}")
            return True
        else:
            print("No test data found to clean up")
            return True
            
    except Exception as e:
        print(f"Error during cleanup: {str(e)}")
        return False

if __name__ == "__main__":
    print("Cleaning up test data...")
    print("=" * 30)
    success = cleanup_test_data()
    if success:
        print("\n✓ Cleanup completed successfully")
    else:
        print("\n✗ Cleanup failed")