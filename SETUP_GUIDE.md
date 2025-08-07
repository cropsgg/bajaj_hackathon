# 🚀 HackRX Setup Guide - Fresh Installation

## Prerequisites
- Python 3.8+ installed
- Git installed
- OpenAI API key

## 📋 Complete Setup Commands

### 1. Clone the Repository
```bash
git clone https://github.com/cropsgg/bajaj_hackathon.git
cd bajaj_hackathon
```

### 2. Create Python Virtual Environment
```bash
# Create virtual environment
python3 -m venv hackrx_env

# Activate virtual environment
# On macOS/Linux:
source hackrx_env/bin/activate
# On Windows:
# hackrx_env\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Set Up Environment Variables
```bash
# Create .env file
touch .env

# Add your OpenAI API key to .env file
echo "OPENAI_API_KEY=your_openai_api_key_here" >> .env
```

**⚠️ IMPORTANT**: Replace `your_openai_api_key_here` with your actual OpenAI API key!

### 5. Verify Installation
```bash
# Test imports
python -c "import fastapi, langchain, openai, faiss; print('✅ All dependencies installed successfully!')"
```

### 6. Run the Application
```bash
# Start the FastAPI server
uvicorn app:app --host 127.0.0.1 --port 8000
```

### 7. Test the Application

#### Option A: Browser Test
Open your browser and go to: `http://127.0.0.1:8000/`

You should see:
```json
{
    "status": "healthy",
    "message": "HackRX Intelligent Query-Retrieval System is running"
}
```

#### Option B: API Documentation
Visit: `http://127.0.0.1:8000/docs` for interactive API documentation

#### Option C: Command Line Test
```bash
# Health check
curl -X GET "http://127.0.0.1:8000/"

# API test (in a new terminal)
curl -X POST "http://127.0.0.1:8000/hackrx/run" \
     -H "Content-Type: application/json" \
     -H "Accept: application/json" \
     -H "Authorization: Bearer a2f387310984b739ae7e4accffad70a62e5673145dd05bc749dc913c0e6d0c42" \
     -d '{
    "documents": "https://hackrx.blob.core.windows.net/assets/policy.pdf?sv=2023-01-03&st=2025-07-04T09%3A11%3A24Z&se=2027-07-05T09%3A11%3A00Z&sr=b&sp=r&sig=N4a9OU0w0QXO6AOIBiu4bpl7AXvEZogeT%2FjUHNO7HzQ%3D",
    "questions": [
        "What is the grace period for premium payment?"
    ]
}'
```

## 🔧 Troubleshooting

### Issue 1: Python Virtual Environment
If you get "externally-managed-environment" error:
```bash
# Use --break-system-packages flag (not recommended) OR
pip install --user -r requirements.txt
# OR create virtual environment as shown above
```

### Issue 2: OpenAI API Key Not Found
```bash
# Verify .env file exists and has correct content
cat .env
# Should show: OPENAI_API_KEY=sk-...
```

### Issue 3: Module Not Found Errors
```bash
# Ensure virtual environment is activated
source hackrx_env/bin/activate  # macOS/Linux
# OR
hackrx_env\Scripts\activate     # Windows

# Reinstall requirements
pip install -r requirements.txt
```

### Issue 4: Port Already in Use
```bash
# Use different port
uvicorn app:app --host 127.0.0.1 --port 8001
```

## 📦 Dependencies Included

- `fastapi>=0.104.1` - Web framework
- `uvicorn>=0.24.0` - ASGI server
- `langchain>=0.0.350` - LLM framework
- `langchain-community>=0.0.350` - LangChain community features
- `langchain-openai>=0.0.2` - OpenAI integration
- `openai>=1.3.0` - OpenAI API client
- `faiss-cpu>=1.7.4` - Vector similarity search
- `pypdf>=3.17.0` - PDF processing
- `pdfplumber` - Enhanced PDF parsing
- `requests>=2.31.0` - HTTP requests
- `pydantic>=2.5.0` - Data validation
- `python-dotenv>=1.0.0` - Environment variables
- And more...

## 🎯 Quick Start Summary

```bash
# 1. Clone and enter directory
git clone https://github.com/cropsgg/bajaj_hackathon.git && cd bajaj_hackathon

# 2. Setup environment
python3 -m venv hackrx_env && source hackrx_env/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Add API key to .env file
echo "OPENAI_API_KEY=your_api_key_here" > .env

# 5. Run application
uvicorn app:app --host 127.0.0.1 --port 8000
```

## 🌐 Production Deployment

The application is already deployed on Railway: https://web-production-4ea4c.up.railway.app/

For local development, use the commands above. For production deployment on Railway, the app will automatically deploy from the GitHub repository.

---

**🎉 You're ready to go! The HackRX Intelligent Query-Retrieval System should now be running locally.**