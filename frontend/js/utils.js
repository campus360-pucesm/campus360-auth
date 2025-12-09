// API Configuration
const API_BASE_URL = 'http://localhost:8000';

// Storage keys
const TOKEN_KEY = 'campus360_token';
const USER_KEY = 'campus360_user';

// Get stored token
function getToken() {
    return localStorage.getItem(TOKEN_KEY);
}

// Set token
function setToken(token) {
    localStorage.setItem(TOKEN_KEY, token);
}

// Get stored user
function getUser() {
    const user = localStorage.getItem(USER_KEY);
    return user ? JSON.parse(user) : null;
}

// Set user
function setUser(user) {
    localStorage.setItem(USER_KEY, JSON.stringify(user));
}

// Clear auth data
function clearAuth() {
    localStorage.removeItem(TOKEN_KEY);
    localStorage.removeItem(USER_KEY);
}

// Check if user is authenticated
function isAuthenticated() {
    return !!getToken();
}

// API request helper
async function apiRequest(endpoint, options = {}) {
    const token = getToken();
    const headers = {
        'Content-Type': 'application/json',
        ...options.headers
    };

    if (token && !options.skipAuth) {
        headers['Authorization'] = `Bearer ${token}`;
    }

    const response = await fetch(`${API_BASE_URL}${endpoint}`, {
        ...options,
        headers
    });

    if (!response.ok) {
        if (response.status === 401) {
            clearAuth();
            window.location.href = '/frontend/index.html';
        }
        const error = await response.json().catch(() => ({ detail: 'Request failed' }));
        throw new Error(error.detail || 'Request failed');
    }

    return response;
}

// Show alert message
function showAlert(message, type = 'success') {
    const alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${type}`;
    alertDiv.textContent = message;

    // Find appropriate container - try multiple selectors
    let container = document.querySelector('.card');
    if (!container) {
        container = document.querySelector('.dashboard');
    }
    if (!container) {
        container = document.querySelector('.admin-container');
    }
    if (!container) {
        container = document.body;
    }

    // Insert at the beginning of container
    if (container.firstChild) {
        container.insertBefore(alertDiv, container.firstChild);
    } else {
        container.appendChild(alertDiv);
    }

    // Auto-remove after 5 seconds
    setTimeout(() => {
        if (alertDiv.parentNode) {
            alertDiv.remove();
        }
    }, 5000);
}

// Show loading state on button
function setButtonLoading(button, loading) {
    if (loading) {
        button.disabled = true;
        button.dataset.originalText = button.textContent;
        button.innerHTML = '<span class="spinner"></span>Cargando...';
    } else {
        button.disabled = false;
        button.textContent = button.dataset.originalText;
    }
}

// Format date
function formatDate(dateString) {
    const date = new Date(dateString);
    return date.toLocaleString('es-ES', {
        year: 'numeric',
        month: 'long',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
    });
}

// Redirect if not authenticated
function requireAuth() {
    if (!isAuthenticated()) {
        window.location.href = '/frontend/index.html';
    }
}

// Redirect if authenticated
function requireGuest() {
    if (isAuthenticated()) {
        window.location.href = '/frontend/pages/dashboard.html';
    }
}
