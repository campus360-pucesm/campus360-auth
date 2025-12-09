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

    if (!localUser) return null;

    return (
        <div className="dashboard-container">
            <div className="dashboard-header">
                <div>
                    <h2>{localUser.full_name}</h2>
                    <p style={{ color: "#6b7280", fontSize: "14px" }}>{localUser.email}</p>
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
                <button
                    className={`tab-button ${activeTab === "scan" ? "active" : ""}`}
                    onClick={() => setActiveTab("scan")}
                >
                    📷 Escanear
                </button>
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

                {activeTab === "scan" && (
                    <QRScanner onScan={handleScanLocation} />
                )}

                {activeTab === "history" && (
                    <AccessHistory history={history} loading={loadingHistory} />
                )}
            </div>
        </div>
    );
}
