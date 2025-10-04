import React, { useState, useEffect } from 'react';

const Shop = () => {
  const [cart, setCart] = useState([]);
  const [isCartOpen, setIsCartOpen] = useState(false);
  const [hoveredItem, setHoveredItem] = useState(null);
  const [currentImageIndex, setCurrentImageIndex] = useState(0);

  // Image gallery data
  const imageGallery = [
    {
      id: 1,
      src: "/house.png",
      title: "Cozy Home Companion",
      subtitle: "Domestic Bliss",
      description: "Transform your living space into a warm, welcoming sanctuary with Hiro's home-focused personality. Perfect for managing daily routines, organizing your space, and creating a cozy atmosphere.",
      features: ["Home organization tips", "Recipe suggestions", "Daily routine management", "Cozy conversation"],
      mood: "Warm & Nurturing",
      color: "#8B4513"
    },
    {
      id: 2,
      src: "/ghost.png",
      title: "Mystical Realm Companion",
      subtitle: "Supernatural Wisdom",
      description: "Dive into the mysteries of the unknown with Hiro's mystical side. Explore paranormal tales, ancient wisdom, and supernatural insights that spark curiosity and wonder.",
      features: ["Mystery storytelling", "Paranormal knowledge", "Mystical guidance", "Dream interpretation"],
      mood: "Mysterious & Wise",
      color: "#4A148C"
    },
    {
      id: 3,
      src: "/clock.png",
      title: "Time Master Companion",
      subtitle: "Productivity Focused",
      description: "Master the art of time management with Hiro's precision-focused personality. Boost your productivity, track goals, and make every moment count towards your success.",
      features: ["Time optimization", "Goal tracking", "Focus sessions", "Productivity analytics"],
      mood: "Efficient & Motivating",
      color: "#1565C0"
    }
  ];

  // Manual navigation functions
  const nextImage = () => {
    setCurrentImageIndex((prevIndex) => 
      (prevIndex + 1) % imageGallery.length
    );
  };

  const prevImage = () => {
    setCurrentImageIndex((prevIndex) => 
      prevIndex === 0 ? imageGallery.length - 1 : prevIndex - 1
    );
  };

  const goToImage = (index) => {
    setCurrentImageIndex(index);
  };

  const getCurrentImage = () => {
    return imageGallery[currentImageIndex];
  };

  const addToCart = (companion) => {
    if (companion.price === "Free") return;
    
    const existingItem = cart.find(item => item.id === companion.id);
    if (existingItem) {
      setCart(cart.map(item => 
        item.id === companion.id 
          ? { ...item, quantity: item.quantity + 1 }
          : item
      ));
    } else {
      setCart([...cart, { ...companion, quantity: 1 }]);
    }
  };

  const removeFromCart = (id) => {
    setCart(cart.filter(item => item.id !== id));
  };

  const updateQuantity = (id, quantity) => {
    if (quantity === 0) {
      removeFromCart(id);
    } else {
      setCart(cart.map(item => 
        item.id === id ? { ...item, quantity } : item
      ));
    }
  };

  const getTotalPrice = () => {
    return cart.reduce((total, item) => {
      const price = parseFloat(item.price.replace('$', ''));
      return total + (price * item.quantity);
    }, 0).toFixed(2);
  };

  const toggleCart = () => {
    setIsCartOpen(!isCartOpen);
  };

  return (
    <div className="shop image-gallery-shop">
      {/* Header */}
      <div className="shop-header">
        <div className="container">
          <div className="header-content">
            <h1 className="shop-title">
              <span className="title-main">Hiro's World</span>
              <span className="title-subtitle">Discover Different Companion Personalities</span>
            </h1>
            <div className="cart-toggle" onClick={toggleCart}>
              <i className="fas fa-shopping-cart"></i>
              <span className="cart-badge">{cart.length}</span>
            </div>
          </div>
        </div>
      </div>

      {/* Main Image Gallery */}
      <div className="gallery-section">
        <div className="container">
          <div className="gallery-layout">
            
            {/* Left Side - Image Display */}
            <div className="image-display">
              <div className="image-container">
                <img 
                  src={getCurrentImage().src} 
                  alt={getCurrentImage().title} 
                  className="main-image"
                />
                <div className="image-overlay" style={{ background: `linear-gradient(45deg, ${getCurrentImage().color}20, transparent)` }}></div>
              </div>
              
              {/* Navigation Controls */}
              <div className="image-controls">
                <button className="nav-button prev" onClick={prevImage}>
                  <i className="fas fa-chevron-left"></i>
                </button>
                
                <div className="image-indicators">
                  {imageGallery.map((_, index) => (
                    <div
                      key={index}
                      className={`indicator ${index === currentImageIndex ? 'active' : ''}`}
                      onClick={() => goToImage(index)}
                      style={{ '--indicator-color': imageGallery[index].color }}
                    ></div>
                  ))}
                </div>
                
                <button className="nav-button next" onClick={nextImage}>
                  <i className="fas fa-chevron-right"></i>
                </button>
              </div>
            </div>

            {/* Right Side - Description */}
            <div className="description-panel">
              <div className="panel-content">
                <div className="companion-header">
                  <h2 className="companion-title">{getCurrentImage().title}</h2>
                  <span className="companion-subtitle" style={{ color: getCurrentImage().color }}>
                    {getCurrentImage().subtitle}
                  </span>
                </div>
                
                <div className="mood-indicator">
                  <span className="mood-label">Personality:</span>
                  <span className="mood-value" style={{ background: getCurrentImage().color }}>
                    {getCurrentImage().mood}
                  </span>
                </div>
                
                <p className="companion-description">
                  {getCurrentImage().description}
                </p>
                
                <div className="features-list">
                  <h4>Key Features:</h4>
                  <ul>
                    {getCurrentImage().features.map((feature, index) => (
                      <li key={index}>
                        <i className="fas fa-star" style={{ color: getCurrentImage().color }}></i>
                        {feature}
                      </li>
                    ))}
                  </ul>
                </div>
                
                <div className="action-buttons">
                  <button className="action-btn primary" style={{ background: getCurrentImage().color }}>
                    <i className="fas fa-download"></i>
                    Get This Companion
                  </button>
                  <button className="action-btn secondary">
                    <i className="fas fa-info-circle"></i>
                    Learn More
                  </button>
                </div>
              </div>
            </div>
            
          </div>
        </div>
      </div>

      {/* Simplified Cart Sidebar */}
      <div className={`cart-sidebar depth-panel ${isCartOpen ? 'open' : ''}`}>        
        <div className="cart-header">
          <h3 className="cart-title">Shopping Cart</h3>
          <button className="close-cart" onClick={toggleCart}>
            <i className="fas fa-times"></i>
          </button>
        </div>
        
        <div className="cart-body">
          {cart.length === 0 ? (
            <div className="empty-state">
              <i className="fas fa-shopping-cart empty-icon"></i>
              <p className="empty-text">Your cart is empty</p>
            </div>
          ) : (
            <div className="cart-items">
              {cart.map(item => (
                <div key={item.id} className="cart-item simple-item">
                  <img src={item.image} alt={item.name} className="item-image" />
                  <div className="item-info">
                    <h4 className="item-name">{item.name}</h4>
                    <div className="item-controls">
                      <div className="quantity-controls">
                        <button 
                          className="qty-btn"
                          onClick={() => updateQuantity(item.id, item.quantity - 1)}
                        >
                          -
                        </button>
                        <span className="quantity">{item.quantity}</span>
                        <button 
                          className="qty-btn"
                          onClick={() => updateQuantity(item.id, item.quantity + 1)}
                        >
                          +
                        </button>
                      </div>
                      <span className="item-price">{item.price}</span>
                    </div>
                  </div>
                  <button 
                    className="remove-btn"
                    onClick={() => removeFromCart(item.id)}
                  >
                    <i className="fas fa-trash"></i>
                  </button>
                </div>
              ))}
            </div>
          )}
        </div>
        
        {cart.length > 0 && (
          <div className="cart-footer">
            <div className="total-section">
              <span className="total-label">Total: </span>
              <span className="total-amount">${getTotalPrice()}</span>
            </div>
            <button className="checkout-button">
              <i className="fas fa-credit-card"></i>
              Checkout
            </button>
          </div>
        )}
      </div>

      {/* Cart Overlay */}
      {isCartOpen && <div className="cart-overlay" onClick={toggleCart}></div>}
    </div>
  );
};

export default Shop;