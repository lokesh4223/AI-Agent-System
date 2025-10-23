"""
Environment loader utility for the AI Agent System
Provides functionality equivalent to env_loader.php in the original PHP implementation
"""

import os
from typing import Optional

def load_env(file_path: str) -> bool:
    """
    Load environment variables from a .env file
    Equivalent to the loadEnv function in env_loader.php
    """
    if not os.path.exists(file_path):
        print(f"❌ .env file not found at: {file_path}")
        return False
    
    try:
        with open(file_path, 'r') as f:
            lines = f.readlines()
    except Exception as e:
        print(f"❌ Failed to read .env file: {str(e)}")
        return False
    
    for line in lines:
        # Skip comments and empty lines
        line = line.strip()
        if line.startswith('#') or not line:
            continue
        
        # Split the line into name and value
        if '=' in line:
            parts = line.split('=', 1)
            if len(parts) == 2:
                name = parts[0].strip()
                value = parts[1].strip()
                
                # Remove quotes if present
                if (value.startswith('"') and value.endswith('"')) or \
                   (value.startswith("'") and value.endswith("'")):
                    value = value[1:-1]
                
                # Set the environment variable
                os.environ[name] = value
                print(f"✅ Loaded env variable: {name} = {value[:10]}...")
    
    return True

def get_env_variable(key: str, default: Optional[str] = None) -> Optional[str]:
    """
    Get environment variable with fallback
    Equivalent to the getEnvVariable function in env_loader.php
    """
    # Try to get the environment variable
    value = os.environ.get(key)
    
    if value is not None:
        return value
    
    print(f"❌ Environment variable not found: {key}")
    return default

# Load the .env file from the same directory
env_file_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env')
env_loaded = load_env(env_file_path)

if not env_loaded:
    print("❌ CRITICAL: Failed to load .env file")