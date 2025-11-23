import { useState } from 'react';
import './TutorialGuide.css';

function TutorialGuide({ onClose }) {
    const [currentStep, setCurrentStep] = useState(0);

    const steps = [
        {
            title: "Welcome to Your ADAS Dashboard",
            description: "Let's take a quick tour to show you around!",
            icon: "🎯",
            target: null
        },
        {
            title: "Live Camera Feed",
            description: "This is your real-time video feed with AI-powered object detection. Watch as YOLO identifies vehicles, pedestrians, and obstacles!",
            icon: "🎥",
            target: ".video-section",
            highlight: true
        },
        {
            title: "Proximity Alerts",
            description: "Get instant alerts when objects come within 50 meters. Each alert shows the object type, distance, confidence level, and a snapshot!",
            icon: "🚨",
            target: ".alerts-section",
            highlight: true
        },
        {
            title: "AI Assistant",
            description: "Chat with your intelligent driving coach! Ask questions about alerts, get safety tips, or request driving advice. It's powered by Google Gemini AI!",
            icon: "🤖",
            target: ".ai-chat-section",
            highlight: true
        },
        {
            title: "Quick Actions",
            description: "Use the quick question buttons for instant answers, or type your own questions in natural language!",
            icon: "⚡",
            target: ".quick-questions",
            highlight: true
        },
        {
            title: "System Status",
            description: "Check your connection status, camera mode, and total alerts at a glance in the stats bar.",
            icon: "📊",
            target: ".stats-bar",
            highlight: true
        },
        {
            title: "You're All Set!",
            description: "You're now ready to use your AI-powered ADAS system. Drive safely and let the AI assist you!",
            icon: "✨",
            target: null
        }
    ];

    const nextStep = () => {
        if (currentStep < steps.length - 1) {
            setCurrentStep(currentStep + 1);
        } else {
            onClose();
        }
    };

    const prevStep = () => {
        if (currentStep > 0) {
            setCurrentStep(currentStep - 1);
        }
    };

    const skip = () => {
        onClose();
    };

    const step = steps[currentStep];

    return (
        <>
            {/* Overlay */}
            <div className="tutorial-overlay" onClick={skip}></div>

            {/* Spotlight highlight */}
            {step.highlight && step.target && (
                <div className="tutorial-spotlight" data-target={step.target}></div>
            )}

            {/* Tutorial card */}
            <div className={`tutorial-card ${step.target ? 'positioned' : 'centered'}`}>
                <div className="tutorial-header">
                    <div className="tutorial-icon">{step.icon}</div>
                    <button onClick={skip} className="tutorial-skip">✕</button>
                </div>

                <div className="tutorial-content">
                    <h2 className="tutorial-title">{step.title}</h2>
                    <p className="tutorial-description">{step.description}</p>
                </div>

                <div className="tutorial-footer">
                    <div className="tutorial-progress">
                        <span className="progress-text">
                            {currentStep + 1} / {steps.length}
                        </span>
                        <div className="progress-dots">
                            {steps.map((_, idx) => (
                                <div
                                    key={idx}
                                    className={`progress-dot ${idx === currentStep ? 'active' : ''} ${idx < currentStep ? 'completed' : ''}`}
                                />
                            ))}
                        </div>
                    </div>

                    <div className="tutorial-actions">
                        {currentStep > 0 && (
                            <button onClick={prevStep} className="tutorial-btn secondary">
                                ← Back
                            </button>
                        )}
                        <button onClick={nextStep} className="tutorial-btn primary">
                            {currentStep === steps.length - 1 ? "Get Started! 🚀" : "Next →"}
                        </button>
                    </div>
                </div>
            </div>
        </>
    );
}

export default TutorialGuide;
