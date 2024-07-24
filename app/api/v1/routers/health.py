from fastapi import APIRouter


router = APIRouter(
    prefix="/health",
    tags=["HEALTH CHECK"],
)


@router.get("/")
async def check_health():
    return {"message": "success"}
