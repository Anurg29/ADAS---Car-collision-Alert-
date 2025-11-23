import { useState } from 'react';
import { signInWithEmailAndPassword, createUserWithEmailAndPassword, sendEmailVerification } from 'firebase/auth';
import { auth } from './firebase';
import './Login.css';

function Login() {
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [isSignUp, setIsSignUp] = useState(false);
    const [error, setError] = useState('');
    const [loading, setLoading] = useState(false);
    const [message, setMessage] = useState('');

    const handleSubmit = async (e) => {
        e.preventDefault();
        setError('');
        setMessage('');
        setLoading(true);

        try {
            if (isSignUp) {
                // Sign up with email verification
                const userCredential = await createUserWithEmailAndPassword(auth, email, password);
                await sendEmailVerification(userCredential.user);
                setMessage('Account created! Please check your email to verify your account.');
                setLoading(false);
            } else {
                // Sign in
                const userCredential = await signInWithEmailAndPassword(auth, email, password);
                if (!userCredential.user.emailVerified) {
                    setError('Please verify your email before signing in. Check your inbox!');
                    await auth.signOut();
                    setLoading(false);
                }
            }
        } catch (err) {
            setError(err.message);
            setLoading(false);
        }
    };

    return (
        <div className="login-container">
            <div className="login-box">
                <div className="login-header">
                    <div className="logo-large">🚗</div>
                    <h1>ADAS Security</h1>
                    <p>{isSignUp ? 'Create Account' : 'Sign In'}</p>
                </div>

                <form onSubmit={handleSubmit} className="login-form">
                    <div className="form-group">
                        <label>Email</label>
                        <input
                            type="email"
                            value={email}
                            onChange={(e) => setEmail(e.target.value)}
                            placeholder="Enter your email"
                            required
                        />
                    </div>

                    <div className="form-group">
                        <label>Password</label>
                        <input
                            type="password"
                            value={password}
                            onChange={(e) => setPassword(e.target.value)}
                            placeholder="Enter your password"
                            required
                            minLength="6"
                        />
                    </div>

                    {error && <div className="error-message">{error}</div>}
                    {message && <div className="success-message">{message}</div>}

                    <button type="submit" className="submit-btn" disabled={loading}>
                        {loading ? 'Loading...' : (isSignUp ? 'Sign Up' : 'Sign In')}
                    </button>

                    <div className="toggle-mode">
                        {isSignUp ? 'Already have an account?' : "Don't have an account?"}
                        {' '}
                        <span onClick={() => {
                            setIsSignUp(!isSignUp);
                            setError('');
                            setMessage('');
                        }}>
                            {isSignUp ? 'Sign In' : 'Sign Up'}
                        </span>
                    </div>
                </form>
            </div>
        </div>
    );
}

export default Login;
