#!/usr/bin/env python
"""Test API key retrieval and Streamlit secrets"""
import os
import sys

# Test 1: Check environment variable
env_key = os.getenv('GOOGLE_API_KEY')
print(f"Test 1 - Environment Variable: {env_key if env_key else 'NOT SET'}")

# Test 2: Check Streamlit secrets
try:
    import streamlit as st
    print(f"Streamlit imported successfully")
    print(f"Has secrets attr: {hasattr(st, 'secrets')}")
    
    if hasattr(st, 'secrets'):
        print(f"Secrets type: {type(st.secrets)}")
        print(f"Secrets dict: {dict(st.secrets)}")
        
        if 'GOOGLE_API_KEY' in st.secrets:
            key = st.secrets['GOOGLE_API_KEY']
            print(f"Test 2 - Streamlit Secrets: {key}")
        else:
            print("Test 2 - Streamlit Secrets: KEY NOT FOUND")
    else:
        print("Test 2 - Streamlit Secrets: NO SECRETS OBJECT")
except ImportError as e:
    print(f"Cannot import streamlit: {e}")
except Exception as e:
    print(f"Test 2 - Error: {e}")

# Test 3: Manual TOML parsing
try:
    import toml
    with open('.streamlit/secrets.toml', 'r') as f:
        secrets = toml.load(f)
    print(f"Test 3 - Direct TOML Parse: {secrets.get('GOOGLE_API_KEY', 'NOT FOUND')}")
except Exception as e:
    print(f"Test 3 - Error: {e}")

# Test 4: Using our secure function
try:
    from utils_ocr_email import get_secure_api_key
    key = get_secure_api_key()
    print(f"Test 4 - get_secure_api_key(): {key}")
except Exception as e:
    print(f"Test 4 - Error: {e}")
