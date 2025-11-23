# 🤖 AI Chatbot Quick Start Guide

## 🎉 What's New?

Your ADAS system now has an intelligent AI assistant powered by Google Gemini!

### Features:
✅ Ask questions about alerts  
✅ Get driving safety tips  
✅ Receive AI-powered suggestions  
✅ Natural conversation interface  
✅ Context-aware responses  

---

## 🔑 Step 1: Get FREE Gemini API Key

1. Visit: https://makersuite.google.com/app/apikey
2. Sign in with Google
3. Click "Create API Key"
4. Copy your key (starts with `AIza...`)

**Free tier**: 60 requests/minute - perfect for your project!

---

## ⚙️ Step 2: Setup

### Add API Key
```bash
# In project root directory
export GEMINI_API_KEY="AIzaSyYOUR_ACTUAL_KEY_HERE"
```

Or create `.env` file:
```
GEMINI_API_KEY=AIzaSyYOUR_ACTUAL_KEY_HERE
```

---

## 🚀 Step 3: Run the System

### Terminal 1: Backend with AI
```bash
export GEMINI_API_KEY="YOUR_KEY"
python3 -m uvicorn backend.main:app --host 0.0.0.0 --port 8000 --reload
```

### Terminal 2: Frontend
```bash
cd frontend
npm run dev
```

---

## 🎮 Step 4: Try It Out!

Visit: **http://localhost:5173**

You'll now see:
- 🎥 Camera feed (left)
- 📊 Alerts (middle)
- 🤖 **AI Chat** (right) ← NEW!

---

## 💬 What to Ask the AI

### Quick Questions (Just click!):
- "What alerts did I get recently?"
- "Give me safety tips"
- "Explain the last alert"
- "How can I improve my driving?"

### Custom Questions:
- "Why did that alert trigger?"
- "What's the safest following distance?"
- "How does YOLO detection work?"
- "Give me a weekly safety summary"

---

## 🎨 AI Chat Features

### 1. **Smart Context**
AI knows about your recent alerts automatically!

### 2. **Safety Suggestions**
Get proactive tips based on your driving patterns

### 3. **Quick Questions**
One-click to ask common questions

### 4. **Typing Indicators**
See when AI is thinking

### 5. **Offline Support**
Works even without backend (gives helpful tips)

---

## 📦 Dependencies Installed

```bash
pip3 install google-generativeai langchain langchain-google-genai
```

Already done! ✅

---

## 🔧 Troubleshooting

### "API key not found"
```bash
# Make sure to export before running backend
export GEMINI_API_KEY="your_key"
```

### Chat not responding?
-Check backend is running on port 8000
- Verify API key is set
- Check browser console for errors

### "Quota exceeded"?
- Free tier: 60 requests/minute
- Wait 1 minute and try again

---

## 🌟 Make It Unique!

### Customize the AI (Edit `backend/routers/chat.py`):

```python
system_prompt = """You are a friendly ADAS assistant named 'Drivio'.
Speak casually and use emojis. Always prioritize safety!"""
```

### Add More Features:
- Voice commands (coming soon!)
- Driving score analytics
- Route suggestions
- Weather alerts

---

## 📱 Deploy with AI

The AI chat works on deployed version too!

```bash
# Set environment variable for production
# (Add to Railway/Render dashboard)
GEMINI_API_KEY=your_key

# Build and deploy frontend
cd frontend && npm run build
npx firebase-tools deploy
```

---

## 🎯 Next Steps

1. ✅ Get Gemini API key
2. ✅ Test locally
3. ✅ Customize responses
4. ✅ Deploy to production

Your ADAS is now **AI-powered**! 🚀

---

**Full Setup Guide**: `docs/GEMINI_SETUP.md`
