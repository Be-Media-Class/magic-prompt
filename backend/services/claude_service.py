import os
import json
import anthropic
from ..models import ConteudoCarrossel, Slide

SYSTEM_PROMPT = """Você é um especialista em marketing digital e educação criativa da Be Media Class (BMC).

SOBRE A BMC:
A Be Media Class é uma escola criativa onde Claudio Soares ensina IAs Criativas para criadores e empreendedores,
com foco em criatividade e produtividade digital. O perfil é @claudiosoares.creator no Instagram.

MISSÃO DOS CARROSSÉIS:
Criar conteúdo educativo, prático e inspirador sobre IA criativa para criadores e empreendedores.
Linguagem: direta, acessível, sem jargões técnicos. Tom: amigável e empoderador.

REGRAS DE COPYWRITING:
- Capa: título impactante (máx 8 palavras) + subtítulo que gera curiosidade
- Slides de conteúdo: um insight por slide, prático e aplicável
- Título do slide: máx 5 palavras, impactante
- Conteúdo: máx 35 palavras, direto ao ponto, fala com "você"
- CTA final: gera ação (salvar, comentar, seguir)

Sempre responda em JSON válido conforme o schema solicitado."""


async def gerar_conteudo_carrossel(tema: str, tom: str, num_slides: int) -> ConteudoCarrossel:
    client = anthropic.AsyncAnthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

    schema = {
        "titulo_capa": "string (título impactante, máx 8 palavras)",
        "subtitulo_capa": "string (subtítulo que gera curiosidade, máx 12 palavras)",
        "slides": [
            {
                "numero": "int (1 a N)",
                "titulo": "string (máx 5 palavras, impactante)",
                "conteudo": "string (máx 35 palavras, prático e direto)",
                "emoji": "string (1 emoji relevante)"
            }
        ],
        "cta_texto": "string (chamada principal para ação, máx 15 palavras)",
        "cta_acao": "string (instrução específica: salvar, comentar, seguir, etc.)"
    }

    prompt = f"""Crie um carrossel de Instagram sobre o tema: "{tema}"

Tom desejado: {tom}
Número de slides de conteúdo: {num_slides}
Perfil: @claudiosoares.creator (Be Media Class - IAs Criativas)

Retorne APENAS o JSON com esta estrutura:
{json.dumps(schema, ensure_ascii=False, indent=2)}

O conteúdo deve ser relevante para criadores de conteúdo e empreendedores que querem usar IA de forma criativa e produtiva."""

    response = await client.messages.create(
        model="claude-opus-4-7",
        max_tokens=2000,
        system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": prompt}]
    )

    texto = response.content[0].text.strip()
    # Extrai JSON mesmo se vier com markdown
    if "```" in texto:
        texto = texto.split("```")[1].replace("json", "").strip()

    dados = json.loads(texto)
    slides = [Slide(**s) for s in dados["slides"]]

    return ConteudoCarrossel(
        titulo_capa=dados["titulo_capa"],
        subtitulo_capa=dados["subtitulo_capa"],
        slides=slides,
        cta_texto=dados["cta_texto"],
        cta_acao=dados["cta_acao"]
    )
