import "../styles/style.css";
import Button from "../components/Button";

export default function NotFound() {
    return (
        <div className="center-container">
            <div className="card" style={{ textAlign: "center" }}>
                <h2 style={{ fontSize: "28px", marginBottom: "10px" }}>⚠ 404</h2>
                <p style={{ color: "#6b7280", marginBottom: "20px" }}>
                    La página que buscas no existe.
                </p>

                <Button onClick={() => (window.location.href = "/dashboard")}>
                    Ir al dashboard
                </Button>
            </div>
        </div>
    );
}
