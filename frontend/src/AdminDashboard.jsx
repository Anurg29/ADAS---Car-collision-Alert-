import { useState, useEffect, useRef } from 'react'
import axios from 'axios'
import AIChat from './AIChat'
import DeveloperInfo from './DeveloperInfo'
import Notifications from './Notifications'
import VoiceControl from './VoiceControl'
import './AdminDashboard.css'

import { API_URL } from './config';

function AdminDashboard({ user, onLogout, onStartTutorial }) {
    const [alerts, setAlerts] = useState([])
    const [isConnected, setIsConnected] = useState(false)
    const [stats, setStats] = useState({ totalAlerts: 0, activeWarnings: 0 })
    const [useLocalCamera, setUseLocalCamera] = useState(false)
    const [hudMode, setHudMode] = useState(false) // New HUD Mode
    const videoRef = useRef(null)
    const canvasRef = useRef(null)

    // Check backend connectivity with retry logic
    useEffect(() => {
        let isMounted = true;

        const checkBackend = async () => {
            try {
                // Check specifically for camera status
                const response = await axios.get(`${API_URL}/camera/status`, { timeout: 3000 })

                if (isMounted) {
                    if (response.data.camera_initialized) {
                        setIsConnected(true)
                        setUseLocalCamera(false)
                    } else {
                        // Backend is up, but camera failed
                        console.warn("Backend up, but camera failed")
                        setIsConnected(true) // Still connected to server
                        setUseLocalCamera(true) // But use local camera
                    }
                }
            } catch (error) {
                if (isMounted) {
                    console.log("Backend offline, switching to local mode")
                    setIsConnected(false)
                    setUseLocalCamera(true)
                }
            }
        }

        checkBackend()
        const interval = setInterval(checkBackend, 5000) // Check every 5s
        return () => {
            isMounted = false;
            clearInterval(interval)
        }
    }, [])

    // Fetch alerts and system stats
    useEffect(() => {
        if (!isConnected) return;

        const fetchData = async () => {
            try {
                // 1. Fetch Alerts
                let alertsData = []
                try {
                    const response = await axios.get(`${API_URL}/alerts?limit=10`)
                    alertsData = response.data || []

                    // Fallback to captures if alerts empty
                    if (alertsData.length === 0) {
                        const capResponse = await axios.get(`${API_URL}/captures?limit=10`)
                        if (capResponse.data && capResponse.data.length > 0) {
                            alertsData = capResponse.data.map(cap => ({
                                id: cap.timestamp,
                                timestamp: new Date(cap.timestamp * 1000).toISOString(),
                                object_class: 'car',
                                confidence: 0.9,
                                distance: parseFloat(cap.distance.replace('m', '')),
                                image_path: cap.url
                            }))
                        }
                    }
                } catch (e) { console.warn("Alerts fetch failed", e) }

                setAlerts(alertsData)

                // 2. Fetch Admin Stats (Users, etc.)
                let adminStats = { total_users: 0, active_users: 0 }
                try {
                    const statsResponse = await axios.get(`${API_URL}/admin/stats`)
                    adminStats = statsResponse.data
                } catch (e) { console.warn("Stats fetch failed", e) }

                // Update State
                setStats({
                    totalAlerts: alertsData.length,
                    activeWarnings: alertsData.filter(a => a.distance < 50).length,
                    totalUsers: adminStats.total_users,
                    activeUsers: adminStats.active_users
                })

            } catch (error) {
                console.error("Error fetching dashboard data:", error)
            }
        }

        const interval = setInterval(fetchData, 2000)
        fetchData()
        return () => clearInterval(interval)
    }, [isConnected])

    // Access user's local camera
    useEffect(() => {
        if (!useLocalCamera) return;

        const startLocalCamera = async () => {
            try {
                const stream = await navigator.mediaDevices.getUserMedia({
                    video: { facingMode: 'user' }
                })
                if (videoRef.current) {
                    videoRef.current.srcObject = stream
                }
            } catch (err) {
                console.error('Error accessing camera:', err)
            }
        }

        startLocalCamera()

        return () => {
            if (videoRef.current && videoRef.current.srcObject) {
                videoRef.current.srcObject.getTracks().forEach(track => track.stop())
            }
        }
    }, [useLocalCamera])

    const captureImage = () => {
        if (!videoRef.current || !canvasRef.current) return;

        const video = videoRef.current
        const canvas = canvasRef.current
        canvas.width = video.videoWidth
        canvas.height = video.videoHeight
        const ctx = canvas.getContext('2d')
        ctx.drawImage(video, 0, 0)

        // Download the image
        canvas.toBlob((blob) => {
            const url = URL.createObjectURL(blob)
            const a = document.createElement('a')
            a.href = url
            a.download = `capture_${Date.now()}.jpg`
            a.click()
            URL.revokeObjectURL(url)
        }, 'image/jpeg')
    }

    const handleVoiceCommand = (command) => {
        console.log("Voice Command Received:", command);
        if (command === 'capture') {
            captureImage();
        } else if (command === 'toggle_camera') {
            setUseLocalCamera(!useLocalCamera);
        } else if (command === 'status') {
            alert(`System Status: ${isConnected ? 'Online' : 'Offline'}\nActive Warnings: ${stats.activeWarnings}`);
        }
    };

    return (
        <div className={`app-container ${hudMode ? 'hud-mode' : ''}`}>
            <header className="header">
                <div className="header-content">
                    <div className="logo-section">
                        <div className="logo-icon">🚗</div>
                        <div>
                            <h1 className="title">ADAS Control Center</h1>
                            <p className="subtitle">Advanced Driver Assistance System</p>
                        </div>
                    </div>
                    <div className="status-section">
                        <div className="user-info">
                            <span className="user-email">{user.email}</span>
                            {user.emailVerified && <span className="verified-badge">✓ Verified</span>}
                            <button onClick={onLogout} className="logout-btn">Logout</button>
                        </div>
                        <div className={`status-indicator ${isConnected ? 'connected' : 'disconnected'}`}>
                            <span className="status-dot"></span>
                            {isConnected ? 'Server Online' : 'Using Local Camera'}
                        </div>
                        <button
                            className={`hud-toggle ${hudMode ? 'active' : ''}`}
                            onClick={() => setHudMode(!hudMode)}
                        >
                            {hudMode ? '🖥️ Standard' : '🏎️ HUD Mode'}
                        </button>
                    </div>
                </div>
            </header>

            <div className="stats-bar">
                <div className="stat-card">
                    <div className="stat-value">{stats.totalAlerts}</div>
                    <div className="stat-label">Total Alerts</div>
                </div>
                <div className="stat-card warning">
                    <div className="stat-value">{stats.activeWarnings}</div>
                    <div className="stat-label">Active Warnings</div>
                </div>
                <div className="stat-card">
                    <div className="stat-value">{stats.totalUsers || 0}</div>
                    <div className="stat-label">Users Online</div>
                </div>
                <div className="stat-card">
                    <div className="stat-value">{useLocalCamera ? 'Local' : 'Server'}</div>
                    <div className="stat-label">Camera Mode</div>
                </div>
            </div>

            <main className="main-grid">
                <section className="video-section">
                    <div className="section-header">
                        <h2>Live Camera Feed</h2>
                        <div className="camera-controls">
                            {useLocalCamera && (
                                <button onClick={captureImage} className="capture-btn">
                                    📸 Capture
                                </button>
                            )}
                            <div className="recording-badge">
                                <span className="rec-dot"></span>
                                {useLocalCamera ? 'LOCAL' : 'RECORDING'}
                            </div>
                        </div>
                    </div>
                    <div className="video-wrapper">
                        {useLocalCamera ? (
                            <>
                                <video
                                    ref={videoRef}
                                    autoPlay
                                    playsInline
                                    muted
                                    className="local-video"
                                />
                                <canvas ref={canvasRef} style={{ display: 'none' }} />
                            </>
                        ) : (
                            <>
                                <img
                                    src={`${API_URL}/video_feed`}
                                    alt="Live Feed"
                                    className="video-feed"
                                    onError={(e) => {
                                        e.target.style.display = 'none'
                                        setUseLocalCamera(true)
                                    }}
                                />
                            </>
                        )}

                        {/* HUD Overlay Elements */}
                        {hudMode && (
                            <div className="hud-overlay">
                                <div className="hud-crosshair"></div>
                                <div className="hud-info top-left">RADAR: ACTIVE</div>
                                <div className="hud-info top-right">REC: {new Date().toLocaleTimeString()}</div>
                                <div className="hud-info bottom-center">
                                    {stats.activeWarnings > 0 ? '⚠️ PROXIMITY ALERT' : 'ALL CLEAR'}
                                </div>
                            </div>
                        )}
                    </div>
                </section>

                <section className="alerts-section">
                    <div className="section-header">
                        <h2>Proximity Alerts</h2>
                        <div className="refresh-indicator">
                            <span className="refresh-icon">↻</span>
                            {isConnected ? 'Live' : 'Offline'}
                        </div>
                    </div>
                    <div className="alerts-scroll">
                        {alerts.length === 0 ? (
                            <div className="empty-state">
                                <div className="empty-icon">🛡️</div>
                                <p className="empty-text">
                                    {isConnected ? 'No alerts detected' : 'Server offline'}
                                </p>
                                <p className="empty-subtext">
                                    {isConnected ? 'System is monitoring' : 'Using local camera mode'}
                                </p>
                            </div>
                        ) : (
                            <div className="alerts-list">
                                {alerts.map(alert => (
                                    <div key={alert.id} className={`alert-card ${alert.distance < 30 ? 'critical' : 'warning'}`}>
                                        <div className="alert-top">
                                            <div className="alert-time-distance">
                                                <span className="alert-time">
                                                    {new Date(alert.timestamp).toLocaleTimeString()}
                                                </span>
                                                <span className={`alert-distance ${alert.distance < 30 ? 'critical' : 'warning'}`}>
                                                    {alert.distance.toFixed(1)}m
                                                </span>
                                            </div>
                                            <div className="alert-badge">{alert.object_class}</div>
                                        </div>
                                        <div className="alert-details">
                                            <div className="detail-row">
                                                <span className="detail-label">Confidence</span>
                                                <div className="confidence-bar">
                                                    <div
                                                        className="confidence-fill"
                                                        style={{ width: `${alert.confidence * 100}%` }}
                                                    ></div>
                                                    <span className="confidence-text">{(alert.confidence * 100).toFixed(0)}%</span>
                                                </div>
                                            </div>
                                        </div>
                                        <div className="alert-image-container">
                                            <img
                                                src={`${API_URL}/alerts/${alert.id}/image`}
                                                alt="Alert Snapshot"
                                                className="alert-image"
                                            />
                                        </div>
                                    </div>
                                ))}
                            </div>
                        )}
                    </div>
                </section>

                <section className="ai-chat-section">
                    <AIChat isBackendOnline={isConnected} />
                </section>
            </main>

            {/* Developer Info Sidebar */}
            <DeveloperInfo />

            {/* Auto-Capture Notifications */}
            <Notifications alerts={alerts} />

            {/* Voice Control System */}
            <VoiceControl onCommand={handleVoiceCommand} />
        </div>
    )
}

export default AdminDashboard
