"""
Sample test file for validating the HackRX system.
This demonstrates how to test the system with sample data.
"""

import requests
import json

# Sample test data
SAMPLE_REQUEST = {
    "documents": "https://hackrx.blob.core.windows.net/assets/policy.pdf?sv=2023-01-03&st=2025-07-04T09%3A11%3A24Z&se=2027-07-05T09%3A11%3A00Z&sr=b&sp=r&sig=N4a9OU0w0QXO6AOIBiu4bpl7AXvEZogeT%2FjUHNO7HzQ%3D",  # Replace with actual PDF URL
    "questions": [
        "What is the waiting period for maternity benefits?",
        "Are dental treatments covered under this policy?",
        "What is the maximum sum insured?",
        "Are pre-existing diseases covered?",
        "What is the claim settlement process?"
    ]
}

AUTH_HEADER = {
    "Authorization": "Bearer a2f387310984b739ae7e4accffad70a62e5673145dd05bc749dc913c0e6d0c42",
    "Content-Type": "application/json"
}

def test_local_endpoint():
    """Test the local FastAPI endpoint."""
    url = "http://localhost:8000/hackrx/run"
    
    try:
        response = requests.post(url, headers=AUTH_HEADER, json=SAMPLE_REQUEST)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        
        if response.status_code == 200:
            print("✅ Test passed!")
        else:
            print("❌ Test failed!")
            
    except requests.exceptions.ConnectionError:
        print("❌ Connection failed. Make sure the server is running on localhost:8000")
    except Exception as e:
        print(f"❌ Test error: {str(e)}")

if __name__ == "__main__":
    print("Testing HackRX Intelligent Query-Retrieval System")
    print("=" * 50)
    test_local_endpoint()