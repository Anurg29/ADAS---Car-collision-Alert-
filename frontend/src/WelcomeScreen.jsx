import { useState, useEffect } from 'react';
import './WelcomeScreen.css';

function WelcomeScreen({ user, onComplete }) {
    const [step, setStep] = useState(0);
    const [isAnimating, setIsAnimating] = useState(true);

    useEffect(() => {
        // Auto-progress through animation
        const timer = setTimeout(() => {
            if (step < 3) {
                setStep(step + 1);
            } else {
                setTimeout(() => {
                    setIsAnimating(false);
                    onComplete();
                }, 1000);
            }
        }, 1500);

        return () => clearTimeout(timer);
    }, [step, onComplete]);

    const features = [
        {
            icon: "🎥",
            title: "Live AI Detection",
            description: "Real-time object detection with YOLOv5"
        },
        {
            icon: "🤖",
            title: "AI Assistant",
            description: "Chat with your intelligent driving coach"
        },
        {
            icon: "🛡️",
            title: "Safety Alerts",
            description: "Instant proximity warnings under 50m"
        },
        {
            icon: "📊",
            title: "Analytics",
            description: "Track your driving patterns and improve"
        }
    ];

    if (!isAnimating) return null;

    return (
        <div className="welcome-screen">
            <div className="welcome-background">
                <div className="grid-animation"></div>
                <div className="particles"></div>
            </div>

            <div className="welcome-content">
                {step === 0 && (
                    <div className="welcome-step fade-in">
                        <div className="welcome-logo">
                            <div className="logo-circle">
                                <span className="logo-icon">🚗</span>
                            </div>
                            <div className="logo-pulse"></div>
                        </div>
                        <h1 className="welcome-title glow">Welcome to ADAS</h1>
                        <p className="welcome-subtitle">Advanced Driver Assistance System</p>
                    </div>
                )}

                {step === 1 && (
                    <div className="welcome-step fade-in">
                        <div className="user-greeting">
                            <div className="greeting-avatar">
                                <span>👋</span>
                            </div>
                            <h2 className="greeting-text">
                                Hello, <span className="user-name">{user.email.split('@')[0]}</span>!
                            </h2>
                            <p className="greeting-subtitle">Let's get you started</p>
                        </div>
                    </div>
                )}

                {step === 2 && (
                    <div className="welcome-step fade-in">
                        <h2 className="features-title">Powered by AI Technology</h2>
                        <div className="features-grid">
                            {features.map((feature, idx) => (
                                <div key={idx} className="feature-card" style={{ animationDelay: `${idx * 0.1}s` }}>
                                    <div className="feature-icon">{feature.icon}</div>
                                    <h3 className="feature-title">{feature.title}</h3>
                                    <p className="feature-description">{feature.description}</p>
                                </div>
                            ))}
                        </div>
                    </div>
                )}

                {step === 3 && (
                    <div className="welcome-step fade-in">
                        <div className="ready-screen">
                            <div className="checkmark-circle">
                                <span className="checkmark">✓</span>
                            </div>
                            <h2 className="ready-title">You're All Set!</h2>
                            <p className="ready-subtitle">Launching your dashboard...</p>
                            <div className="progress-bar">
                                <div className="progress-fill"></div>
                            </div>
                        </div>
                    </div>
                )}
            </div>
        </div>
    );
}

export default WelcomeScreen;
