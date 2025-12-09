import "../styles/style.css";
import Button from "../components/Button";

export default function NotAuthorized() {
    return (
        <div className="center-container">
            <div className="card" style={{ textAlign: "center" }}>
                <h2 style={{ marginBottom: "10px", color: "#ef4444" }}>⛔ Acceso Denegado</h2>
                <p style={{ color: "#6b7280", marginBottom: "20px" }}>
                    No tienes permisos para acceder a esta sección.
                </p>

                <Button onClick={() => (window.location.href = "/dashboard")}>
                    Volver al dashboard
                </Button>
            </div>
        </div>
    );
}
