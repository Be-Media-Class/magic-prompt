# Magic Prompt — Be Media Class 🚀

**Crie carrosséis profissionais para o Instagram com IA, em minutos.**

> Desenvolvido para @claudiosoares.creator e os alunos da Be Media Class.

---

## Como funciona

```
Você digita o tema  →  IA gera o conteúdo  →  Você aprova  →  Publica no Instagram
```

---

## Instalação (só na primeira vez)

### O que você precisa ter instalado:
- [Python 3.11+](https://python.org/downloads) — linguagem do servidor
- [Node.js 20+](https://nodejs.org) — linguagem do site
- [paper.design Desktop](https://app.paper.design) — criador visual (opcional)

### Passos:

**1. Baixe o projeto**
```bash
git clone https://github.com/be-media-class/magic-prompt
cd magic-prompt
```

**2. Rode o instalador**
```bash
./setup.sh
```

**3. Configure suas chaves** — abra o arquivo `.env` e preencha:

---

## Configuração das Chaves

### 🤖 Claude AI (Anthropic)
1. Acesse [console.anthropic.com](https://console.anthropic.com)
2. Clique em **API Keys** → **Create Key**
3. Copie a chave e cole no `.env`:
   ```
   ANTHROPIC_API_KEY=sk-ant-...
   ```

### 📸 Instagram / Meta

**Passo 1: Criar o App no Meta**
1. Acesse [developers.facebook.com](https://developers.facebook.com)
2. Clique em **Meus Apps** → **Criar App**
3. Escolha tipo: **Empresa**
4. Nome: `Magic Prompt BMC`

**Passo 2: Adicionar o Instagram**
1. No App criado, clique em **Adicionar produto**
2. Encontre **Instagram Graph API** e clique **Configurar**
3. Conecte a conta `claudiosoares.creator`

**Passo 3: Pegar o Access Token**
1. Vá em **Ferramentas** → **Graph API Explorer**
2. Selecione seu App
3. Clique em **Gerar Token de Acesso**
4. Marque as permissões: `instagram_basic`, `instagram_content_publish`
5. Copie o token e cole no `.env`

**Passo 4: Pegar o Instagram User ID**
1. No Graph API Explorer, digite na caixa de busca:
   ```
   me/accounts
   ```
2. Execute e procure o `id` da sua conta Instagram
3. Cole no `.env`

**Passo 5: URL pública (para que o Instagram consiga ver as imagens)**

Para testes locais, use o ngrok:
```bash
# Instale: https://ngrok.com/download
ngrok http 8000
```
Copie a URL que aparecer (ex: `https://abc123.ngrok.io`) e cole no `.env`:
```
PUBLIC_BASE_URL=https://abc123.ngrok.io
```

### 🎨 paper.design (opcional, mas recomendado!)
1. Baixe o [Paper Desktop](https://app.paper.design)
2. Abra qualquer arquivo no Paper
3. O servidor MCP sobe automaticamente — nenhuma configuração necessária!
4. No `.env`, mude para:
   ```
   USE_PAPER_DESIGN=true
   ```

---

## Iniciar o projeto

```bash
./start.sh
```

Acesse: **http://localhost:3000**

---

## O fluxo completo

### 1. Criar carrossel
- Acesse a página inicial
- Clique em **"+ Criar Carrossel"**
- Digite o tema (ex: "5 IAs para criadores de conteúdo")
- Escolha o tom e número de slides
- Clique em **"Gerar carrossel com IA"**

### 2. Revisar e aprovar
- Aguarde ~30-60 segundos enquanto a IA trabalha
- Veja os slides gerados com a identidade visual BMC
- Leia o conteúdo de cada slide
- Clique **"✅ Aprovar"** ou **"❌ Rejeitar e regenerar"**

### 3. Publicar no Instagram
- Após aprovar, clique **"🚀 Publicar no Instagram agora"**
- Pronto! O carrossel vai para o Instagram automaticamente

---

## Identidade Visual BMC

Os carrosséis seguem automaticamente:
- **Cores**: #7543b4 (roxo), #1d1d1d (preto), #123356 (azul), #2ae19e (verde)
- **Fonte**: Raleway (todas as variações)
- **Formato**: 1080×1080px (padrão Instagram)
- **Estrutura**: Capa + N slides de conteúdo + Slide CTA

---

## Para os alunos da BMC

Este projeto foi desenvolvido como exemplo de como usar IA criativa na prática:

| Componente | O que aprende |
|---|---|
| `backend/services/claude_service.py` | Como usar a API do Claude para gerar conteúdo |
| `backend/services/renderer_service.py` | Como converter HTML em imagens com IA |
| `backend/services/meta_service.py` | Como usar a API do Instagram (Meta) |
| `backend/services/paper_service.py` | Como integrar ferramentas via MCP |
| `frontend/app/` | Como construir interfaces modernas |

---

## Problemas comuns

**"Erro ao criar carrossel"**
→ Verifique se o backend está rodando (`./start.sh`) e se a `ANTHROPIC_API_KEY` está correta.

**"Erro ao publicar no Instagram"**
→ Verifique se o ngrok está rodando e a `PUBLIC_BASE_URL` está correta no `.env`.

**paper.design não conecta**
→ Abra o Paper Desktop e garanta que tem um arquivo aberto.

---

*Be Media Class © 2025 · @claudiosoares.creator*
