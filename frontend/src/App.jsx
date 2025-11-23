import { useState, useEffect } from 'react'
import { onAuthStateChanged, signOut } from 'firebase/auth'
import { auth } from './firebase'
import Login from './Login'
import AdminDashboard from './AdminDashboard'
import UserDashboard from './UserDashboard'
import WelcomeScreen from './WelcomeScreen'
import TutorialGuide from './TutorialGuide'
import './App.css'

function App() {
    const [user, setUser] = useState(null)
    const [loading, setLoading] = useState(true)
    const [showWelcome, setShowWelcome] = useState(false)
    const [showTutorial, setShowTutorial] = useState(false)

    useEffect(() => {
        const unsubscribe = onAuthStateChanged(auth, (currentUser) => {
            setUser(currentUser)
            setLoading(false)

            // Show welcome screen EVERY TIME user logs in
            if (currentUser) {
                setShowWelcome(true)
            }
        })

        return () => unsubscribe()
    }, [])


    const handleLogout = async () => {
        try {
            await signOut(auth)
            sessionStorage.removeItem('welcomeShown')
        } catch (error) {
            console.error('Logout error:', error)
        }
    }

    const handleWelcomeComplete = () => {
        setShowWelcome(false)
        // Only show tutorial for new users or admins
        if (user?.email === 'admin@adas.com') {
            setTimeout(() => setShowTutorial(true), 500)
        }
    }

    const handleTutorialClose = () => {
        setShowTutorial(false)
    }

    const startTutorial = () => {
        setShowTutorial(true)
    }

    if (loading) {
        return (
            <div className="loading-screen">
                <div className="loader"></div>
                <p>Loading ADAS System...</p>
            </div>
        )
    }

    if (!user) {
        return <Login />
    }

    // Role-based Routing
    const isAdmin = user.email === 'admin@adas.com';

    return (
        <>
            {showWelcome && <WelcomeScreen user={user} onComplete={handleWelcomeComplete} />}
            {showTutorial && <TutorialGuide onClose={handleTutorialClose} />}

            {isAdmin ? (
                <AdminDashboard user={user} onLogout={handleLogout} onStartTutorial={startTutorial} />
            ) : (
                <UserDashboard user={user} onLogout={handleLogout} />
            )}
        </>
    )
}

export default App
