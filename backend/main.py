import os
from pathlib import Path
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

load_dotenv()

from .routers import carousel, instagram

app = FastAPI(
    title="Magic Prompt — Be Media Class",
    description="Criador automático de carrosséis para Instagram com identidade visual BMC",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", os.getenv("PUBLIC_BASE_URL", "")],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve imagens geradas publicamente (necessário para a Meta API)
imagens_dir = Path(__file__).parent / "static" / "images"
imagens_dir.mkdir(parents=True, exist_ok=True)
app.mount("/static", StaticFiles(directory=str(Path(__file__).parent / "static")), name="static")

app.include_router(carousel.router)
app.include_router(instagram.router)


@app.get("/")
async def raiz():
    return {
        "app": "Magic Prompt — Be Media Class",
        "versao": "1.0.0",
        "docs": "/docs",
        "status": "online"
    }


@app.get("/saude")
async def verificar_saude():
    """Verifica se o servidor está funcionando e as configurações estão corretas."""
    from .services.paper_service import PaperMCPClient

    paper_client = PaperMCPClient()
    paper_disponivel = await paper_client.disponivel()

    return {
        "servidor": "online",
        "anthropic_configurado": bool(os.getenv("ANTHROPIC_API_KEY")),
        "instagram_configurado": bool(os.getenv("INSTAGRAM_ACCESS_TOKEN")),
        "paper_design_disponivel": paper_disponivel,
        "url_publica": os.getenv("PUBLIC_BASE_URL", "não configurada"),
    }
