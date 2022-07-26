#  olly-tools-api | template.py
#  Last modified: 06/07/2022, 21:07
#  Copyright (c) 2022 Olly (https://olly.ml/). All rights reserved.

from fastapi import APIRouter

router = APIRouter(
    prefix="/template",
    tags=["template"],
)


@router.get("/", summary="A demo route in the template file")
def demo():
    """
    Some demo text that will show up in the docs.
    """
    return {"message": "Hello World"}
