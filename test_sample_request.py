#!/usr/bin/env python3
"""
HackRX Sample Request Tester
Test the system with the exact format provided by the user.
Supports testing with multiple different PDFs and question sets.
"""

import requests
import json
import time
import sys
from pathlib import Path

# API Configuration
API_URL = "http://localhost:8000/hackrx/run"
AUTH_TOKEN = "a2f387310984b739ae7e4accffad70a62e5673145dd05bc749dc913c0e6d0c42"

HEADERS = {
    "Content-Type": "application/json",
    "Accept": "application/json", 
    "Authorization": f"Bearer {AUTH_TOKEN}"
}

# Sample request data (as provided by user)
SAMPLE_REQUEST = {
    "documents": "https://hackrx.blob.core.windows.net/assets/policy.pdf?sv=2023-01-03&st=2025-07-04T09%3A11%3A24Z&se=2027-07-05T09%3A11%3A00Z&sr=b&sp=r&sig=N4a9OU0w0QXO6AOIBiu4bpl7AXvEZogeT%2FjUHNO7HzQ%3D",
    "questions": [
        "What is the grace period for premium payment under the National Parivar Mediclaim Plus Policy?",
        "What is the waiting period for pre-existing diseases (PED) to be covered?",
        "Does this policy cover maternity expenses, and what are the conditions?",
        "What is the waiting period for cataract surgery?",
        "Are the medical expenses for an organ donor covered under this policy?",
        "What is the No Claim Discount (NCD) offered in this policy?",
        "Is there a benefit for preventive health check-ups?",
        "How does the policy define a 'Hospital'?",
        "What is the extent of coverage for AYUSH treatments?",
        "Are there any sub-limits on room rent and ICU charges for Plan A?"
    ]
}

# Alternative test PDFs with corresponding question sets
TEST_SCENARIOS = {
    "insurance_policy": {
        "documents": "https://www.w3.org/WAI/ER/tests/xhtml/testfiles/resources/pdf/dummy.pdf",
        "questions": [
            "What type of insurance policy is this?",
            "What are the coverage details?",
            "Are there any waiting periods mentioned?",
            "What exclusions are listed?",
            "What is the claim process?"
        ]
    },
    "sample_document": {
        "documents": "https://www.adobe.com/support/products/enterprise/knowledgecenter/media/c4611_sample_explain.pdf",
        "questions": [
            "What is this document about?",
            "What are the main sections?",
            "What information is provided?",
            "What is the document structure?"
        ]
    }
}

def test_document_accessibility(url):
    """Test if the document URL is accessible."""
    print(f"📄 Testing document accessibility: {url}")
    try:
        response = requests.head(url, timeout=15, allow_redirects=True)
        print(f"📊 Status: {response.status_code}")
        
        if response.status_code == 200:
            print("✅ Document is accessible")
            # Try to get content length if available
            content_length = response.headers.get('content-length')
            if content_length:
                size_mb = int(content_length) / (1024 * 1024)
                print(f"📏 Document size: {size_mb:.2f} MB")
            return True
        else:
            print(f"⚠️  Document returned status: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Document accessibility error: {e}")
        return False

def send_request(request_data, scenario_name="Custom"):
    """Send the request to the API and process response."""
    print(f"\n🚀 Testing Scenario: {scenario_name}")
    print("=" * 50)
    
    # First test document accessibility
    if not test_document_accessibility(request_data["documents"]):
        print("🔄 Continuing with API test anyway...\n")
    
    print(f"📝 Questions to test: {len(request_data['questions'])}")
    for i, question in enumerate(request_data['questions'], 1):
        print(f"   {i}. {question[:80]}{'...' if len(question) > 80 else ''}")
    
    print(f"\n🔗 Sending POST request to: {API_URL}")
    
    start_time = time.time()
    
    try:
        response = requests.post(
            API_URL,
            headers=HEADERS,
            json=request_data,
            timeout=180  # 3 minutes timeout for large documents
        )
        
        end_time = time.time()
        processing_time = end_time - start_time
        
        print(f"\n⏱️  Total processing time: {processing_time:.2f} seconds")
        print(f"📊 HTTP Status Code: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print("\n🎉 SUCCESS! API Response:")
            print("=" * 60)
            
            answers = result.get('answers', [])
            
            for i, (question, answer) in enumerate(zip(request_data['questions'], answers), 1):
                print(f"\n❓ Q{i}: {question}")
                print(f"✅ A{i}: {answer}")
                print("-" * 50)
            
            # Performance metrics
            print(f"\n📈 Performance Summary:")
            print(f"   • Total processing time: {processing_time:.2f} seconds")
            print(f"   • Questions processed: {len(request_data['questions'])}")
            print(f"   • Average per question: {processing_time/len(request_data['questions']):.2f}s")
            print(f"   • Answers received: {len(answers)}")
            
            # Save results
            timestamp = int(time.time())
            results_file = f"test_results_{scenario_name}_{timestamp}.json"
            with open(results_file, 'w') as f:
                json.dump({
                    "scenario": scenario_name,
                    "request": request_data,
                    "response": result,
                    "processing_time": processing_time,
                    "timestamp": timestamp
                }, f, indent=2)
            print(f"💾 Results saved to: {results_file}")
            
            return True
            
        else:
            print(f"\n❌ API Error: {response.status_code}")
            try:
                error_detail = response.json()
                print(f"📝 Error details:")
                print(json.dumps(error_detail, indent=2))
            except:
                print(f"📝 Raw response: {response.text}")
            return False
                
    except requests.exceptions.ConnectionError:
        print("\n❌ Connection failed!")
        print("🔧 Make sure the server is running:")
        print("   source hackrx_env/bin/activate")
        print("   uvicorn app:app --reload")
        return False
        
    except requests.exceptions.Timeout:
        print(f"\n⏰ Request timed out after {processing_time:.2f} seconds!")
        print("📄 The document might be large or processing is taking longer than expected.")
        return False
        
    except Exception as e:
        print(f"\n❌ Unexpected error: {str(e)}")
        return False

def test_from_file(file_path):
    """Test using a JSON file."""
    try:
        with open(file_path, 'r') as f:
            request_data = json.load(f)
        print(f"📂 Loaded request from: {file_path}")
        return send_request(request_data, f"File_{Path(file_path).stem}")
    except Exception as e:
        print(f"❌ Error loading file {file_path}: {e}")
        return False

def main():
    """Main test function."""
    print("🧪 HackRX Sample Request Tester")
    print("=" * 40)
    
    if len(sys.argv) > 1:
        # Test from provided JSON file
        file_path = sys.argv[1]
        if Path(file_path).exists():
            test_from_file(file_path)
        else:
            print(f"❌ File not found: {file_path}")
    else:
        # Test all scenarios
        print("🎯 Testing all scenarios...")
        
        # Test the main sample request
        print("\n" + "="*60)
        send_request(SAMPLE_REQUEST, "Main_Sample_Request")
        
        # Test alternative scenarios
        for scenario_name, request_data in TEST_SCENARIOS.items():
            print("\n" + "="*60)
            send_request(request_data, scenario_name)
        
        print(f"\n✅ All tests completed!")
        print(f"📁 Check generated test_results_*.json files for detailed results")

if __name__ == "__main__":
    main()