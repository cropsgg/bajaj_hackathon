# 🧪 HackRX System Testing Guide

## Quick Setup & Testing Instructions

### 1. **One-Command Setup**
```bash
# Run the installation script
./install_and_setup.sh
```

### 2. **Manual Setup (Alternative)**
```bash
# Create virtual environment
python3 -m venv hackrx_env
source hackrx_env/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 3. **Configure API Key**
Edit the `.env` file:
```bash
# Replace with your actual OpenAI API key
OPENAI_API_KEY=sk-your-actual-openai-api-key-here
```

### 4. **Start the Server**
```bash
# Make sure virtual environment is activated
source hackrx_env/bin/activate

# Start FastAPI server
uvicorn app:app --reload
```
✅ Server runs on: `http://localhost:8000`  
✅ API endpoint: `POST /hackrx/run`

### 5. **Test with Real Document**
```bash
# In a new terminal (keep server running)
source hackrx_env/bin/activate
python test_with_real_doc.py
```

### 6. **Manual API Testing**

#### Using curl:
```bash
curl -X POST "http://localhost:8000/hackrx/run" \
     -H "Authorization: Bearer a2f387310984b739ae7e4accffad70a62e5673145dd05bc749dc913c0e6d0c42" \
     -H "Content-Type: application/json" \
     -d '{
       "documents": "https://www.africau.edu/images/default/sample.pdf",
       "questions": [
         "What is this document about?",
         "What type of content does it contain?"
       ]
     }'
```

#### Expected Response:
```json
{
  "answers": [
    "This is a sample PDF document...",
    "The document contains sample text content..."
  ]
}
```

### 7. **Verification Checklist**

✅ **Installation**: All packages installed without errors  
✅ **Environment**: OpenAI API key configured  
✅ **Server**: FastAPI starts on port 8000  
✅ **Authentication**: Bearer token accepted  
✅ **Document Processing**: PDF downloads and parses  
✅ **Vector Search**: FAISS indexing works  
✅ **LLM**: GPT-3.5-Turbo responses generated  
✅ **Performance**: <20s for 5 questions  

### 8. **Testing with Your Own Documents**

Replace the document URL in `test_with_real_doc.py`:
```python
TEST_REQUEST = {
    "documents": "https://your-document-url.pdf",
    "questions": [
        "Your specific questions here..."
    ]
}
```

### 9. **Common Issues & Solutions**

**Issue**: `ModuleNotFoundError`  
**Solution**: Activate virtual environment: `source hackrx_env/bin/activate`

**Issue**: `OpenAI API Error`  
**Solution**: Check API key in `.env` file and ensure you have credits

**Issue**: `Document download failed`  
**Solution**: Verify URL is publicly accessible

**Issue**: `Server won't start`  
**Solution**: Check if port 8000 is available: `lsof -i :8000`

### 10. **Performance Testing**

Expected benchmarks:
- **Document Processing**: 2-5 seconds
- **Question Answering**: 1-3 seconds per question
- **Total (5 questions)**: 7-20 seconds
- **Memory Usage**: <2GB RAM
- **Token Usage**: ~500-1000 tokens per question

### 11. **API Documentation**

Once server is running, visit:
- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

### 12. **Production Deployment**

For hackathon submission:
```bash
# Run with production settings
uvicorn app:app --host 0.0.0.0 --port 8000
```

---

## 🎯 Ready for Hackathon Submission!

The system is now fully configured and tested. It meets all requirements:
- ✅ High accuracy with semantic search + LLM
- ✅ Token efficient (GPT-3.5-Turbo)  
- ✅ Low latency (FAISS + optimized chunks)
- ✅ Explainable (custom prompts with rationale)
- ✅ Reusable (modular architecture)