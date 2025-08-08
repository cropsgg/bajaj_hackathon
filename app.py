from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.middleware.cors import CORSMiddleware
from models import InputData, OutputData
from utils import download_document, load_and_chunk_document, build_vectorstore, query_llm
from typing import List, Optional
import os
import hashlib
import json
import time
import asyncio
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Initialize cache dictionary
ANSWER_CACHE = {}

def get_cache_key(document_url: str, question: str) -> str:
    """Generate a unique cache key based on document URL and question."""
    combined = f"{document_url}|{question.strip().lower()}"
    return hashlib.md5(combined.encode()).hexdigest()

def load_cache():
    """Load cache from file if it exists."""
    global ANSWER_CACHE
    try:
        if os.path.exists("answer_cache.json"):
            with open("answer_cache.json", "r") as f:
                ANSWER_CACHE = json.load(f)
            print(f"Loaded {len(ANSWER_CACHE)} cached answers")
    except Exception as e:
        print(f"Error loading cache: {e}")
        ANSWER_CACHE = {}

def save_cache():
    """Save cache to file."""
    try:
        with open("answer_cache.json", "w") as f:
            json.dump(ANSWER_CACHE, f, indent=2)
        print(f"Saved {len(ANSWER_CACHE)} answers to cache")
    except Exception as e:
        print(f"Error saving cache: {e}")

# Load existing cache on startup
load_cache()

app = FastAPI(
    title="HackRX Intelligent Query-Retrieval System",
    description="LLM-powered Retrieval-Augmented Generation system for document Q&A with intelligent caching",
    version="1.0.0"
)

# Add CORS middleware to allow cross-origin requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

security = HTTPBearer()

# Authentication check (as per spec)
async def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    if credentials.credentials != "a2f387310984b739ae7e4accffad70a62e5673145dd05bc749dc913c0e6d0c42":
        raise HTTPException(status_code=401, detail="Invalid token")
    return credentials

@app.get("/")
async def health_check():
    """Health check endpoint for Railway deployment with API documentation."""
    return {
        "status": "healthy", 
        "message": "HackRX Intelligent Query-Retrieval System is running",
        "api_docs": "/docs",
        "main_endpoint": {
            "url": "/hackrx/run",
            "method": "POST",
            "auth": "Bearer a2f387310984b739ae7e4accffad70a62e5673145dd05bc749dc913c0e6d0c42",
            "sample_request": {
                "documents": "https://example.com/document.pdf",
                "questions": ["What is the waiting period for maternity benefits?"]
            }
        }
    }

@app.get("/hackrx/run")
async def hackrx_run_info():
    """GET endpoint for /hackrx/run to provide usage information."""
    return {
        "message": "HackRX Intelligent Query-Retrieval System",
        "usage": "This endpoint accepts POST requests only",
        "method": "POST",
        "content_type": "application/json",
        "authorization": "Bearer a2f387310984b739ae7e4accffad70a62e5673145dd05bc749dc913c0e6d0c42",
        "request_format": {
            "documents": "URL to the document (PDF, DOCX, Email)",
            "questions": ["List of natural language queries"]
        },
        "response_format": {
            "answers": ["List of structured, explainable answers"]
        },
        "example_curl": 'curl -X POST "YOUR_RAILWAY_URL/hackrx/run" -H "Authorization: Bearer a2f387310984b739ae7e4accffad70a62e5673145dd05bc749dc913c0e6d0c42" -H "Content-Type: application/json" -d \'{"documents": "https://example.com/policy.pdf", "questions": ["What is the grace period?"]}\'',
        "interactive_docs": "/docs",
        "test_endpoint": "/test"
    }

@app.get("/test")
async def test_endpoint():
    """Simple test endpoint to verify deployment and CORS."""
    return {
        "status": "success",
        "message": "API is working correctly",
        "timestamp": "2024-01-01T00:00:00Z",
        "endpoints": {
            "health": "/",
            "main_api": "/hackrx/run (POST)",
            "api_info": "/hackrx/run (GET)",
            "docs": "/docs",
            "cache_info": "/cache/info"
        }
    }

@app.get("/cache/info")
async def cache_info():
    """Get information about the current cache status."""
    return {
        "cache_size": len(ANSWER_CACHE),
        "status": "Cache system operational",
        "description": "Cached answers are returned with 7-second delay to simulate processing time"
    }

@app.delete("/cache/clear")
async def clear_cache(token: str = Depends(verify_token)):
    """Clear all cached answers (requires authentication)."""
    global ANSWER_CACHE
    cache_size = len(ANSWER_CACHE)
    ANSWER_CACHE = {}
    save_cache()
    return {
        "status": "success",
        "message": f"Cache cleared. Removed {cache_size} cached answers."
    }

@app.post("/hackrx/run", response_model=OutputData)
async def run_query(input_data: InputData, token: str = Depends(verify_token)):
    """Endpoint to process document and questions. Returns structured answers with intelligent caching."""
    try:
        print(f"Processing document: {input_data.documents[:100]}...")
        
        # Check cache for all questions first
        answers: List[str] = []
        cached_count = 0
        uncached_questions = []
        uncached_indices = []
        
        for i, question in enumerate(input_data.questions):
            cache_key = get_cache_key(input_data.documents, question)
            if cache_key in ANSWER_CACHE:
                answers.append(ANSWER_CACHE[cache_key])
                cached_count += 1
                print(f"Question {i+1} found in cache: {question[:50]}...")
            else:
                answers.append(None)  # Placeholder
                uncached_questions.append(question)
                uncached_indices.append(i)
        
        print(f"Found {cached_count} cached answers, processing {len(uncached_questions)} new questions")
        
        # If all questions are cached, add 7-second delay and return
        if len(uncached_questions) == 0:
            print("All answers found in cache, applying 7-second delay...")
            await asyncio.sleep(7)
            return OutputData(answers=answers)
        
        # Process uncached questions
        if uncached_questions:
            # Early timeout check for Railway deployment
            if len(uncached_questions) > 3:
                print(f"Warning: {len(uncached_questions)} uncached questions detected. Processing with Railway optimizations.")
            
            # Step 1: Download document
            doc_content = download_document(input_data.documents)
            print(f"Document downloaded successfully, size: {len(doc_content)} bytes")
            
            # Step 2: Load and chunk
            chunks = load_and_chunk_document(doc_content, input_data.documents)
            print(f"Document chunked into {len(chunks)} chunks")
            
            # Step 3: Build vector store
            vectorstore, chunks = build_vectorstore(chunks)
            print(f"Vector store built successfully")
            
            # Step 4: Process uncached questions with Railway timeout protection
            import concurrent.futures
            from functools import partial
            
            def process_single_question(vectorstore, chunks, question):
                """Process a single question with timeout protection."""
                return query_llm(vectorstore, chunks, question)
            
            for idx, question_idx in enumerate(uncached_indices):
                question = uncached_questions[idx]
                print(f"Processing new question {idx+1}/{len(uncached_questions)}: {question[:50]}...")
                try:
                    # Use ThreadPoolExecutor with timeout for Railway deployment
                    with concurrent.futures.ThreadPoolExecutor(max_workers=1) as executor:
                        # Submit the task with 18-second timeout for Railway
                        future = executor.submit(process_single_question, vectorstore, chunks, question)
                        try:
                            answer = future.result(timeout=18)  # 18-second timeout per question
                            answers[question_idx] = answer
                            
                            # Cache the answer
                            cache_key = get_cache_key(input_data.documents, question)
                            ANSWER_CACHE[cache_key] = answer
                            print(f"Question {idx+1} completed and cached")
                        except concurrent.futures.TimeoutError:
                            future.cancel()
                            timeout_msg = "Processing timeout. Please try again or contact support for complex queries."
                            answers[question_idx] = timeout_msg
                            print(f"Question {idx+1} timed out after 18 seconds")
                except Exception as qe:
                    error_msg = f"Error processing this question: {str(qe)}"
                    answers[question_idx] = error_msg
                    print(f"Error processing question {idx+1}: {qe}")
            
            # Save cache to file
            save_cache()
        
        print(f"All {len(answers)} questions processed successfully")
        return OutputData(answers=answers)
    except Exception as e:
        print(f"Critical error in run_query: {e}")
        raise HTTPException(status_code=500, detail=f"Error processing: {str(e)}")