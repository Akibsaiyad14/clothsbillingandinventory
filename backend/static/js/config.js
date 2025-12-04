// API Configuration
// Use relative URL for API calls (works for both localhost and production)
const API_BASE_URL = window.location.origin + '/api';

const API_ENDPOINTS = {
    items: `${API_BASE_URL}/inventory/items/`,
    stock: `${API_BASE_URL}/inventory/stock/`,
    lowStock: `${API_BASE_URL}/inventory/items/low_stock/`,
    updateStock: `${API_BASE_URL}/inventory/stock/update_stock/`,
    bills: `${API_BASE_URL}/billing/bills/`,
    authLogin: `${API_BASE_URL}/auth/login/`,
    authLogout: `${API_BASE_URL}/auth/logout/`,
    authWhoami: `${API_BASE_URL}/auth/whoami/`,
    authRegister: `${API_BASE_URL}/auth/register/`,
    authRefresh: `${API_BASE_URL}/auth/token/refresh/`,
};

// Token management
const TokenManager = {
    getAccessToken() {
        return localStorage.getItem('access_token');
    },
    
    getRefreshToken() {
        return localStorage.getItem('refresh_token');
    },
    
    setTokens(access, refresh) {
        localStorage.setItem('access_token', access);
        if (refresh) localStorage.setItem('refresh_token', refresh);
    },
    
    clearTokens() {
        localStorage.removeItem('access_token');
        localStorage.removeItem('refresh_token');
        localStorage.removeItem('username');
    },
    
    async refreshAccessToken() {
        const refreshToken = this.getRefreshToken();
        if (!refreshToken) return false;
        
        try {
            const response = await fetch(API_ENDPOINTS.authRefresh, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ refresh: refreshToken })
            });
            
            if (response.ok) {
                const data = await response.json();
                this.setTokens(data.access, null);
                return true;
            }
        } catch (error) {
            console.error('Token refresh failed:', error);
        }
        
        this.clearTokens();
        return false;
    }
};

// Helper function to handle API requests
async function apiRequest(url, options = {}) {
    const token = TokenManager.getAccessToken();
    
    const headers = {
        'Content-Type': 'application/json',
        ...options.headers,
    };
    
    if (token) {
        headers['Authorization'] = `Bearer ${token}`;
    }
    
    try {
        let response = await fetch(url, {
            ...options,
            credentials: 'include',
            headers,
        });

        // If unauthorized, try to refresh token
        if (response.status === 401 && token) {
            const refreshed = await TokenManager.refreshAccessToken();
            if (refreshed) {
                // Retry with new token
                headers['Authorization'] = `Bearer ${TokenManager.getAccessToken()}`;
                response = await fetch(url, {
                    ...options,
                    credentials: 'include',
                    headers,
                });
            } else {
                // Refresh failed, redirect to login
                window.location.href = '/login/';
                throw new Error('Session expired');
            }
        }

        // If still unauthorized or forbidden, redirect to login
        if (response.status === 401 || response.status === 403) {
            TokenManager.clearTokens();
            window.location.href = '/login/';
            throw new Error('Authentication required');
        }

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        return await response.json();
    } catch (error) {
        console.error('API Request Error:', error);
        throw error;
    }
}

// Helper function to format currency
function formatCurrency(amount) {
    // Format amount in Indian Rupees
    const num = parseFloat(amount) || 0;
    return `₹${num.toFixed(2)}`;
}

// Helper function to format date to dd-mm-yyyy HH:MM
function formatDate(dateString) {
    if (!dateString) return '';
    
    // If it's already in dd-mm-yyyy format from API, return as is
    if (dateString.includes('-') && dateString.split('-')[0].length <= 2) {
        return dateString;
    }
    
    const date = new Date(dateString);
    const day = String(date.getDate()).padStart(2, '0');
    const month = String(date.getMonth() + 1).padStart(2, '0');
    const year = date.getFullYear();
    const hours = String(date.getHours()).padStart(2, '0');
    const minutes = String(date.getMinutes()).padStart(2, '0');
    
    return `${day}-${month}-${year} ${hours}:${minutes}`;
}

// Helper function to show notifications
function showNotification(message, type = 'success') {
    const notification = document.createElement('div');
    notification.className = `notification ${type}`;
    notification.textContent = message;
    notification.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        padding: 1rem 1.5rem;
        background: ${type === 'success' ? '#43e97b' : '#f5576c'};
        color: white;
        border-radius: 8px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
        z-index: 10000;
        animation: slideIn 0.3s ease;
    `;
    
    document.body.appendChild(notification);
    
    setTimeout(() => {
        notification.style.animation = 'slideOut 0.3s ease';
        setTimeout(() => notification.remove(), 300);
    }, 3000);
}

// Check authentication and update UI
async function checkAuth() {
    const username = localStorage.getItem('username');
    const token = TokenManager.getAccessToken();
    
    const authInfo = document.getElementById('authInfo');
    if (!authInfo) return;
    
    if (username && token) {
        authInfo.innerHTML = `
            <span class="username-display">Hello, ${username}</span>
            <button class="btn btn-sm btn-secondary" onclick="logout()">Logout</button>
        `;
    } else {
        authInfo.innerHTML = `
            <a href="/login/" class="btn btn-sm btn-secondary">Login</a>
        `;
        
        // Redirect to login if on protected page and not logged in
        const currentPath = window.location.pathname;
        const protectedPages = ['/dashboard/', '/inventory/', '/billing/', '/reports/'];
        if (protectedPages.includes(currentPath)) {
            window.location.href = '/login/';
        }
    }
}

// Logout function
async function logout() {
    try {
        await apiRequest(API_ENDPOINTS.authLogout, { method: 'POST' });
    } catch (error) {
        console.error('Logout error:', error);
    }
    
    TokenManager.clearTokens();
    showNotification('Logged out successfully');
    setTimeout(() => {
        window.location.href = '/login/';
    }, 1000);
}

// Toggle mobile menu
function toggleMobileMenu() {
    const navMenu = document.getElementById('navMenu');
    if (navMenu) {
        navMenu.classList.toggle('active');
    }
}

// Initialize auth check on page load
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', checkAuth);
} else {
    checkAuth();
}
