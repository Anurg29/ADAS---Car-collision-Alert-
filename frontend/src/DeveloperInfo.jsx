import { useState } from 'react';
import './DeveloperInfo.css';

function DeveloperInfo() {
    const [isExpanded, setIsExpanded] = useState(false);

    const developer = {
        name: "Anurag Dinesh Rokade",
        role: "Full Stack Developer",
        project: "ADAS - Advanced Driver Assistance System",
        email: "anurag@adas.com",
        github: "https://github.com/anuragrokade",
        linkedin: "https://linkedin.com/in/anuragrokade",
        portfolio: "https://anuragrokade.dev",
        technologies: ["React", "FastAPI", "YOLOv5", "MySQL", "Firebase", "Google Gemini AI"],
        year: "2025",
        version: "1.0.0"
    };

    return (
        <>
            {/* Toggle Button */}
            <button
                className="dev-info-toggle"
                onClick={() => setIsExpanded(!isExpanded)}
                title="Developer Info"
            >
                {isExpanded ? '←' : 'ℹ️'}
            </button>

            {/* Sidebar */}
            <div className={`developer-sidebar ${isExpanded ? 'expanded' : ''}`}>
                <div className="dev-sidebar-content">
                    {/* Header */}
                    <div className="dev-header">
                        <div className="dev-avatar">
                            <span className="avatar-icon">👨‍💻</span>
                        </div>
                        <h3 className="dev-title">Developer</h3>
                    </div>

                    {/* Developer Info */}
                    <div className="dev-info-section">
                        <div className="dev-name">{developer.name}</div>
                        <div className="dev-role">{developer.role}</div>
                    </div>

                    {/* Project Info */}
                    <div className="dev-section">
                        <div className="section-label">Project</div>
                        <div className="section-value">{developer.project}</div>
                        <div className="version-badge">v{developer.version}</div>
                    </div>

                    {/* Contact Links */}
                    <div className="dev-section">
                        <div className="section-label">Connect</div>
                        <div className="contact-links">
                            <a href={`mailto:${developer.email}`} className="contact-link" title="Email">
                                <span className="link-icon">📧</span>
                                <span className="link-text">Email</span>
                            </a>
                            <a href={developer.github} target="_blank" rel="noopener noreferrer" className="contact-link" title="GitHub">
                                <span className="link-icon">💻</span>
                                <span className="link-text">GitHub</span>
                            </a>
                            <a href={developer.linkedin} target="_blank" rel="noopener noreferrer" className="contact-link" title="LinkedIn">
                                <span className="link-icon">💼</span>
                                <span className="link-text">LinkedIn</span>
                            </a>
                            <a href={developer.portfolio} target="_blank" rel="noopener noreferrer" className="contact-link" title="Portfolio">
                                <span className="link-icon">🌐</span>
                                <span className="link-text">Portfolio</span>
                            </a>
                        </div>
                    </div>

                    {/* Tech Stack */}
                    <div className="dev-section">
                        <div className="section-label">Built With</div>
                        <div className="tech-stack">
                            {developer.technologies.map((tech, idx) => (
                                <span key={idx} className="tech-badge">{tech}</span>
                            ))}
                        </div>
                    </div>

                    {/* Footer */}
                    <div className="dev-footer">
                        <div className="copyright">
                            © {developer.year} {developer.name}
                        </div>
                        <div className="made-with">
                            Made with <span className="heart">❤️</span> in India
                        </div>
                    </div>
                </div>
            </div>

            {/* Overlay */}
            {isExpanded && (
                <div
                    className="dev-sidebar-overlay"
                    onClick={() => setIsExpanded(false)}
                />
            )}
        </>
    );
}

export default DeveloperInfo;
