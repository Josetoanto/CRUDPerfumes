from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

from app.core.database import Base, engine
from app.core.config import settings
from app.modules.auth.router import router as auth_router
from app.modules.perfumes.router import router as perfume_router


# ==========================================
# Lifespan
# ==========================================

@asynccontextmanager
async def lifespan(app: FastAPI):
    
    yield


# ==========================================
# App Initialization
# ==========================================

app = FastAPI(
    title="Perfume Inventory API",
    description="API para gestión de perfumes con autenticación JWT",
    version="1.0.0",
    lifespan=lifespan,
)


# ==========================================
# CORS (Permitir todos los origins)
# ==========================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # Escucha cualquier origin
    allow_credentials=False,  # Obligatorio cuando usas "*"
    allow_methods=["*"],
    allow_headers=["*"],
)


# ==========================================
# Global Exception Handler
# ==========================================

@app.exception_handler(Exception)
async def unhandled_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={
            "error_code": "SERVER_ERROR",
            "message": "Internal server error",
        },
    )


# ==========================================
# Routers
# ==========================================

app.include_router(auth_router, prefix="/api/v1")
app.include_router(perfume_router, prefix="/api/v1")



@app.get("/health", tags=["System"])
def health_check():
    return {
        "status": "ok",
        "service": "Perfume Inventory API",
        "version": app.version,
    }
