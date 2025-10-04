import React, { useState } from 'react';

const Shop = () => {
  const [cart, setCart] = useState([]);
  const [isCartOpen, setIsCartOpen] = useState(false);

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

  return (
    <div className="shop">
      <div className="shop-header">
        <div className="container">
          <h1 className="page-title">Digital Companions Shop</h1>
          <p className="page-subtitle">Choose your perfect AI companion</p>
          
          <div className="cart-toggle" onClick={toggleCart}>
            <i className="fas fa-shopping-cart"></i>
            <span className="cart-count">{cart.length}</span>
          </div>
        </div>
      </div>

      <div className="shop-content">
        <div className="container">
          <div className="companions-grid">
            {companions.map(companion => (
              <div key={companion.id} className="companion-card">
                <div className="card-image">
                  <img src={companion.image} alt={companion.name} />
                  <div className="category-badge">{companion.category}</div>
                </div>
                
                <div className="card-content">
                  <h3 className="companion-name">{companion.name}</h3>
                  <p className="companion-description">{companion.description}</p>
                  
                  <div className="features-list">
                    {companion.features.map((feature, index) => (
                      <span key={index} className="feature-tag">
                        {feature}
                      </span>
                    ))}
                  </div>
                  
                  <div className="card-footer">
                    <div className="price">{companion.price}</div>
                    {companion.price === "Free" ? (
                      <button className="download-btn">
                        <i className="fas fa-download"></i>
                        Download
                      </button>
                    ) : (
                      <button 
                        className="add-to-cart-btn"
                        onClick={() => addToCart(companion)}
                      >
                        <i className="fas fa-plus"></i>
                        Add to Cart
                      </button>
                    )}
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Shopping Cart Sidebar */}
      <div className={`cart-sidebar ${isCartOpen ? 'open' : ''}`}>
        <div className="cart-header">
          <h3>Shopping Cart</h3>
          <button className="close-cart" onClick={toggleCart}>
            <i className="fas fa-times"></i>
          </button>
        </div>
        
        <div className="cart-items">
          {cart.length === 0 ? (
            <p className="empty-cart">Your cart is empty</p>
          ) : (
            cart.map(item => (
              <div key={item.id} className="cart-item">
                <img src={item.image} alt={item.name} className="cart-item-image" />
                <div className="cart-item-details">
                  <h4>{item.name}</h4>
                  <div className="quantity-controls">
                    <button onClick={() => updateQuantity(item.id, item.quantity - 1)}>
                      <i className="fas fa-minus"></i>
                    </button>
                    <span>{item.quantity}</span>
                    <button onClick={() => updateQuantity(item.id, item.quantity + 1)}>
                      <i className="fas fa-plus"></i>
                    </button>
                  </div>
                  <div className="item-price">{item.price}</div>
                </div>
                <button 
                  className="remove-item"
                  onClick={() => removeFromCart(item.id)}
                >
                  <i className="fas fa-trash"></i>
                </button>
              </div>
            ))
          )}
        </div>
        
        {cart.length > 0 && (
          <div className="cart-footer">
            <div className="cart-total">
              Total: ${getTotalPrice()}
            </div>
            <button className="checkout-btn">
              <i className="fas fa-credit-card"></i>
              Checkout
            </button>
          </div>
        )}
      </div>

      {/* Overlay */}
      {isCartOpen && <div className="cart-overlay" onClick={toggleCart}></div>}
    </div>
  );
};

export default Shop;