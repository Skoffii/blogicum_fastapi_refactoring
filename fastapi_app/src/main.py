import asyncio
import uvicorn

from app import create_app

import logging
import sys


logging.basicConfig(
    level=logging.INFO,
    # format=": %(levelname)-8s %(name)-20s %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
    # force=True
)

app = create_app()

async def main() -> None:
    config = uvicorn.Config(
        "main:app", host="0.0.0.0", port=8000, reload=False
    )
    server = uvicorn.Server(config=config)
    tasks = (
        asyncio.create_task(server.serve()),
    )

    await asyncio.wait(tasks, return_when=asyncio.FIRST_COMPLETED)


if __name__ == "__main__":
    asyncio.run(main())