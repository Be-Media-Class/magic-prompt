from fastapi import APIRouter, HTTPException, BackgroundTasks

from ..database import buscar_por_id, atualizar_status
from ..models import StatusCarrossel
from ..services.meta_service import postar_carrossel_instagram, verificar_credenciais, MetaAPIError

router = APIRouter(prefix="/instagram", tags=["Instagram"])


async def _publicar_em_background(carrossel_id: str):
    carrossel = buscar_por_id(carrossel_id)
    if not carrossel:
        return
    try:
        url = await postar_carrossel_instagram(
            tema=carrossel["tema"],
            cta_acao=carrossel["conteudo"]["cta_acao"],
            caminhos_imagens=carrossel["imagens"],
            carrossel_id=carrossel_id
        )
        atualizar_status(carrossel_id, StatusCarrossel.publicado, instagram_url=url)
    except MetaAPIError as e:
        atualizar_status(carrossel_id, StatusCarrossel.aprovado, erro_publicacao=str(e))
        print(f"[Instagram] Erro ao publicar: {e}")


@router.post("/publicar/{id}")
async def publicar_no_instagram(id: str, background_tasks: BackgroundTasks):
    """Publica o carrossel aprovado no Instagram."""
    carrossel = buscar_por_id(id)
    if not carrossel:
        raise HTTPException(status_code=404, detail="Carrossel não encontrado")
    if carrossel["status"] != StatusCarrossel.aprovado:
        raise HTTPException(status_code=400, detail="Carrossel precisa estar aprovado antes de publicar")

    background_tasks.add_task(_publicar_em_background, id)
    return {"mensagem": "Publicando no Instagram... aguarde alguns segundos."}


@router.get("/verificar-credenciais")
async def checar_credenciais():
    """Verifica se as credenciais da Meta API estão configuradas e funcionando."""
    resultado = await verificar_credenciais()
    return resultado
