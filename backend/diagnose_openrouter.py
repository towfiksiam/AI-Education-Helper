#!/usr/bin/env python3
"""
Advanced diagnostic script for OpenRouter API issues.
Helps identify why 405 errors occur.
"""

import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()

def print_section(title):
    print(f"\n{'='*70}")
    print(f"  {title}")
    print(f"{'='*70}\n")

def test_api_key_validity():
    """Test if API key is valid by checking account info"""
    print_section("Testing API Key Validity")
    
    api_key = os.getenv("OPENROUTER_API_KEY")
    
    if not api_key:
        print("❌ ERROR: OPENROUTER_API_KEY not set in .env")
        return False
    
    print(f"API Key: {api_key[:30]}...")
    
    # Try to get account info
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    
    try:
        print("\n1. Testing with account info endpoint...")
        response = requests.get(
            "https://openrouter.io/api/v1/auth/key",
            headers=headers,
            timeout=10
        )
        
        print(f"   Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"   ✓ API Key is valid!")
            print(f"   Account: {data}")
            return True
        else:
            print(f"   ✗ Status {response.status_code}")
            print(f"   Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"   ✗ Error: {str(e)}")
        return False

def test_simple_request():
    """Test with the simplest possible request"""
    print_section("Testing Simple Request")
    
    api_key = os.getenv("OPENROUTER_API_KEY")
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    
    payload = {
        "model": "gpt-3.5-turbo",
        "messages": [
            {"role": "user", "content": "Hi"}
        ]
    }
    
    print("Request Details:")
    print(f"  URL: https://openrouter.io/api/v1/chat/completions")
    print(f"  Method: POST")
    print(f"  Headers: {json.dumps(headers, indent=2)}")
    print(f"  Payload: {json.dumps(payload, indent=2)}")
    
    try:
        print("\nSending request...")
        response = requests.post(
            "https://openrouter.io/api/v1/chat/completions",
            data=json.dumps(payload),
            headers=headers,
            timeout=30
        )
        
        print(f"\nResponse Status: {response.status_code}")
        print(f"Response Headers: {dict(response.headers)}")
        print(f"Response Body: {response.text[:500]}")
        
        if response.status_code == 200:
            print("\n✓ Request successful!")
            return True
        elif response.status_code == 401:
            print("\n❌ 401 Unauthorized - Invalid API key")
            return False
        elif response.status_code == 405:
            print("\n❌ 405 Method Not Allowed")
            print("   Possible causes:")
            print("   - Invalid API key")
            print("   - API key has no credits")
            print("   - API key is restricted")
            print("   - Account is suspended")
            return False
        else:
            print(f"\n❌ Unexpected status: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        return False

def test_with_different_models():
    """Test with different model names"""
    print_section("Testing Different Model Names")
    
    api_key = os.getenv("OPENROUTER_API_KEY")
    
    models_to_test = [
        "gpt-3.5-turbo",
        "openai/gpt-3.5-turbo",
        "gpt-4",
        "openai/gpt-4",
        "meta-llama/llama-2-70b-chat",
    ]
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    
    for model in models_to_test:
        print(f"\nTesting model: {model}")
        
        payload = {
            "model": model,
            "messages": [{"role": "user", "content": "Hi"}]
        }
        
        try:
            response = requests.post(
                "https://openrouter.io/api/v1/chat/completions",
                data=json.dumps(payload),
                headers=headers,
                timeout=10
            )
            
            if response.status_code == 200:
                print(f"  ✓ {model} works!")
            else:
                print(f"  ✗ {model} - Status {response.status_code}")
                
        except Exception as e:
            print(f"  ✗ {model} - Error: {str(e)}")

def test_with_curl_equivalent():
    """Show equivalent curl command"""
    print_section("Equivalent cURL Command")
    
    api_key = os.getenv("OPENROUTER_API_KEY")
    
    curl_cmd = f"""curl -X POST "https://openrouter.io/api/v1/chat/completions" \\
  -H "Authorization: Bearer {api_key}" \\
  -H "Content-Type: application/json" \\
  -d '{{
    "model": "gpt-3.5-turbo",
    "messages": [
      {{"role": "user", "content": "What is 2+2?"}}
    ]
  }}'"""
    
    print("Run this command to test:")
    print(curl_cmd)
    print("\nOr on Windows (PowerShell):")
    
    ps_cmd = f"""$headers = @{{
    "Authorization" = "Bearer {api_key}"
    "Content-Type" = "application/json"
}}

$body = @{{
    model = "gpt-3.5-turbo"
    messages = @(@{{
        role = "user"
        content = "What is 2+2?"
    }})
}} | ConvertTo-Json

Invoke-WebRequest -Uri "https://openrouter.io/api/v1/chat/completions" `
    -Method POST `
    -Headers $headers `
    -Body $body"""
    
    print(ps_cmd)

def check_openrouter_status():
    """Check OpenRouter service status"""
    print_section("Checking OpenRouter Service Status")
    
    try:
        print("Checking if openrouter.io is reachable...")
        response = requests.head("https://openrouter.io", timeout=5)
        print(f"✓ openrouter.io is reachable (Status: {response.status_code})")
        
        print("\nChecking API endpoint...")
        response = requests.head("https://openrouter.io/api/v1/chat/completions", timeout=5)
        print(f"✓ API endpoint is reachable (Status: {response.status_code})")
        
    except Exception as e:
        print(f"✗ Error: {str(e)}")

def main():
    print("\n" + "="*70)
    print("  OpenRouter API Diagnostic Tool")
    print("="*70)
    
    # Check connectivity
    check_openrouter_status()
    
    # Test API key
    key_valid = test_api_key_validity()
    
    # Test simple request
    request_works = test_simple_request()
    
    # Test different models
    test_with_different_models()
    
    # Show curl equivalent
    test_with_curl_equivalent()
    
    # Summary
    print_section("Diagnostic Summary")
    
    if request_works:
        print("✓ Everything looks good! Your API key is working.")
    elif key_valid:
        print("⚠ API key is valid but requests are failing.")
        print("  Possible causes:")
        print("  - Account has no credits")
        print("  - Account is suspended")
        print("  - Rate limit exceeded")
    else:
        print("❌ API key appears to be invalid or restricted.")
        print("  Solutions:")
        print("  1. Generate a new API key from https://openrouter.ai/")
        print("  2. Verify your account has credits")
        print("  3. Check if your account is active")
        print("  4. Try a different model")
    
    print("\nNext steps:")
    print("1. Check your OpenRouter account: https://openrouter.ai/account")
    print("2. Verify you have credits available")
    print("3. Generate a new API key if needed")
    print("4. Update your .env file with the new key")
    print("5. Restart the application")

if __name__ == "__main__":
    main()
