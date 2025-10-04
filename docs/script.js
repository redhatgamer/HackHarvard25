// HIRONO - Vintage Digital Companion Website JavaScript

document.addEventListener('DOMContentLoaded', function() {
    // Mobile navigation toggle
    const hamburger = document.querySelector('.hamburger');
    const navMenu = document.querySelector('.nav-menu');
    
    if (hamburger && navMenu) {
        hamburger.addEventListener('click', () => {
            hamburger.classList.toggle('active');
            navMenu.classList.toggle('active');
        });

        // Close mobile menu when clicking on a link
        document.querySelectorAll('.nav-link').forEach(n => n.addEventListener('click', () => {
            hamburger.classList.remove('active');
            navMenu.classList.remove('active');
        }));
    }

    // Smooth scrolling for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });

    // Glitch effect enhancement
    const glitchElements = document.querySelectorAll('.glitch');
    glitchElements.forEach(element => {
        element.addEventListener('mouseenter', () => {
            element.style.animationDuration = '0.1s';
        });
        element.addEventListener('mouseleave', () => {
            element.style.animationDuration = '1s';
        });
    });

    // CRT flicker effect
    function addCRTFlicker() {
        const crtElements = document.querySelectorAll('.crt-box, .terminal-window, .product-screen');
        crtElements.forEach(element => {
            setInterval(() => {
                if (Math.random() > 0.98) {
                    element.style.filter = 'brightness(1.2) contrast(1.1)';
                    setTimeout(() => {
                        element.style.filter = '';
                    }, 50);
                }
            }, 100);
        });
    }
    addCRTFlicker();

    // Terminal typing effect
    const terminalLines = document.querySelectorAll('.terminal-line');
    if (terminalLines.length > 0) {
        terminalLines.forEach((line, index) => {
            line.style.opacity = '0';
            setTimeout(() => {
                line.style.opacity = '1';
                line.style.animation = 'fadeInLeft 0.5s ease';
            }, index * 500);
        });
    }

    // Product card hover effects
    const productCards = document.querySelectorAll('.product-card, .collection-card');
    productCards.forEach(card => {
        card.addEventListener('mouseenter', () => {
            const character = card.querySelector('.product-character, .pixel-art');
            if (character) {
                character.style.transform = 'scale(1.1) rotate(5deg)';
                character.style.filter = 'drop-shadow(0 0 20px var(--shadow-green))';
            }
        });
        
        card.addEventListener('mouseleave', () => {
            const character = card.querySelector('.product-character, .pixel-art');
            if (character) {
                character.style.transform = '';
                character.style.filter = '';
            }
        });
    });

    // Shopping cart functionality
    let cart = [];
    let cartCount = 0;

    function updateCartUI() {
        const cartCountElement = document.querySelector('.cart-count');
        const cartItems = document.querySelector('.cart-items');
        const cartTotal = document.querySelector('.cart-total');
        
        if (cartCountElement) {
            cartCountElement.textContent = cartCount;
        }
        
        if (cartItems) {
            if (cart.length === 0) {
                cartItems.innerHTML = '<p class="cart-empty">Your cart is empty</p>';
            } else {
                cartItems.innerHTML = cart.map(item => `
                    <div class="cart-item">
                        <h4>${item.name}</h4>
                        <p>$${item.price}</p>
                    </div>
                `).join('');
            }
        }
        
        if (cartTotal) {
            const total = cart.reduce((sum, item) => sum + parseFloat(item.price), 0);
            cartTotal.textContent = `Total: $${total.toFixed(2)}`;
        }
    }

    // Add to cart functionality
    document.querySelectorAll('.product-btn').forEach(btn => {
        if (btn.textContent.includes('ADD TO CART') || btn.textContent.includes('COLLECT NOW')) {
            btn.addEventListener('click', (e) => {
                e.preventDefault();
                const card = btn.closest('.product-card');
                const name = card.querySelector('h3').textContent;
                const priceElement = card.querySelector('.price');
                const price = priceElement.textContent.replace('$', '').replace('FREE', '0');
                
                if (price !== '0' && price !== 'TBA') {
                    cart.push({ name, price });
                    cartCount++;
                    updateCartUI();
                    
                    // Visual feedback
                    btn.textContent = 'ADDED!';
                    btn.style.background = 'var(--primary-green)';
                    setTimeout(() => {
                        btn.innerHTML = '<i class="fas fa-cart-plus"></i> ADD TO CART';
                        btn.style.background = '';
                    }, 2000);
                }
            });
        }
    });

    updateCartUI();

    // Add sound effects (optional)
    function playSound(type) {
        // Web Audio API for retro sound effects
        const audioContext = new (window.AudioContext || window.webkitAudioContext)();
        const oscillator = audioContext.createOscillator();
        const gainNode = audioContext.createGain();
        
        oscillator.connect(gainNode);
        gainNode.connect(audioContext.destination);
        
        switch(type) {
            case 'hover':
                oscillator.frequency.setValueAtTime(800, audioContext.currentTime);
                oscillator.frequency.exponentialRampToValueAtTime(1200, audioContext.currentTime + 0.1);
                break;
            case 'click':
                oscillator.frequency.setValueAtTime(400, audioContext.currentTime);
                oscillator.frequency.exponentialRampToValueAtTime(800, audioContext.currentTime + 0.2);
                break;
        }
        
        gainNode.gain.setValueAtTime(0.1, audioContext.currentTime);
        gainNode.gain.exponentialRampToValueAtTime(0.01, audioContext.currentTime + 0.3);
        
        oscillator.start(audioContext.currentTime);
        oscillator.stop(audioContext.currentTime + 0.3);
    }

    // Add sound to interactions (uncomment to enable)
    /*
    document.querySelectorAll('.btn, .nav-link').forEach(element => {
        element.addEventListener('mouseenter', () => playSound('hover'));
        element.addEventListener('click', () => playSound('click'));
    });
    */

    // Matrix rain effect for background
    function createMatrixRain() {
        const canvas = document.createElement('canvas');
        const ctx = canvas.getContext('2d');
        
        canvas.style.cssText = `
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            pointer-events: none;
            z-index: 1;
            opacity: 0.1;
        `;
        
        document.body.appendChild(canvas);
        
        canvas.width = window.innerWidth;
        canvas.height = window.innerHeight;
        
        const chars = 'HIRONO0123456789ヒロノ';
        const charSize = 14;
        const columns = canvas.width / charSize;
        const drops = Array(Math.floor(columns)).fill(1);
        
        function draw() {
            ctx.fillStyle = 'rgba(10, 10, 10, 0.05)';
            ctx.fillRect(0, 0, canvas.width, canvas.height);
            
            ctx.fillStyle = '#00ff41';
            ctx.font = `${charSize}px monospace`;
            
            drops.forEach((drop, i) => {
                const text = chars[Math.floor(Math.random() * chars.length)];
                ctx.fillText(text, i * charSize, drop * charSize);
                
                if (drop * charSize > canvas.height && Math.random() > 0.975) {
                    drops[i] = 0;
                }
                drops[i]++;
            });
        }
        
        setInterval(draw, 50);
        
        window.addEventListener('resize', () => {
            canvas.width = window.innerWidth;
            canvas.height = window.innerHeight;
        });
    }

    // Uncomment to enable matrix rain effect
    // createMatrixRain();

    // Page load animations
    window.addEventListener('load', () => {
        document.body.style.opacity = '1';
        
        // Animate in elements
        const animateElements = document.querySelectorAll('.hero-title, .japanese-subtitle, .crt-box');
        animateElements.forEach((element, index) => {
            element.style.opacity = '0';
            element.style.transform = 'translateY(50px)';
            setTimeout(() => {
                element.style.transition = 'all 0.8s ease';
                element.style.opacity = '1';
                element.style.transform = 'translateY(0)';
            }, index * 200);
        });
    });

    // Add keyboard navigation
    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape') {
            const cartSidebar = document.querySelector('.cart-sidebar');
            if (cartSidebar && cartSidebar.classList.contains('open')) {
                toggleCart();
            }
        }
    });
});

// Cart toggle function (global scope for HTML onclick)
function toggleCart() {
    const cartSidebar = document.querySelector('.cart-sidebar');
    if (cartSidebar) {
        cartSidebar.classList.toggle('open');
    }
}