import { useState, useEffect } from 'react';
import './VoiceControl.css';

const VoiceControl = ({ onCommand }) => {
    const [isListening, setIsListening] = useState(false);
    const [transcript, setTranscript] = useState('');
    const [feedback, setFeedback] = useState('');

    useEffect(() => {
        if (!('webkitSpeechRecognition' in window)) {
            setFeedback('Voice control not supported in this browser.');
            return;
        }

        const recognition = new window.webkitSpeechRecognition();
        recognition.continuous = false;
        recognition.interimResults = false;
        recognition.lang = 'en-US';

        recognition.onstart = () => {
            setIsListening(true);
            setFeedback('Listening...');
        };

        recognition.onresult = (event) => {
            const command = event.results[0][0].transcript.toLowerCase();
            setTranscript(command);
            processCommand(command);
        };

        recognition.onend = () => {
            setIsListening(false);
        };

        recognition.onerror = (event) => {
            setFeedback('Error: ' + event.error);
            setIsListening(false);
        };

        const startBtn = document.getElementById('voice-trigger');
        if (startBtn) {
            startBtn.onclick = () => recognition.start();
        }

        return () => {
            recognition.abort();
        };
    }, []);

    const processCommand = (cmd) => {
        if (cmd.includes('capture') || cmd.includes('photo')) {
            onCommand('capture');
            setFeedback('Command: Capture Image');
        } else if (cmd.includes('local') || cmd.includes('camera')) {
            onCommand('toggle_camera');
            setFeedback('Command: Switching Camera Mode');
        } else if (cmd.includes('status') || cmd.includes('report')) {
            onCommand('status');
            setFeedback('Command: System Status');
        } else {
            setFeedback(`Unknown command: "${cmd}"`);
        }

        // Clear feedback after 3 seconds
        setTimeout(() => setFeedback(''), 3000);
    };

    return (
        <div className={`voice-control-panel ${isListening ? 'active' : ''}`}>
            <button id="voice-trigger" className="voice-btn">
                {isListening ? '🎙️ Listening...' : '🎙️ Voice Command'}
            </button>
            {feedback && <div className="voice-feedback">{feedback}</div>}
        </div>
    );
};

export default VoiceControl;
