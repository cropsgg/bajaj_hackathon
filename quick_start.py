#!/usr/bin/env python3
"""
Quick Start Script for HackRX System
This script helps you set up and test the system quickly.
"""

import os
import sys
import subprocess
import time

def check_and_install_packages():
    """Install required packages if not present."""
    print("📦 Checking and installing required packages...")
    
    try:
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], 
                      check=True, capture_output=True, text=True)
        print("✅ All packages installed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Package installation failed: {e}")
        print("Try running manually: pip install -r requirements.txt")
        return False

def check_openai_key():
    """Check and prompt for OpenAI API key."""
    api_key = os.getenv('OPENAI_API_KEY')
    
    if not api_key or api_key == 'sk-your-openai-api-key-here':
        print("\n🔑 OpenAI API Key Setup Required")
        print("-" * 40)
        print("1. Go to: https://platform.openai.com/api-keys")
        print("2. Create a new API key")
        print("3. Set it as environment variable:")
        print("   export OPENAI_API_KEY='sk-your-actual-key-here'")
        print("\nOr edit the .env file and restart this script.")
        return False
    else:
        print("✅ OpenAI API key is configured")
        return True

def start_server():
    """Start the FastAPI server."""
    print("\n🚀 Starting FastAPI server...")
    print("Server will start on: http://localhost:8000")
    print("API endpoint: POST /hackrx/run")
    print("\nPress Ctrl+C to stop the server")
    print("-" * 50)
    
    try:
        subprocess.run([sys.executable, "-m", "uvicorn", "app:app", "--reload"], check=True)
    except KeyboardInterrupt:
        print("\n🛑 Server stopped by user")
    except subprocess.CalledProcessError as e:
        print(f"❌ Server failed to start: {e}")
        print("Make sure all dependencies are installed!")

def run_quick_test():
    """Run a quick test to verify everything works."""
    print("\n🧪 Running Quick Test")
    print("-" * 30)
    
    # Give server time to start
    time.sleep(2)
    
    try:
        result = subprocess.run([sys.executable, "test_with_real_doc.py"], 
                              capture_output=True, text=True, timeout=60)
        print(result.stdout)
        if result.stderr:
            print("Errors:", result.stderr)
    except subprocess.TimeoutExpired:
        print("⏰ Test timed out - this is normal for the first run")
    except Exception as e:
        print(f"❌ Test failed: {e}")

def main():
    """Main quick start workflow."""
    print("🎯 HackRX Quick Start")
    print("=" * 30)
    
    # Step 1: Install packages
    if not check_and_install_packages():
        return
    
    # Step 2: Check API key
    if not check_openai_key():
        return
    
    print("\n✅ Setup completed! Choose an option:")
    print("1. Start server only")
    print("2. Start server and run test")
    print("3. Exit")
    
    choice = input("\nEnter choice (1-3): ").strip()
    
    if choice == "1":
        start_server()
    elif choice == "2":
        import threading
        # Start server in background
        server_thread = threading.Thread(target=start_server)
        server_thread.daemon = True
        server_thread.start()
        
        # Wait a bit then run test
        time.sleep(5)
        run_quick_test()
    else:
        print("👋 Exiting quick start")

if __name__ == "__main__":
    main()