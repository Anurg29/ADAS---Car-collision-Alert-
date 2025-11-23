import { useState, useEffect, useRef } from 'react'
import axios from 'axios'
import VoiceControl from './VoiceControl'
import './AdminDashboard.css' // Reuse the styles

import { API_URL } from './config';

function UserDashboard({ user, onLogout }) {
    const [isConnected, setIsConnected] = useState(false)
    const [useLocalCamera, setUseLocalCamera] = useState(false)
    const [activeWarnings, setActiveWarnings] = useState(0)
    const videoRef = useRef(null)

    // Check backend connectivity
    useEffect(() => {
        const checkBackend = async () => {
            try {
                const response = await axios.get(`${API_URL}/camera/status`, { timeout: 3000 })
                if (response.data.camera_initialized) {
                    setIsConnected(true)
                    setUseLocalCamera(false)
                } else {
                    setIsConnected(true)
                    setUseLocalCamera(true)
                }
            } catch (error) {
                setIsConnected(false)
                setUseLocalCamera(true)
            }
        }
        checkBackend()
        const interval = setInterval(checkBackend, 5000)
        return () => clearInterval(interval)
    }, [])

    const [lastAlert, setLastAlert] = useState(null)
    const [showPopup, setShowPopup] = useState(false)

    // Poll for latest alerts and warnings
    useEffect(() => {
        if (!isConnected) return;
        const fetchStatus = async () => {
            try {
                const response = await axios.get(`${API_URL}/alerts?limit=1`)
                const latest = response.data[0]

                // Update warnings count (mock logic if needed, or rely on backend)
                // For now, assume if latest alert is close, it's a warning
                if (latest && latest.distance < 50) {
                    setActiveWarnings(1)
                } else {
                    setActiveWarnings(0)
                }

                // Check for new alert to show popup
                if (latest && (!lastAlert || latest.id !== lastAlert.id)) {
                    setLastAlert(latest)
                    setShowPopup(true)
                    // Hide popup after 5 seconds
                    setTimeout(() => setShowPopup(false), 5000)

                    // Voice feedback
                    if (latest.distance < 30) {
                        const msg = new SpeechSynthesisUtterance(`Warning. ${latest.object_class} detected at ${latest.distance} meters.`);
                        window.speechSynthesis.speak(msg);
                    }
                }
            } catch (error) {
                console.error(error)
            }
        }
        const interval = setInterval(fetchStatus, 2000)
        return () => clearInterval(interval)
    }, [isConnected, lastAlert])

    // Local Camera Logic
    useEffect(() => {
        if (!useLocalCamera) return;
        const startLocalCamera = async () => {
            try {
                const stream = await navigator.mediaDevices.getUserMedia({ video: { facingMode: 'user' } })
                if (videoRef.current) videoRef.current.srcObject = stream
            } catch (err) { console.error(err) }
        }
        startLocalCamera()
        return () => {
            if (videoRef.current && videoRef.current.srcObject) {
                videoRef.current.srcObject.getTracks().forEach(track => track.stop())
            }
        }
    }, [useLocalCamera])

    const handleVoiceCommand = (command) => {
        if (command === 'status') {
            const msg = new SpeechSynthesisUtterance(`System is ${isConnected ? 'Online' : 'Offline'}. ${activeWarnings} active warnings.`);
            window.speechSynthesis.speak(msg);
        }
    };

    return (
        <div className="app-container hud-mode"> {/* Force HUD mode for drivers */}
            <header className="header">
                <div className="header-content">
                    <div className="logo-section">
                        <div className="logo-icon">🚘</div>
                        <div>
                            <h1 className="title">Driver Mode</h1>
                            <p className="subtitle">Focus on the Road</p>
                        </div>
                    </div>
                    <div className="status-section">
                        <div className="user-info">
                            <span className="user-email">{user.email}</span>
                            <button onClick={onLogout} className="logout-btn">Logout</button>
                            <small style={{ display: 'block', fontSize: '10px', marginTop: '4px', opacity: 0.7 }}>
                                Not you? Login as Admin
                            </small>
                        </div>
                        <div className={`status-indicator ${isConnected ? 'connected' : 'disconnected'}`}>
                            <span className="status-dot"></span>
                            {isConnected ? 'System Active' : 'Local Backup'}
                        </div>
                    </div>
                </div>
            </header>

            <main className="main-grid" style={{ gridTemplateColumns: '1fr' }}> {/* Full width video */}
                <section className="video-section" style={{ height: 'calc(100vh - 100px)' }}>
                    <div className="video-wrapper">
                        {useLocalCamera ? (
                            <video ref={videoRef} autoPlay playsInline muted className="local-video" />
                        ) : (
                            <img src={`${API_URL}/video_feed`} alt="Live Feed" className="video-feed"
                                onError={(e) => { e.target.style.display = 'none'; setUseLocalCamera(true); }} />
                        )}

                        {/* HUD Overlay Elements */}
                        <div className="hud-overlay">
                            <div className="hud-crosshair"></div>
                            <div className="hud-info top-left">DRIVER ASSIST: ON</div>
                            <div className="hud-info top-right">{new Date().toLocaleTimeString()}</div>
                            <div className="hud-info bottom-center">
                                {activeWarnings > 0 ? '⚠️ OBSTACLE DETECTED' : 'PATH CLEAR'}
                            </div>
                        </div>

                        {/* New Alert Popup */}
                        {showPopup && lastAlert && (
                            <div className="alert-popup">
                                <div className="popup-header">
                                    <span className="popup-title">📸 New Capture</span>
                                    <span className="popup-time">{new Date(lastAlert.timestamp).toLocaleTimeString()}</span>
                                </div>
                                <img
                                    src={`${API_URL}/alerts/${lastAlert.id}/image`}
                                    alt="Detection"
                                    className="popup-image"
                                    onError={(e) => e.target.style.display = 'none'}
                                />
                                <div className="popup-details">
                                    <span className="popup-class">{lastAlert.object_class}</span>
                                    <span className="popup-dist">{lastAlert.distance.toFixed(1)}m</span>
                                </div>
                            </div>
                        )}
                    </div>
                </section>
            </main>

            <VoiceControl onCommand={handleVoiceCommand} />
        </div>
    )
}

export default UserDashboard
