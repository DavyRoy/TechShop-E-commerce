// API Configuration
const API_BASE_URL = '/api';

// Fetch all products
async function fetchProducts(page = 1, limit = 12) {
    try {
        const response = await fetch(`${API_BASE_URL}/products?page=${page}&limit=${limit}`);
        if (!response.ok) {
            throw new Error('Failed to fetch products');
        }
        return await response.json();
    } catch (error) {
        console.error('Error fetching products:', error);
        return null;
    }
}

// Fetch single product by ID
async function fetchProduct(id) {
    try {
        const response = await fetch(`${API_BASE_URL}/products/${id}`);
        if (!response.ok) {
            throw new Error('Product not found');
        }
        return await response.json();
    } catch (error) {
        console.error('Error fetching product:', error);
        return null;
    }
}

// Fetch all categories
async function fetchCategories() {
    try {
        const response = await fetch(`${API_BASE_URL}/categories`);
        if (!response.ok) {
            throw new Error('Failed to fetch categories');
        }
        return await response.json();
    } catch (error) {
        console.error('Error fetching categories:', error);
        return null;
    }
}

// Fetch products by category
async function fetchProductsByCategory(categoryId) {
    try {
        const response = await fetch(`${API_BASE_URL}/products/category/${categoryId}`);
        if (!response.ok) {
            throw new Error('Failed to fetch products by category');
        }
        return await response.json();
    } catch (error) {
        console.error('Error fetching products by category:', error);
        return null;
    }
}

// Create an order
async function createOrder(orderData) {
    try {
        const response = await fetch(`${API_BASE_URL}/orders`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(orderData)
        });
        
        const data = await response.json();
        
        if (!response.ok) {
            throw new Error(data.error || 'Failed to create order');
        }
        
        return data;
    } catch (error) {
        console.error('Error creating order:', error);
        throw error;
    }
}

// Health check
async function checkHealth() {
    try {
        const response = await fetch(`${API_BASE_URL}/health`);
        return await response.json();
    } catch (error) {
        console.error('Error checking health:', error);
        return { status: 'error' };
    }
}