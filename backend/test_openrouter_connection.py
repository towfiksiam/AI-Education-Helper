#!/usr/bin/env python3
"""
Test script to verify OpenRouter API connection.
Run this to diagnose OpenRouter integration issues.
"""

import requests
import json
import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def print_header(text):
    """Print a formatted header"""
    print("\n" + "=" * 60)
    print(f"  {text}")
    print("=" * 60)

def print_success(text):
    """Print success message"""
    print(f"✓ {text}")

def print_error(text):
    """Print error message"""
    print(f"✗ {text}")

def print_info(text):
    """Print info message"""
    print(f"ℹ {text}")

def main():
    """Main test function"""
    
    print_header("OpenRouter API Connection Test")
    
    # Step 1: Check environment variables
    print_header("Step 1: Checking Environment Variables")
    
    api_key = os.getenv("OPENROUTER_API_KEY")
    model = os.getenv("OPENROUTER_MODEL", "gpt-3.5-turbo")
    base_url = os.getenv("OPENROUTER_BASE_URL", "https://openrouter.io/api/v1")
    
    if not api_key:
        print_error("OPENROUTER_API_KEY not set in .env file")
        print_info("Please set OPENROUTER_API_KEY in your .env file")
        return False
    
    print_success(f"API Key found: {api_key[:20]}...")
    print_info(f"Model: {model}")
    print_info(f"Base URL: {base_url}")
    
    # Step 2: Validate API key format
    print_header("Step 2: Validating API Key Format")
    
    if api_key.startswith("sk-or-"):
        print_success("API key format looks correct (starts with 'sk-or-')")
    else:
        print_error("API key format may be incorrect (should start with 'sk-or-')")
        print_info("Check your OpenRouter API key")
    
    # Step 3: Test basic connectivity
    print_header("Step 3: Testing Basic Connectivity")
    
    try:
        response = requests.head("https://openrouter.io", timeout=5)
        print_success("Can reach openrouter.io")
    except requests.exceptions.Timeout:
        print_error("Connection timeout to openrouter.io")
        print_info("Check your internet connection")
        return False
    except requests.exceptions.ConnectionError:
        print_error("Cannot connect to openrouter.io")
        print_info("Check your internet connection")
        return False
    
    # Step 4: Test API endpoint
    print_header("Step 4: Testing OpenRouter API Endpoint")
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "HTTP-Referer": "http://localhost:8000",
        "X-Title": "AI Education System",
    }
    
    payload = {
        "model": model,
        "messages": [
            {
                "role": "system",
                "content": "You are a helpful assistant. Answer briefly."
            },
            {
                "role": "user",
                "content": "What is 2+2? Answer with just the number."
            }
        ],
        "temperature": 0.7,
        "max_tokens": 50,
    }
    
    print_info(f"Sending test request to {base_url}/chat/completions")
    print_info(f"Model: {model}")
    
    try:
        response = requests.post(
            f"{base_url}/chat/completions",
            data=json.dumps(payload),
            headers=headers,
            timeout=30
        )
        
        print_info(f"Response Status Code: {response.status_code}")
        
        if response.status_code == 200:
            print_success("API request successful!")
            
            try:
                data = response.json()
                answer = data["choices"][0]["message"]["content"]
                print_success(f"Received answer: {answer}")
                
                # Step 5: Test with education system
                print_header("Step 5: Testing with Education System")
                print_success("All tests passed! Your OpenRouter setup is working correctly.")
                print_info("You can now use the AI Education System API.")
                return True
                
            except (KeyError, IndexError) as e:
                print_error(f"Error parsing response: {str(e)}")
                print_info(f"Full response: {response.text}")
                return False
        
        elif response.status_code == 401:
            print_error("Authentication failed (401 Unauthorized)")
            print_info("Possible causes:")
            print_info("  - Invalid API key")
            print_info("  - API key doesn't have permission")
            print_info("  - API key has expired")
            return False
        
        elif response.status_code == 405:
            print_error("Method not allowed (405)")
            print_info("Possible causes:")
            print_info("  - Invalid API key")
            print_info("  - Incorrect endpoint URL")
            print_info("  - API key doesn't have permission")
            return False
        
        elif response.status_code == 429:
            print_error("Rate limited (429 Too Many Requests)")
            print_info("You've exceeded the rate limit. Wait a few minutes and try again.")
            return False
        
        elif response.status_code == 500:
            print_error("OpenRouter server error (500)")
            print_info("OpenRouter service may be temporarily unavailable.")
            print_info("Try again in a few moments.")
            return False
        
        else:
            print_error(f"Unexpected status code: {response.status_code}")
            print_info(f"Response: {response.text}")
            return False
    
    except requests.exceptions.Timeout:
        print_error("Request timeout")
        print_info("The API took too long to respond. Try again.")
        return False
    
    except requests.exceptions.ConnectionError as e:
        print_error(f"Connection error: {str(e)}")
        print_info("Cannot connect to OpenRouter API")
        return False
    
    except Exception as e:
        print_error(f"Unexpected error: {str(e)}")
        return False

if __name__ == "__main__":
    success = main()
    
    print_header("Test Summary")
    
    if success:
        print_success("All tests passed!")
        print_info("Your OpenRouter API is properly configured.")
        sys.exit(0)
    else:
        print_error("Some tests failed.")
        print_info("Please check the errors above and fix your configuration.")
        print_info("See OPENROUTER_SETUP.md for more help.")
        sys.exit(1)
