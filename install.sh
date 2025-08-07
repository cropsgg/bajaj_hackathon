#!/bin/bash

# 🚀 HackRX One-Click Installation Script
# This script sets up the entire HackRX application from scratch

echo "🚀 Starting HackRX Installation..."

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8+ first."
    exit 1
fi

echo "✅ Python 3 found: $(python3 --version)"

# Check if we're already in the project directory
if [ ! -f "app.py" ]; then
    echo "📁 Cloning repository..."
    git clone https://github.com/cropsgg/bajaj_hackathon.git
    cd bajaj_hackathon
else
    echo "📁 Already in project directory"
fi

# Create virtual environment
echo "🔧 Creating virtual environment..."
python3 -m venv hackrx_env

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source hackrx_env/bin/activate

# Upgrade pip
echo "📦 Upgrading pip..."
pip install --upgrade pip

# Install dependencies
echo "📦 Installing dependencies..."
pip install -r requirements.txt

# Check if .env exists
if [ ! -f ".env" ]; then
    echo "🔑 Creating .env file..."
    echo "OPENAI_API_KEY=your_openai_api_key_here" > .env
    echo "⚠️  IMPORTANT: Please edit .env file and add your actual OpenAI API key!"
    echo "   You can edit it with: nano .env"
else
    echo "✅ .env file already exists"
fi

# Verify installation
echo "🔍 Verifying installation..."
python -c "import fastapi, langchain, openai, faiss; print('✅ All dependencies installed successfully!')" 2>/dev/null

if [ $? -eq 0 ]; then
    echo ""
    echo "🎉 Installation completed successfully!"
    echo ""
    echo "📋 Next steps:"
    echo "1. Edit .env file and add your OpenAI API key:"
    echo "   nano .env"
    echo ""
    echo "2. Start the application:"
    echo "   source hackrx_env/bin/activate"
    echo "   uvicorn app:app --host 127.0.0.1 --port 8000"
    echo ""
    echo "3. Test in browser: http://127.0.0.1:8000/"
    echo ""
    echo "🌐 Production URL: https://web-production-4ea4c.up.railway.app/"
else
    echo "❌ Installation verification failed. Please check error messages above."
fi