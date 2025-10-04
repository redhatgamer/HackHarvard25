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
          
          <div className="hero-content">
            <div className="hero-title-wrapper">
              <h1 className="hero-title cardboard-text animated-title">
                <span className="letter">H</span>
                <span className="letter">I</span>
                <span className="letter">R</span>
                <span className="letter">O</span>
                <span className="letter">N</span>
                <span className="letter">O</span>
              </h1>
              <p className="hero-subtitle marker-text fade-in-up">ヒロノ - Your AI Companion</p>
              <div className="title-underline animated-underline"></div>
            </div>
            <p className="hero-description handwritten-text fade-in-up-delayed">
              Experience the magic of virtual companionship with Hirono, 
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
          
          <div className="hero-visual enhanced-visual">
            <div className="pet-showcase cardboard-frame floating-card">
              <div className="frame-corners animated-corners">
                <div className="corner top-left"></div>
                <div className="corner top-right"></div>
                <div className="corner bottom-left"></div>
                <div className="corner bottom-right"></div>
              </div>
              <div className="image-container">
                <img src="/api/placeholder/300/300" alt="Hirono Pet" className="pet-image hover-zoom" />
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

      {/* Tech Stack Section */}
      <section className={`tech-stack animate-section ${isVisible['techstack'] ? 'visible' : ''}`} id="techstack">
        <div className="container">
          <div className="section-header cardboard-label">
            <h2 className="section-title marker-title">Built with Modern Technology</h2>
            <div className="label-pin"></div>
          </div>
          
          <div className="tech-grid">
            {techStack.map((tech, index) => (
              <div 
                key={index}
                className={`tech-card ${activeFeature === index ? 'active' : ''}`}
                onMouseEnter={() => setActiveFeature(index)}
                style={{ 
                  animationDelay: `${index * 0.2}s`,
                  '--tech-color': tech.color 
                }}
              >
                <div className="card-header">
                  <div className="tech-logo-container">
                    <img 
                      src={tech.logo} 
                      alt={`${tech.title} logo`} 
                      className="tech-logo"
                      style={{ '--tech-color': tech.color }}
                      onError={(e) => {
                        e.target.style.display = 'none';
                        e.target.nextSibling.style.display = 'block';
                      }}
                    />
                    <div className="tech-fallback" style={{ display: 'none', fontSize: '3.5rem' }}>
                      {tech.fallback}
                    </div>
                  </div>
                  <h3 className="tech-title">{tech.title}</h3>
                </div>
                
                <div className="card-body">
                  <p className="tech-description">{tech.desc}</p>
                </div>
                
                <div className="card-footer">
                  <div className="tech-badge" style={{ backgroundColor: tech.color }}>
                    Technology
                  </div>
                </div>
                
                <div className="card-corner-tape"></div>
                <div className="card-shadow"></div>
              </div>
            ))}
          </div>
        </div>
      </section>
    </div>
  );
};

export default Home;