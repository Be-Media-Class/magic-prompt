"""
INSTRUÇÕES PARA O CLAUDE CODE
==============================
Execute este script no terminal:

    pip install playwright pillow
    playwright install chromium
    python postar_instagram.py

O script vai:
1. Renderizar os 6 slides do carrossel como PNG
2. Abrir o Instagram no browser
3. Fazer login (você digita as credenciais)
4. Criar o post com os 6 imagens + legenda
"""

import asyncio
import os
from pathlib import Path
from playwright.async_api import async_playwright

# ─── LEGENDA ───────────────────────────────────────────────────────────────

LEGENDA = """Você abre o Claude todo dia.

Mas provavelmente usa só uma das três versões.

Claude AI pensa junto com você.
Claude Cowork age dentro dos seus apps.
Claude Code cria sistemas que funcionam sozinhos.

São três ferramentas com funções completamente diferentes — e a maioria das pessoas nunca ativou as outras duas.

Mande GUIA nos comentários e eu te mando o guia com as melhores IAs do mundo agora."""

# ─── HTML DO CARROSSEL ─────────────────────────────────────────────────────

HTML = r"""
<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<style>
@import url('https://fonts.googleapis.com/css2?family=Raleway:wght@400;700;900&display=swap');
* { margin: 0; padding: 0; box-sizing: border-box; }
body { font-family: 'Raleway', sans-serif; }
.slide {
  width: 1080px;
  height: 1350px;
  position: relative;
  overflow: hidden;
  font-family: 'Raleway', sans-serif;
}

/* ── SLIDE 1 ── */
.s1 { background: #1d1d1d; }
.s1 .stripe { position:absolute;top:0;left:0;right:0;height:8px;background:#2ae19e; }
.s1 .eyebrow { position:absolute;top:64px;left:80px;font-size:18px;font-weight:700;letter-spacing:6px;text-transform:uppercase;color:rgba(255,255,255,0.3); }
.s1 .headline { position:absolute;top:130px;left:80px;right:80px; }
.s1 .h-line { font-size:118px;font-weight:900;text-transform:uppercase;line-height:0.88;color:#fff; }
.s1 .h-line.accent { color:#2ae19e; }
.s1 .rule { width:64px;height:6px;background:#7543b4;margin:56px 0 40px; }
.s1 .sub { font-size:34px;font-weight:400;color:rgba(255,255,255,0.55);line-height:1.45;max-width:780px; }
.s1 .pills { position:absolute;bottom:140px;left:80px;display:flex;gap:20px; }
.s1 .pill { font-size:22px;font-weight:900;letter-spacing:2px;text-transform:uppercase;padding:16px 36px;border-radius:6px; }
.s1 .pill-ai   { background:rgba(117,67,180,0.25);color:#b08ce8;border:2px solid rgba(117,67,180,0.5); }
.s1 .pill-cw   { background:rgba(91,159,212,0.15);color:#5b9fd4;border:2px solid rgba(91,159,212,0.4); }
.s1 .pill-code { background:rgba(42,225,158,0.12);color:#2ae19e;border:2px solid rgba(42,225,158,0.35); }
.s1 .footer { position:absolute;bottom:60px;left:80px;right:80px;display:flex;justify-content:space-between;align-items:center; }
.s1 .swipe { font-size:18px;letter-spacing:4px;text-transform:uppercase;color:rgba(255,255,255,0.2);display:flex;align-items:center;gap:16px; }
.s1 .swipe::after { content:'';width:40px;height:2px;background:rgba(255,255,255,0.2); }
.s1 .bmc { font-size:18px;font-weight:900;letter-spacing:4px;color:#2ae19e;opacity:0.5; }

/* ── SLIDE 2 ── */
.s2 { background:#1d1d1d; }
.s2 .top-bar { position:absolute;top:0;left:0;right:0;height:8px;background:#7543b4; }
.s2 .num { position:absolute;top:60px;right:80px;font-size:200px;font-weight:900;color:rgba(117,67,180,0.06);line-height:1; }
.s2 .badge { position:absolute;top:68px;left:80px;background:#7543b4;color:#fff;font-size:18px;font-weight:700;letter-spacing:4px;text-transform:uppercase;padding:10px 24px;border-radius:4px; }
.s2 .name { position:absolute;top:150px;left:80px; }
.s2 .n1 { font-size:96px;font-weight:900;text-transform:uppercase;color:#fff;line-height:0.9; }
.s2 .n2 { font-size:96px;font-weight:900;text-transform:uppercase;color:#7543b4;line-height:0.9; }
.s2 .tagline { position:absolute;top:390px;left:80px;right:80px;font-size:36px;font-weight:400;color:rgba(255,255,255,0.45);line-height:1.4;font-style:italic;border-left:4px solid #7543b4;padding-left:32px; }
.s2 .section-title { position:absolute;top:590px;left:80px;font-size:18px;font-weight:700;letter-spacing:5px;text-transform:uppercase;color:#7543b4; }
.s2 .def { position:absolute;top:640px;left:80px;right:80px;font-size:46px;font-weight:700;color:#fff;line-height:1.2; }
.s2 .items { position:absolute;top:870px;left:80px;right:80px;display:flex;flex-direction:column;gap:28px; }
.s2 .item { display:flex;align-items:flex-start;gap:24px; }
.s2 .dot { width:10px;height:10px;border-radius:50%;background:#7543b4;flex-shrink:0;margin-top:14px; }
.s2 .item-text { font-size:34px;font-weight:400;color:rgba(255,255,255,0.65);line-height:1.3; }
.s2 .footer { position:absolute;bottom:60px;left:80px;right:80px;display:flex;justify-content:space-between; }
.s2 .pg { font-size:18px;color:rgba(255,255,255,0.15);font-weight:700;letter-spacing:2px; }
.s2 .bmc { font-size:18px;font-weight:900;letter-spacing:4px;color:#2ae19e;opacity:0.5; }

/* ── SLIDE 3 ── */
.s3 { background:#1d1d1d; }
.s3 .top-bar { position:absolute;top:0;left:0;right:0;height:8px;background:#5b9fd4; }
.s3 .num { position:absolute;top:60px;right:80px;font-size:200px;font-weight:900;color:rgba(91,159,212,0.05);line-height:1; }
.s3 .badge { position:absolute;top:68px;left:80px;background:rgba(91,159,212,0.15);color:#5b9fd4;font-size:18px;font-weight:700;letter-spacing:4px;text-transform:uppercase;padding:10px 24px;border-radius:4px;border:2px solid rgba(91,159,212,0.4); }
.s3 .name { position:absolute;top:150px;left:80px; }
.s3 .n1 { font-size:96px;font-weight:900;text-transform:uppercase;color:#fff;line-height:0.9; }
.s3 .n2 { font-size:96px;font-weight:900;text-transform:uppercase;color:#5b9fd4;line-height:0.9; }
.s3 .tagline { position:absolute;top:390px;left:80px;right:80px;font-size:36px;font-weight:400;color:rgba(255,255,255,0.45);line-height:1.4;font-style:italic;border-left:4px solid #5b9fd4;padding-left:32px; }
.s3 .section-title { position:absolute;top:590px;left:80px;font-size:18px;font-weight:700;letter-spacing:5px;text-transform:uppercase;color:#5b9fd4; }
.s3 .def { position:absolute;top:640px;left:80px;right:80px;font-size:46px;font-weight:700;color:#fff;line-height:1.2; }
.s3 .chips-label { position:absolute;top:890px;left:80px;font-size:18px;font-weight:700;letter-spacing:5px;text-transform:uppercase;color:rgba(255,255,255,0.25); }
.s3 .chips { position:absolute;top:940px;left:80px;right:80px;display:flex;flex-wrap:wrap;gap:16px; }
.s3 .chip { background:rgba(91,159,212,0.12);border:2px solid rgba(91,159,212,0.3);color:#5b9fd4;font-size:26px;font-weight:700;padding:14px 28px;border-radius:6px; }
.s3 .footer { position:absolute;bottom:60px;left:80px;right:80px;display:flex;justify-content:space-between; }
.s3 .pg { font-size:18px;color:rgba(255,255,255,0.15);font-weight:700;letter-spacing:2px; }
.s3 .bmc { font-size:18px;font-weight:900;letter-spacing:4px;color:#2ae19e;opacity:0.5; }

/* ── SLIDE 4 ── */
.s4 { background:#1d1d1d; }
.s4 .top-bar { position:absolute;top:0;left:0;right:0;height:8px;background:#2ae19e; }
.s4 .num { position:absolute;top:60px;right:80px;font-size:200px;font-weight:900;color:rgba(42,225,158,0.04);line-height:1; }
.s4 .badge { position:absolute;top:68px;left:80px;background:rgba(42,225,158,0.1);color:#2ae19e;font-size:18px;font-weight:700;letter-spacing:4px;text-transform:uppercase;padding:10px 24px;border-radius:4px;border:2px solid rgba(42,225,158,0.3); }
.s4 .name { position:absolute;top:150px;left:80px; }
.s4 .n1 { font-size:96px;font-weight:900;text-transform:uppercase;color:#fff;line-height:0.9; }
.s4 .n2 { font-size:96px;font-weight:900;text-transform:uppercase;color:#2ae19e;line-height:0.9; }
.s4 .tagline { position:absolute;top:390px;left:80px;right:80px;font-size:36px;font-weight:400;color:rgba(255,255,255,0.45);line-height:1.4;font-style:italic;border-left:4px solid #2ae19e;padding-left:32px; }
.s4 .section-title { position:absolute;top:590px;left:80px;font-size:18px;font-weight:700;letter-spacing:5px;text-transform:uppercase;color:#2ae19e; }
.s4 .def { position:absolute;top:640px;left:80px;right:80px;font-size:46px;font-weight:700;color:#fff;line-height:1.2; }
.s4 .code-box { position:absolute;top:880px;left:80px;right:80px;background:#111;border:2px solid rgba(42,225,158,0.2);border-left:6px solid #2ae19e;padding:36px 40px;border-radius:8px; }
.s4 .code-line { font-family:'Courier New',monospace;font-size:28px;line-height:1.9; }
.s4 .c-dim { color:rgba(255,255,255,0.2); }
.s4 .c-kw { color:#b08ce8; }
.s4 .c-fn { color:#2ae19e; }
.s4 .c-punc { color:rgba(255,255,255,0.4); }
.s4 .footer { position:absolute;bottom:60px;left:80px;right:80px;display:flex;justify-content:space-between; }
.s4 .pg { font-size:18px;color:rgba(255,255,255,0.15);font-weight:700;letter-spacing:2px; }
.s4 .bmc { font-size:18px;font-weight:900;letter-spacing:4px;color:#2ae19e;opacity:0.5; }

/* ── SLIDE 5 ── */
.s5 { background:#1d1d1d; }
.s5 .top-bar { position:absolute;top:0;left:0;right:0;height:8px;background:linear-gradient(90deg,#7543b4 0% 33%,#5b9fd4 33% 66%,#2ae19e 66% 100%); }
.s5 .eyebrow { position:absolute;top:64px;left:80px;font-size:18px;font-weight:700;letter-spacing:5px;text-transform:uppercase;color:rgba(255,255,255,0.3); }
.s5 .headline { position:absolute;top:116px;left:80px;right:80px;font-size:86px;font-weight:900;text-transform:uppercase;color:#fff;line-height:0.92; }
.s5 .headline span { color:#2ae19e; }
.s5 .tbl { position:absolute;top:400px;left:80px;right:80px; }
.s5 .trow { display:grid;grid-template-columns:320px 1fr 1fr 1fr;gap:8px;margin-bottom:8px; }
.s5 .th { font-size:22px;font-weight:900;letter-spacing:2px;text-transform:uppercase;padding:18px 0;text-align:center;border-radius:6px; }
.s5 .th-empty { background:transparent; }
.s5 .th-ai { background:rgba(117,67,180,0.2);color:#b08ce8; }
.s5 .th-cw { background:rgba(91,159,212,0.15);color:#5b9fd4; }
.s5 .th-code { background:rgba(42,225,158,0.1);color:#2ae19e; }
.s5 .td { font-size:22px;padding:22px 16px;border-radius:6px;text-align:center;display:flex;align-items:center;justify-content:center; }
.s5 .td-label { font-size:22px;font-weight:700;color:rgba(255,255,255,0.4);text-align:left;justify-content:flex-start;background:rgba(255,255,255,0.03);padding:22px 20px;letter-spacing:1px;text-transform:uppercase;border-radius:6px; }
.s5 .td-yes { background:rgba(42,225,158,0.1);color:#2ae19e;font-size:34px;font-weight:900; }
.s5 .td-no { background:rgba(255,255,255,0.03);color:rgba(255,255,255,0.15);font-size:30px; }
.s5 .td-partial { background:rgba(255,200,0,0.07);color:rgba(255,200,0,0.6);font-size:18px;font-weight:700; }
.s5 .insight { position:absolute;bottom:120px;left:80px;right:80px;background:rgba(42,225,158,0.07);border:2px solid rgba(42,225,158,0.18);border-left:6px solid #2ae19e;padding:28px 32px;border-radius:8px;font-size:28px;font-weight:400;color:rgba(255,255,255,0.6);line-height:1.5; }
.s5 .insight strong { color:#fff;font-weight:700; }
.s5 .footer { position:absolute;bottom:60px;left:80px;right:80px;display:flex;justify-content:space-between; }
.s5 .pg { font-size:18px;color:rgba(255,255,255,0.15);font-weight:700;letter-spacing:2px; }
.s5 .bmc { font-size:18px;font-weight:900;letter-spacing:4px;color:#2ae19e;opacity:0.5; }

/* ── SLIDE 6 ── */
.s6 { background:#1d1d1d; }
.s6 .top-bar { position:absolute;top:0;left:0;right:0;height:8px;background:#2ae19e; }
.s6 .eyebrow { position:absolute;top:64px;left:80px;font-size:18px;font-weight:700;letter-spacing:6px;text-transform:uppercase;color:#2ae19e; }
.s6 .question { position:absolute;top:130px;left:80px;right:80px;font-size:100px;font-weight:900;text-transform:uppercase;color:#fff;line-height:0.9; }
.s6 .question .hl { color:#2ae19e; }
.s6 .body { position:absolute;top:550px;left:80px;right:80px;font-size:38px;font-weight:400;color:rgba(255,255,255,0.5);line-height:1.5; }
.s6 .ctas { position:absolute;top:820px;left:80px;right:80px;display:flex;flex-direction:column;gap:24px; }
.s6 .cta-item { display:flex;align-items:center;gap:24px;background:rgba(255,255,255,0.04);border:2px solid rgba(255,255,255,0.08);padding:28px 32px;border-radius:8px; }
.s6 .cta-dot { width:12px;height:12px;border-radius:50%;background:#2ae19e;flex-shrink:0; }
.s6 .cta-text { font-size:32px;font-weight:700;color:#fff;line-height:1.3; }
.s6 .cta-text strong { color:#2ae19e; }
.s6 .bar-footer { position:absolute;bottom:0;left:0;right:0;height:100px;background:#111;display:flex;align-items:center;justify-content:space-between;padding:0 80px;border-top:2px solid rgba(255,255,255,0.06); }
.s6 .brand { font-size:20px;font-weight:900;letter-spacing:4px;color:#2ae19e;text-transform:uppercase;opacity:0.7; }
.s6 .handle { font-size:20px;font-weight:400;color:rgba(255,255,255,0.25); }
</style>
</head>
<body>

<div id="slide-1" class="slide s1">
  <div class="s1 stripe"></div>
  <div class="s1 eyebrow">Guia prático</div>
  <div class="s1 headline">
    <div class="s1 h-line">Você</div>
    <div class="s1 h-line">usa só</div>
    <div class="s1 h-line accent">1 dos 3.</div>
    <div class="s1 rule"></div>
    <div class="s1 sub">Claude tem três versões com funções completamente diferentes. A maioria dos alunos nunca ativou as outras duas.</div>
  </div>
  <div class="s1 pills">
    <div class="s1 pill pill-ai">AI</div>
    <div class="s1 pill pill-cw">Cowork</div>
    <div class="s1 pill pill-code">Code</div>
  </div>
  <div class="s1 footer">
    <div class="s1 swipe">arraste</div>
    <div class="s1 bmc">BMC</div>
  </div>
</div>

<div id="slide-2" class="slide s2" style="display:none">
  <div class="s2 top-bar"></div>
  <div class="s2 num">01</div>
  <div class="s2 badge">Produto 01</div>
  <div class="s2 name">
    <div class="s2 n1">Claude</div>
    <div class="s2 n2">AI</div>
  </div>
  <div class="s2 tagline">"O Claude que você abre pra pensar. Não executa. Raciocina junto."</div>
  <div class="s2 section-title">Para que serve</div>
  <div class="s2 def">Pensar, escrever, estruturar e validar qualquer ideia antes de agir.</div>
  <div class="s2 items">
    <div class="s2 item"><div class="s2 dot"></div><div class="s2 item-text">Criar textos com contexto real do seu negócio</div></div>
    <div class="s2 item"><div class="s2 dot"></div><div class="s2 item-text">Revisar estratégias e antecipar erros</div></div>
    <div class="s2 item"><div class="s2 dot"></div><div class="s2 item-text">Organizar ideias antes de executar</div></div>
  </div>
  <div class="s2 footer"><span class="s2 pg">2 / 6</span><span class="s2 bmc">BMC</span></div>
</div>

<div id="slide-3" class="slide s3" style="display:none">
  <div class="s3 top-bar"></div>
  <div class="s3 num">02</div>
  <div class="s3 badge">Produto 02</div>
  <div class="s3 name">
    <div class="s3 n1">Claude</div>
    <div class="s3 n2">Cowork</div>
  </div>
  <div class="s3 tagline">"O Claude que age dentro dos seus apps. Ele não responde. Executa."</div>
  <div class="s3 section-title">Para que serve</div>
  <div class="s3 def">Realizar tarefas reais dentro de ferramentas que você já usa todo dia.</div>
  <div class="s3 chips-label">Conecta com</div>
  <div class="s3 chips">
    <div class="s3 chip">Drive</div>
    <div class="s3 chip">Gmail</div>
    <div class="s3 chip">Calendar</div>
    <div class="s3 chip">Planilhas</div>
    <div class="s3 chip">PDFs</div>
  </div>
  <div class="s3 footer"><span class="s3 pg">3 / 6</span><span class="s3 bmc">BMC</span></div>
</div>

<div id="slide-4" class="slide s4" style="display:none">
  <div class="s4 top-bar"></div>
  <div class="s4 num">03</div>
  <div class="s4 badge">Produto 03</div>
  <div class="s4 name">
    <div class="s4 n1">Claude</div>
    <div class="s4 n2">Code</div>
  </div>
  <div class="s4 tagline">"O Claude dentro do seu computador. Cria coisas que funcionam sozinhas."</div>
  <div class="s4 section-title">Para que serve</div>
  <div class="s4 def">Construir automações, scripts e sistemas que trabalham enquanto você dorme.</div>
  <div class="s4 code-box">
    <div class="s4 code-line"><span class="s4 c-dim">// o que o Code entrega:</span></div>
    <div class="s4 code-line"><span class="s4 c-kw">const</span> <span class="s4 c-fn">resultado</span> <span class="s4 c-punc">= {</span></div>
    <div class="s4 code-line">&nbsp;&nbsp;<span class="s4 c-fn">automatizar</span><span class="s4 c-punc">(),</span></div>
    <div class="s4 code-line">&nbsp;&nbsp;<span class="s4 c-fn">integrar</span><span class="s4 c-punc">(),</span></div>
    <div class="s4 code-line">&nbsp;&nbsp;<span class="s4 c-fn">entregar</span><span class="s4 c-punc">()</span></div>
    <div class="s4 code-line"><span class="s4 c-punc">}</span></div>
  </div>
  <div class="s4 footer"><span class="s4 pg">4 / 6</span><span class="s4 bmc">BMC</span></div>
</div>

<div id="slide-5" class="slide s5" style="display:none">
  <div class="s5 top-bar"></div>
  <div class="s5 eyebrow">Resumo visual</div>
  <div class="s5 headline">Qual usar<br>em cada<br><span>situação?</span></div>
  <div class="s5 tbl">
    <div class="s5 trow">
      <div class="s5 th th-empty"></div>
      <div class="s5 th th-ai">AI</div>
      <div class="s5 th th-cw">Cowork</div>
      <div class="s5 th th-code">Code</div>
    </div>
    <div class="s5 trow">
      <div class="s5 td td-label">Conversar</div>
      <div class="s5 td td-yes">✓</div><div class="s5 td td-no">—</div><div class="s5 td td-no">—</div>
    </div>
    <div class="s5 trow">
      <div class="s5 td td-label">Agir nos apps</div>
      <div class="s5 td td-no">—</div><div class="s5 td td-yes">✓</div><div class="s5 td td-no">—</div>
    </div>
    <div class="s5 trow">
      <div class="s5 td td-label">Criar sistemas</div>
      <div class="s5 td td-no">—</div><div class="s5 td td-no">—</div><div class="s5 td td-yes">✓</div>
    </div>
    <div class="s5 trow">
      <div class="s5 td td-label">Sem instalar</div>
      <div class="s5 td td-yes">✓</div><div class="s5 td td-partial">Parcial</div><div class="s5 td td-no">—</div>
    </div>
    <div class="s5 trow">
      <div class="s5 td td-label">Pra iniciante</div>
      <div class="s5 td td-yes">✓</div><div class="s5 td td-yes">✓</div><div class="s5 td td-partial">Com guia</div>
    </div>
  </div>
  <div class="s5 insight"><strong>Regra prática:</strong> comece pelo AI. Quando precisar de ação real, ative o Cowork. Quando quiser automatizar, entre no Code.</div>
  <div class="s5 footer"><span class="s5 pg">5 / 6</span><span class="s5 bmc">BMC</span></div>
</div>

<div id="slide-6" class="slide s6" style="display:none">
  <div class="s6 top-bar"></div>
  <div class="s6 eyebrow">Próximo passo</div>
  <div class="s6 question">Qual<br>você<br>ainda<br>não<br><span class="hl">ativou?</span></div>
  <div class="s6 body">O poder real aparece quando os três trabalham juntos. Mas tudo começa com saber qual usar agora.</div>
  <div class="s6 ctas">
    <div class="s6 cta-item">
      <div class="s6 cta-dot"></div>
      <div class="s6 cta-text">Mande <strong>GUIA</strong> nos comentários para pegar as melhores IAs do mundo agora.</div>
    </div>
  </div>
  <div class="s6 bar-footer">
    <span class="s6 brand">Be Media Class</span>
    <span class="s6 handle">@claudiosoares.creator</span>
  </div>
</div>

</body>
</html>
"""

# ─── EXPORTAR SLIDES COMO PNG ──────────────────────────────────────────────

async def exportar_slides():
    output_dir = Path("slides_png")
    output_dir.mkdir(exist_ok=True)

    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page(viewport={"width": 1080, "height": 1350})

        html_path = Path("_slides_temp.html")
        html_path.write_text(HTML, encoding="utf-8")

        await page.goto(f"file://{html_path.resolve()}")
        await page.wait_for_timeout(2000)  # aguarda fontes carregarem

        slide_files = []
        for i in range(1, 7):
            for j in range(1, 7):
                display = "block" if j == i else "none"
                await page.evaluate(f"""
                    document.getElementById('slide-{j}').style.display = '{display}';
                """)
            await page.wait_for_timeout(300)

            path = output_dir / f"slide_{i:02d}.png"
            await page.screenshot(path=str(path), clip={"x": 0, "y": 0, "width": 1080, "height": 1350})
            slide_files.append(str(path))
            print(f"✓ slide_{i:02d}.png exportado")

        await browser.close()
        html_path.unlink()
        print(f"\n6 slides salvos em: {output_dir.resolve()}")
        return slide_files

# ─── POSTAR NO INSTAGRAM ───────────────────────────────────────────────────

async def postar_instagram(slide_files: list[str]):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context()
        page = await context.new_page()

        print("\n🌐 Abrindo Instagram...")
        await page.goto("https://www.instagram.com/")
        await page.wait_for_timeout(3000)

        print("🔐 Fazendo login...")
        try:
            await page.fill('input[name="username"]', input("Digite seu usuário do Instagram: "))
            await page.fill('input[name="password"]', input("Digite sua senha: "))
            await page.click('button[type="submit"]')
            await page.wait_for_timeout(5000)
        except Exception as e:
            print(f"Erro no login: {e}")
            input("Faça o login manualmente e pressione Enter para continuar...")

        # Fechar popups
        for _ in range(3):
            try:
                not_now = page.get_by_text("Agora não")
                if await not_now.is_visible():
                    await not_now.click()
                    await page.wait_for_timeout(1000)
            except Exception:
                pass

        print("📸 Iniciando criação do post...")
        await page.wait_for_timeout(2000)

        try:
            await page.click('svg[aria-label="Nova publicação"]')
        except Exception:
            try:
                await page.click('[aria-label="Nova publicação"]')
            except Exception:
                input("Clique no botão '+' para criar post e pressione Enter para continuar...")

        await page.wait_for_timeout(2000)

        print("📤 Fazendo upload dos slides...")
        try:
            file_input = page.locator('input[type="file"]')
            await file_input.set_input_files(slide_files)
            await page.wait_for_timeout(4000)
        except Exception as e:
            print(f"Upload automático falhou: {e}")
            print("Faça o upload manualmente dos arquivos em:", Path("slides_png").resolve())
            input("Pressione Enter após fazer o upload...")

        print("➡️  Avançando etapas...")
        for step in ["Cortar", "Avançar", "Avançar"]:
            try:
                btn = page.get_by_text(step)
                if await btn.is_visible():
                    await btn.click()
                    await page.wait_for_timeout(2000)
            except Exception:
                pass

        print("✍️  Inserindo legenda...")
        try:
            caption_area = page.locator('[aria-label="Escreva uma legenda..."]')
            await caption_area.click()
            await caption_area.fill(LEGENDA)
            await page.wait_for_timeout(1000)
        except Exception as e:
            print(f"Legenda manual necessária: {e}")
            print("\n── LEGENDA ──")
            print(LEGENDA)
            print("────────────")
            input("Cole a legenda manualmente e pressione Enter...")

        print("🚀 Publicando...")
        try:
            share_btn = page.get_by_text("Compartilhar")
            await share_btn.click()
            await page.wait_for_timeout(5000)
            print("✅ Post publicado com sucesso!")
        except Exception as e:
            print(f"Clique em Compartilhar manualmente. Erro: {e}")
            input("Pressione Enter após publicar...")

        await browser.close()

# ─── MAIN ──────────────────────────────────────────────────────────────────

async def main():
    print("=" * 50)
    print("  BMC — Carrossel Instagram")
    print("  Claude AI x Cowork x Code")
    print("=" * 50)

    print("\n[1/2] Exportando slides como PNG...")
    slide_files = await exportar_slides()

    print("\n[2/2] Postando no Instagram...")
    await postar_instagram(slide_files)

if __name__ == "__main__":
    asyncio.run(main())
