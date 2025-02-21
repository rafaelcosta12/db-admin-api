from fastapi import APIRouter

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/login")
async def login():
    return {"message": "Login successful"}

@router.post("/logout")
async def logout():
    return {"message": "Logout successful"}

@router.post("/register")
async def register():
    return {"message": "Registration successful"}
