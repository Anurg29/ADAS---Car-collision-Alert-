// Configuration for API URL
// Priority:
// 1. VITE_API_URL environment variable (for production/cloud hosting)
// 2. Dynamic hostname check (for local network testing)
// 3. Default localhost fallback

const getApiUrl = () => {
    // Check if env var is set (e.g. from .env file)
    if (import.meta.env.VITE_API_URL) {
        return import.meta.env.VITE_API_URL;
    }

    // If running on local network (e.g. 192.168.x.x), try to use the same IP for backend
    if (window.location.hostname !== 'localhost' && window.location.hostname !== '127.0.0.1') {
        return `http://${window.location.hostname}:8000`;
    }

    // Default local fallback
    return 'http://localhost:8000';
};

export const API_URL = getApiUrl();
