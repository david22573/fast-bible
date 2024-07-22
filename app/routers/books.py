from fastapi import APIRouter

router = APIRouter(
    prefix="/books",
    tags=["books"],
    responses={404: {"description": "Not found"}},
)


@router.get("/")
async def index():
    return "Fast Bible - Books"
