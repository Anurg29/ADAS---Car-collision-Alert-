# ADAS Deployment Checklist

## ✅ Pre-Deployment Setup

### 1. Firebase Project Configuration
- [ ] Created Firebase project named "ADAS"
- [ ] Enabled Firebase Authentication (Email/Password)
- [ ] Copied Firebase config to `frontend/src/firebase.js`
- [ ] Verified API key and project ID are correct

### 2. Code Configuration
- [ ] Updated Firebase config in `frontend/src/firebase.js`
- [ ] Checked all API endpoints point to correct backend URL
- [ ] Tested login/signup locally

### 3. Dependencies
- [ ] Installed: `npm install -g firebase-tools`
- [ ] Logged in: `firebase login`
- [ ] Ran: `firebase init` and selected "ADAS" project

---

## 🚀 Deployment Steps

### Frontend Deployment
```bash
# 1. Build frontend
cd frontend
npm run build

# 2. Deploy to Firebase
cd ..
firebase deploy
```

**Or use the deploy script**:
```bash
./deploy.sh
```

### Your Site URL
After deployment, you'll get a URL like:
```
https://adas-XXXXX.web.app
```

---

## 🔧 Backend Setup (Choose One)

### Option A: Local Backend with ngrok (Testing)
```bash
# Terminal 1: Run backend
python3 -m uvicorn backend.main:app --host 0.0.0.0 --port 8000

# Terminal 2: Expose with ngrok  
ngrok http 8000
```

Copy the ngrok URL (e.g., `https://abc123.ngrok.io`) and update `Dashboard.jsx`

### Option B: Railway Deployment (Production)
1. Go to railway.app
2. Deploy backend from GitHub
3. Add database environment variables
4. Get deployment URL
5. Update `Dashboard.jsx` with Railway URL

---

## 📝 Post-Deployment Tasks

- [ ] Test login on live site
- [ ] Create first user account
- [ ] Verify camera feed loads
- [ ] Check alerts are fetching
- [ ] Test logout functionality
- [ ] Share URL with team/users

---

## 🔄 Updating the Site

When you make changes:
```bash
./deploy.sh
```

Or manually:
```bash
cd frontend && npm run build && cd .. && firebase deploy
```

---

## 🌐 Your Deployed URLs

**Frontend (Firebase)**: https://adas-XXXXX.web.app  
**Backend**: (Update after choosing deployment method)

**Firebase Console**: https://console.firebase.google.com/project/adas-XXXXX

---

## 📞 Support

- Firebase docs: https://firebase.google.com/docs/hosting
- Railway docs: https://docs.railway.app/
- Full guide: `docs/DEPLOYMENT_GUIDE.md`

---

**Last Deployment**: _[Date/Time here]_
