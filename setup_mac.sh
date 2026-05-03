#!/bin/bash
# Setup BMC — roda uma vez só

set -e

echo ""
echo "════════════════════════════════════"
echo "  BMC — Setup (Mac)"
echo "════════════════════════════════════"
echo ""

# ── Python ────────────────────────────────────────────────────────────────
if ! command -v python3 &>/dev/null; then
  echo "Python não encontrado. Instalando via Homebrew..."
  if ! command -v brew &>/dev/null; then
    echo "Instalando Homebrew primeiro..."
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
  fi
  brew install python
fi

echo "✓ Python $(python3 --version)"

# ── pip ───────────────────────────────────────────────────────────────────
python3 -m pip install --upgrade pip --quiet

# ── Dependências ──────────────────────────────────────────────────────────
echo "Instalando dependências..."
python3 -m pip install playwright pillow --quiet
echo "✓ playwright e pillow instalados"

# ── Chromium ──────────────────────────────────────────────────────────────
echo "Instalando Chromium (pode demorar 1-2 min)..."
python3 -m playwright install chromium
echo "✓ Chromium instalado"

# ── Concluído ─────────────────────────────────────────────────────────────
echo ""
echo "════════════════════════════════════"
echo "  Setup concluído!"
echo ""
echo "  Para postar um carrossel:"
echo "  1. Salve o HTML como carrossel.html aqui"
echo "  2. Edite legenda.txt com a legenda"
echo "  3. python3 postar.py"
echo "════════════════════════════════════"
echo ""
