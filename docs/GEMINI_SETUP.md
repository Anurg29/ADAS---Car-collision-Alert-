# Google Gemini AI Setup Guide

## 🔑 Get Your Free Gemini API Key

### Step 1: Go to Google AI Studio
Visit: **https://makersuite.google.com/app/apikey**

### Step 2: Sign In
- Click "Sign in with Google"
- Use your Google account

### Step 3: Create API Key
1. Click **"Create API key"**
2. Select **"Create API key in new project"** (or choose existing project)
3. Click **"Create"**
4. **Copy your API key** (starts with `AIza...`)

⚠️ **Important**: Save this key securely! You won't be able to see it again.

---

## ⚙️ Add API Key to Your Project

### Method 1: Environment Variable (Recommended)
```bash
# Create .env file in project root
echo "GEMINI_API_KEY=YOUR_API_KEY_HERE" > .env
```

### Method 2: Direct in Code (Quick Test)
Edit `backend/routers/chat.py`:
```python
GEMINI_API_KEY = "AIzaSyYOUR_ACTUAL_API_KEY_HERE"
```

---

## 📊 Gemini Free Tier Limits

✅ **60 requests per minute**  
✅ **1,500 requests per day**  
✅ **Totally FREE!**  

Perfect for your ADAS project!

---

## 🚀 Test Your Setup

### Step 1: Start Backend
```bash
export GEMINI_API_KEY="YOUR_API_KEY"
python3 -m uvicorn backend.main:app --host 0.0.0.0 --port 8000 --reload
```

### Step 2: Test Chat Endpoint
```bash
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello AI!"}'
```

You should get a response from the AI!

---

## ✅ Verify Setup

### Start Both Servers
```bash
# Terminal 1 - Backend (withAPI key)
export GEMINI_API_KEY="YOUR_KEY"
python3 -m uvicorn backend.main:app --host 0.0.0.0 --port 8000 --reload

# Terminal 2 - Frontend
cd frontend && npm run dev
```

### Open Dashboard
Visit: **http://localhost:5173**

You should now see:
- 🤖 AI Chat section on the right
- Type questions and get AI responses!
- Click quick questions for instant answers

---

## 💬 What You Can Ask the AI

### About Alerts:
- "What alerts did I get recently?"
- "Explain the last alert"
- "How many close calls today?"

### Safety Tips:
- "Give me driving safety tips"
- "How can I avoid accidents?"
- "What should I do in heavy traffic?"

### System Questions:
- "How does ADAS work?"
- "What is the safe following distance?"
- "Explain object detection"

---

## 🐛 Troubleshooting

### "API key not found"
```bash
# Make sure to export the key before running backend
export GEMINI_API_KEY="AIzaSy..."
python3 -m uvicorn backend.main:app --reload
```

### "Quota exceeded"
- You've hit the 60/minute limit
- Wait 1 minute and try again
- Or upgrade to paid plan (optional)

### "Invalid API key"
- Check you copied the full key
- Ensure no extra spaces
- Generate a new key if needed

---

## 🔒 Security Best Practices

1. ✅ Never commit API key to Git
2. ✅ Use environment variables
3. ✅ Add `.env` to `.gitignore`
4. ✅ Rotate keys periodically

---

## 🎯 Next Steps

Once setup:
1. Test the chat with different questions
2. Customize the system prompt in `backend/routers/chat.py`
3. Add more AI features (voice commands, etc.)

Your ADAS now has AI superpowers! 🚀
