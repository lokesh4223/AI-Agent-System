"""
Database utilities for the AI Agent System
Provides functionality equivalent to connection.php in the original PHP implementation
"""

import os
from typing import Dict, Any, Optional
from pymongo import MongoClient
from pymongo.database import Database
from pymongo.collection import Collection

# Database configuration for MongoDB
MONGO_URI = os.environ.get('MONGO_URI', 'mongodb://localhost:27017/ai_agent_system')
DB_NAME = os.environ.get('DB_NAME', 'ai_agent_system')

def get_db_connection() -> Optional[Database]:
    """
    Create and return a MongoDB database connection
    Equivalent to the mysqli_connect in connection.php
    """
    try:
        # Create connection using MONGO_URI
        client = MongoClient(MONGO_URI)
        db = client[DB_NAME]
        # Test the connection
        client.admin.command('ping')
        return db
    except Exception as e:
        print(f"Connection failed: {str(e)}")
        return None

def get_collection(db: Database, collection_name: str) -> Collection:
    """
    Get a collection from the database
    """
    return db[collection_name]

def find_documents(collection: Collection, query: Dict) -> Optional[list]:
    """
    Find documents in a collection
    """
    try:
        return list(collection.find(query))
    except Exception as e:
        print(f"Query execution failed: {str(e)}")
        return None

def insert_document(collection: Collection, document: Dict) -> Optional[str]:
    """
    Insert a document into a collection
    """
    try:
        result = collection.insert_one(document)
        return str(result.inserted_id)
    except Exception as e:
        print(f"Insert execution failed: {str(e)}")
        return None

def update_document(collection: Collection, query: Dict, update: Dict) -> bool:
    """
    Update documents in a collection
    """
    try:
        result = collection.update_one(query, update)
        return result.matched_count > 0
    except Exception as e:
        print(f"Update execution failed: {str(e)}")
        return False

def delete_document(collection: Collection, query: Dict) -> bool:
    """
    Delete documents from a collection
    """
    try:
        result = collection.delete_one(query)
        return result.deleted_count > 0
    except Exception as e:
        print(f"Delete execution failed: {str(e)}")
        return False