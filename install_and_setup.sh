#!/bin/bash
# HackRX System Installation and Setup Script

echo "🎯 HackRX Intelligent Query-Retrieval System Setup"
echo "=================================================="

# Create virtual environment
echo "📦 Creating virtual environment..."
python3 -m venv hackrx_env

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source hackrx_env/bin/activate

# Upgrade pip
echo "⬆️  Upgrading pip..."
pip install --upgrade pip

# Install requirements
echo "📚 Installing Python packages..."
pip install -r requirements.txt

echo "✅ Installation completed!"
echo ""
echo "🔑 IMPORTANT: Set your OpenAI API Key"
echo "Edit the .env file and replace 'sk-your-openai-api-key-here' with your actual API key"
echo ""
echo "🚀 To start the system:"
echo "1. source hackrx_env/bin/activate"
echo "2. uvicorn app:app --reload"
echo ""
echo "🧪 To test the system:"
echo "python test_with_real_doc.py"