#!/usr/bin/env python3
"""
Setup script for HackRX Intelligent Query-Retrieval System
Run this to verify your environment is correctly configured.
"""

import os
import sys
import subprocess

def check_python_version():
    """Check if Python version is 3.10+"""
    version = sys.version_info
    print(f"Python version: {version.major}.{version.minor}.{version.micro}")
    
    if version.major == 3 and version.minor >= 10:
        print("✅ Python version is compatible")
        return True
    else:
        print("❌ Python 3.10+ required")
        return False

def check_openai_key():
    """Check if OpenAI API key is set"""
    api_key = os.getenv('OPENAI_API_KEY')
    
    if api_key:
        print("✅ OPENAI_API_KEY is set")
        return True
    else:
        print("❌ OPENAI_API_KEY not found in environment")
        print("   Set it with: export OPENAI_API_KEY='sk-your-key-here'")
        return False

def check_packages():
    """Check if required packages are installed"""
    required_packages = [
        'fastapi', 'uvicorn', 'langchain', 'langchain-openai', 
        'openai', 'faiss-cpu', 'pypdf', 'requests', 'pydantic'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
            print(f"✅ {package}")
        except ImportError:
            print(f"❌ {package}")
            missing_packages.append(package)
    
    if missing_packages:
        print(f"\nInstall missing packages with:")
        print(f"pip install {' '.join(missing_packages)}")
        return False
    
    return True

def run_setup_check():
    """Run all setup checks"""
    print("HackRX System Setup Verification")
    print("=" * 40)
    
    checks = [
        check_python_version(),
        check_openai_key(),
        check_packages()
    ]
    
    if all(checks):
        print("\n🎉 All checks passed! You're ready to run the system.")
        print("\nNext steps:")
        print("1. Start the server: uvicorn app:app --reload")
        print("2. Test with: python tests/test_sample.py")
    else:
        print("\n⚠️  Some checks failed. Please fix the issues above.")

if __name__ == "__main__":
    run_setup_check()