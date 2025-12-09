import { useState } from "react";
import "../styles/style.css";
import Input from "../components/Input";
import Button from "../components/Button";
import Alert from "../components/Alert";
import { api } from "../api/api";

export default function Register() {
    const [fullName, setFullName] = useState("");
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const [role, setRole] = useState("student");
    const [errorMsg, setErrorMsg] = useState("");
    const [successMsg, setSuccessMsg] = useState("");

    const handleRegister = async (e) => {
        e.preventDefault();
        setErrorMsg("");
        setSuccessMsg("");

        try {
            const res = await api("/auth/register", {
                method: "POST",
                body: JSON.stringify({
                    full_name: fullName,
                    email,
                    password,
                    role
                }),
                skipAuth: true
            });

            await res.json();
            setSuccessMsg("Cuenta creada exitosamente. Redirigiendo...");
            setTimeout(() => (window.location.href = "/"), 1500);
        } catch (err) {
            setErrorMsg(err.message);
        }
    };

    return (
        <div className="center-container">
            <div className="card">
                <div className="app-title">
                    <h1>CAMPUS360</h1>
                    <p>Crear Cuenta</p>
                </div>

                <Alert type="error" message={errorMsg} />
                <Alert type="success" message={successMsg} />

                <form onSubmit={handleRegister}>
                    <Input
                        label="Nombre Completo"
                        value={fullName}
                        onChange={(e) => setFullName(e.target.value)}
                        placeholder="Juan Pérez"
                    />

                    <Input
                        label="Email"
                        type="email"
                        value={email}
                        onChange={(e) => setEmail(e.target.value)}
                        placeholder="usuario@mail.com"
                    />

                    <Input
                        label="Contraseña"
                        type="password"
                        value={password}
                        onChange={(e) => setPassword(e.target.value)}
                        placeholder="Mínimo 6 caracteres"
                    />

                    <div className="form-group">
                        <label>Rol</label>
                        <select value={role} onChange={(e) => setRole(e.target.value)}>
                            <option value="student">Estudiante</option>
                            <option value="teacher">Profesor</option>
                            <option value="admin">Administrador</option>
                        </select>
                    </div>

                    <Button type="submit">Registrarse</Button>
                    <Button variant="secondary" onClick={() => (window.location.href = "/")}>
                        Ya tengo cuenta
                    </Button>
                </form>
            </div>
        </div>
    );
}
