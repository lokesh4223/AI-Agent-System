"""
Unit tests for the user controller module
"""

import pytest
from unittest.mock import Mock, patch
from utils.user_controller import signup_user, login_user, verify_otp


class TestUserController:
    """Test cases for user controller functions"""

    def test_signup_user_success(self, mocker):
        """Test successful user registration"""
        # Mock database operations
        mock_db = Mock()
        mock_collection = Mock()
        mock_collection.find_documents.return_value = []  # No existing user
        mock_collection.insert_document.return_value = True
        
        mocker.patch('utils.database.get_db_connection', return_value=mock_db)
        mocker.patch('utils.database.get_collection', return_value=mock_collection)
        mocker.patch('utils.mail.send_email_brevo', return_value=True)
        
        # Test signup
        success, errors = signup_user("John Doe", "john@example.com", "password123", "password123")
        
        # Assertions
        assert success == True
        assert len(errors) == 0
        mock_collection.find_documents.assert_called_once_with({'email': 'john@example.com'})
        mock_collection.insert_document.assert_called_once()

    def test_signup_user_password_mismatch(self):
        """Test signup with password mismatch"""
        success, errors = signup_user("John Doe", "john@example.com", "password123", "different123")
        
        assert success == False
        assert "Passwords do not match" in errors[0]

    def test_signup_user_existing_email(self, mocker):
        """Test signup with existing email"""
        # Mock database to return existing user
        mock_db = Mock()
        mock_collection = Mock()
        mock_collection.find_documents.return_value = [{'email': 'john@example.com'}]
        
        mocker.patch('utils.database.get_db_connection', return_value=mock_db)
        mocker.patch('utils.database.get_collection', return_value=mock_collection)
        
        success, errors = signup_user("John Doe", "john@example.com", "password123", "password123")
        
        assert success == False
        assert "already registered" in errors[0]

    def test_login_user_success(self, mocker):
        """Test successful user login"""
        # Mock database operations
        mock_db = Mock()
        mock_collection = Mock()
        mock_user = {
            'email': 'john@example.com',
            'password': 'hashed_password',
            'name': 'John Doe',
            'status': 'verified',
            '_id': 'user123'
        }
        mock_collection.find_documents.return_value = [mock_user]
        
        mocker.patch('utils.database.get_db_connection', return_value=mock_db)
        mocker.patch('utils.database.get_collection', return_value=mock_collection)
        mocker.patch('werkzeug.security.check_password_hash', return_value=True)
        
        success, errors = login_user("john@example.com", "password123")
        
        assert success == True
        assert len(errors) == 0

    def test_login_user_invalid_credentials(self, mocker):
        """Test login with invalid credentials"""
        # Mock database operations
        mock_db = Mock()
        mock_collection = Mock()
        mock_collection.find_documents.return_value = []
        
        mocker.patch('utils.database.get_db_connection', return_value=mock_db)
        mocker.patch('utils.database.get_collection', return_value=mock_collection)
        
        success, errors = login_user("john@example.com", "wrongpassword")
        
        assert success == False
        assert "No account found" in errors[0]

    def test_verify_otp_success(self, mocker):
        """Test successful OTP verification"""
        # Mock database operations
        mock_db = Mock()
        mock_collection = Mock()
        mock_user = {
            '_id': 'user123',
            'name': 'John Doe',
            'email': 'john@example.com'
        }
        mock_collection.find_documents.return_value = [mock_user]
        mock_collection.update_document.return_value = True
        
        mocker.patch('utils.database.get_db_connection', return_value=mock_db)
        mocker.patch('utils.database.get_collection', return_value=mock_collection)
        
        success, errors = verify_otp("123456")
        
        assert success == True
        assert len(errors) == 0

    def test_verify_otp_invalid_code(self, mocker):
        """Test OTP verification with invalid code"""
        # Mock database operations
        mock_db = Mock()
        mock_collection = Mock()
        mock_collection.find_documents.return_value = []
        
        mocker.patch('utils.database.get_db_connection', return_value=mock_db)
        mocker.patch('utils.database.get_collection', return_value=mock_collection)
        
        success, errors = verify_otp("000000")
        
        assert success == False
        assert "Invalid verification code" in errors[0]


if __name__ == '__main__':
    pytest.main([__file__])