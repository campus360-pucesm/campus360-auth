from fastapi import APIRouter

router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)

@router.get("/validate")
def validate_token(token: str):
    # Esta función será reemplazada por JWT real
    if token == "valid-token":
        return {"valid": True, "user_id": 1}
    return {"valid": False}
