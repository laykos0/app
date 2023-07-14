from typing import Annotated

from fastapi import Header


async def get_token_header(x_token: Annotated[str, Header()]):
    pass
