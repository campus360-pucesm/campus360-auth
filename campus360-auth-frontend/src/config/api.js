/**
 * API Configuration for Campus360 Auth Frontend
 * Centralizes all API endpoint URLs and configuration
 */

// Get API base URL from environment variable or use localhost for development
const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

/**
 * API Endpoints
 */
export const API_ENDPOINTS = {
    // Authentication
    LOGIN: `${API_BASE_URL}/auth/login`,

    // QR Access
    QR_ME: `${API_BASE_URL}/qr/me`,
    QR_SCAN: `${API_BASE_URL}/qr/scan`,
    QR_HISTORY: `${API_BASE_URL}/qr/history`,

    // Admin - User Management
    ADMIN_USERS: `${API_BASE_URL}/admin/users`,
    ADMIN_USER_BY_ID: (userId) => `${API_BASE_URL}/admin/users/${userId}`,

    // Admin - Dashboard
    ADMIN_STATS: `${API_BASE_URL}/admin/stats`,
    ADMIN_RECENT_ACCESS: `${API_BASE_URL}/admin/recent-access`,

    // Health Check
    HEALTH: `${API_BASE_URL}/health`,
    ROOT: `${API_BASE_URL}/`,
};

/**
 * API Configuration
 */
export const API_CONFIG = {
    BASE_URL: API_BASE_URL,
    TIMEOUT: 30000, // 30 seconds
    HEADERS: {
        'Content-Type': 'application/json',
    },
};

/**
 * Helper function to get authorization headers
 */
export const getAuthHeaders = () => {
    const token = localStorage.getItem('token');
    return {
        ...API_CONFIG.HEADERS,
        ...(token && { Authorization: `Bearer ${token}` }),
    };
};

export default API_ENDPOINTS;
