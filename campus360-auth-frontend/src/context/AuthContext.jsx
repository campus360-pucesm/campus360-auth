import { createContext, useContext, useState } from "react";
import { setToken, clearToken, setUser, clearUser, getUser } from "../api/api";

const AuthContext = createContext();

export function AuthProvider({ children }) {
    const [user, setUserState] = useState(getUser());

    const login = (token, userData) => {
        setToken(token);
        setUser(userData);
        setUserState(userData);
    };

    const logout = () => {
        clearToken();
        clearUser();
        setUserState(null);
    };

    return (
        <AuthContext.Provider value={{ user, login, logout }}>
            {children}
        </AuthContext.Provider>
    );
}

export const useAuth = () => useContext(AuthContext);
