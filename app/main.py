from fastapi import FastAPI
from contextlib import asynccontextmanager
from routes import routers
from memory import db_utils
from core.logging import setup_logger

logger = setup_logger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting Astra...")
    db_utils.init_db()
    yield
    logger.info("Shutting down Astra...")

app = FastAPI(lifespan=lifespan)

for router in routers:
    app.include_router(router)
    logger.debug(f"Registered router: {router.prefix if hasattr(router, 'prefix') else 'root'}")

from fastapi.staticfiles import StaticFiles
app.mount("/static", StaticFiles(directory="static", html=True), name="static")

@app.get("/")
async def root():
    from fastapi.responses import FileResponse
    return FileResponse("static/index.html")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)