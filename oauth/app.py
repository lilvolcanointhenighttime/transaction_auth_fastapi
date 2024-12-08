import uvicorn
from contextlib import asynccontextmanager
from fastapi import FastAPI
import aiohttp
from .routers import router
from .config.database import create_tables, drop_tables
from fastapi.middleware.cors import CORSMiddleware


aiohttp_clientsession: aiohttp.ClientSession = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    global aiohttp_clientsession
    aiohttp_clientsession = aiohttp.ClientSession()
    await create_tables()
    yield
    await aiohttp_clientsession.close()
    # await drop_tables()

app = FastAPI(title="OAuth", lifespan=lifespan, root_path="/api/oauth")

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS", "DELETE", "PATCH", "PUT"],
    allow_headers=["Content-Type", "Access-Control-Allow-Origin", "Access-Control-Allow-Credentials", "Access-Control-Allow-Headers"],
)


app.include_router(router)

if __name__ == "__main__":
    uvicorn.run(app='app:app', host="0.0.0.0", port=8800, reload=True, debug=True)