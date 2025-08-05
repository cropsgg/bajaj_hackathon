#!/usr/bin/env python3
"""
Test script with a real publicly available PDF document.
This uses a sample insurance policy PDF for realistic testing.
"""

import requests
import json
import time

# Real publicly available insurance policy PDF for testing
SAMPLE_PDF_URL = "https://www.irdai.gov.in/ADMINCMS/cms/whatsNew_Layout.aspx?page=PageNo4140&flag=1"

# Alternative test URLs (use any publicly available PDF)
ALTERNATIVE_URLS = [
    "https://www.w3.org/WAI/ER/tests/xhtml/testfiles/resources/pdf/dummy.pdf",  # Simple test PDF
    "https://www.africau.edu/images/default/sample.pdf",  # Sample PDF
]

# Test data with authentication
TEST_REQUEST = {
    "documents": ALTERNATIVE_URLS[1],  # Using sample PDF
    "questions": [
        "What is this document about?",
        "What are the main topics covered?",
        "Are there any specific terms or conditions mentioned?",
        "What type of document is this?",
        "What information can you extract from this document?"
    ]
}

AUTH_HEADER = {
    "Authorization": "Bearer a2f387310984b739ae7e4accffad70a62e5673145dd05bc749dc913c0e6d0c42",
    "Content-Type": "application/json"
}

def test_with_real_document():
    """Test the system with a real PDF document."""
    print("🧪 Testing HackRX System with Real Document")
    print("=" * 50)
    
    # Test document accessibility first
    print(f"📄 Testing document URL: {TEST_REQUEST['documents']}")
    try:
        doc_response = requests.head(TEST_REQUEST['documents'], timeout=10)
        if doc_response.status_code == 200:
            print("✅ Document is accessible")
        else:
            print(f"⚠️  Document returned status: {doc_response.status_code}")
    except Exception as e:
        print(f"❌ Document accessibility test failed: {e}")
        return
    
    # Test the API endpoint
    api_url = "http://localhost:8000/hackrx/run"
    
    print(f"\n🚀 Sending request to: {api_url}")
    print(f"📝 Questions to test:")
    for i, q in enumerate(TEST_REQUEST['questions'], 1):
        print(f"   {i}. {q}")
    
    start_time = time.time()
    
    try:
        response = requests.post(
            api_url, 
            headers=AUTH_HEADER, 
            json=TEST_REQUEST,
            timeout=120  # 2 minutes timeout for processing
        )
        
        end_time = time.time()
        processing_time = end_time - start_time
        
        print(f"\n⏱️  Total processing time: {processing_time:.2f} seconds")
        print(f"📊 Status Code: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print("\n🎉 SUCCESS! Here are the answers:")
            print("-" * 40)
            
            for i, answer in enumerate(result.get('answers', []), 1):
                print(f"\nQ{i}: {TEST_REQUEST['questions'][i-1]}")
                print(f"A{i}: {answer}")
                print("-" * 40)
                
            print(f"\n✅ Test completed successfully!")
            print(f"📈 Performance: {len(TEST_REQUEST['questions'])} questions in {processing_time:.2f}s")
            print(f"⚡ Average: {processing_time/len(TEST_REQUEST['questions']):.2f}s per question")
            
        else:
            print(f"\n❌ API Error: {response.status_code}")
            try:
                error_detail = response.json()
                print(f"Error details: {json.dumps(error_detail, indent=2)}")
            except:
                print(f"Raw response: {response.text}")
                
    except requests.exceptions.ConnectionError:
        print("\n❌ Connection failed!")
        print("Make sure the server is running:")
        print("   uvicorn app:app --reload")
        
    except requests.exceptions.Timeout:
        print("\n⏰ Request timed out!")
        print("The document might be too large or processing is taking longer than expected.")
        
    except Exception as e:
        print(f"\n❌ Unexpected error: {str(e)}")

def test_authentication():
    """Test the authentication mechanism."""
    print("\n🔐 Testing Authentication")
    print("-" * 30)
    
    # Test with wrong token
    wrong_auth = {
        "Authorization": "Bearer wrong-token",
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.post(
            "http://localhost:8000/hackrx/run",
            headers=wrong_auth,
            json={"documents": "test", "questions": ["test"]},
            timeout=10
        )
        
        if response.status_code == 401:
            print("✅ Authentication properly rejects invalid tokens")
        else:
            print(f"⚠️  Unexpected response for invalid token: {response.status_code}")
            
    except requests.exceptions.ConnectionError:
        print("❌ Server not running - skipping auth test")
    except Exception as e:
        print(f"❌ Auth test error: {e}")

if __name__ == "__main__":
    test_with_real_document()
    test_authentication()