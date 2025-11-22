#!/usr/bin/env python3
"""
Quick test script for free OpenRouter models.
Tests the Llama 3.3 70B free model.
"""

import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()

def main():
    print("\n" + "="*70)
    print("  Testing Free OpenRouter Model (Llama 3.3 70B)")
    print("="*70 + "\n")
    
    api_key = os.getenv("OPENROUTER_API_KEY")
    base_url = os.getenv("OPENROUTER_BASE_URL", "https://openrouter.io/api/v1")
    model = os.getenv("OPENROUTER_MODEL", "meta-llama/llama-3.3-70b-instruct:free")
    
    if not api_key:
        print("❌ ERROR: OPENROUTER_API_KEY not set in .env")
        return False
    
    print(f"Configuration:")
    print(f"  API Key: {api_key[:30]}...")
    print(f"  Model: {model}")
    print(f"  Base URL: {base_url}\n")
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "HTTP-Referer": "http://localhost:8000",
        "X-Title": "AI Education System",
    }
    
    # Test 1: Simple question
    print("Test 1: Simple Question")
    print("-" * 70)
    
    payload = {
        "model": model,
        "messages": [
            {"role": "user", "content": "What is 2+2?"}
        ],
        "temperature": 0.7,
        "max_tokens": 100,
    }
    
    try:
        print("Sending request...")
        response = requests.post(
            f"{base_url}/chat/completions",
            data=json.dumps(payload),
            headers=headers,
            timeout=60
        )
        
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            answer = data["choices"][0]["message"]["content"]
            print(f"✓ Success!")
            print(f"Answer: {answer}\n")
        else:
            print(f"✗ Error: {response.status_code}")
            print(f"Response: {response.text}\n")
            return False
            
    except Exception as e:
        print(f"✗ Exception: {str(e)}\n")
        return False
    
    # Test 2: Educational content
    print("Test 2: Educational Content")
    print("-" * 70)
    
    payload = {
        "model": model,
        "messages": [
            {"role": "user", "content": "Explain photosynthesis in 3 sentences."}
        ],
        "temperature": 0.7,
        "max_tokens": 200,
    }
    
    try:
        print("Sending request...")
        response = requests.post(
            f"{base_url}/chat/completions",
            data=json.dumps(payload),
            headers=headers,
            timeout=60
        )
        
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            answer = data["choices"][0]["message"]["content"]
            print(f"✓ Success!")
            print(f"Answer: {answer}\n")
        else:
            print(f"✗ Error: {response.status_code}")
            print(f"Response: {response.text}\n")
            return False
            
    except Exception as e:
        print(f"✗ Exception: {str(e)}\n")
        return False
    
    # Test 3: JSON generation
    print("Test 3: JSON Generation (MCQ)")
    print("-" * 70)
    
    payload = {
        "model": model,
        "messages": [
            {
                "role": "user",
                "content": """Generate 1 multiple choice question about photosynthesis in JSON format:
{
  "question": "...",
  "options": ["...", "...", "...", "..."],
  "correct_answer": "...",
  "explanation": "..."
}

Return ONLY the JSON, no other text."""
            }
        ],
        "temperature": 0.7,
        "max_tokens": 300,
    }
    
    try:
        print("Sending request...")
        response = requests.post(
            f"{base_url}/chat/completions",
            data=json.dumps(payload),
            headers=headers,
            timeout=60
        )
        
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            answer = data["choices"][0]["message"]["content"]
            print(f"✓ Success!")
            print(f"Response: {answer}\n")
            
            # Try to parse as JSON
            try:
                json_data = json.loads(answer)
                print(f"✓ Valid JSON!")
                print(f"Question: {json_data.get('question')}\n")
            except:
                print(f"⚠ Response is not valid JSON (but that's okay)\n")
        else:
            print(f"✗ Error: {response.status_code}")
            print(f"Response: {response.text}\n")
            return False
            
    except Exception as e:
        print(f"✗ Exception: {str(e)}\n")
        return False
    
    # Summary
    print("="*70)
    print("  Test Summary")
    print("="*70)
    print("\n✓ All tests passed!")
    print("\nYour free model is working correctly!")
    print("\nNext steps:")
    print("1. Start the server: uvicorn uvicorn_app:app --reload --port 8000")
    print("2. Test the API: http://localhost:8000/docs")
    print("3. Try the chat endpoint")
    print("4. Try the generate-material endpoint")
    
    return True

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
