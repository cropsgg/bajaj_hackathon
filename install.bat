@echo off
REM 🚀 HackRX One-Click Installation Script for Windows
REM This script sets up the entire HackRX application from scratch

echo 🚀 Starting HackRX Installation...

REM Check if Python 3 is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python is not installed. Please install Python 3.8+ first.
    pause
    exit /b 1
)

echo ✅ Python found
python --version

REM Check if we're already in the project directory
if not exist "app.py" (
    echo 📁 Cloning repository...
    git clone https://github.com/cropsgg/bajaj_hackathon.git
    cd bajaj_hackathon
) else (
    echo 📁 Already in project directory
)

REM Create virtual environment
echo 🔧 Creating virtual environment...
python -m venv hackrx_env

REM Activate virtual environment
echo 🔧 Activating virtual environment...
call hackrx_env\Scripts\activate.bat

REM Upgrade pip
echo 📦 Upgrading pip...
python -m pip install --upgrade pip

REM Install dependencies
echo 📦 Installing dependencies...
pip install -r requirements.txt

REM Check if .env exists
if not exist ".env" (
    echo 🔑 Creating .env file...
    echo OPENAI_API_KEY=your_openai_api_key_here > .env
    echo ⚠️  IMPORTANT: Please edit .env file and add your actual OpenAI API key!
    echo    You can edit it with: notepad .env
) else (
    echo ✅ .env file already exists
)

REM Verify installation
echo 🔍 Verifying installation...
python -c "import fastapi, langchain, openai, faiss; print('✅ All dependencies installed successfully!')" 2>nul

if %errorlevel% equ 0 (
    echo.
    echo 🎉 Installation completed successfully!
    echo.
    echo 📋 Next steps:
    echo 1. Edit .env file and add your OpenAI API key:
    echo    notepad .env
    echo.
    echo 2. Start the application:
    echo    hackrx_env\Scripts\activate.bat
    echo    uvicorn app:app --host 127.0.0.1 --port 8000
    echo.
    echo 3. Test in browser: http://127.0.0.1:8000/
    echo.
    echo 🌐 Production URL: https://web-production-4ea4c.up.railway.app/
) else (
    echo ❌ Installation verification failed. Please check error messages above.
)

pause