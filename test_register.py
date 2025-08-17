#!/usr/bin/env python3
"""
Test script for registration endpoint
"""

import requests
import json

def test_register():
    """Test the registration endpoint"""
    base_url = "https://gossipai-backend.onrender.com"
    
    print("Testing registration endpoint...")
    print("=" * 50)
    
    # Test data
    test_data = {
        "email": "test@example.com",
        "password": "password123",
        "name": "Test User"
    }
    
    print(f"Test data: {test_data}")
    
    try:
        # Test registration endpoint
        response = requests.post(
            f"{base_url}/api/v1/auth/register",
            json=test_data,
            headers={"Content-Type": "application/json"}
        )
        
        print(f"Status: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_register()
