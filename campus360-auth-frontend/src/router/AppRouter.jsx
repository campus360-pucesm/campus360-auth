import { BrowserRouter, Routes, Route } from "react-router-dom";
import Login from "../pages/Login";
import Register from "../pages/Register";
import Dashboard from "../pages/Dashboard";
import AdminPanel from "../pages/AdminPanel";
import NotAuthorized from "../pages/NotAuthorized";
import NotFound from "../pages/NotFound";
import { useAuth } from "../context/AuthContext";

function ProtectedRoute({ children }) {
    const { user } = useAuth();
    return user ? children : <Login />;
}

function AdminRoute({ children }) {
    const { user } = useAuth();
    return user?.role === "admin" ? children : <NotAuthorized />;
}

export default function AppRouter() {
    return (
        <BrowserRouter>
            <Routes>
                <Route path="/" element={<Login />} />
                <Route path="/register" element={<Register />} />

                <Route
                    path="/dashboard"
                    element={
                        <ProtectedRoute>
                            <Dashboard />
                        </ProtectedRoute>
                    }
                />

                <Route
                    path="/admin"
                    element={
                        <AdminRoute>
                            <AdminPanel />
                        </AdminRoute>
                    }
                />

                <Route path="/no-access" element={<NotAuthorized />} />
                <Route path="*" element={<NotFound />} />
            </Routes>
        </BrowserRouter>
    );
}
