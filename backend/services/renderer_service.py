"""
Renderiza slides do carrossel como imagens 1080x1080px
usando Playwright (Chromium headless) com identidade visual BMC.
"""
import os
import asyncio
from pathlib import Path
from ..models import ConteudoCarrossel

OUTPUT_DIR = Path(__file__).parent.parent / "static" / "images"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Identidade visual BMC
CORES = {
    "preto": "#1d1d1d",
    "roxo": "#7543b4",
    "azul": "#123356",
    "verde": "#2ae19e",
    "branco": "#ffffff",
}

CSS_BASE = """
@import url('https://fonts.googleapis.com/css2?family=Raleway:wght@300;400;500;600;700;800;900&display=swap');
* { margin: 0; padding: 0; box-sizing: border-box; }
body { width: 1080px; height: 1080px; overflow: hidden; font-family: 'Raleway', sans-serif; }
.slide { width: 1080px; height: 1080px; display: flex; flex-direction: column; position: relative; }
"""


def _html_capa(conteudo: ConteudoCarrossel) -> str:
    return f"""<!DOCTYPE html>
<html><head><meta charset="UTF-8">
<style>
{CSS_BASE}
.slide {{ background: {CORES['roxo']}; justify-content: center; align-items: center; padding: 80px; }}
.logo {{ position: absolute; top: 60px; left: 70px; display: flex; align-items: center; gap: 12px; }}
.logo-icon {{ width: 48px; height: 48px; background: {CORES['verde']}; clip-path: polygon(20% 0%, 80% 0%, 100% 100%, 0% 100%); }}
.logo-text {{ font-size: 28px; font-weight: 800; color: {CORES['branco']}; letter-spacing: -0.5px; }}
.logo-text span {{ font-weight: 300; }}
.conteudo {{ text-align: center; max-width: 880px; }}
.titulo {{ font-size: 72px; font-weight: 900; color: {CORES['branco']}; line-height: 1.1; margin-bottom: 32px; letter-spacing: -2px; }}
.subtitulo {{ font-size: 32px; font-weight: 300; color: {CORES['verde']}; line-height: 1.4; }}
.deslize {{ position: absolute; bottom: 60px; right: 70px; font-size: 22px; color: rgba(255,255,255,0.6); font-weight: 400; }}
.barra {{ position: absolute; bottom: 0; left: 0; right: 0; height: 8px; background: {CORES['verde']}; }}
</style></head>
<body>
<div class="slide">
  <div class="logo">
    <div class="logo-icon"></div>
    <div class="logo-text">BE<span>media</span>class</div>
  </div>
  <div class="conteudo">
    <div class="titulo">{conteudo.titulo_capa}</div>
    <div class="subtitulo">{conteudo.subtitulo_capa}</div>
  </div>
  <div class="deslize">Deslize →</div>
  <div class="barra"></div>
</div>
</body></html>"""


def _html_slide_conteudo(slide, total: int) -> str:
    return f"""<!DOCTYPE html>
<html><head><meta charset="UTF-8">
<style>
{CSS_BASE}
.slide {{ background: {CORES['preto']}; padding: 80px; justify-content: space-between; }}
.numero-bg {{ position: absolute; top: -20px; right: 60px; font-size: 240px; font-weight: 900;
  color: rgba(117,67,180,0.15); line-height: 1; pointer-events: none; }}
.header {{ display: flex; align-items: center; gap: 24px; margin-bottom: 60px; }}
.emoji {{ font-size: 56px; }}
.titulo {{ font-size: 52px; font-weight: 800; color: {CORES['verde']}; line-height: 1.2; max-width: 700px; }}
.conteudo {{ font-size: 34px; font-weight: 400; color: {CORES['branco']}; line-height: 1.6;
  max-width: 900px; flex: 1; display: flex; align-items: center; }}
.footer {{ display: flex; justify-content: space-between; align-items: flex-end; }}
.progresso {{ font-size: 20px; color: rgba(255,255,255,0.3); font-weight: 400; }}
.logo-small {{ font-size: 22px; font-weight: 800; color: rgba(255,255,255,0.2); letter-spacing: -0.5px; }}
.logo-small span {{ font-weight: 300; }}
.linha-verde {{ position: absolute; left: 0; top: 0; bottom: 0; width: 8px; background: {CORES['roxo']}; }}
</style></head>
<body>
<div class="slide">
  <div class="linha-verde"></div>
  <div class="numero-bg">{slide.numero}</div>
  <div class="header">
    <div class="emoji">{slide.emoji or '💡'}</div>
    <div class="titulo">{slide.titulo}</div>
  </div>
  <div class="conteudo">{slide.conteudo}</div>
  <div class="footer">
    <div class="progresso">{slide.numero} / {total}</div>
    <div class="logo-small">BE<span>media</span>class</div>
  </div>
</div>
</body></html>"""


def _html_cta(conteudo: ConteudoCarrossel) -> str:
    return f"""<!DOCTYPE html>
<html><head><meta charset="UTF-8">
<style>
{CSS_BASE}
.slide {{ background: {CORES['azul']}; justify-content: center; align-items: center; padding: 80px; text-align: center; }}
.logo {{ position: absolute; top: 60px; left: 50%; transform: translateX(-50%);
  display: flex; align-items: center; gap: 12px; }}
.logo-icon {{ width: 40px; height: 40px; background: {CORES['verde']}; clip-path: polygon(20% 0%, 80% 0%, 100% 100%, 0% 100%); }}
.logo-text {{ font-size: 24px; font-weight: 800; color: {CORES['branco']}; }}
.logo-text span {{ font-weight: 300; }}
.estrela {{ font-size: 56px; margin-bottom: 40px; }}
.cta-texto {{ font-size: 48px; font-weight: 800; color: {CORES['branco']}; line-height: 1.2;
  margin-bottom: 32px; max-width: 800px; }}
.cta-acao {{ font-size: 28px; font-weight: 400; color: {CORES['verde']}; margin-bottom: 60px; }}
.handle {{ font-size: 34px; font-weight: 700; color: {CORES['branco']}; background: rgba(255,255,255,0.1);
  padding: 20px 48px; border-radius: 50px; border: 2px solid {CORES['verde']}; }}
.barra {{ position: absolute; bottom: 0; left: 0; right: 0; height: 8px; background: {CORES['verde']}; }}
</style></head>
<body>
<div class="slide">
  <div class="logo">
    <div class="logo-icon"></div>
    <div class="logo-text">BE<span>media</span>class</div>
  </div>
  <div class="estrela">🚀</div>
  <div class="cta-texto">{conteudo.cta_texto}</div>
  <div class="cta-acao">{conteudo.cta_acao}</div>
  <div class="handle">@claudiosoares.creator</div>
  <div class="barra"></div>
</div>
</body></html>"""


async def renderizar_carrossel(carrossel_id: str, conteudo: ConteudoCarrossel) -> list[str]:
    from playwright.async_api import async_playwright

    pasta = OUTPUT_DIR / carrossel_id
    pasta.mkdir(exist_ok=True)

    slides_html = [_html_capa(conteudo)]
    for slide in conteudo.slides:
        slides_html.append(_html_slide_conteudo(slide, len(conteudo.slides)))
    slides_html.append(_html_cta(conteudo))

    caminhos = []

    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page(viewport={"width": 1080, "height": 1080})

        for i, html in enumerate(slides_html):
            nome = f"slide_{i:02d}.jpg"
            caminho = pasta / nome
            await page.set_content(html, wait_until="networkidle")
            await page.screenshot(path=str(caminho), type="jpeg", quality=95, full_page=False)
            caminhos.append(f"/static/images/{carrossel_id}/{nome}")

        await browser.close()

    return caminhos
