"""
Integração com Instagram Graph API (Meta) para publicar carrosséis.
API versão: v22.0

Documentação: https://developers.facebook.com/docs/instagram-platform/content-publishing/
"""
import os
import httpx
from pathlib import Path

GRAPH_URL = "https://graph.facebook.com/v22.0"
INSTAGRAM_USER_ID = os.getenv("INSTAGRAM_USER_ID")
ACCESS_TOKEN = os.getenv("INSTAGRAM_ACCESS_TOKEN")
PUBLIC_BASE_URL = os.getenv("PUBLIC_BASE_URL", "http://localhost:8000")


class MetaAPIError(Exception):
    pass


async def _post(endpoint: str, dados: dict) -> dict:
    dados["access_token"] = ACCESS_TOKEN
    async with httpx.AsyncClient(timeout=60) as client:
        r = await client.post(f"{GRAPH_URL}/{endpoint}", data=dados)
        resultado = r.json()
        if "error" in resultado:
            raise MetaAPIError(f"Meta API: {resultado['error']['message']}")
        return resultado


async def criar_container_imagem(url_imagem: str) -> str:
    """Cria um container de mídia para uma imagem do carrossel."""
    resultado = await _post(f"{INSTAGRAM_USER_ID}/media", {
        "image_url": url_imagem,
        "is_carousel_item": "true",
    })
    return resultado["id"]


async def criar_container_carrossel(ids_filhos: list[str], legenda: str) -> str:
    """Cria o container do carrossel com todos os slides."""
    resultado = await _post(f"{INSTAGRAM_USER_ID}/media", {
        "media_type": "CAROUSEL",
        "children": ",".join(ids_filhos),
        "caption": legenda,
    })
    return resultado["id"]


async def publicar_carrossel(id_container: str) -> str:
    """Publica o carrossel e retorna o ID do post."""
    resultado = await _post(f"{INSTAGRAM_USER_ID}/media_publish", {
        "creation_id": id_container,
    })
    return resultado["id"]


def _gerar_legenda(tema: str, cta_acao: str) -> str:
    return f"""{cta_acao}

🎓 Aprenda a usar IAs Criativas na prática com a Be Media Class.

#IACriativa #BeMediaClass #MarketingDigital #CriacaoDeConteudo #IA #Produtividade #Criatividade #Empreendedorismo #InstagramMarketing #{tema.replace(' ', '')}"""


async def postar_carrossel_instagram(
    tema: str,
    cta_acao: str,
    caminhos_imagens: list[str],
    carrossel_id: str
) -> str:
    """
    Fluxo completo: cria containers → monta carrossel → publica.
    Retorna a URL do post publicado.
    """
    if not INSTAGRAM_USER_ID or not ACCESS_TOKEN:
        raise MetaAPIError(
            "Configure INSTAGRAM_USER_ID e INSTAGRAM_ACCESS_TOKEN no arquivo .env"
        )

    # Converte caminhos locais em URLs públicas
    urls_publicas = [
        f"{PUBLIC_BASE_URL}{caminho}" for caminho in caminhos_imagens
    ]

    # Passo 1: Cria um container para cada imagem
    ids_filhos = []
    for url in urls_publicas:
        container_id = await criar_container_imagem(url)
        ids_filhos.append(container_id)

    # Passo 2: Cria o container do carrossel
    legenda = _gerar_legenda(tema, cta_acao)
    id_carrossel = await criar_container_carrossel(ids_filhos, legenda)

    # Passo 3: Publica
    id_post = await publicar_carrossel(id_carrossel)

    return f"https://www.instagram.com/p/{id_post}/"


async def verificar_credenciais() -> dict:
    """Verifica se as credenciais da Meta API estão corretas."""
    async with httpx.AsyncClient(timeout=15) as client:
        r = await client.get(
            f"{GRAPH_URL}/{INSTAGRAM_USER_ID}",
            params={
                "fields": "id,username,account_type",
                "access_token": ACCESS_TOKEN
            }
        )
        dados = r.json()
        if "error" in dados:
            return {"ok": False, "erro": dados["error"]["message"]}
        return {"ok": True, "usuario": dados.get("username"), "tipo": dados.get("account_type")}
