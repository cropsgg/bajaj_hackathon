# HackRX Intelligent Query-Retrieval System

## Overview

This is a high-accuracy LLM-powered Retrieval-Augmented Generation (RAG) system built for the HackRX hackathon. The system processes documents (PDF, DOCX, emails) and answers natural language queries with explainable, factual responses using GPT-3.5-Turbo and semantic search.

## Key Features

- **High Accuracy**: Semantic retrieval + custom prompts ensure precise clause matching
- **Explainable AI**: Responses include rationale and cite specific clauses/sections
- **Fast Performance**: FAISS in-memory vector search (<1s per query)
- **Token Efficient**: GPT-3.5-Turbo with optimized context (~$0.002/1k tokens)
- **Modular Design**: Reusable components for easy extension
- **Multi-Format Support**: PDF, DOCX, and email documents

## Architecture

```
Document URL → Download → Parse → Chunk → Embed → FAISS Index
                                                        ↓
Query → Semantic Search → Top-K Retrieval → LLM → Explainable Answer
```

## Setup Instructions

### 1. Environment Setup

```bash
# Create virtual environment (Python 3.10+ recommended)
python -m venv hackrx_env

# Activate environment
# On macOS/Linux:
source hackrx_env/bin/activate
# On Windows:
hackrx_env\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. OpenAI API Key

```bash
# Get API key from openai.com (need ~$1-2 credit for testing)
export OPENAI_API_KEY='sk-your-key-here'

# Or create .env file
echo "OPENAI_API_KEY=sk-your-key-here" > .env
```

### 3. Run the Application

```bash
# Start FastAPI server
uvicorn app:app --reload

# Server runs on http://localhost:8000
# API endpoint: POST /hackrx/run
```

## Usage

### API Request Format

```json
{
    "documents": "https://example.com/document.pdf",
    "questions": [
        "What is the waiting period for maternity benefits?",
        "Are dental treatments covered under this policy?"
    ]
}
```

### Authentication

Include Authorization header:
```
Authorization: Bearer a2f387310984b739ae7e4accffad70a62e5673145dd05bc749dc913c0e6d0c42
```

### Example with curl

```bash
curl -X POST "http://localhost:8000/hackrx/run" \
     -H "Authorization: Bearer a2f387310984b739ae7e4accffad70a62e5673145dd05bc749dc913c0e6d0c42" \
     -H "Content-Type: application/json" \
     -d '{
       "documents": "https://example.com/policy.pdf",
       "questions": ["What is covered under this policy?"]
     }'
```

### Response Format

```json
{
    "answers": [
        "Yes, maternity benefits are covered with a 9-month waiting period as per clause 4.2. Coverage includes hospitalization and delivery costs up to ₹50,000 per claim."
    ]
}
```

## Technical Implementation

### Document Processing
- **Download**: Handles blob URLs with SAS tokens using requests
- **Parsing**: PyPDF for PDFs, Docx2txt for DOCX, Unstructured for emails
- **Chunking**: 800 characters with 150 overlap for semantic coherence

### Semantic Search
- **Embeddings**: OpenAI text-embedding-ada-002 for accuracy
- **Vector Store**: FAISS for fast local search
- **Retrieval**: Top-5 chunks with cosine similarity

### LLM Processing
- **Model**: GPT-3.5-Turbo (temperature=0 for factual responses)
- **Prompt**: Custom template for explainable clause matching
- **Context**: Limited to ~2000-3000 tokens for efficiency

## Evaluation Parameters Addressed

### 1. Accuracy
- **Semantic Retrieval**: OpenAI embeddings + FAISS for precise clause matching
- **Custom Prompts**: Force LLM to parse queries and match clauses semantically
- **Small Chunks**: 800 characters for granular clause-level retrieval
- **Validation**: Tested against sample documents with known answers

### 2. Token Efficiency
- **Model Choice**: GPT-3.5-Turbo (~$0.002/1k tokens vs GPT-4's ~$0.03/1k)
- **Context Limiting**: Top-5 retrieval + max 500 tokens per response
- **Optimized Chunking**: Prevents oversized context windows

### 3. Latency
- **FAISS**: In-memory vector search (<1s per query)
- **Local Processing**: No external DB calls during query time
- **Batch Processing**: Single model load for multiple questions
- **Target**: ~10-20s for 10 questions total

### 4. Explainability
- **Custom Prompt**: Forces rationale and clause citations
- **Source Tracking**: Maintains page/section metadata
- **Structured Output**: "Yes/No, [details], [conditions], [rationale]" format
- **Traceability**: Option to include source page numbers

### 5. Reusability
- **Modular Functions**: Separate loading, chunking, embedding, querying
- **Easy Extension**: Swap FAISS for Pinecone, add PostgreSQL metadata
- **Format Support**: PDF, DOCX, email with extensible loader system
- **Configuration**: Environment variables for API keys and settings

## File Structure

```
hackrx_project/
├── app.py              # FastAPI application with /hackrx/run endpoint
├── models.py           # Pydantic models for input/output validation
├── prompts.py          # Custom LLM prompts for explainable QA
├── utils.py            # Core functions: download, parse, embed, query
├── requirements.txt    # Python dependencies
├── README.md          # This documentation
├── .env               # Environment variables (create manually)
└── tests/             # Testing directory (optional)
```

## Extensions

### Add Pinecone Vector Store
```python
from langchain.vectorstores import Pinecone
vectorstore = Pinecone.from_documents(chunks, embeddings, index_name="hackrx")
```

### Add PostgreSQL Metadata
```python
import psycopg2
# Store chunk metadata: page numbers, sections, document IDs
```

### Multi-Document Support
```python
# Process multiple documents in parallel
# Combine vector stores or use namespace separation
```

## Testing

### Local Testing
1. Start server: `uvicorn app:app --reload`
2. Use Postman or curl with sample requests
3. Validate responses against expected answers

### Sample Test Case
```bash
# Test with insurance policy PDF
curl -X POST "http://localhost:8000/hackrx/run" \
     -H "Authorization: Bearer a2f387310984b739ae7e4accffad70a62e5673145dd05bc749dc913c0e6d0c42" \
     -H "Content-Type: application/json" \
     -d '{
       "documents": "https://example.com/sample-policy.pdf",
       "questions": [
         "What is the waiting period for pre-existing diseases?",
         "Are OPD consultations covered?",
         "What is the maximum sum insured?"
       ]
     }'
```

## Troubleshooting

### Common Issues

1. **OpenAI API Key Error**
   - Ensure OPENAI_API_KEY is set correctly
   - Check API key has sufficient credits

2. **Download Failures**
   - Verify document URL is accessible
   - Check for authentication requirements on blob URLs

3. **Memory Issues**
   - Large PDFs may require more RAM for FAISS indexing
   - Consider chunking documents before processing

4. **Slow Responses**
   - Check internet connection for OpenAI API calls
   - Monitor token usage and context size

### Performance Optimization

- Use GPU FAISS (`faiss-gpu`) for faster indexing
- Cache vector stores for repeated queries on same document
- Implement hybrid search (semantic + keyword) for better recall

## License

This project is built for the HackRX hackathon and follows the competition guidelines.