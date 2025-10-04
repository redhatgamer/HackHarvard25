import React from 'react';

const About = () => {
  return (
    <div className="about simple-about">
      <div className="container">
        <section className="about-content cardboard-section">
          <div className="cardboard-box simple-box horizontal-layout">
            <div className="tape tape-top-right"></div>
            
            <h1 className="about-title">About HIRO</h1>
            
            <div className="about-horizontal-container">
              <div className="about-text-content">
                <div className="why-section">
                  <h2 className="section-title">Why HIRO?</h2>
                  <p className="why-text">
                    We created HIRO to bring companionship to your digital life. 
                    In a world where technology often feels cold and impersonal, 
                    HIRO provides warmth, personality, and genuine interaction 
                    right on your desktop.
                  </p>
                </div>
                
                <div className="github-section">
                  <h2 className="section-title">Source Code</h2>
                  <a 
                    href="https://github.com/redhatgamer/HackHarvard25" 
                    target="_blank" 
                    rel="noopener noreferrer"
                    className="github-link"
                  >
                    <i className="fab fa-github"></i>
                    View on GitHub
                  </a>
                </div>
              </div>
              
              <div className="about-image-content">
                <div className="thank-you-image-container">
                  <img 
                    src="/thankyou.jpg" 
                    alt="Thank you" 
                    className="thank-you-image"
                  />
                  <div className="image-credit">
                    <a 
                      href="https://www.instagram.com/langswork/?hl=en" 
                      target="_blank" 
                      rel="noopener noreferrer"
                      className="credit-link"
                    >
                      <i className="fab fa-instagram"></i>
                      Design by @langswork
                    </a>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </section>
      </div>
    </div>
  );
};

export default About;