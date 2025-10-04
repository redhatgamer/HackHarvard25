import React from 'react';
import { Link } from 'react-router-dom';

const About = () => {
  return (
    <div className="about">
      <div className="container">
        {/* Hero Section */}
        <section className="about-hero">
          <h1 className="page-title">About Hirono</h1>
          <p className="hero-text">
            Born from a passion for creating meaningful digital relationships, 
            Hirono represents the next evolution in virtual companionship.
          </p>
        </section>

        {/* Story Section */}
        <section className="story-section">
          <div className="story-content">
            <h2 className="section-title">Our Story</h2>
            <div className="story-text">
              <p>
                In the bustling world of modern technology, we noticed something was missing - 
                genuine connection. While our devices became smarter, they often felt colder. 
                That's when the idea of Hirono was born.
              </p>
              <p>
                Named after the Japanese concept of "広野" (hirono), meaning "wide field" or 
                "expansive plain", our virtual companion represents endless possibilities for 
                connection and growth. Hirono isn't just software; it's a friend, a helper, 
                and a companion designed to bring warmth to your digital experience.
              </p>
              <p>
                What started as a simple desktop pet has evolved into a sophisticated AI 
                companion that learns, grows, and adapts to your unique personality and needs. 
                Every interaction helps Hirono become more attuned to your preferences, 
                creating a truly personalized experience.
              </p>
            </div>
          </div>
          <div className="story-visual">
            <img src="/api/placeholder/400/300" alt="Hirono Development" className="story-image" />
          </div>
        </section>

        {/* Mission Section */}
        <section className="mission-section">
          <h2 className="section-title">Our Mission</h2>
          <div className="mission-grid">
            <div className="mission-card">
              <div className="mission-icon">🤝</div>
              <h3>Connection</h3>
              <p>
                Foster meaningful digital relationships that enrich daily life 
                and provide genuine companionship in our increasingly connected world.
              </p>
            </div>
            <div className="mission-card">
              <div className="mission-icon">🌱</div>
              <h3>Growth</h3>
              <p>
                Create an AI that grows with you, learning your preferences and 
                adapting to support your personal and professional development.
              </p>
            </div>
            <div className="mission-card">
              <div className="mission-icon">✨</div>
              <h3>Joy</h3>
              <p>
                Bring moments of delight and wonder to everyday interactions, 
                making technology feel more human and approachable.
              </p>
            </div>
          </div>
        </section>

        {/* Technology Section */}
        <section className="technology-section">
          <h2 className="section-title">The Technology Behind Hirono</h2>
          <div className="tech-content">
            <div className="tech-text">
              <h3>Advanced AI Integration</h3>
              <p>
                Hirono is powered by Google's Gemini AI, providing natural language 
                processing and intelligent responses that make conversations feel 
                authentic and engaging.
              </p>
              
              <h3>Adaptive Learning</h3>
              <p>
                Our companion uses machine learning algorithms to understand your 
                preferences, schedule, and interaction patterns, becoming more 
                helpful over time.
              </p>
              
              <h3>Cross-Platform Compatibility</h3>
              <p>
                Built with modern technologies including Python, Tkinter for the 
                desktop application, and web technologies for broader accessibility.
              </p>
            </div>
            <div className="tech-specs">
              <h3>Technical Specifications</h3>
              <ul className="specs-list">
                <li><strong>AI Engine:</strong> Google Gemini Pro</li>
                <li><strong>Framework:</strong> Python 3.13+</li>
                <li><strong>UI Library:</strong> Tkinter with modern components</li>
                <li><strong>Animations:</strong> Custom animation system</li>
                <li><strong>Screen Capture:</strong> Real-time monitoring</li>
                <li><strong>Data Storage:</strong> Local configuration files</li>
                <li><strong>Privacy:</strong> Fully local processing</li>
              </ul>
            </div>
          </div>
        </section>

        {/* Team Section */}
        <section className="team-section">
          <h2 className="section-title">Meet the Creator</h2>
          <div className="team-card">
            <div className="team-member">
              <img src="/api/placeholder/150/150" alt="Creator" className="member-photo" />
              <div className="member-info">
                <h3>Development Team</h3>
                <p className="member-role">AI & Software Engineers</p>
                <p className="member-bio">
                  A passionate team of developers dedicated to creating meaningful 
                  AI experiences that enhance human connection rather than replace it. 
                  We believe in technology that serves humanity with warmth and intelligence.
                </p>
              </div>
            </div>
          </div>
        </section>

        {/* Values Section */}
        <section className="values-section">
          <h2 className="section-title">Our Values</h2>
          <div className="values-grid">
            <div className="value-item">
              <h3>Privacy First</h3>
              <p>
                Your interactions with Hirono remain private. All processing 
                happens locally on your device, ensuring your personal data stays personal.
              </p>
            </div>
            <div className="value-item">
              <h3>Open Development</h3>
              <p>
                We believe in transparency. Our development process is open, 
                and we welcome feedback from our community to improve Hirono.
              </p>
            </div>
            <div className="value-item">
              <h3>Ethical AI</h3>
              <p>
                Hirono is designed to be helpful, harmless, and honest. We're 
                committed to responsible AI development that benefits users.
              </p>
            </div>
            <div className="value-item">
              <h3>Continuous Innovation</h3>
              <p>
                We're constantly exploring new ways to make Hirono more helpful, 
                engaging, and meaningful in your daily life.
              </p>
            </div>
          </div>
        </section>

        {/* Contact Section */}
        <section className="contact-section">
          <h2 className="section-title">Get In Touch</h2>
          <div className="contact-content">
            <p>
              Have questions, suggestions, or just want to say hello? 
              We'd love to hear from you!
            </p>
            <div className="contact-methods">
              <a href="mailto:hello@hirono.ai" className="contact-method">
                <i className="fas fa-envelope"></i>
                <span>hello@hirono.ai</span>
              </a>
              <a href="https://github.com/hirono-project" className="contact-method">
                <i className="fab fa-github"></i>
                <span>GitHub Repository</span>
              </a>
              <a href="https://twitter.com/hironoai" className="contact-method">
                <i className="fab fa-twitter"></i>
                <span>@HironoAI</span>
              </a>
            </div>
          </div>
        </section>

        {/* CTA Section */}
        <section className="cta-section">
          <div className="cta-content">
            <h2>Ready to Meet Hirono?</h2>
            <p>
              Join thousands of users who have already discovered the joy 
              of having an AI companion by their side.
            </p>
            <div className="cta-buttons">
              <Link to="/shop" className="cta-button primary">
                <i className="fas fa-shopping-cart"></i>
                Visit Shop
              </Link>
              <button className="cta-button secondary">
                <i className="fas fa-download"></i>
                Download Free Version
              </button>
            </div>
          </div>
        </section>
      </div>
    </div>
  );
};

export default About;