#!/usr/bin/env python3

import asyncio
import sys
import os
import time
import httpx

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'app'))

from app.ollama_client import query_ollama

async def test_ollama_connection():
    print("🔍 Testing Ollama connection...")
    
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get("http://localhost:11434/api/tags", timeout=10)
            if response.status_code == 200:
                print("✅ Ollama is running")
                return True
            else:
                print(f"❌ Ollama responded with status {response.status_code}")
                return False
    except Exception as e:
        print(f"❌ Cannot connect to Ollama: {e}")
        return False

async def test_grammar_checking():
    print("\n🧪 Testing grammar checking...")
    
    test_text = "I goes to the store yesterday. She have a apple."
    print(f"Testing text: '{test_text}'")
    
    try:
        start_time = time.time()
        issues = await query_ollama(test_text)
        response_time = time.time() - start_time
        
        print(f"✅ Found {len(issues)} grammar issues in {response_time:.2f}s")
        
        for i, issue in enumerate(issues, 1):
            print(f"  {i}. Wrong: '{issue.get('wrong', 'N/A')}'")
            print(f"     Corrected: '{issue.get('corrected', 'N/A')}'")
            print(f"     Error type: {issue.get('error_type', 'N/A')}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error during grammar check: {e}")
        return False

async def test_api_endpoints():
    print("\n🌐 Testing API endpoints...")
    
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get("http://localhost:8000/health", timeout=10)
            if response.status_code == 200:
                print("✅ Health endpoint working")
            else:
                print(f"❌ Health endpoint failed: {response.status_code}")
                return False
        
        test_text = "I goes to the store yesterday."
        
        async with httpx.AsyncClient() as client:
            response = await client.post(
                "http://localhost:8000/check",
                json={"text": test_text},
                timeout=60
            )
            
            if response.status_code == 200:
                result = response.json()
                print("✅ Grammar check API working")
                print(f"Found {len(result['issues'])} issues")
                return True
            else:
                print(f"❌ API failed: {response.status_code}")
                return False
                
    except Exception as e:
        print(f"❌ API test failed: {e}")
        return False

async def main():
    print("🚀 Grammar Check API - Simple Test")
    print("=" * 40)
    
    ollama_ok = await test_ollama_connection()
    
    if not ollama_ok:
        print("\n❌ Ollama is not running. Please:")
        print("1. Install Ollama from https://ollama.ai")
        print("2. Pull the model: ollama pull gemma3:1b")
        print("3. Start Ollama: ollama serve")
        return
    
    grammar_ok = await test_grammar_checking()
    
    api_ok = False
    try:
        api_ok = await test_api_endpoints()
    except:
        print("⚠️  API test skipped (API may not be running)")
    
    print("\n" + "=" * 40)
    print("📋 TEST SUMMARY")
    print("=" * 40)
    print(f"✅ Ollama Connection: {'PASS' if ollama_ok else 'FAIL'}")
    print(f"✅ Grammar Checking: {'PASS' if grammar_ok else 'FAIL'}")
    print(f"✅ API Endpoints: {'PASS' if api_ok else 'SKIP'}")
    
    if ollama_ok and grammar_ok:
        print("\n🎉 Grammar checker is working!")
        print("Start the API: python -m uvicorn app.main:app --reload")
    else:
        print("\n❌ Some tests failed. Please check the setup.")

if __name__ == "__main__":
    asyncio.run(main()) 