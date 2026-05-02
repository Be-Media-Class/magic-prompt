#!/bin/bash
# ============================================================
# MAGIC PROMPT — Be Media Class
# Script de instalação (rode uma vez só)
# ============================================================

set -e

echo ""
echo "╔══════════════════════════════════════════╗"
echo "║   Magic Prompt — Be Media Class          ║"
echo "║   Instalando dependências...             ║"
echo "╚══════════════════════════════════════════╝"
echo ""

# Verifica Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 não encontrado. Instale em: https://python.org/downloads"
    exit 1
fi

# Verifica Node.js
if ! command -v node &> /dev/null; then
    echo "❌ Node.js não encontrado. Instale em: https://nodejs.org"
    exit 1
fi

echo "✅ Python $(python3 --version) encontrado"
echo "✅ Node $(node --version) encontrado"
echo ""

# Backend
echo "📦 Instalando dependências do backend..."
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install -q -r requirements.txt
playwright install chromium
mkdir -p static/images data
cd ..
echo "✅ Backend pronto!"
echo ""

# Frontend
echo "📦 Instalando dependências do frontend..."
cd frontend
npm install --silent
cd ..
echo "✅ Frontend pronto!"
echo ""

# Cria .env se não existir
if [ ! -f .env ]; then
    cp .env.example .env
    echo "📝 Arquivo .env criado a partir do .env.example"
    echo "   ⚠️  IMPORTANTE: Abra o arquivo .env e preencha suas chaves!"
    echo ""
fi

echo "╔══════════════════════════════════════════╗"
echo "║   ✅ Instalação completa!                ║"
echo "║                                          ║"
echo "║   Próximos passos:                       ║"
echo "║   1. Preencha o arquivo .env             ║"
echo "║   2. Execute: ./start.sh                 ║"
echo "╚══════════════════════════════════════════╝"
echo ""
