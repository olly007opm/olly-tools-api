from fastapi import APIRouter

router = APIRouter(
    prefix="/template",
    tags=["template"],
)


@router.get("/", summary="A demo route in the template file")
async def demo():
    """
    Some demo text that will show up in the docs.
    """
    return {"message": "Hello World"}
