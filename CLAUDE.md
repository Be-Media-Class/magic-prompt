# magic-prompt

This project uses a **trimmed subset** of the [Everything Claude Code (ECC)](https://github.com/affaan-m/ECC)
toolkit, installed under `.claude/`. The full `full` profile (67 agents / 280 skills / 94 commands) was
installed first, then cut down to what's actually relevant: general engineering baseline (planning,
review, security, TDD, docs) plus Be Media Class's content/marketing/AI-media focus. No
language-specific stack was kept since this repo has no code yet.

- Agent roster and usage guidance: `.claude/AGENTS.md`
- Rules (coding style, git workflow, testing, security, etc. — common only, no language packs): `.claude/rules/ecc/`
- Skills (26 curated, see `.claude/AGENTS.md` for the list): `.claude/skills/`
- Slash commands: `.claude/commands/`
- Hook definitions (not yet wired into `settings.json` — see `.claude/hooks/README.md` before enabling): `.claude/hooks/hooks.json`
- MCP server templates: `.claude/mcp-configs/`
- To pull back anything trimmed (e.g. once a language/framework is chosen), see "Reinstalling library items" in `.claude/AGENTS.md`.
