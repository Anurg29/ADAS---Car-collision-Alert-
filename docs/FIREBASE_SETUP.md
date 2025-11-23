# Firebase Setup Guide

## 🔥 Step 1: Create Firebase Project

1. Go to [Firebase Console](https://console.firebase.google.com/)
2. Click **"Add project"**
3. Enter project name: `adas-system` (or any name)
4. Disable Google Analytics (optional)
5. Click **"Create project"**

---

## 🔑 Step 2: Enable Authentication

1. In Firebase Console, click **"Authentication"** in left menu
2. Click **"Get Started"**
3. Click **"Email/Password"** under Sign-in providers
4. **Enable** the toggle
5. Click **"Save"**

---

## 📝 Step 3: Get Firebase Config

1. Click the gear icon ⚙️ → **"Project settings"**
2. Scroll down to **"Your apps"**
3. Click the **Web icon** (`</>`)
4. Register app name: `ADAS Dashboard`
5. **Copy the firebaseConfig object**

Example:
```javascript
const firebaseConfig = {
  apiKey: "AIzaSyD...",
  authDomain: "adas-system.firebaseapp.com",
  projectId: "adas-system",
  storageBucket: "adas-system.appspot.com",
  messagingSenderId: "123456789",
  appId: "1:123456789:web:abc123"
};
```

---

## 🔧 Step 4: Update Your Code

1. Open `frontend/src/firebase.js`
2. **Replace** the placeholder values with your actual config:

```javascript
const firebaseConfig = {
  apiKey: "YOUR_ACTUAL_API_KEY",           // ← Paste here
  authDomain: "YOUR_PROJECT.firebaseapp.com",
  projectId: "YOUR_PROJECT_ID",
  storageBucket: "YOUR_PROJECT_ID.appspot.com",
  messagingSenderId: "YOUR_SENDER_ID",
  appId: "YOUR_APP_ID"
};
```

---

## 👤 Step 5: Create First User

### Option A: Through Firebase Console
1. Go to **Authentication** → **Users** tab
2. Click **"Add user"**
3. Enter email and password
4. Click **"Add user"**

### Option B: Through Your App
1. Run `./run_web.sh`
2. Open http://localhost:5173
3. Click **"Sign Up"**
4. Enter email and password (min 6 characters)
5. Click **"Sign Up"**

---

## ✅ Step 6: Verify Setup

1. Open http://localhost:5173
2. You should see the **login screen**
3. Sign in with your credentials
4. You should see the **dashboard**
5. Check Firebase Console → Users to see your registered user

---

## 🔒 Security Features Now Active

✅ **Login Required**: Users must authenticate to view dashboard  
✅ **Protected Routes**: Unauthenticated users redirected to login  
✅ **Secure Sessions**: Firebase handles token management  
✅ **User Tracking**: See who accessed the system  
✅ **Logout Function**: Users can securely log out  

---

## 🚨 Important Notes

### DO NOT share your Firebase config publicly!
- Add `.env` file for sensitive data (optional enhancement)
- Never commit API keys to GitHub

### Password Requirements
- Minimum 6 characters
- Firebase handles all validation

### User Management
- View all users in Firebase Console → Authentication
- Delete users, reset passwords from console
- Enable additional providers (Google, GitHub, etc.)

---

## 🔐 Backend Protection (Optional Next Step)

To fully secure the API:

1. Install Firebase Admin SDK (already done)
2. Verify Firebase tokens in backend middleware
3. Protect `/video_feed` and `/alerts` endpoints

This ensures even direct API calls require authentication!

---

## 📞 Troubleshooting

### "Firebase not defined"
- Check that `firebase.js` is properly imported
- Verify Firebase config is correct

### "Email already in use"
- User already exists
- Use "Sign In" instead of "Sign Up"

### "Wrong password"
- Check password is correct
- Must be at least 6 characters

### Can't see login screen
- Clear browser cache
- Check console for errors (F12)

---

**Ready to use!** Your ADAS system is now protected by Firebase Authentication! 🎉
