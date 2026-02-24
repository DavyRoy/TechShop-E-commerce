// Wait for DOM to be ready
document.addEventListener('DOMContentLoaded', function() {
    // Check if we're on the home page
    if (document.getElementById('featured-products')) {
        loadFeaturedProducts();
    }
    
    // Check if we're on the catalog page
    if (document.getElementById('catalog-products')) {
        loadCatalogProducts();
        loadCategories();
    }
    
    // Setup order form if it exists
    const orderForm = document.getElementById('order-form');
    if (orderForm) {
        orderForm.addEventListener('submit', handleOrderSubmit);
    }
});

// Load featured products for home page
async function loadFeaturedProducts() {
    const container = document.getElementById('featured-products');
    
    // Show loading
    container.innerHTML = '<p class="loading">Loading products...</p>';
    
    try {
        const data = await fetchProducts(1, 6); // Get first 6 products
        
        if (data && data.products && data.products.length > 0) {
            displayProducts(data.products, container);
        } else {
            container.innerHTML = '<p class="error">No products available.</p>';
        }
    } catch (error) {
        container.innerHTML = '<p class="error">Failed to load products. Please try again later.</p>';
    }
}

// Load all products for catalog page
async function loadCatalogProducts() {
    const container = document.getElementById('catalog-products');
    
    container.innerHTML = '<p class="loading">Loading products...</p>';
    
    try {
        const data = await fetchProducts(1, 20); // Get 20 products
        
        if (data && data.products && data.products.length > 0) {
            displayProducts(data.products, container);
        } else {
            container.innerHTML = '<p class="error">No products available.</p>';
        }
    } catch (error) {
        container.innerHTML = '<p class="error">Failed to load products. Please try again later.</p>';
    }
}

// Load categories
async function loadCategories() {
    const container = document.getElementById('categories-list');
    if (!container) return;
    
    try {
        const categories = await fetchCategories();
        
        if (categories && categories.length > 0) {
            container.innerHTML = categories.map(cat => `
                <li>
                    <a href="#" onclick="filterByCategory(${cat.id}); return false;">
                        ${cat.name}
                    </a>
                </li>
            `).join('');
        }
    } catch (error) {
        console.error('Failed to load categories');
    }
}

// Filter products by category
async function filterByCategory(categoryId) {
    const container = document.getElementById('catalog-products');
    container.innerHTML = '<p class="loading">Loading products...</p>';
    
    try {
        const products = await fetchProductsByCategory(categoryId);
        
        if (products && products.length > 0) {
            displayProducts(products, container);
        } else {
            container.innerHTML = '<p class="error">No products in this category.</p>';
        }
    } catch (error) {
        container.innerHTML = '<p class="error">Failed to load products.</p>';
    }
}

// Display products in a container
function displayProducts(products, container) {
    container.innerHTML = products.map(product => `
        <div class="product-card">
            <div class="product-image">
                <img src="${product.url_image || '/images/placeholder.png'}" 
                     alt="${product.name}"
                     onerror="this.src='/images/placeholder.png'">
            </div>
            <div class="product-info">
                <h3 class="product-title">${product.name}</h3>
                <p class="product-description">${product.description || ''}</p>
                <div class="product-footer">
                    <span class="product-price">$${parseFloat(product.price).toFixed(2)}</span>
                    <span class="product-stock">${product.stock > 0 ? 'In Stock' : 'Out of Stock'}</span>
                </div>
                ${product.stock > 0 ? 
                    `<button class="btn-add-to-cart" onclick="addToCart(${product.id}, '${product.name}', ${product.price})">
                        Add to Cart
                    </button>` : 
                    '<button class="btn-out-of-stock" disabled>Out of Stock</button>'
                }
            </div>
        </div>
    `).join('');
}

// Simple cart functionality (stored in localStorage)
let cart = JSON.parse(localStorage.getItem('cart')) || [];

function addToCart(productId, productName, price) {
    const existingItem = cart.find(item => item.product_id === productId);
    
    if (existingItem) {
        existingItem.quantity += 1;
    } else {
        cart.push({
            product_id: productId,
            name: productName,
            price: price,
            quantity: 1
        });
    }
    
    localStorage.setItem('cart', JSON.stringify(cart));
    updateCartDisplay();
    
    // Show notification
    alert(`${productName} added to cart!`);
}

function updateCartDisplay() {
    const cartCount = document.getElementById('cart-count');
    if (cartCount) {
        const totalItems = cart.reduce((sum, item) => sum + item.quantity, 0);
        cartCount.textContent = totalItems;
    }
}

// Handle order form submission
async function handleOrderSubmit(event) {
    event.preventDefault();
    
    const formData = new FormData(event.target);
    const customerName = formData.get('customer_name');
    const customerEmail = formData.get('customer_email');
    
    if (cart.length === 0) {
        alert('Your cart is empty!');
        return;
    }
    
    const orderData = {
        customer_name: customerName,
        customer_email: customerEmail,
        items: cart.map(item => ({
            product_id: item.product_id,
            quantity: item.quantity
        }))
    };
    
    try {
        const result = await createOrder(orderData);
        
        // Clear cart
        cart = [];
        localStorage.removeItem('cart');
        updateCartDisplay();
        
        // Show success message
        alert(`Order created successfully! Order ID: ${result.order_id}`);
        
        // Reset form
        event.target.reset();
        
        // Redirect to home
        window.location.href = 'index.html';
        
    } catch (error) {
        alert(`Failed to create order: ${error.message}`);
    }
}

// Initialize cart display on page load
updateCartDisplay();