from pydantic import BaseModel
from typing import Optional
from enum import Enum


class StatusCarrossel(str, Enum):
    gerando = "gerando"
    aguardando_aprovacao = "aguardando_aprovacao"
    aprovado = "aprovado"
    rejeitado = "rejeitado"
    publicado = "publicado"


class Slide(BaseModel):
    numero: int
    titulo: str
    conteudo: str
    emoji: Optional[str] = ""


class ConteudoCarrossel(BaseModel):
    titulo_capa: str
    subtitulo_capa: str
    slides: list[Slide]
    cta_texto: str
    cta_acao: str


class CriarCarrosselRequest(BaseModel):
    tema: str
    tom: Optional[str] = "educativo e inspirador"
    num_slides: Optional[int] = 5


class CarrosselResponse(BaseModel):
    id: str
    tema: str
    status: StatusCarrossel
    conteudo: Optional[ConteudoCarrossel] = None
    imagens: Optional[list[str]] = None
    instagram_url: Optional[str] = None
    criado_em: str
    atualizado_em: str
