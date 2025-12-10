import { useEffect, useState } from "react";
import "../styles/style.css";
import { api, getUser, clearToken, clearUser } from "../api/api";
import { useAuth } from "../context/AuthContext";
import Button from "../components/Button";
import Alert from "../components/Alert";
import UserManagement from "../components/UserManagement";

export default function AdminPanel() {
    const { user, logout } = useAuth();
    const [localUser, setLocalUser] = useState(user || getUser());
    const [activeTab, setActiveTab] = useState("users"); // "users" or "qr"
    const [locationCode, setLocationCode] = useState("");
    const [locationName, setLocationName] = useState("");
    const [qrBlobUrl, setQrBlobUrl] = useState(null);
    const [alert, setAlert] = useState({ type: "", message: "" });
    const [loading, setLoading] = useState(false);

    useEffect(() => {
        if (!localUser || localUser.role !== "admin") {
            clearToken();
            clearUser();
            window.location.href = "/";
        }
        // eslint-disable-next-line react-hooks/exhaustive-deps
    }, []);

    const showAlert = (type, message) => {
        setAlert({ type, message });
        setTimeout(() => setAlert({ type: "", message: "" }), 4000);
    };

    const handleLogout = () => {
        logout();
        window.location.href = "/";
    };

    const generateQR = async (code, name = "") => {
        if (!code) {
            showAlert("error", "El código de ubicación es obligatorio.");
            return;
        }

        try {
            setLoading(true);
            const res = await api("/admin/qr/generate-location", {
                method: "POST",
                body: JSON.stringify({
                    location_code: code,
                    location_name: name,
                }),
                // si backend requiere auth en el futuro, quitar skipAuth
            });

            const blob = await res.blob();
            const url = URL.createObjectURL(blob);
            setQrBlobUrl(url);
            showAlert("success", "QR generado correctamente.");
        } catch (err) {
            showAlert("error", "Error al generar QR: " + err.message);
        } finally {
            setLoading(false);
        }
    };

    const handleSubmit = (e) => {
        e.preventDefault();
        generateQR(locationCode, locationName);
    };

    const handleQuickGenerate = (code) => {
        setLocationCode(code);
        setLocationName("");
        generateQR(code, "");
    };

    const handleDownload = () => {
        if (!qrBlobUrl || !locationCode) return;
        const a = document.createElement("a");
        a.href = qrBlobUrl;
        a.download = `${locationCode}.png`;
        a.click();
    };

    if (!localUser || localUser.role !== "admin") return null;

    return (
        <div className="dashboard-container">
            <div className="dashboard-header">
                <div>
                    <h2>Panel de Administración</h2>
                    <p style={{ color: "#6b7280", fontSize: "14px" }}>
                        Gestión completa del sistema CAMPUS360
                    </p>
                </div>
                <div style={{ display: "flex", gap: "10px" }}>
                    <Button
                        variant="secondary"
                        onClick={() => (window.location.href = "/dashboard")}
                    >
                        Mi Dashboard
                    </Button>
                    <Button variant="secondary" onClick={handleLogout}>
                        Cerrar sesión
                    </Button>
                </div>
            </div>

            <Alert type={alert.type} message={alert.message} />

            {/* Tabs */}
            <div style={{ 
                display: "flex", 
                gap: "10px", 
                marginBottom: "24px",
                borderBottom: "2px solid #e5e7eb"
            }}>
                <button
                    className={`tab-button ${activeTab === "users" ? "active" : ""}`}
                    onClick={() => setActiveTab("users")}
                    style={{
                        padding: "12px 24px",
                        background: "none",
                        border: "none",
                        borderBottom: activeTab === "users" ? "2px solid #667eea" : "2px solid transparent",
                        color: activeTab === "users" ? "#667eea" : "#6b7280",
                        fontWeight: activeTab === "users" ? "600" : "400",
                        cursor: "pointer",
                        marginBottom: "-2px"
                    }}
                >
                    👥 Gestión de Usuarios
                </button>
                <button
                    className={`tab-button ${activeTab === "qr" ? "active" : ""}`}
                    onClick={() => setActiveTab("qr")}
                    style={{
                        padding: "12px 24px",
                        background: "none",
                        border: "none",
                        borderBottom: activeTab === "qr" ? "2px solid #667eea" : "2px solid transparent",
                        color: activeTab === "qr" ? "#667eea" : "#6b7280",
                        fontWeight: activeTab === "qr" ? "600" : "400",
                        cursor: "pointer",
                        marginBottom: "-2px"
                    }}
                >
                    📍 Generador de QR
                </button>
            </div>

            {/* Tab Content */}
            {activeTab === "users" && <UserManagement />}

            {activeTab === "qr" && (
                <>
                    <div className="admin-card" style={{ marginBottom: "24px" }}>
                        <h3 style={{ marginBottom: "6px" }}>Generar QR de ubicación</h3>
                        <p
                            style={{
                                color: "#6b7280",
                                fontSize: "14px",
                                marginBottom: "16px",
                            }}
                        >
                            Crea códigos QR para aulas, laboratorios y otros puntos del campus.
                        </p>

                        <form onSubmit={handleSubmit}>
                            <div className="form-group">
                                <label>Código de ubicación *</label>
                                <input
                                    type="text"
                                    value={locationCode}
                                    onChange={(e) => setLocationCode(e.target.value)}
                                    placeholder="Ej: LAB-101, AULA-302"
                                />
                            </div>

                            <div className="form-group">
                                <label>Nombre de ubicación (opcional)</label>
                                <input
                                    type="text"
                                    value={locationName}
                                    onChange={(e) => setLocationName(e.target.value)}
                                    placeholder="Laboratorio de Computación 1"
                                />
                            </div>

                            <Button type="submit">
                                {loading ? "Generando..." : "Generar QR"}
                            </Button>
                        </form>

                        {qrBlobUrl && (
                            <div
                                className="qr-preview"
                                style={{ marginTop: "20px", textAlign: "center" }}
                            >
                                <p style={{ marginBottom: "10px" }}>
                                    Código: <strong>{locationCode}</strong>
                                    {locationName ? ` - ${locationName}` : ""}
                                </p>
                                <img
                                    src={qrBlobUrl}
                                    alt="QR ubicación"
                                    style={{ maxWidth: "260px" }}
                                />
                                <div style={{ marginTop: "12px" }}>
                                    <Button onClick={handleDownload}>Descargar QR</Button>
                                </div>
                            </div>
                        )}
                    </div>

                    <div className="admin-card">
                        <h3 style={{ marginBottom: "6px" }}>Ubicaciones sugeridas</h3>
                        <p
                            style={{
                                color: "#6b7280",
                                fontSize: "14px",
                                marginBottom: "12px",
                            }}
                        >
                            Genera rápido algunos QR frecuentes del campus.
                        </p>

                        <div
                            style={{
                                display: "grid",
                                gridTemplateColumns: "repeat(auto-fit, minmax(140px, 1fr))",
                                gap: "10px",
                            }}
                        >
                            {["LAB-101", "LAB-102", "AULA-301", "BIBLIOTECA", "CAFETERIA", "GIMNASIO"].map(
                                (code) => (
                                    <button
                                        key={code}
                                        className="btn btn-secondary"
                                        type="button"
                                        onClick={() => handleQuickGenerate(code)}
                                    >
                                        {code}
                                    </button>
                                )
                            )}
                        </div>
                    </div>
                </>
            )}
        </div>
    );
}
