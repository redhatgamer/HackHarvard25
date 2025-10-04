import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';

const About = () => {
  const [activeSection, setActiveSection] = useState('story');
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
      { threshold: 0.2 }
    );

    const sections = document.querySelectorAll('.animate-section');
    sections.forEach((section) => observer.observe(section));

    return () => observer.disconnect();
  }, []);

  return (
    <div className="about cardboard-workspace">
      <div className="container">
        {/* Hero Section */}
        <section className="about-hero cardboard-section">
          <div className="cardboard-box hero-journal">
            <div className="journal-binding"></div>
            <div className="tape tape-top-right"></div>
            
            <div className="journal-header">
              <h1 className="page-title handwritten-title">About Hirono</h1>
              <div className="title-underline sketch"></div>
              <div className="page-number">Page 1</div>
            </div>
            
            <p className="hero-text handwritten-text">
              Born from a passion for creating meaningful digital relationships, 
              Hirono represents the next evolution in virtual companionship.
            </p>
            
            <div className="hero-doodles">
              <span className="doodle heart"></span>
              <span className="doodle star"></span>
              <span className="doodle robot"></span>
            </div>
          </div>
        </section>

        {/* Story Section */}
        <section className={`story-section animate-section ${isVisible['story'] ? 'visible' : ''}`} id="story">
          <div className="story-layout">
            <div className="story-notebook">
              <div className="notebook-spiral"></div>
              <div className="notebook-holes"></div>
              
              <div className="story-content">
                <h2 className="section-title marker-title">Our Story</h2>
                <div className="story-pages">
                  <div className="story-page">
                    <div className="page-lines"></div>
                    <div className="story-text handwritten-text">
                      <p>
                        In the bustling world of modern technology, we noticed something was missing - 
                        genuine connection. While our devices became smarter, they often felt colder. 
                        That's when the idea of Hirono was born.
                      </p>
                      <div className="margin-note">
                        <span className="note-arrow">→</span>
                        <span className="note-text">The spark!</span>
                      </div>
                    </div>
                  </div>
                  
                  <div className="story-page">
                    <div className="page-lines"></div>
                    <div className="story-text handwritten-text">
                      <p>
                        Named after the Japanese concept of "広野" (hirono), meaning "wide field" or 
                        "expansive plain", our virtual companion represents endless possibilities for 
                        connection and growth.
                      </p>
                      <div className="highlight-box">
                        <span className="highlight-text">Hirono isn't just software; it's a friend!</span>
                      </div>
                    </div>
                  </div>
                  
                  <div className="story-page">
                    <div className="page-lines"></div>
                    <div className="story-text handwritten-text">
                      <p>
                        What started as a simple desktop pet has evolved into a sophisticated AI 
                        companion that learns, grows, and adapts to your unique personality and needs.
                      </p>
                      <div className="story-doodle">idea → growth → AI</div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
            
            <div className="story-visual polaroid-collection">
              <div className="polaroid main-photo">
                <div className="polaroid-tape"></div>
                <img src="/api/placeholder/300/250" alt="Hirono Development" />
                <div className="photo-caption handwritten-text">Early prototype sketches</div>
              </div>
              
              <div className="polaroid side-photo-1">
                <div className="polaroid-tape"></div>
                <img src="/api/placeholder/200/180" alt="Team brainstorming" />
                <div className="photo-caption handwritten-text">Team brainstorming</div>
              </div>
              
              <div className="polaroid side-photo-2">
                <div className="polaroid-tape"></div>
                <img src="/api/placeholder/180/200" alt="First working version" />
                <div className="photo-caption handwritten-text">First working version!</div>
              </div>
            </div>
          </div>
        </section>

        {/* Mission Section */}
        <section className={`mission-section animate-section ${isVisible['mission'] ? 'visible' : ''}`} id="mission">
          <div className="mission-board">
            <div className="board-header">
              <h2 className="section-title marker-title">Our Mission</h2>
              <div className="pushpins">
                <div className="pushpin red"></div>
                <div className="pushpin blue"></div>
                <div className="pushpin green"></div>
              </div>
            </div>
            
            <div className="mission-notes">
              {[
                { 
                  icon: "C", 
                  title: "Connection", 
                  text: "Foster meaningful digital relationships that enrich daily life and provide genuine companionship.",
                  color: "yellow"
                },
                { 
                  icon: "G", 
                  title: "Growth", 
                  text: "Create an AI that grows with you, learning your preferences and adapting to support your development.",
                  color: "green"
                },
                { 
                  icon: "J", 
                  title: "Joy", 
                  text: "Bring moments of delight and wonder to everyday interactions, making technology feel more human.",
                  color: "pink"
                }
              ].map((mission, index) => (
                <div key={index} className={`mission-note sticky-note ${mission.color}`}>
                  <div className="note-pin"></div>
                  <div className="mission-icon doodle-icon">{mission.icon}</div>
                  <h3 className="handwritten-title">{mission.title}</h3>
                  <p className="handwritten-text">{mission.text}</p>
                  <div className="note-fold"></div>
                </div>
              ))}
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