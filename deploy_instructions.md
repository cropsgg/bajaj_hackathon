# 🚀 HackRX Model Hosting & Submission Guide

## 🎯 Quick Deployment Options

### Option 1: ngrok (Fastest - 2 minutes) ⚡
**Perfect for hackathon submission - Creates instant public URL**

1. **Install ngrok:**
   ```bash
   # On macOS (if you have Homebrew)
   brew install ngrok
   
   # Or download from: https://ngrok.com/download
   ```

2. **Start your local server:**
   ```bash
   source hackrx_env/bin/activate
   uvicorn app:app --host 0.0.0.0 --port 8000
   ```

3. **In a new terminal, expose with ngrok:**
   ```bash
   ngrok http 8000
   ```

4. **Copy the public URL (looks like: https://abc123.ngrok.io)**
   - Submit: `https://abc123.ngrok.io/hackrx/run`

### Option 2: Railway (Free hosting) 🚂
**Great for persistent hosting beyond hackathon**

1. **Create account at railway.app**
2. **Connect GitHub repo**
3. **Auto-deploys from your code**

### Option 3: Heroku (Free tier) 🟣
**Reliable cloud hosting**

1. **Create Heroku account**
2. **Install Heroku CLI**
3. **Deploy with git**

### Option 4: Replit (Browser-based) 🌐
**No local setup needed**

1. **Import project to Replit**
2. **Install packages**
3. **Get instant public URL**

## 📋 HackRX Submission Format

**Your webhook URL will be:**
```
https://your-domain.com/hackrx/run
```

**Authentication header:**
```
Authorization: Bearer a2f387310984b739ae7e4accffad70a62e5673145dd05bc749dc913c0e6d0c42
```

**Test payload format:**
```json
{
    "documents": "https://hackrx.blob.core.windows.net/assets/policy.pdf?sv=...",
    "questions": [
        "What is the grace period for premium payment?",
        "What is the waiting period for PED?"
    ]
}
```

## 🎯 Recommended: ngrok (Fastest Setup)

**Perfect for hackathon - no code changes needed!**