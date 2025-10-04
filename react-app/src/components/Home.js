import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';

const Home = () => {
  const [activeFeature, setActiveFeature] = useState(0);
  const [isVisible, setIsVisible] = useState({});

  useEffect(() => {
    const observer = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          setIsVisible(prev => ({
            ...prev,
            [entry.target.id]: entry.isIntersecting
          }));
        });
      },
      { threshold: 0.3 }
    );

    const sections = document.querySelectorAll('.animate-section');
    sections.forEach((section) => observer.observe(section));

    return () => observer.disconnect();
  }, []);

  const techStack = [
    { 
      logo: "https://raw.githubusercontent.com/devicons/devicon/master/icons/react/react-original.svg", 
      fallback: "R",
      title: "React.js", 
      desc: "Modern frontend framework for building interactive user interfaces with component-based architecture.",
      color: "#61DAFB"
    },
    { 
      logo: "https://raw.githubusercontent.com/devicons/devicon/master/icons/python/python-original.svg", 
      fallback: "P",
      title: "Python", 
      desc: "Powerful backend language for AI integration, data processing, and desktop application development.",
      color: "#3776AB"
    },
    { 
      logo: "https://upload.wikimedia.org/wikipedia/commons/8/8a/Google_Gemini_logo.svg", 
      fallback: "G",
      title: "Google Gemini AI", 
      desc: "Advanced artificial intelligence for natural language processing and intelligent responses.",
      color: "#4285F4"
    },
    { 
      logo: "https://upload.wikimedia.org/wikipedia/commons/thumb/0/0a/Python_logo_and_wordmark.svg/320px-Python_logo_and_wordmark.svg.png", 
      fallback: "T",
      title: "Tkinter", 
      desc: "Cross-platform GUI toolkit for creating native desktop applications and interactive experiences.",
      color: "#306998"
    }
  ];

  return (
    <div className="home">
      {/* Enhanced Hero Section */}
      <section className="hero cardboard-section enhanced-hero">
        <div className="floating-elements">
          <div className="float-shape shape-1"></div>
          <div className="float-shape shape-2"></div>
          <div className="float-shape shape-3"></div>
          <div className="float-shape shape-4"></div>
        </div>
        
        <div className="cardboard-box hero-box animated-entrance">
          <div className="tape tape-top-left animated-tape"></div>
          <div className="tape tape-top-right animated-tape"></div>
          <div className="tape tape-bottom-left animated-tape"></div>
          <div className="tape tape-bottom-right animated-tape"></div>
          <div className="gradient-overlay"></div>
          
          <div className="hero-layout">
            <div className="hero-content">
            <div className="hero-title-wrapper">
              <h1 className="hero-title cardboard-text animated-title">
                <span className="letter">H</span>
                <span className="letter">I</span>
                <span className="letter">R</span>
                <span className="letter">O</span>
              </h1>
              <div className="title-underline animated-underline"></div>
            </div>
            <p className="hero-description handwritten-text fade-in-up-delayed">
              Experience the magic of virtual companionship with Hiro, 
              an intelligent desktop pet that brings joy and assistance to your daily routine.
            </p>
            <div className="hero-buttons staggered-buttons">
              <Link to="/shop" className="cardboard-button primary pulse-button">
                <div className="button-tape"></div>
                <span className="button-glow"></span>
                <i className="fas fa-download"></i>
                Download Now
                <div className="button-shadow"></div>
              </Link>
              <button className="cardboard-button secondary hover-tilt">
                <div className="button-tape"></div>
                <span className="button-glow"></span>
                <i className="fas fa-play"></i>
                Watch Demo
                <div className="button-shadow"></div>
              </button>
            </div>
          </div>
          
          <div className="hero-image-section">
            <div className="mark-image-container cardboard-frame">
              <div className="frame-corners animated-corners">
                <div className="corner top-left"></div>
                <div className="corner top-right"></div>
                <div className="corner bottom-left"></div>
                <div className="corner bottom-right"></div>
              </div>
              <img src="/mark.jpg" alt="Hiro Figure Inspiration" className="mark-image hover-zoom" />
              <div className="image-caption handwritten-text">
                Inspired by Hirono figures
              </div>
            </div>
          </div>
        </div>
          
          <div className="hero-visual enhanced-visual">
            <div className="pet-showcase cardboard-frame floating-card">
              <div className="frame-corners animated-corners">
                <div className="corner top-left"></div>
                <div className="corner top-right"></div>
                <div className="corner bottom-left"></div>
                <div className="corner bottom-right"></div>
              </div>
              <div className="image-container">
                <img src="/api/placeholder/300/300" alt="Hiro Pet" className="pet-image hover-zoom" />
                <div className="image-overlay gradient-shine"></div>
              </div>
              <div className="showcase-effects">
                <div className="particle particle-1"></div>
                <div className="particle particle-2"></div>
                <div className="particle particle-3"></div>
                <div className="particle particle-4"></div>
                <div className="particle particle-5"></div>
                <div className="particle particle-6"></div>
              </div>
            </div>
            
            <div className="visual-enhancements">
              <div className="glow-ring"></div>
              <div className="orbit-dots">
                <div className="orbit-dot dot-1"></div>
                <div className="orbit-dot dot-2"></div>
                <div className="orbit-dot dot-3"></div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Tech Workspace Section */}
      <section className={`tech-workspace animate-section ${isVisible['techstack'] ? 'visible' : ''}`} id="techstack">
        <div className="container">
          <div className="workspace-board">
            <div className="board-header">
              <h2 className="workspace-title handwritten-title">HIRO's Tech Stack</h2>
              <div className="board-pins">
                <div className="pin red-pin"></div>
                <div className="pin blue-pin"></div>
                <div className="pin green-pin"></div>
              </div>
            </div>
            
            <div className="tech-cards-workspace">
              {techStack.map((tech, index) => (
                <div 
                  key={index}
                  className={`tech-spec-card ${activeFeature === index ? 'active' : ''}`}
                  onMouseEnter={() => setActiveFeature(index)}
                  style={{ 
                    '--rotation': `${(index % 2 === 0 ? 1 : -1) * (Math.random() * 3 + 1)}deg`,
                    '--tech-color': tech.color 
                  }}
                >
                  <div className="card-pin"></div>
                  
                  <div className="spec-header">
                    <div className="tech-icon-wrapper">
                      <img 
                        src={tech.logo} 
                        alt={`${tech.title} logo`} 
                        className="tech-logo"
                        onError={(e) => {
                          e.target.style.display = 'none';
                          e.target.nextSibling.style.display = 'flex';
                        }}
                      />
                      <div className="tech-fallback" style={{ display: 'none' }}>
                        {tech.fallback}
                      </div>
                    </div>
                    <h3 className="spec-title">{tech.title}</h3>
                    <div className="spec-category" style={{ color: tech.color }}>
                      {index === 0 ? "Frontend Framework" : 
                       index === 1 ? "Backend Language" :
                       index === 2 ? "AI Integration" : "UI Framework"}
                    </div>
                  </div>
                  
                  <div className="spec-content">
                    <p className="spec-description">{tech.desc}</p>
                    
                    <div className="spec-features">
                      <span className="feature-tag">
                        {index === 0 ? "⚛️ Component-Based" :
                         index === 1 ? "🐍 AI-Ready" :
                         index === 2 ? "🤖 Smart Chat" : "🖥️ Cross-Platform"}
                      </span>
                    </div>
                  </div>
                  
                  <div className="card-tape tape-corner"></div>
                </div>
              ))}
            </div>
            
            <div className="workspace-notes">
              <div className="sticky-note yellow" style={{ '--rotation': '2deg' }}>
                <p>🚀 Fast & Responsive</p>
              </div>
              <div className="sticky-note pink" style={{ '--rotation': '-1deg' }}>
                <p>🔧 Easy to Maintain</p>
              </div>
              <div className="sticky-note green" style={{ '--rotation': '3deg' }}>
                <p>🎨 Beautiful UI</p>
              </div>
            </div>
          </div>
        </div>
      </section>
    </div>
  );
};

export default Home;