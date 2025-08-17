#!/usr/bin/env python3
"""
Test script for registration validation
"""

import requests
import json

# Test data
test_cases = [
    {
        "name": "Valid registration",
        "data": {
            "email": "test@example.com",
            "password": "password123",
            "name": "Test User"
        }
    },
    {
        "name": "Invalid email",
        "data": {
            "email": "invalid-email",
            "password": "password123",
            "name": "Test User"
        }
    },
    {
        "name": "Short password",
        "data": {
            "email": "test@example.com",
            "password": "123",
            "name": "Test User"
        }
    },
    {
        "name": "Empty name",
        "data": {
            "email": "test@example.com",
            "password": "password123",
            "name": ""
        }
    }
]

def test_validation():
    """Test the validation endpoint"""
    base_url = "https://gossipai-backend.onrender.com"
    
    print("Testing registration validation...")
    print("=" * 50)
    
    for test_case in test_cases:
        print(f"\nTest: {test_case['name']}")
        print(f"Data: {test_case['data']}")
        
        try:
            # Test validation endpoint
            response = requests.post(
                f"{base_url}/api/v1/auth/test-validation",
                json=test_case['data'],
                headers={"Content-Type": "application/json"}
            )
            
            print(f"Status: {response.status_code}")
            print(f"Response: {json.dumps(response.json(), indent=2)}")
            
        except Exception as e:
            print(f"Error: {e}")
        
        print("-" * 30)

if __name__ == "__main__":
    test_validation()
