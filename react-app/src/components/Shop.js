import React, { useState, useEffect } from 'react';

const Shop = () => {
  const [cart, setCart] = useState([]);
  const [isCartOpen, setIsCartOpen] = useState(false);
  const [hoveredItem, setHoveredItem] = useState(null);

  const companions = [
    {
      id: 1,
      name: "Hirono Classic",
      price: "Free",
      description: "The original Hirono experience with classic animations and gentle personality.",
      features: ["Basic AI responses", "Classic animations", "Daily interactions", "Mood system"],
      image: "/api/placeholder/250/250",
      category: "classic"
    },
    {
      id: 2,
      name: "Hirono Pixel",
      price: "$4.99",
      description: "Retro-styled companion with 8-bit charm and nostalgic gaming references.",
      features: ["Pixel art style", "Retro sound effects", "Gaming references", "Achievement system"],
      image: "/api/placeholder/250/250",
      category: "retro"
    },
    {
      id: 3,
      name: "Hirono Zen",
      price: "$6.99",
      description: "Peaceful meditation companion focused on mindfulness and relaxation.",
      features: ["Meditation guides", "Breathing exercises", "Calming animations", "Zen quotes"],
      image: "/api/placeholder/250/250",
      category: "wellness"
    },
    {
      id: 4,
      name: "Hirono Scholar",
      price: "$7.99",
      description: "Academic-focused companion that helps with learning and productivity.",
      features: ["Study timer", "Knowledge base", "Quiz games", "Progress tracking"],
      image: "/api/placeholder/250/250",
      category: "education"
    },
    {
      id: 5,
      name: "Hirono Artist",
      price: "$8.99",
      description: "Creative companion that inspires artistic expression and creativity.",
      features: ["Drawing prompts", "Color theory tips", "Art history facts", "Creative challenges"],
      image: "/api/placeholder/250/250",
      category: "creative"
    },
    {
      id: 6,
      name: "Hirono Premium",
      price: "$12.99",
      description: "The ultimate Hirono experience with all features and exclusive content.",
      features: ["All companion styles", "Premium animations", "Exclusive dialogues", "Priority support"],
      image: "/api/placeholder/250/250",
      category: "premium"
    }
  ];

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

  // Simplified companions data
  const displayCompanions = companions.slice(0, 4); // Show only first 4 for simplicity

  return (
    <div className="shop simple-depth">
      {/* Simplified Header */}
      <div className="shop-header depth-layer-1">
        <div className="container">
          <div className="header-content">
            <h1 className="shop-title">Digital Companions</h1>
            <p className="shop-subtitle">Choose your perfect AI companion</p>
            
            <div className="cart-toggle simple-button" onClick={toggleCart}>
              <i className="fas fa-shopping-cart"></i>
              <span className="cart-badge">{cart.length}</span>
            </div>
          </div>
        </div>
      </div>

      {/* Simple Product Grid */}
      <div className="shop-content depth-layer-2">
        <div className="container">            
          <div className="products-grid">
            {displayCompanions.map((companion, index) => (
              <div 
                key={companion.id} 
                className={`product-card depth-card ${hoveredItem === companion.id ? 'hovered' : ''}`}
                onMouseEnter={() => setHoveredItem(companion.id)}
                onMouseLeave={() => setHoveredItem(null)}
                style={{ 
                  animationDelay: `${index * 0.15}s`,
                  '--card-index': index 
                }}
              >
                <div className="card-depth-shadow"></div>
                
                <div className="product-image">
                  <img src={companion.image} alt={companion.name} />
                  <div className="image-overlay"></div>
                </div>
                
                <div className="product-info">
                  <h3 className="product-name">{companion.name}</h3>
                  <p className="product-description">{companion.description}</p>
                  
                  <div className="product-features">
                    {companion.features.slice(0, 2).map((feature, fIndex) => (
                      <span key={fIndex} className="feature-tag">
                        {feature}
                      </span>
                    ))}
                  </div>
                </div>
                
                <div className="product-footer">
                  <div className="price-display">
                    <span className="price">{companion.price}</span>
                  </div>
                  
                  {companion.price === "Free" ? (
                    <button className="action-button primary">
                      <i className="fas fa-download"></i>
                      Download
                    </button>
                  ) : (
                    <button 
                      className="action-button secondary"
                      onClick={() => addToCart(companion)}
                    >
                      <i className="fas fa-plus"></i>
                      Add to Cart
                    </button>
                  )}
                </div>
              </div>
            ))}
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