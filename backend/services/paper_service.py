"""
Integração com paper.design via servidor MCP local.
Requer Paper Desktop aberto com um arquivo.
MCP server: http://127.0.0.1:29979/mcp

Documentação: https://paper.design/docs/mcp
"""
import os
import httpx
import json
from ..models import ConteudoCarrossel

PAPER_MCP_URL = os.getenv("PAPER_MCP_URL", "http://127.0.0.1:29979/mcp")

CORES_BMC = {
    "roxo": "#7543b4",
    "preto": "#1d1d1d",
    "azul": "#123356",
    "verde": "#2ae19e",
    "branco": "#ffffff",
}


class PaperMCPClient:
    """Cliente para o servidor MCP do paper.design."""

    def __init__(self):
        self.url = PAPER_MCP_URL
        self._session_id = None

    async def _rpc(self, method: str, params: dict) -> dict:
        payload = {
            "jsonrpc": "2.0",
            "method": method,
            "params": params,
            "id": 1
        }
        async with httpx.AsyncClient(timeout=30) as client:
            r = await client.post(self.url, json=payload)
            r.raise_for_status()
            data = r.json()
            if "error" in data:
                raise Exception(f"Paper MCP erro: {data['error']}")
            return data.get("result", {})

    async def listar_ferramentas(self) -> list[str]:
        result = await self._rpc("tools/list", {})
        return [t["name"] for t in result.get("tools", [])]

    async def chamar(self, nome_ferramenta: str, argumentos: dict) -> dict:
        return await self._rpc("tools/call", {
            "name": nome_ferramenta,
            "arguments": argumentos
        })

    async def disponivel(self) -> bool:
        try:
            await self._rpc("initialize", {
                "protocolVersion": "2024-11-05",
                "clientInfo": {"name": "magic-prompt-bmc", "version": "1.0"}
            })
            return True
        except Exception:
            return False


async def criar_carrossel_no_paper(carrossel_id: str, conteudo: ConteudoCarrossel) -> bool:
    """
    Cria um carrossel no paper.design usando as ferramentas MCP.
    Retorna True se criou com sucesso, False se Paper não está disponível.
    """
    client = PaperMCPClient()

    if not await client.disponivel():
        return False

    ferramentas = await client.listar_ferramentas()

    # Tenta criar um novo arquivo com artboards para o carrossel
    try:
        # Cada slide = um artboard 1080x1080
        total_slides = len(conteudo.slides) + 2  # capa + conteúdo + CTA

        for i in range(total_slides):
            if "create_artboard" in ferramentas:
                await client.chamar("create_artboard", {
                    "width": 1080,
                    "height": 1080,
                    "name": f"Slide {i + 1}"
                })

        # Aplica identidade visual BMC se as ferramentas permitirem
        if "set_fill" in ferramentas or "update_node" in ferramentas:
            await _aplicar_identidade_visual(client, conteudo, ferramentas)

        return True

    except Exception as e:
        print(f"[paper.design] Erro ao criar design: {e}")
        return False


async def _aplicar_identidade_visual(client: PaperMCPClient, conteudo: ConteudoCarrossel, ferramentas: list):
    """Aplica cores e textos BMC nos artboards criados."""
    # Esta função adapta os comandos dependendo das ferramentas disponíveis no paper.design
    # O paper.design MCP expõe ~24 ferramentas que variam conforme a versão

    if "add_text" in ferramentas:
        # Adiciona título da capa
        await client.chamar("add_text", {
            "text": conteudo.titulo_capa,
            "fontSize": 72,
            "fontWeight": "900",
            "color": CORES_BMC["branco"],
            "artboardIndex": 0
        })

    # Aplica textos nos slides de conteúdo
    for i, slide in enumerate(conteudo.slides):
        if "add_text" in ferramentas:
            await client.chamar("add_text", {
                "text": slide.titulo,
                "fontSize": 52,
                "fontWeight": "800",
                "color": CORES_BMC["verde"],
                "artboardIndex": i + 1
            })
            await client.chamar("add_text", {
                "text": slide.conteudo,
                "fontSize": 34,
                "fontWeight": "400",
                "color": CORES_BMC["branco"],
                "artboardIndex": i + 1
            })
