# 🚀 Railway.app Deployment Guide

## Quick Deployment (5 minutes)

### Step 1: Create Railway Account
1. Go to: https://railway.app
2. Click "Start a New Project"
3. Sign up with GitHub (recommended)

### Step 2: Deploy from GitHub

#### Option A: Deploy from GitHub (Recommended)
1. Push your code to GitHub
2. In Railway, click "Deploy from GitHub repo"
3. Select your repository
4. Railway will auto-detect and deploy!

#### Option B: Deploy with Railway CLI
```bash
# Install Railway CLI
npm install -g @railway/cli

# Login
railway login

# Initialize and deploy
railway init
railway up
```

### Step 3: Get Your Public URL
1. Go to your Railway dashboard
2. Click on your project
3. Go to "Settings" → "Domains"
4. Click "Generate Domain"
5. Copy your URL: `https://your-app.up.railway.app`

### Step 4: Update Frontend
Edit `frontend/src/Dashboard.jsx`:
```javascript
// Change from:
const API_URL = 'http://localhost:8000';

// To:
const API_URL = 'https://your-app.up.railway.app';
```

---

## 📋 What Railway Will Do

✅ Install Python packages from `requirements.txt`  
✅ Start the backend with `Procfile`  
✅ Provide a public HTTPS URL  
✅ Auto-deploy on git push  
✅ Free $5/month credit  

---

## 🎯 Quick Commands

```bash
# Check deployment status
railway status

# View logs
railway logs

# Open in browser
railway open
```

---

## 🔧 Environment Variables (Optional)

If you want to add any secrets:
1. Go to Railway dashboard
2. Click "Variables"
3. Add:
   - `GEMINI_API_KEY=your_key` (if you want AI chat)

---

## 💡 Free Tier Limits

- $5 credit per month
- ~500 hours of runtime
- Perfect for your ADAS project!

---

## 🚨 Troubleshooting

### Build fails?
- Check `requirements.txt` has all dependencies
- Make sure Python 3.10+ is used

### Can't access camera?
- Railway servers don't have webcams
- Backend will show "Camera Offline" (this is OK!)
- You can still test all other features

### Deployment stuck?
```bash
railway logs --follow
```

---

## ✅ Success!

Once deployed, you'll have:
- 🌐 Public backend URL
- 🚀 Always online (no localhost needed!)
- 📱 Accessible from anywhere
- 🔄 Auto-deploys on code changes

Share your deployed URL with anyone to showcase your ADAS system!
