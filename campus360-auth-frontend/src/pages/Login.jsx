import { useState } from "react";
import "../styles/style.css";
import Input from "../components/Input";
import Button from "../components/Button";
import Alert from "../components/Alert";
import { api, setUser, setToken } from "../api/api";
import { useAuth } from "../context/AuthContext";

export default function Login() {
    const { login } = useAuth();

    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const [errorMsg, setErrorMsg] = useState("");

    const handleLogin = async (e) => {
        e.preventDefault();
        setErrorMsg("");

        try {
            const formData = new URLSearchParams();
            formData.append("username", email);
            formData.append("password", password);

            const res = await api("/auth/login", {
                method: "POST",
                headers: { "Content-Type": "application/x-www-form-urlencoded" },
                body: formData,
                skipAuth: true
            });

            const data = await res.json();
            setToken(data.access_token);

            const resUser = await api("/qr/me");
            const userData = await resUser.json();

            setUser(userData);
            login(data.access_token, userData);

            if (userData.role === "admin") {
                window.location.href = "/admin";
            } else {
                window.location.href = "/dashboard";
            }

        } catch (err) {
            setErrorMsg(err.message);
        }
    };

    return (
        <div className="center-container">
            <div className="card">
                <div className="app-title">
                    <h1>CAMPUS360</h1>
                    <p>Autenticación Inteligente</p>
                </div>

                <Alert type="error" message={errorMsg} />

                <form onSubmit={handleLogin}>
                    <Input
                        label="Email"
                        type="email"
                        value={email}
                        placeholder="usuario@mail.com"
                        onChange={(e) => setEmail(e.target.value)}
                    />

                    <Input
                        label="Contraseña"
                        type="password"
                        value={password}
                        placeholder="••••••••"
                        onChange={(e) => setPassword(e.target.value)}
                    />

                    <Button type="submit">Ingresar</Button>
                </form>

                <div style={{ marginTop: '16px', textAlign: 'center', fontSize: '14px', color: '#6b7280' }}>
                    <p>¿No tienes cuenta? Contacta al administrador</p>
                </div>
            </div>
        </div>
    );
}
