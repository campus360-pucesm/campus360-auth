// src/api/api.js
const API_URL = import.meta.env.VITE_API_URL || "http://localhost:8000";

export const getToken = () => localStorage.getItem("token");
export const setToken = (token) => localStorage.setItem("token", token);
export const clearToken = () => localStorage.removeItem("token");

export const setUser = (user) =>
    localStorage.setItem("user", JSON.stringify(user));

export const getUser = () => {
    const u = localStorage.getItem("user");
    return u ? JSON.parse(u) : null;
};

export const clearUser = () => localStorage.removeItem("user");

export const api = async (endpoint, options = {}) => {
    const token = getToken();

    const headers = {
        "Content-Type": "application/json",
        ...options.headers,
    };

    if (token && !options.skipAuth) {
        headers.Authorization = `Bearer ${token}`;
    }

    const response = await fetch(`${API_URL}${endpoint}`, {
        ...options,
        headers,
    });

    if (!response.ok) {
        if (response.status === 401) {
            clearToken();
            clearUser();
            window.location.href = "/";
        }
        const error = await response.json().catch(() => ({
            detail: "Error desconocido",
        }));
        throw new Error(error.detail);
    }

    return response;
};
