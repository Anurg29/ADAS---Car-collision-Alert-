# 🚗 ADAS - Advanced Driver Assistance System

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115.0-green.svg)](https://fastapi.tiangolo.com)
[![React](https://img.shields.io/badge/React-18.0-61DAFB.svg)](https://reactjs.org)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

**AI-Powered Real-Time Object Detection System for Vehicle Safety**

![ADAS Demo](https://img.shields.io/badge/Status-Production%20Ready-success)

---

## 🎯 Overview

ADAS is a production-ready Advanced Driver Assistance System featuring:
- 🎥 **Real-time object detection** using YOLOv5
- 📏 **Distance estimation** and proximity alerts
- 🤖 **AI chatbot** for driving assistance
- 📊 **Web dashboard** with Firebase authentication
- 🔔 **Automated alerts** with image capture
- 📱 **Responsive design** for mobile and desktop

---

## ✨ Features

### Core Functionality
- ✅ Real-time vehicle detection (cars, trucks, buses)
- ✅ Distance calculation and proximity warnings (<50m)
- ✅ Automatic image capture on detection
- ✅ Alert history with timestamps
- ✅ Visual and audio notifications

### Web Interface
- ✅ Modern React dashboard with glassmorphism design
- ✅ Firebase authentication with email verification
- ✅ Welcome animation and interactive tutorial
- ✅ AI chatbot for safety tips
- ✅ Local camera fallback mode

### Backend
- ✅ FastAPI REST API
- ✅ Production-ready (Railway/Render/Fly.io compatible)
- ✅ In-memory alert storage
- ✅ Video streaming endpoint
- ✅ Health check and monitoring

---

## 🚀 Quick Start

### Prerequisites
- Python 3.10+
- Node.js 18+
- Webcam (for local testing)

### Installation

```bash
# Clone the repository
git clone https://github.com/YOUR_USERNAME/ADAS-System.git
cd ADAS-System

# Backend setup
pip install -r requirements.txt

# Frontend setup
cd frontend
npm install
```

### Running Locally

```bash
# Terminal 1 - Backend
python3 -m uvicorn backend.main_production:app --host 0.0.0.0 --port 8000 --reload

# Terminal 2 - Frontend
cd frontend && npm run dev

# Visit: http://localhost:5173
```

---

## 📦 Project Structure

```
ADAS-System/
├── backend/
│   ├── main_production.py      # Production backend
│   ├── camera.py                # Camera & YOLO detection
│   └── routers/                 # API endpoints
├── frontend/
│   ├── src/
│   │   ├── Dashboard.jsx        # Main dashboard
│   │   ├── Login.jsx            # Authentication
│   │   ├── AIChat.jsx           # AI assistant
│   │   ├── WelcomeScreen.jsx    # Onboarding
│   │   └── TutorialGuide.jsx    # Interactive guide
│   └── dist/                    # Built files
├── docs/                        # Documentation
├── requirements.txt             # Python dependencies
├── Procfile                     # Railway deployment
└── README.md                    # This file
```

---

## 🌐 Deployment

### Railway.app (Recommended)

1. Push to GitHub
2. Go to [Railway.app](https://railway.app)
3. Click "Deploy from GitHub"
4. Select this repository
5. ✅ Done! Get your public URL

**Detailed guide:** [docs/RAILWAY_DEPLOYMENT.md](docs/RAILWAY_DEPLOYMENT.md)

### Frontend Deployment (Firebase)

```bash
cd frontend
npm run build
npx firebase-tools deploy
```

---

## 🎓 Usage

1. **Login** - Sign up and verify your email
2. **Welcome** - Watch the intro animation
3. **Tutorial** - Follow the interactive guide
4. **Dashboard** - View live camera with AI detection
5. **Alerts** - Get notified of nearby vehicles
6. **AI Chat** - Ask for safety tips

---

## 🛠️ Tech Stack

### Backend
- **FastAPI** - Modern Python web framework
- **OpenCV** - Computer vision
- **YOLOv5** - Object detection model
- **Uvicorn** - ASGI server

### Frontend
- **React** - UI framework
- **Vite** - Build tool
- **Firebase** - Authentication & hosting
- **Axios** - HTTP client

### Deployment
- **Railway.app** - Backend hosting
- **Firebase Hosting** - Frontend hosting

---

## 📊 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | System status |
| `/video_feed` | GET | Live camera stream |
| `/alerts` | GET | Get recent alerts |
| `/stats` | GET | System statistics |
| `/health` | GET | Health check |

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 👨‍💻 Author

**Anurag Dinesh Rokade**
- GitHub: [@anuragrokade](https://github.com/anuragrokade)
- Email: anuragrokade9@gmail.com

---

## 🙏 Acknowledgments

- YOLOv5 by Ultralytics
- FastAPI by Sebastián Ramírez
- React by Meta
- Firebase by Google

---

## 📸 Screenshots

### Dashboard
![Dashboard](docs/screenshots/dashboard.png)

### Alerts
![Alerts](docs/screenshots/alerts.png)

### AI Chat
![AI Chat](docs/screenshots/ai-chat.png)

---

## 🔮 Future Enhancements

- [ ] Multi-camera support
- [ ] Lane detection
- [ ] Traffic sign recognition
- [ ] Night vision mode
- [ ] Mobile app (React Native)
- [ ] Advanced analytics

---

## ⭐ Star History

If you find this project useful, please consider giving it a star!

[![Star History Chart](https://api.star-history.com/svg?repos=YOUR_USERNAME/ADAS-System&type=Date)](https://star-history.com/#YOUR_USERNAME/ADAS-System&Date)

---

**Made with ❤️ in India**
# ADAS---Car-collision-Alert-
