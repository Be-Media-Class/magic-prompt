"""
Como usar
─────────────────────────────────────────────────────
1. Salve o HTML do seu carrossel como  carrossel.html  nesta pasta
2. No terminal, rode:
       python postar.py
3. O script exporta os slides como PNG e abre o Instagram
─────────────────────────────────────────────────────
Primeira vez apenas:
    pip install playwright pillow
    playwright install chromium
"""

import asyncio
import sys
from pathlib import Path
from playwright.async_api import async_playwright

# ── Configurações ──────────────────────────────────────────────────────────

HTML_FILE = Path("carrossel.html")   # arquivo que você troca a cada carrossel
OUTPUT_DIR = Path("slides_png")
LEGENDA_FILE = Path("legenda.txt")   # opcional: coloque a legenda aqui

# ── Exportar slides ────────────────────────────────────────────────────────

async def exportar_slides() -> list[str]:
    if not HTML_FILE.exists():
        print(f"ERRO: arquivo '{HTML_FILE}' não encontrado nesta pasta.")
        print("Salve o HTML do carrossel como 'carrossel.html' e tente novamente.")
        sys.exit(1)

    OUTPUT_DIR.mkdir(exist_ok=True)

    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page(viewport={"width": 1080, "height": 1350})

        await page.goto(f"file://{HTML_FILE.resolve()}")
        await page.wait_for_timeout(2500)  # aguarda fontes do Google carregarem

        # Encontra todos os elementos .slide na página
        slides = await page.query_selector_all(".slide")

        if not slides:
            print("ERRO: nenhum slide encontrado. Verifique se o HTML usa a classe '.slide'.")
            await browser.close()
            sys.exit(1)

        print(f"  {len(slides)} slides encontrados.")
        slide_files = []

        for i, slide in enumerate(slides, start=1):
            # Garante que o slide esteja visível antes de capturar
            await page.evaluate("(el) => el.style.display = 'block'", slide)
            await page.wait_for_timeout(200)

            path = OUTPUT_DIR / f"slide_{i:02d}.png"

            # Captura o elemento exatamente em 1080x1350
            await slide.screenshot(path=str(path))

            # Valida dimensão mínima (evita capturar elemento vazio)
            from PIL import Image
            img = Image.open(path)
            if img.width < 100:
                print(f"  Aviso: slide {i} parece vazio, pulando.")
                path.unlink()
                continue

            slide_files.append(str(path))
            print(f"  ✓ slide_{i:02d}.png  ({img.width}×{img.height})")

        await browser.close()

    print(f"\nSlides salvos em: {OUTPUT_DIR.resolve()}\n")
    return slide_files


# ── Ler legenda ────────────────────────────────────────────────────────────

def ler_legenda() -> str:
    if LEGENDA_FILE.exists():
        legenda = LEGENDA_FILE.read_text(encoding="utf-8").strip()
        print(f"Legenda carregada de '{LEGENDA_FILE}'.")
        return legenda

    print("Arquivo 'legenda.txt' não encontrado.")
    print("Cole a legenda abaixo e pressione Enter duas vezes quando terminar:\n")
    linhas = []
    while True:
        linha = input()
        if linha == "" and linhas and linhas[-1] == "":
            break
        linhas.append(linha)
    return "\n".join(linhas).strip()


# ── Postar no Instagram ────────────────────────────────────────────────────

async def postar_instagram(slide_files: list[str], legenda: str):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False, slow_mo=200)
        context = await browser.new_context(
            viewport={"width": 1280, "height": 900},
            locale="pt-BR",
        )
        page = await context.new_page()

        # ── Login ──────────────────────────────────────────────────────────
        print("Abrindo Instagram...")
        await page.goto("https://www.instagram.com/accounts/login/")
        await page.wait_for_load_state("networkidle")

        usuario = input("\nUsuário do Instagram: ")
        senha   = input("Senha: ")

        await page.fill('input[name="username"]', usuario)
        await page.fill('input[name="password"]', senha)
        await page.click('button[type="submit"]')

        print("\nFazendo login... aguarde.")
        await page.wait_for_timeout(5000)

        # Verificação de segurança / 2FA
        if "challenge" in page.url or "two_factor" in page.url:
            print("\nInstagram pediu verificação de segurança.")
            input("Complete a verificação no browser e pressione Enter para continuar...")
            await page.wait_for_timeout(2000)

        # Fechar pop-ups "Agora não"
        for _ in range(4):
            for texto in ["Agora não", "Not Now", "Agora não"]:
                try:
                    btn = page.get_by_text(texto, exact=True)
                    if await btn.is_visible(timeout=2000):
                        await btn.click()
                        await page.wait_for_timeout(1000)
                except Exception:
                    pass

        # ── Criar post ─────────────────────────────────────────────────────
        print("\nAbrindo criador de post...")
        await page.goto("https://www.instagram.com/")
        await page.wait_for_load_state("networkidle")
        await page.wait_for_timeout(2000)

        # Botão de nova publicação
        criou = False
        for seletor in [
            '[aria-label="Nova publicação"]',
            '[aria-label="New post"]',
            'svg[aria-label="Nova publicação"]',
        ]:
            try:
                btn = page.locator(seletor).first
                if await btn.is_visible(timeout=3000):
                    await btn.click()
                    criou = True
                    break
            except Exception:
                pass

        if not criou:
            input("\nNão encontrei o botão '+'. Clique nele manualmente e pressione Enter...")

        await page.wait_for_timeout(2000)

        # ── Upload dos arquivos ────────────────────────────────────────────
        print("Fazendo upload dos slides...")
        try:
            file_input = page.locator('input[type="file"]').first
            await file_input.set_input_files(slide_files)
            await page.wait_for_timeout(4000)
        except Exception as e:
            print(f"\nUpload automático falhou: {e}")
            print(f"Faça o upload manualmente dos arquivos em: {OUTPUT_DIR.resolve()}")
            input("Pressione Enter após fazer o upload...")

        # ── Avançar pelas etapas ───────────────────────────────────────────
        print("Avançando etapas...")
        for passo in ["Cortar", "Avançar", "Avançar"]:
            for _ in range(3):
                try:
                    btn = page.get_by_text(passo, exact=True)
                    if await btn.is_visible(timeout=3000):
                        await btn.click()
                        await page.wait_for_timeout(2500)
                        break
                except Exception:
                    pass

        # ── Legenda ────────────────────────────────────────────────────────
        print("Inserindo legenda...")
        colou = False
        for seletor in [
            '[aria-label="Escreva uma legenda..."]',
            '[aria-label="Write a caption..."]',
            'textarea[aria-label]',
        ]:
            try:
                area = page.locator(seletor).first
                if await area.is_visible(timeout=3000):
                    await area.click()
                    await area.fill(legenda)
                    colou = True
                    break
            except Exception:
                pass

        if not colou:
            print("\nNão consegui inserir a legenda automaticamente.")
            print("\n── LEGENDA ──────────────────────────")
            print(legenda)
            print("─────────────────────────────────────")
            input("Cole manualmente e pressione Enter...")

        await page.wait_for_timeout(1000)

        # ── Publicar ───────────────────────────────────────────────────────
        print("Publicando...")
        publicou = False
        for texto in ["Compartilhar", "Share"]:
            try:
                btn = page.get_by_text(texto, exact=True)
                if await btn.is_visible(timeout=5000):
                    await btn.click()
                    publicou = True
                    break
            except Exception:
                pass

        if not publicou:
            input("\nClique em 'Compartilhar' manualmente e pressione Enter...")

        await page.wait_for_timeout(6000)
        print("\n✅ Post publicado!")
        await browser.close()


# ── Main ───────────────────────────────────────────────────────────────────

async def main():
    print("=" * 52)
    print("  BMC — Publicador de Carrossel")
    print("=" * 52)

    print("\n[1/3] Exportando slides...")
    slide_files = await exportar_slides()

    print("[2/3] Preparando legenda...")
    legenda = ler_legenda()

    print("\n[3/3] Postando no Instagram...")
    await postar_instagram(slide_files, legenda)

if __name__ == "__main__":
    asyncio.run(main())
