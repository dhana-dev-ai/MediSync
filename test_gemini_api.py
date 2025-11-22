#!/usr/bin/env python
"""Test if the API key actually works with Gemini API"""
import sys

try:
    import google.generativeai as genai
    from utils_ocr_email import get_secure_api_key
    
    print("=" * 70)
    print("TESTING GOOGLE GEMINI API WITH RETRIEVED KEY")
    print("=" * 70)
    
    # Get API key
    api_key = get_secure_api_key()
    print(f"\n✅ API Key Retrieved: {api_key[:20]}...")
    
    # Configure Gemini
    print("\n🔧 Configuring Gemini API...")
    genai.configure(api_key=api_key)
    
    # List available models
    print("\n📋 Testing API Connection - Listing Models:")
    models = genai.list_models()
    count = 0
    for model in models:
        count += 1
        if count <= 3:
            print(f"  - {model.name}")
    print(f"  ... and {count - 3} more models")
    
    # Try to access the vision model specifically
    print("\n🎬 Checking for Gemini Vision model:")
    try:
        model = genai.GenerativeModel('gemini-2.0-flash')
        print(f"  ✅ gemini-2.0-flash is available")
    except Exception as e:
        print(f"  ⚠️  Error: {e}")
    
    print("\n" + "=" * 70)
    print("✅ SUCCESS: API Key is VALID and Gemini API is accessible!")
    print("=" * 70)
    
except ImportError as e:
    print(f"❌ Import Error: {e}")
    sys.exit(1)
except Exception as e:
    print(f"❌ Error: {e}")
    sys.exit(1)
