import uuid
from datetime import datetime
from fastapi import APIRouter, HTTPException, BackgroundTasks

from ..models import CriarCarrosselRequest, CarrosselResponse, StatusCarrossel
from ..database import salvar, buscar_por_id, listar_todos, atualizar_status
from ..services.claude_service import gerar_conteudo_carrossel
from ..services.renderer_service import renderizar_carrossel
from ..services.paper_service import criar_carrossel_no_paper, PaperMCPClient

router = APIRouter(prefix="/carrossel", tags=["Carrossel"])


async def _processar_carrossel(carrossel_id: str, tema: str, tom: str, num_slides: int):
    """Job em background: gera conteúdo, renderiza slides e atualiza status."""
    try:
        # 1. Gera o conteúdo com Claude
        conteudo = await gerar_conteudo_carrossel(tema, tom, num_slides)
        atualizar_status(carrossel_id, StatusCarrossel.gerando, conteudo=conteudo.model_dump())

        # 2. Verifica se paper.design está disponível (opcional)
        paper_client = PaperMCPClient()
        if await paper_client.disponivel():
            await criar_carrossel_no_paper(carrossel_id, conteudo)

        # 3. Renderiza slides como imagens (sempre disponível)
        imagens = await renderizar_carrossel(carrossel_id, conteudo)

        # 4. Atualiza para aguardando aprovação
        atualizar_status(
            carrossel_id,
            StatusCarrossel.aguardando_aprovacao,
            imagens=imagens,
            conteudo=conteudo.model_dump()
        )

    except Exception as e:
        atualizar_status(carrossel_id, "erro", erro=str(e))
        print(f"[Erro] Carrossel {carrossel_id}: {e}")


@router.post("/criar", response_model=CarrosselResponse)
async def criar_carrossel(request: CriarCarrosselRequest, background_tasks: BackgroundTasks):
    """Inicia a criação de um novo carrossel (processamento em background)."""
    carrossel_id = str(uuid.uuid4())[:8]
    agora = datetime.now().isoformat()

    carrossel = {
        "id": carrossel_id,
        "tema": request.tema,
        "status": StatusCarrossel.gerando,
        "conteudo": None,
        "imagens": None,
        "instagram_url": None,
        "criado_em": agora,
        "atualizado_em": agora,
    }
    salvar(carrossel)

    background_tasks.add_task(
        _processar_carrossel, carrossel_id, request.tema, request.tom, request.num_slides
    )

    return CarrosselResponse(**carrossel)


@router.get("/listar", response_model=list[CarrosselResponse])
async def listar_carrosseis():
    """Lista todos os carrosséis criados."""
    return [CarrosselResponse(**c) for c in listar_todos()]


@router.get("/{id}", response_model=CarrosselResponse)
async def buscar_carrossel(id: str):
    """Busca um carrossel pelo ID."""
    carrossel = buscar_por_id(id)
    if not carrossel:
        raise HTTPException(status_code=404, detail="Carrossel não encontrado")
    return CarrosselResponse(**carrossel)


@router.post("/{id}/aprovar")
async def aprovar_carrossel(id: str):
    """Aprova o carrossel para publicação no Instagram."""
    carrossel = buscar_por_id(id)
    if not carrossel:
        raise HTTPException(status_code=404, detail="Carrossel não encontrado")
    if carrossel["status"] != StatusCarrossel.aguardando_aprovacao:
        raise HTTPException(status_code=400, detail="Carrossel não está aguardando aprovação")

    atualizar_status(id, StatusCarrossel.aprovado)
    return {"mensagem": "Carrossel aprovado! Pronto para publicar no Instagram."}


@router.post("/{id}/rejeitar")
async def rejeitar_carrossel(id: str, motivo: str = ""):
    """Rejeita o carrossel e permite reprocessamento."""
    carrossel = buscar_por_id(id)
    if not carrossel:
        raise HTTPException(status_code=404, detail="Carrossel não encontrado")

    atualizar_status(id, StatusCarrossel.rejeitado, motivo_rejeicao=motivo)
    return {"mensagem": "Carrossel rejeitado."}


@router.post("/{id}/regenerar")
async def regenerar_carrossel(id: str, background_tasks: BackgroundTasks):
    """Regenera o conteúdo de um carrossel rejeitado."""
    carrossel = buscar_por_id(id)
    if not carrossel:
        raise HTTPException(status_code=404, detail="Carrossel não encontrado")

    atualizar_status(id, StatusCarrossel.gerando)
    background_tasks.add_task(
        _processar_carrossel, id, carrossel["tema"], "educativo e inspirador", 5
    )
    return {"mensagem": "Regenerando carrossel..."}
