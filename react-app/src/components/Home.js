import React from 'react';
import { Link } from 'react-router-dom';

const Home = () => {
  return (
    <div className="home">
      {/* Hero Section */}
      <section className="hero">
        <div className="hero-content">
          <div className="hero-title-wrapper">
            <h1 className="hero-title">HIRONO</h1>
            <p className="hero-subtitle">ヒロノ - Your AI Companion</p>
          </div>
          <p className="hero-description">
            Experience the magic of virtual companionship with Hirono, 
            an intelligent desktop pet that brings joy and assistance to your daily routine.
          </p>
          <div className="hero-buttons">
            <a href="/shop" className="cta-button primary">
              <i className="fas fa-download"></i>
              Download Now
            </a>
            <button className="cta-button secondary">
              <i className="fas fa-play"></i>
              Watch Demo
            </button>
          </div>
        </div>
        <div className="hero-visual">
          <div className="pet-showcase">
            <img src="/api/placeholder/300/300" alt="Hirono Pet" className="pet-image" />
            <div className="showcase-effects">
              <div className="sparkle sparkle-1">✨</div>
              <div className="sparkle sparkle-2">⭐</div>
              <div className="sparkle sparkle-3">💫</div>
            </div>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="features">
        <div className="container">
          <h2 className="section-title">What Makes Hirono Special?</h2>
          <div className="features-grid">
            <div className="feature-card">
              <div className="feature-icon">🤖</div>
              <h3>AI-Powered Intelligence</h3>
              <p>Hirono learns from your interactions and adapts to your preferences using advanced AI technology.</p>
            </div>
            <div className="feature-card">
              <div className="feature-icon">🎮</div>
              <h3>Interactive Gameplay</h3>
              <p>Engage with mini-games, customization options, and dynamic responses that keep you entertained.</p>
            </div>
            <div className="feature-card">
              <div className="feature-icon">💝</div>
              <h3>Emotional Connection</h3>
              <p>Build a meaningful relationship with your virtual companion through daily interactions and care.</p>
            </div>
            <div className="feature-card">
              <div className="feature-icon">⚙️</div>
              <h3>Smart Assistance</h3>
              <p>Get help with daily tasks, reminders, and productivity features integrated into your workflow.</p>
            </div>
          </div>
        </div>
      </section>

      {/* Collection Preview */}
      <section className="collection-preview">
        <div className="container">
          <h2 className="section-title">Meet Our Digital Companions</h2>
          <div className="preview-grid">
            <div className="preview-card">
              <img src="/api/placeholder/200/200" alt="Hirono Classic" />
              <h3>Hirono Classic</h3>
              <p>The original companion</p>
            </div>
            <div className="preview-card">
              <img src="/api/placeholder/200/200" alt="Hirono Pixel" />
              <h3>Hirono Pixel</h3>
              <p>Retro gaming vibes</p>
            </div>
            <div className="preview-card">
              <img src="/api/placeholder/200/200" alt="Hirono Zen" />
              <h3>Hirono Zen</h3>
              <p>Peaceful meditation buddy</p>
            </div>
          </div>
          <div className="preview-actions">
            <Link to="/shop" className="cta-button primary">
              Explore All Companions
            </Link>
          </div>
        </div>
      </section>

      {/* Stats Section */}
      <section className="stats">
        <div className="container">
          <div className="stats-grid">
            <div className="stat-item">
              <div className="stat-number">10K+</div>
              <div className="stat-label">Happy Users</div>
            </div>
            <div className="stat-item">
              <div className="stat-number">500+</div>
              <div className="stat-label">Interactions Daily</div>
            </div>
            <div className="stat-item">
              <div className="stat-number">24/7</div>
              <div className="stat-label">Companionship</div>
            </div>
            <div className="stat-item">
              <div className="stat-number">100%</div>
              <div className="stat-label">AI-Powered</div>
            </div>
          </div>
        </div>
      </section>
    </div>
  );
};

export default Home;