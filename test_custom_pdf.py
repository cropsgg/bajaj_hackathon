#!/usr/bin/env python3
"""
Custom PDF Test Script - Easy to update with your own PDF URLs
Usage: python test_custom_pdf.py [PDF_URL]
"""

import requests
import json
import sys
import time

# Default PDF URL (replace this with your PDF URL)
DEFAULT_PDF_URL = "https://www.w3.org/WAI/ER/tests/xhtml/testfiles/resources/pdf/dummy.pdf"

# Authentication header
AUTH_HEADER = {
    "Authorization": "Bearer a2f387310984b739ae7e4accffad70a62e5673145dd05bc749dc913c0e6d0c42",
    "Content-Type": "application/json"
}

def test_custom_pdf(pdf_url=None):
    """Test the system with a custom PDF URL."""
    
    # Use command line argument or default
    if pdf_url is None:
        pdf_url = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_PDF_URL
    
    print("🧪 Testing HackRX System with Custom PDF")
    print("=" * 50)
    print(f"📄 PDF URL: {pdf_url}")
    
    # Test document accessibility first
    try:
        doc_response = requests.head(pdf_url, timeout=10, allow_redirects=True)
        print(f"📊 Document Status: {doc_response.status_code}")
        if doc_response.status_code == 200:
            print("✅ Document is accessible")
        else:
            print(f"⚠️  Document returned status: {doc_response.status_code}")
    except Exception as e:
        print(f"❌ Document accessibility error: {e}")
        return

    # Test questions - customize these for your document type
    questions = [
        "What is this document about?",
        "What are the main topics covered?", 
        "Are there any specific terms or conditions mentioned?",
        "What key information can you extract?",
        "What is the document structure?"
    ]
    
    # If it looks like an insurance policy, ask insurance-specific questions
    if "insurance" in pdf_url.lower() or "policy" in pdf_url.lower():
        questions = [
            "What type of insurance policy is this?",
            "What are the coverage details?",
            "Are there any waiting periods mentioned?",
            "What exclusions are listed?",
            "What is the claim process?",
            "What are the premium details?",
            "Are there any deductibles mentioned?"
        ]
    
    test_request = {
        "documents": pdf_url,
        "questions": questions
    }
    
    print(f"\n🚀 Sending request to API...")
    print(f"📝 Testing {len(questions)} questions...")
    
    start_time = time.time()
    
    try:
        response = requests.post(
            "http://localhost:8000/hackrx/run",
            headers=AUTH_HEADER,
            json=test_request,
            timeout=120
        )
        
        end_time = time.time()
        processing_time = end_time - start_time
        
        print(f"\n⏱️  Processing time: {processing_time:.2f} seconds")
        print(f"📊 Status Code: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print("\n🎉 SUCCESS! Here are the answers:")
            print("=" * 60)
            
            for i, (question, answer) in enumerate(zip(questions, result.get('answers', [])), 1):
                print(f"\n❓ Q{i}: {question}")
                print(f"✅ A{i}: {answer}")
                print("-" * 40)
            
            print(f"\n📈 Performance Summary:")
            print(f"   • Total time: {processing_time:.2f} seconds")
            print(f"   • Questions: {len(questions)}")
            print(f"   • Avg per question: {processing_time/len(questions):.2f}s")
            print(f"   • Token efficiency: Optimized for GPT-3.5-Turbo")
            
        else:
            print(f"\n❌ API Error: {response.status_code}")
            try:
                error_detail = response.json()
                print(f"📝 Error details:")
                print(json.dumps(error_detail, indent=2))
            except:
                print(f"📝 Raw response: {response.text}")
                
    except requests.exceptions.ConnectionError:
        print("\n❌ Connection failed!")
        print("🔧 Make sure the server is running:")
        print("   source hackrx_env/bin/activate")
        print("   uvicorn app:app --reload")
        
    except requests.exceptions.Timeout:
        print("\n⏰ Request timed out!")
        print("📄 The document might be large or processing is taking longer than expected.")
        
    except Exception as e:
        print(f"\n❌ Unexpected error: {str(e)}")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        print(f"🎯 Using provided PDF URL: {sys.argv[1]}")
        test_custom_pdf(sys.argv[1])
    else:
        print(f"🎯 Using default PDF URL. To test your own PDF:")
        print(f"   python test_custom_pdf.py 'YOUR_PDF_URL_HERE'")
        print()
        test_custom_pdf()