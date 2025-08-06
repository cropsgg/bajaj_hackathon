from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from models import InputData, OutputData
from utils import download_document, load_and_chunk_document, build_vectorstore, query_llm
from typing import List
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = FastAPI(
    title="HackRX Intelligent Query-Retrieval System",
    description="LLM-powered Retrieval-Augmented Generation system for document Q&A",
    version="1.0.0"
)

security = HTTPBearer()

# Authentication check (as per spec)
async def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    if credentials.credentials != "a2f387310984b739ae7e4accffad70a62e5673145dd05bc749dc913c0e6d0c42":
        raise HTTPException(status_code=401, detail="Invalid token")
    return credentials

@app.get("/")
async def health_check():
    """Health check endpoint for Railway deployment."""
    return {"status": "healthy", "message": "HackRX Intelligent Query-Retrieval System is running"}

@app.post("/hackrx/run", response_model=OutputData)
async def run_query(input_data: InputData, token: str = Depends(verify_token)):
    """Endpoint to process document and questions. Returns structured answers."""
    try:
        # Step 1: Download document with timeout
        print(f"Processing document: {input_data.documents[:100]}...")
        doc_content = download_document(input_data.documents)
        print(f"Document downloaded successfully, size: {len(doc_content)} bytes")
        
        # Step 2: Load and chunk
        chunks = load_and_chunk_document(doc_content, input_data.documents)
        print(f"Document chunked into {len(chunks)} chunks")
        
        # Step 3: Build vector store
        vectorstore, chunks = build_vectorstore(chunks)
        print(f"Vector store built successfully")
        
        # Step 4: Process each question with progress tracking
        answers: List[str] = []
        for i, question in enumerate(input_data.questions):
            print(f"Processing question {i+1}/{len(input_data.questions)}: {question[:50]}...")
            try:
                answer = query_llm(vectorstore, chunks, question)
                answers.append(answer)
                print(f"Question {i+1} completed")
            except Exception as qe:
                print(f"Error processing question {i+1}: {qe}")
                answers.append(f"Error processing this question: {str(qe)}")
        
        print(f"All {len(answers)} questions processed successfully")
        return OutputData(answers=answers)
    except Exception as e:
        print(f"Critical error in run_query: {e}")
        raise HTTPException(status_code=500, detail=f"Error processing: {str(e)}")