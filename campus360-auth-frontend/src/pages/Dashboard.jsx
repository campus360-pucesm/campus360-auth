import { useEffect, useState } from "react";
import "../styles/style.css";
import { api, getUser, clearToken, clearUser } from "../api/api";
import { useAuth } from "../context/AuthContext";
import Button from "../components/Button";
import Alert from "../components/Alert";
import CredentialCard from "../components/CredentialCard";
import QRScanner from "../components/QRScanner";
import AccessHistory from "../components/AccessHistory";

export default function Dashboard() {
    const { user, logout } = useAuth();
    const [localUser, setLocalUser] = useState(user || getUser());
    const [activeTab, setActiveTab] = useState("credential");
    const [qrImageUrl, setQrImageUrl] = useState(null);
    const [alert, setAlert] = useState({ type: "", message: "" });
    const [history, setHistory] = useState([]);
    const [loadingHistory, setLoadingHistory] = useState(false);
    const [generatingQR, setGeneratingQR] = useState(false);
    
    // For teacher location QR generation
    const [locationCode, setLocationCode] = useState("");
    const [locationName, setLocationName] = useState("");
    const [locationQrUrl, setLocationQrUrl] = useState(null);
    const [loadingLocationQR, setLoadingLocationQR] = useState(false);

    useEffect(() => {
        // si no hay usuario → fuera
        if (!localUser) {
            clearToken();
            clearUser();
            window.location.href = "/";
        } else {
            loadHistory();
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

    const loadHistory = async () => {
        try {
            setLoadingHistory(true);
            const res = await api("/qr/history?limit=10");
            const data = await res.json();
            setHistory(data);
        } catch (err) {
            console.error(err);
        } finally {
            setLoadingHistory(false);
        }
    };

    const generateCredential = async () => {
        try {
            setGeneratingQR(true);
            const res = await api(`/admin/qr/generate-credential/${localUser.id}`, {
                method: "GET",
            });

            const blob = await res.blob();
            const url = URL.createObjectURL(blob);
            setQrImageUrl(url);

            showAlert("success", "Credencial generada correctamente.");
        } catch (err) {
            showAlert("error", "Error al generar la credencial: " + err.message);
        } finally {
            setGeneratingQR(false);
        }
    };

    const handleScanLocation = async (locationCode) => {
        try {
            const res = await api("/qr/scan", {
                method: "POST",
                body: JSON.stringify({ location_code: locationCode }),
            });

            const data = await res.json();
            showAlert("success", `Acceso registrado en ${data.location_code}`);
            loadHistory();
        } catch (err) {
            showAlert("error", "Error al registrar acceso: " + err.message);
        }
    };

    const generateLocationQR = async (e) => {
        e.preventDefault();
        if (!locationCode) {
            showAlert("error", "El código de ubicación es obligatorio");
            return;
        }

        try {
            setLoadingLocationQR(true);
            const res = await api("/admin/qr/generate-location", {
                method: "POST",
                body: JSON.stringify({
                    location_code: locationCode,
                    location_name: locationName,
                }),
            });

            const blob = await res.blob();
            const url = URL.createObjectURL(blob);
            setLocationQrUrl(url);
            showAlert("success", "QR de ubicación generado correctamente");
        } catch (err) {
            showAlert("error", "Error al generar QR: " + err.message);
        } finally {
            setLoadingLocationQR(false);
        }
    };

    const downloadLocationQR = () => {
        if (!locationQrUrl || !locationCode) return;
        const a = document.createElement("a");
        a.href = locationQrUrl;
        a.download = `${locationCode}.png`;
        a.click();
    };

    const getRoleLabel = (role) => {
        switch (role) {
            case "admin": return "Administrador";
            case "teacher": return "Profesor";
            case "student": return "Estudiante";
            default: return role;
        }
    };

    const getRoleBadgeColor = (role) => {
        switch (role) {
            case "admin": return "#dc2626";
            case "teacher": return "#2563eb";
            case "student": return "#16a34a";
            default: return "#6b7280";
        }
    };

    if (!localUser) return null;

    const isTeacherOrAdmin = localUser.role === "admin" || localUser.role === "teacher";
    const isStudent = localUser.role === "student";

    return (
        <div className="dashboard-container">
            <div className="dashboard-header">
                <div>
                    <h2>{localUser.full_name}</h2>
                    <div style={{ display: "flex", alignItems: "center", gap: "10px", marginTop: "4px" }}>
                        <p style={{ color: "#6b7280", fontSize: "14px", margin: 0 }}>{localUser.email}</p>
                        <span style={{
                            background: getRoleBadgeColor(localUser.role),
                            color: "white",
                            padding: "2px 8px",
                            borderRadius: "8px",
                            fontSize: "12px",
                            fontWeight: "500"
                        }}>
                            {getRoleLabel(localUser.role)}
                        </span>
                    </div>
                </div>
                <div style={{ display: "flex", gap: "10px" }}>
                    {localUser.role === "admin" && (
                        <Button
                            variant="secondary"
                            onClick={() => (window.location.href = "/admin")}
                        >
                            Panel Admin
                        </Button>
                    )}
                    <Button variant="secondary" onClick={handleLogout}>
                        Cerrar sesión
                    </Button>
                </div>
            </div>

            <Alert type={alert.type} message={alert.message} />

            {/* TABS */}
            <div className="tabs">
                <button
                    className={`tab-button ${
                        activeTab === "credential" ? "active" : ""
                    }`}
                    onClick={() => setActiveTab("credential")}
                >
                    🎓 Credencial
                </button>
                
                {isStudent && (
                    <button
                        className={`tab-button ${activeTab === "scan" ? "active" : ""}`}
                        onClick={() => setActiveTab("scan")}
                    >
                        📷 Escanear
                    </button>
                )}
                
                {isTeacherOrAdmin && (
                    <button
                        className={`tab-button ${activeTab === "generate-qr" ? "active" : ""}`}
                        onClick={() => setActiveTab("generate-qr")}
                    >
                        📍 Generar QR
                    </button>
                )}
                
                <button
                    className={`tab-button ${
                        activeTab === "history" ? "active" : ""
                    }`}
                    onClick={() => setActiveTab("history")}
                >
                    📋 Historial
                </button>
            </div>

            <div className="tab-content" style={{ marginTop: "-1px" }}>
                {activeTab === "credential" && (
                    <div>
                        {!qrImageUrl && (
                            <div style={{ marginBottom: "20px" }}>
                                <div className="dashboard-section-title">
                                    Mi credencial digital
                                </div>
                                <p className="dashboard-section-subtitle">
                                    Genera tu carnet digital con código QR para identificarte en
                                    el campus.
                                </p>
                                <Button onClick={generateCredential}>
                                    {generatingQR ? "Generando..." : "✨ Generar credencial"}
                                </Button>
                            </div>
                        )}

                        <CredentialCard user={localUser} qrImageUrl={qrImageUrl} />
                    </div>
                )}

                {activeTab === "scan" && isStudent && (
                    <QRScanner onScan={handleScanLocation} />
                )}

                {activeTab === "generate-qr" && isTeacherOrAdmin && (
                    <div className="admin-card">
                        <h3 style={{ marginBottom: "6px" }}>Generar QR de Ubicación</h3>
                        <p style={{ color: "#6b7280", fontSize: "14px", marginBottom: "16px" }}>
                            Crea códigos QR para aulas, laboratorios y otros puntos del campus.
                        </p>

                        <form onSubmit={generateLocationQR}>
                            <div className="form-group">
                                <label>Código de ubicación *</label>
                                <input
                                    type="text"
                                    value={locationCode}
                                    onChange={(e) => setLocationCode(e.target.value)}
                                    placeholder="Ej: LAB-101, AULA-302"
                                    required
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
                                {loadingLocationQR ? "Generando..." : "Generar QR"}
                            </Button>
                        </form>

                        {locationQrUrl && (
                            <div style={{ marginTop: "20px", textAlign: "center" }}>
                                <p style={{ marginBottom: "10px" }}>
                                    Código: <strong>{locationCode}</strong>
                                    {locationName ? ` - ${locationName}` : ""}
                                </p>
                                <img
                                    src={locationQrUrl}
                                    alt="QR ubicación"
                                    style={{ maxWidth: "260px", border: "2px solid #e5e7eb", borderRadius: "8px" }}
                                />
                                <div style={{ marginTop: "12px" }}>
                                    <Button onClick={downloadLocationQR}>Descargar QR</Button>
                                </div>
                            </div>
                        )}
                    </div>
                )}

                {activeTab === "history" && (
                    <AccessHistory history={history} loading={loadingHistory} />
                )}
            </div>
        </div>
    );
}
