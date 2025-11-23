# Deployment Guide

## 1. Frontend Deployment (Firebase)

Your frontend is a React app. We will host it on Firebase Hosting.

### Prerequisites
- Install Firebase tools: `npm install -g firebase-tools`
- Login to Firebase: `firebase login`

### Steps
1. **Build the Frontend:**
   ```bash
   cd frontend
   npm run build
   ```
   This creates a `dist` folder with your production website.

2. **Initialize Firebase (First time only):**
   ```bash
   firebase init hosting
   ```
   - Select "Use an existing project" (or create new).
   - Public directory: `dist`
   - Configure as a single-page app? **Yes**
   - Set up automatic builds and deploys with GitHub? (Optional)
   - Overwrite index.html? **No** (if asked)

3. **Deploy:**
   ```bash
   firebase deploy
   ```
   You will get a URL like `https://your-project.web.app`.

---

## 2. Backend Deployment (Railway)

Your backend is a FastAPI Python app. We will host it on Railway.

### Steps
1. **Push to GitHub:**
   Ensure your latest code is pushed to a GitHub repository.

2. **Create Project on Railway:**
   - Go to [Railway.app](https://railway.app)
   - Click "New Project" -> "Deploy from GitHub repo"
   - Select your repository.

3. **Add Database:**
   - In your Railway project, click "New" -> "Database" -> "MySQL".
   - This will create a cloud database for you.

4. **Configure Environment Variables:**
   - Click on your Backend Service card -> "Variables".
   - Add the following variables (get values from the MySQL service "Connect" tab):
     - `DB_HOST`: (e.g., containers-us-west-1.railway.app)
     - `DB_PORT`: (e.g., 6543)
     - `DB_USER`: root
     - `DB_PASSWORD`: (your railway db password)
     - `DB_NAME`: railway (or whatever the default is)

5. **Wait for Build:**
   Railway will automatically install dependencies from `requirements.txt` and start the server using the `Procfile`.

---

## 3. Connecting Them

1. **Update Frontend Config:**
   - Once your backend is live on Railway, copy its URL (e.g., `https://adas-backend-production.up.railway.app`).
   - In your local project, create/edit `frontend/.env`:
     ```
     VITE_API_URL=https://your-railway-backend-url.app
     ```
   - Re-build and re-deploy the frontend:
     ```bash
     cd frontend
     npm run build
     firebase deploy
     ```

## FAQ: Why not Django?
You asked about using Django. Here is why we stuck with FastAPI:
1. **Performance:** FastAPI is significantly faster for handling real-time video streams and AI inference.
2. **Simplicity:** Django adds a lot of "heavy" features (templating, built-in admin) that we don't need because we have a custom React frontend.
3. **Async Support:** FastAPI's native async support is crucial for handling multiple camera streams and WebSocket connections efficiently.
4. **Effort:** Switching to Django would require rewriting the entire backend logic.
