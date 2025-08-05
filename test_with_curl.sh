#!/bin/bash
# HackRX cURL Test Script
# Test the API using the exact format provided by the user

echo "🧪 HackRX cURL Tester"
echo "====================="

# API Configuration
API_URL="http://localhost:8000/hackrx/run"
AUTH_TOKEN="a2f387310984b739ae7e4accffad70a62e5673145dd05bc749dc913c0e6d0c42"

echo "🔗 Testing endpoint: $API_URL"
echo "🔑 Using authentication token"
echo

# Test 1: Main sample request (as provided by user)
echo "📋 Test 1: Main Sample Request (Insurance Policy)"
echo "================================================"

curl -X POST "$API_URL" \
     -H "Content-Type: application/json" \
     -H "Accept: application/json" \
     -H "Authorization: Bearer $AUTH_TOKEN" \
     -d '{
    "documents": "https://hackrx.blob.core.windows.net/assets/policy.pdf?sv=2023-01-03&st=2025-07-04T09%3A11%3A24Z&se=2027-07-05T09%3A11%3A00Z&sr=b&sp=r&sig=N4a9OU0w0QXO6AOIBiu4bpl7AXvEZogeT%2FjUHNO7HzQ%3D",
    "questions": [
        "What is the grace period for premium payment under the National Parivar Mediclaim Plus Policy?",
        "What is the waiting period for pre-existing diseases (PED) to be covered?",
        "Does this policy cover maternity expenses, and what are the conditions?",
        "What is the waiting period for cataract surgery?",
        "Are the medical expenses for an organ donor covered under this policy?",
        "What is the No Claim Discount (NCD) offered in this policy?",
        "Is there a benefit for preventive health check-ups?",
        "How does the policy define a '\''Hospital'\''?",
        "What is the extent of coverage for AYUSH treatments?",
        "Are there any sub-limits on room rent and ICU charges for Plan A?"
    ]
}' | python3 -m json.tool

echo
echo "============================================"
echo

# Test 2: Alternative PDF test
echo "📋 Test 2: Alternative PDF Test"
echo "==============================="

curl -X POST "$API_URL" \
     -H "Content-Type: application/json" \
     -H "Accept: application/json" \
     -H "Authorization: Bearer $AUTH_TOKEN" \
     -d '{
    "documents": "https://www.w3.org/WAI/ER/tests/xhtml/testfiles/resources/pdf/dummy.pdf",
    "questions": [
        "What type of insurance policy is this?",
        "What are the coverage details?",
        "Are there any waiting periods mentioned?",
        "What exclusions are listed?",
        "What is the claim process?"
    ]
}' | python3 -m json.tool

echo
echo "✅ cURL tests completed!"
echo "📊 Check the JSON responses above for results"