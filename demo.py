#!/usr/bin/env python3
"""
Demo script for HackRX Intelligent Query-Retrieval System
This demonstrates the complete workflow without running the FastAPI server.
"""

import os
from utils import download_document, load_and_chunk_document, build_vectorstore, query_llm

def demo_workflow():
    """Demonstrate the complete RAG workflow"""
    
    # Check if OpenAI API key is set
    if not os.getenv('OPENAI_API_KEY'):
        print("❌ Please set OPENAI_API_KEY environment variable")
        print("   export OPENAI_API_KEY='sk-your-key-here'")
        return
    
    print("🚀 HackRX Intelligent Query-Retrieval System Demo")
    print("=" * 50)
    
    # Sample document URL (replace with actual PDF)
    document_url = "https://example.com/sample-policy.pdf"  # Replace with real URL
    
    # Sample questions
    questions = [
        "What is the waiting period for maternity benefits?",
        "Are dental treatments covered under this policy?",
        "What is the maximum sum insured?",
        "Are pre-existing diseases covered?",
        "What is the claim settlement process?"
    ]
    
    try:
        print("📥 Step 1: Downloading document...")
        # Note: This will fail with the example URL, but shows the workflow
        doc_content = download_document(document_url)
        print(f"✅ Downloaded {len(doc_content)} bytes")
        
        print("📄 Step 2: Loading and chunking document...")
        chunks = load_and_chunk_document(doc_content, document_url)
        print(f"✅ Created {len(chunks)} chunks")
        
        print("🔍 Step 3: Building vector store...")
        vectorstore = build_vectorstore(chunks)
        print("✅ Vector store created with FAISS")
        
        print("🤖 Step 4: Processing questions...")
        for i, question in enumerate(questions, 1):
            print(f"\nQ{i}: {question}")
            answer = query_llm(vectorstore, question)
            print(f"A{i}: {answer}")
            
        print("\n🎉 Demo completed successfully!")
        
    except Exception as e:
        print(f"❌ Demo failed: {str(e)}")
        print("\nNote: This demo requires a valid document URL and OpenAI API key.")
        print("To test with real data:")
        print("1. Replace document_url with actual PDF URL")
        print("2. Set OPENAI_API_KEY environment variable")
        print("3. Run: python demo.py")

def test_components():
    """Test individual components"""
    print("\n🧪 Testing Individual Components")
    print("-" * 30)
    
    # Test imports
    try:
        from langchain_openai import OpenAIEmbeddings, ChatOpenAI
        from langchain.vectorstores import FAISS
        print("✅ All imports successful")
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return
    
    # Test OpenAI connection (requires API key)
    if os.getenv('OPENAI_API_KEY'):
        try:
            embeddings = OpenAIEmbeddings(model="text-embedding-ada-002")
            print("✅ OpenAI embeddings initialized")
            
            llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
            print("✅ ChatOpenAI initialized")
        except Exception as e:
            print(f"❌ OpenAI initialization error: {e}")
    else:
        print("⚠️  OpenAI API key not set - skipping connection test")

if __name__ == "__main__":
    demo_workflow()
    test_components()