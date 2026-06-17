# Be Media Class — magic-prompt

Repositorio de skills e prompts da Be Media Class para uso com Claude Code.

## Contexto da marca

**Be Media Class** e uma plataforma de educacao em marketing digital, social media e criacao de conteudo. Seu publico e formado por criadores, profissionais de comunicacao e pequenos negocios que querem dominar ferramentas digitais sem depender de agencias.

Tom de voz: direto, pratico, sem hype. Prefere "na pratica" a "revolucionario". Ensina por exemplos reais.

## Skill instalada: Gerador de Carrosseis

Localizada em `.claude/skills/gerador-carrosseis-claude/`.

### Como ativar

Quando o usuario pedir para criar um carrossel, configurar a marca, gerar roteiro de slides, legenda ou direcao visual para Instagram, leia `.claude/skills/gerador-carrosseis-claude/SKILL.md` e siga as instrucoes ali descritas.

Prompt de ativacao rapida:
> Configure meu gerador de carrosseis. Sou leigo e quero fazer tudo por conversa.

### Arquivos da skill

| Arquivo | Funcao |
|---|---|
| `SKILL.md` | Instrucoes completas do gerador |
| `references/perfil-marca-template.md` | Template para configurar a marca |
| `references/checklist-revisao.md` | Checklist obrigatorio antes de aprovar |
| `assets/conteudo-carrossel-template.json` | Template JSON de conteudo |
| `assets/template-carrossel-html.html` | Template HTML para preview visual |

### Regra de uso

- Sempre leia o perfil de marca configurado antes de criar um carrossel.
- Se nao existir perfil, inicie o Modo 1 (configurar marca) antes do Modo 2 (criar carrossel).
- Execute o checklist de revisao antes de considerar qualquer carrossel pronto.
- Nao publique sem autorizacao explicita do usuario.
