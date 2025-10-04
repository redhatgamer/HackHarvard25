import React, { useState, useEffect } from 'react';
import { Link, useLocation } from 'react-router-dom';

const Navbar = () => {
  const [isMenuOpen, setIsMenuOpen] = useState(false);
  const [isScrolled, setIsScrolled] = useState(false);
  const location = useLocation();

  useEffect(() => {
    const handleScroll = () => {
      setIsScrolled(window.scrollY > 50);
    };
    window.addEventListener('scroll', handleScroll);
    return () => window.removeEventListener('scroll', handleScroll);
  }, []);

  const toggleMenu = () => {
    setIsMenuOpen(!isMenuOpen);
  };

  const isActive = (path) => {
    return location.pathname === path;
  };

  const navItems = [
    { path: '/', label: 'HOME', icon: '' },
    { path: '/shop', label: 'SHOP', icon: '' },
    { path: '/about', label: 'ABOUT', icon: '' }
  ];

  return (
    <nav className={`navbar cardboard-nav ${isScrolled ? 'scrolled' : ''}`}>
      <div className="nav-tape tape-left"></div>
      <div className="nav-tape tape-right"></div>
      
      <div className="nav-container">
        <div className="nav-logo cardboard-label">
          <div className="label-pin"></div>
          <Link to="/" className="logo-text marker-title">HIRONO</Link>
          <span className="logo-subtitle handwritten-text">ヒロノ</span>
          <div className="logo-doodle"></div>
        </div>
        
        <ul className={`nav-menu ${isMenuOpen ? 'active' : ''}`}>
          {navItems.map((item, index) => (
            <li key={item.path} className="nav-item">
              <Link 
                to={item.path} 
                className={`nav-link cardboard-tab ${isActive(item.path) ? 'active' : ''}`}
                onClick={() => setIsMenuOpen(false)}
              >
                <div className="tab-tape"></div>
                <span className="nav-icon">{item.icon}</span>
                <span className="nav-text">{item.label}</span>
                <div className="tab-shadow"></div>
              </Link>
            </li>
          ))}
        </ul>
        
        <div 
          className={`hamburger cardboard-button mobile-toggle ${isMenuOpen ? 'active' : ''}`} 
          onClick={toggleMenu}
        >
          <div className="button-tape"></div>
          <div className="hamburger-lines">
            <span className="line"></span>
            <span className="line"></span>
            <span className="line"></span>
          </div>
          <div className="button-shadow"></div>
        </div>
      </div>
    </nav>
  );
};

export default Navbar;