#!/usr/bin/env python3
"""
Script to run all test cases and populate the cache.
"""

import requests
import json
import time

# API configuration
BASE_URL = "http://127.0.0.1:8000"
AUTH_TOKEN = "a2f387310984b739ae7e4accffad70a62e5673145dd05bc749dc913c0e6d0c42"

HEADERS = {
    "Content-Type": "application/json",
    "Accept": "application/json",
    "Authorization": f"Bearer {AUTH_TOKEN}"
}

# All test cases
TEST_CASES = [
    {
        "name": "Happy Family Floater Policy",
        "documents": "https://hackrx.blob.core.windows.net/assets/Happy%20Family%20Floater%20-%202024%20OICHLIP25046V062425%201.pdf?sv=2023-01-03&spr=https&st=2025-07-31T17%3A24%3A30Z&se=2026-08-01T17%3A24%3A00Z&sr=b&sp=r&sig=VNMTTQUjdXGYb2F4Di4P0zNvmM2rTBoEHr%2BnkUXIqpQ%3D",
        "questions": [
            "While checking the process for submitting a dental claim for a 23-year-old financially dependent daughter (who recently married and changed her surname), also confirm the process for updating her last name in the policy records and provide the company's grievance redressal email.",
            "For a claim submission involving robotic surgery for a spouse at \"Apollo Care Hospital\" (city not specified), what supporting documents are needed, how to confirm if the hospital is a network provider, and can a sibling above 26 continue as a dependent if financially dependent after job loss?",
            "While inquiring about the maximum cashless hospitalization benefit for accidental trauma for a covered parent-in-law, simultaneously provide the claim notification procedure, and confirm the process to replace a lost ID card for another dependent.",
            "If you wish to admit your 17-year-old son for psychiatric illness to a hospital outside your city, also request an address update for all family members, and inquire about coverage for OPD dental checkups under Gold and Platinum plans.",
            "Describe the steps to port a prior individual policy from another insurer for a dependent parent-in-law, list documents needed for a post-hospitalization medicine claim for your child, and provide the toll-free customer service number."
        ]
    },
    {
        "name": "UNI Group Health Insurance Policy",
        "documents": "https://hackrx.blob.core.windows.net/assets/UNI%20GROUP%20HEALTH%20INSURANCE%20POLICY%20-%20UIIHLGP26043V022526%201.pdf?sv=2023-01-03&spr=https&st=2025-07-31T17%3A06%3A03Z&se=2026-08-01T17%3A06%3A00Z&sr=b&sp=r&sig=wLlooaThgRx91i2z4WaeggT0qnuUUEzIUKj42GsvMfg%3D",
        "questions": [
            "If an insured person takes treatment for arthritis at home because no hospital beds are available, under what circumstances would these expenses NOT be covered, even if a doctor declares the treatment was medically required?",
            "A claim was lodged for expenses on a prosthetic device after a hip replacement surgery. The hospital bill also includes the cost of a walker and a lumbar belt post-discharge. Which items are payable?",
            "An insured's child (a dependent above 18 but under 26, unemployed and unmarried) requires dental surgery after an accident. What is the claim admissibility, considering both eligibility and dental exclusions, and what is the process for this specific scenario?",
            "If an insured undergoes Intra Operative Neuro Monitoring (IONM) during brain surgery, and also needs ICU care in a city over 1 million population, how are the respective expenses limited according to modern treatments, critical care definition, and policy schedule?",
            "A policyholder requests to add their newly-adopted child as a dependent. The child is 3 years old. What is the process and under what circumstances may the insurer refuse cover for the child, referencing eligibility and addition/deletion clauses?"
        ]
    },
    {
        "name": "Newton's Principia",
        "documents": "https://hackrx.blob.core.windows.net/assets/principia_newton.pdf?sv=2023-01-03&st=2025-07-28T07%3A20%3A32Z&se=2026-07-29T07%3A20%3A00Z&sr=b&sp=r&sig=V5I1QYyigoxeUMbnUKsdEaST99F5%2FDfo7wpKg9XXF5w%3D",
        "questions": [
            "How does Newton define 'quantity of motion' and how is it distinct from 'force'?",
            "According to Newton, what are the three laws of motion and how do they apply in celestial mechanics?",
            "How does Newton derive Kepler's Second Law (equal areas in equal times) from his laws of motion and gravitation?",
            "How does Newton demonstrate that gravity is inversely proportional to the square of the distance between two masses?",
            "What is Newton's argument for why gravitational force must act on all masses universally?"
        ]
    },
    {
        "name": "Indian Constitution",
        "documents": "https://hackrx.blob.core.windows.net/assets/indian_constitution.pdf?sv=2023-01-03&st=2025-07-28T06%3A42%3A00Z&se=2026-11-29T06%3A42%3A00Z&sr=b&sp=r&sig=5Gs%2FOXqP3zY00lgciu4BZjDV5QjTDIx7fgnfdz6Pu24%3D",
        "questions": [
            "What is the official name of India according to Article 1 of the Constitution?",
            "Which Article guarantees equality before the law and equal protection of laws to all persons?",
            "What is abolished by Article 17 of the Constitution?",
            "What are the key ideals mentioned in the Preamble of the Constitution of India?",
            "Under which Article can Parliament alter the boundaries, area, or name of an existing State?"
        ]
    },
    {
        "name": "Family Medicare Policy",
        "documents": "https://hackrx.blob.core.windows.net/assets/Family%20Medicare%20Policy%20(UIN-%20UIIHLIP22070V042122)%201.pdf?sv=2023-01-03&st=2025-07-22T10%3A17%3A39Z&se=2025-08-23T10%3A17%3A00Z&sr=b&sp=r&sig=dA7BEMIZg3WcePcckBOb4QjfxK%2B4rIfxBs2%2F%2BNwoPjQ%3D",
        "questions": [
            "Is Non-infective Arthritis covered?",
            "I renewed my policy yesterday, and I have been a customer for the last 6 years. Can I raise a claim for Hydrocele?",
            "Is abortion covered?"
        ]
    },
    {
        "name": "Arogya Sanjeevani Policy",
        "documents": "https://hackrx.blob.core.windows.net/assets/Arogya%20Sanjeevani%20Policy%20-%20CIN%20-%20U10200WB1906GOI001713%201.pdf?sv=2023-01-03&st=2025-07-21T08%3A29%3A02Z&se=2025-09-22T08%3A29%3A00Z&sr=b&sp=r&sig=nzrz1K9Iurt%2BBXom%2FB%2BMPTFMFP3PRnIvEsipAX10Ig4%3D",
        "questions": [
            "When will my root canal claim of Rs 25,000 be settled?",
            "I have done an IVF for Rs 56,000. Is it covered?",
            "I did a cataract treatment of Rs 100,000. Will you settle the full Rs 100,000?",
            "Give me a list of documents to be uploaded for hospitalization for heart surgery."
        ]
    }
]

def test_api_call(test_case):
    """Make API call and return response."""
    print(f"\n🔄 Testing: {test_case['name']}")
    print(f"📄 Document: {test_case['documents'][:80]}...")
    print(f"❓ Questions: {len(test_case['questions'])}")
    
    payload = {
        "documents": test_case["documents"],
        "questions": test_case["questions"]
    }
    
    start_time = time.time()
    
    try:
        response = requests.post(
            f"{BASE_URL}/hackrx/run",
            headers=HEADERS,
            json=payload,
            timeout=300  # 5 minutes timeout
        )
        
        end_time = time.time()
        duration = end_time - start_time
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Success! Duration: {duration:.2f}s")
            print(f"📝 Answers received: {len(result.get('answers', []))}")
            return True, result
        else:
            print(f"❌ Error {response.status_code}: {response.text}")
            return False, None
            
    except Exception as e:
        print(f"❌ Exception: {str(e)}")
        return False, None

def main():
    """Run all test cases."""
    print("🚀 Starting comprehensive API testing...")
    print(f"📊 Total test cases: {len(TEST_CASES)}")
    
    results = []
    successful_tests = 0
    
    for i, test_case in enumerate(TEST_CASES, 1):
        print(f"\n{'='*60}")
        print(f"Test {i}/{len(TEST_CASES)}")
        print(f"{'='*60}")
        
        success, result = test_api_call(test_case)
        results.append({
            "name": test_case["name"],
            "success": success,
            "result": result
        })
        
        if success:
            successful_tests += 1
        
        # Small delay between tests
        time.sleep(2)
    
    # Summary
    print(f"\n{'='*60}")
    print("📊 TESTING SUMMARY")
    print(f"{'='*60}")
    print(f"✅ Successful tests: {successful_tests}/{len(TEST_CASES)}")
    print(f"❌ Failed tests: {len(TEST_CASES) - successful_tests}/{len(TEST_CASES)}")
    
    # Cache status
    try:
        cache_response = requests.get(f"{BASE_URL}/cache/info")
        if cache_response.status_code == 200:
            cache_info = cache_response.json()
            print(f"💾 Cache size: {cache_info['cache_size']} answers")
    except:
        print("❌ Could not get cache info")
    
    print("\n🎉 Testing completed!")

if __name__ == "__main__":
    main()
