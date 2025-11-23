// Firebase Configuration for ADAS Project
import { initializeApp } from 'firebase/app';
import { getAuth } from 'firebase/auth';
import { getAnalytics } from 'firebase/analytics';

// Your web app's Firebase configuration
const firebaseConfig = {
    apiKey: "AIzaSyDVZ8nOUDqcLSLr3kdIt-1UYtGyoX1bbOA",
    authDomain: "adas-7c31c.firebaseapp.com",
    projectId: "adas-7c31c",
    storageBucket: "adas-7c31c.firebasestorage.app",
    messagingSenderId: "432179791880",
    appId: "1:432179791880:web:853cec29551526b8ec29bd",
    measurementId: "G-1GMHZ16J1P"
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);
export const auth = getAuth(app);
export const analytics = getAnalytics(app);
export default app;
