import { useState, useEffect } from 'react';
import './Notifications.css';

function Notifications({ alerts }) {
    const [notifications, setNotifications] = useState([]);
    const [lastAlertId, setLastAlertId] = useState(null);

    useEffect(() => {
        if (alerts.length > 0) {
            const latestAlert = alerts[0];

            // Only show notification for new alerts
            if (latestAlert.id !== lastAlertId) {
                setLastAlertId(latestAlert.id);

                // Create notification
                const notification = {
                    id: latestAlert.id,
                    message: `${latestAlert.object_class} detected at ${latestAlert.distance.toFixed(1)}m!`,
                    type: latestAlert.distance < 30 ? 'critical' : latestAlert.distance < 50 ? 'warning' : 'info',
                    timestamp: new Date(),
                    image: `/api/alerts/${latestAlert.id}/image`
                };

                setNotifications(prev => [notification, ...prev].slice(0, 5));

                // Play sound for critical alerts
                if (latestAlert.distance < 30) {
                    playAlertSound();
                }

                // Auto-remove after 5 seconds
                setTimeout(() => {
                    setNotifications(prev => prev.filter(n => n.id !== notification.id));
                }, 5000);
            }
        }
    }, [alerts, lastAlertId]);

    const playAlertSound = () => {
        // Create beep sound
        const audioContext = new (window.AudioContext || window.webkitAudioContext)();
        const oscillator = audioContext.createOscillator();
        const gainNode = audioContext.createGain();

        oscillator.connect(gainNode);
        gainNode.connect(audioContext.destination);

        oscillator.frequency.value = 800;
        oscillator.type = 'sine';

        gainNode.gain.setValueAtTime(0.3, audioContext.currentTime);
        gainNode.gain.exponentialRampToValueAtTime(0.01, audioContext.currentTime + 0.5);

        oscillator.start(audioContext.currentTime);
        oscillator.stop(audioContext.currentTime + 0.5);
    };

    const dismissNotification = (id) => {
        setNotifications(prev => prev.filter(n => n.id !== id));
    };

    return (
        <div className="notifications-container">
            {notifications.map(notification => (
                <div
                    key={notification.id}
                    className={`notification ${notification.type} slide-in`}
                >
                    <div className="notification-icon">
                        {notification.type === 'critical' ? '🚨' :
                            notification.type === 'warning' ? '⚠️' : 'ℹ️'}
                    </div>
                    <div className="notification-content">
                        <div className="notification-title">
                            {notification.type === 'critical' ? 'CRITICAL ALERT!' :
                                notification.type === 'warning' ? 'Warning!' : 'Detection'}
                        </div>
                        <div className="notification-message">{notification.message}</div>
                        <div className="notification-time">
                            📸 Picture captured • {new Date(notification.timestamp).toLocaleTimeString()}
                        </div>
                    </div>
                    <button
                        className="notification-close"
                        onClick={() => dismissNotification(notification.id)}
                    >
                        ✕
                    </button>
                </div>
            ))}
        </div>
    );
}

export default Notifications;
