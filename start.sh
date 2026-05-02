#!/bin/bash
# ============================================================
# MAGIC PROMPT — Be Media Class
# Inicia o servidor (backend + frontend)
# ============================================================

# Verifica se .env existe
if [ ! -f .env ]; then
    echo "❌ Arquivo .env não encontrado. Execute ./setup.sh primeiro."
    exit 1
fi

echo ""
echo "╔══════════════════════════════════════════╗"
echo "║   Magic Prompt — Iniciando...            ║"
echo "╚══════════════════════════════════════════╝"
echo ""

# Inicia o backend em background
echo "🚀 Iniciando backend (porta 8000)..."
cd backend
source .venv/bin/activate
python3 -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload &
BACKEND_PID=$!
cd ..

sleep 2

# Inicia o frontend
echo "🌐 Iniciando frontend (porta 3000)..."
cd frontend
npm run dev &
FRONTEND_PID=$!
cd ..

echo ""
echo "╔══════════════════════════════════════════╗"
echo "║   ✅ Tudo rodando!                       ║"
echo "║                                          ║"
echo "║   Acesse: http://localhost:3000          ║"
echo "║   API docs: http://localhost:8000/docs   ║"
echo "║                                          ║"
echo "║   Para parar: pressione Ctrl+C           ║"
echo "╚══════════════════════════════════════════╝"
echo ""

# Aguarda Ctrl+C e mata os processos
trap "echo ''; echo 'Encerrando...'; kill $BACKEND_PID $FRONTEND_PID 2>/dev/null; exit" INT TERM
wait
