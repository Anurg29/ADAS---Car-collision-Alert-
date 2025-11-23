# Firebase Hosting Deployment Guide

## 🚀 Deploy Your ADAS Website to Firebase

This guide will help you host your ADAS dashboard on Firebase so it's accessible from anywhere!

---

## ⚠️ Important: Two-Part Deployment

Your ADAS system has two parts:
1. **Frontend (React Dashboard)** → Can be hosted on Firebase ✅
2. **Backend (FastAPI + Camera)** → Needs a server (see alternatives below) ⚠️

---

## Part 1: Deploy Frontend to Firebase

### Step 1: Login to Firebase
```bash
firebase login
```
This will open your browser. Sign in with your Google account.

### Step 2: Initialize Firebase
```bash
firebase init
```

When prompted:
1. **Select features**: Choose **"Hosting"** (use spacebar to select, enter to continue)
2. **Use existing project**: Yes
3. **Select project**: Choose **"ADAS"** (your project)
4. **Public directory**: Type `frontend/dist` and press Enter
5. **Configure as SPA**: **Yes**
6. **Set up automatic builds**: **No**
7. **Overwrite index.html**: **No**

### Step 3: Update Firebase Config
1. Go to Firebase Console: https://console.firebase.google.com/
2. Click your **"ADAS"** project
3. Go to Project Settings (gear icon)
4. Scroll to "Your apps" and copy your config
5. Paste it in `frontend/src/firebase.js`

Example:
```javascript
const firebaseConfig = {
  apiKey: "AIzaSyB1a2b3c4d5e6f7g8h9i0j...",
  authDomain: "adas-12345.firebaseapp.com",
  projectId: "adas-12345",
  storageBucket: "adas-12345.appspot.com",
  messagingSenderId: "123456789012",
  appId: "1:123456789012:web:abcdef123456"
};
```

### Step 4: Build Frontend for Production
```bash
cd frontend
npm run build
cd ..
```

This creates an optimized production build in `frontend/dist/`.

### Step 5: Deploy to Firebase
```bash
firebase deploy
```

You'll get a URL like: **`https://adas-12345.web.app`**

---

## 🎉 Your Frontend is Now Live!

Visit your deployment URL to see your dashboard online!

**Note**: The camera feed won't work yet because the backend isn't deployed. See Part 2 below.

---

## Part 2: Backend Deployment Options

Your backend (FastAPI + camera access) **cannot** run on Firebase Hosting because:
- Firebase Hosting is for static files only
- Your backend needs Python, camera access, and MySQL

### Option A: Keep Backend Local (Easiest)
**Best for**: Development and personal use

1. Run backend on your computer:
   ```bash
   python3 -m uvicorn backend.main:app --host 0.0.0.0 --port 8000
   ```

2. Use **ngrok** to expose it to the internet:
   ```bash
   # Install ngrok
   brew install ngrok
   
   # Expose port 8000
   ngrok http 8000
   ```

3. Update frontend API URL:
   - Edit `frontend/src/Dashboard.jsx`
   - Replace `http://localhost:8000` with your ngrok URL
   - Example: `https://abc123.ngrok.io`

4. Rebuild and redeploy frontend

**Pros**: Easy, free  
**Cons**: Computer must stay on, URL changes each time

---

### Option B: Deploy to Railway/Render (Recommended for Production)
**Best for**: Production deployment

#### Using Railway.app (Free tier available):

1. Go to https://railway.app/
2. Sign up with GitHub
3. Create new project → "Deploy from GitHub repo"
4. Connect your ADAS repository
5. Configure:
   - **Root Directory**: Leave empty or `/`
   - **Start Command**: `uvicorn backend.main:app --host 0.0.0.0 --port $PORT`
6. Add environment variables:
   - `MYSQL_HOST`, `MYSQL_USER`, `MYSQL_PASSWORD`, `MYSQL_DATABASE`
7. Deploy!

You'll get a URL like: `https://adas-production.up.railway.app`

**Then update frontend**:
- Edit `frontend/src/Dashboard.jsx`
- Replace `localhost:8000` with your Railway URL
- Rebuild: `npm run build`
- Redeploy: `firebase deploy`

---

### Option C: Deploy to Google Cloud Run (Advanced)
**Best for**: Scalable production with Google integration

1. Containerize backend with Docker
2. Push to Google Container Registry
3. Deploy to Cloud Run
4. Connect to Cloud SQL for MySQL

(Full tutorial available if needed)

---

## 📝 Quick Deployment Checklist

- [ ] Firebase CLI installed (`npm install -g firebase-tools`)
- [ ] Logged into Firebase (`firebase login`)
- [ ] Firebase config updated in `frontend/src/firebase.js`
- [ ] Frontend built (`cd frontend && npm run build`)
- [ ] Deployed to Firebase (`firebase deploy`)
- [ ] Backend deployed (choose option A, B, or C)
- [ ] Frontend updated with backend URL
- [ ] Rebuilt and redeployed frontend
- [ ] Tested live website!

---

## 🔧 Update Backend URL in Frontend

When you have your backend URL, update these files:

**`frontend/src/Dashboard.jsx`**:
```javascript
// Change this:
const response = await axios.get('http://localhost:8000/alerts?limit=10')

// To this:
const response = await axios.get('https://your-backend-url.com/alerts?limit=10')

// Also update the image src:
src="https://your-backend-url.com/video_feed"
src={`https://your-backend-url.com/alerts/${alert.id}/image`}
```

---

## 🌐 Custom Domain (Optional)

After deployment, you can add a custom domain:

1. Firebase Console → Hosting
2. Click "Add custom domain"
3. Follow DNS setup instructions
4. Your site will be at: `https://yourdomain.com`

---

## 🔄 Updating Your Site

When you make changes:

```bash
# 1. Make changes to your code
# 2. Rebuild frontend
cd frontend
npm run build
cd ..

# 3. Deploy
firebase deploy
```

---

## 🐛 Troubleshooting

### "Command not found: firebase"
```bash
npm install -g firebase-tools
```

### Build fails
```bash
cd frontend
rm -rf node_modules
npm install
npm run build
```

### CORS errors with backend
Add CORS middleware in `backend/main.py` with your frontend URL:
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://adas-12345.web.app"],  # Your Firebase URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

---

## 📊 Deployment Summary

| Component | Hosting Solution | Cost | Complexity |
|-----------|-----------------|------|------------|
| Frontend | Firebase Hosting | Free | ⭐ Easy |
| Backend (Dev) | Local + ngrok | Free | ⭐⭐ Medium |
| Backend (Prod) | Railway/Render | Free tier | ⭐⭐⭐ Medium |
| Database | MySQL (Local) | Free | ⭐ Easy |
| Database (Prod) | PlanetScale/Railway | Free tier | ⭐⭐⭐ Medium |

---

## 🎯 Recommended Setup

**For Development/Testing**:
- Frontend → Firebase Hosting
- Backend → Local + ngrok
- Database → Local MySQL

**For Production**:
- Frontend → Firebase Hosting
- Backend → Railway.app
- Database → Railway MySQL or PlanetScale

---

**Need help?** Check the Firebase Console for deployment logs and errors!

**Your website will be live at**: `https://adas-XXXXX.web.app` 🚀
