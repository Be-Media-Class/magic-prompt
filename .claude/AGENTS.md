# Everything Claude Code (ECC) — Agent Instructions

This project installs a **trimmed subset** of the ECC toolkit (originally 67 agents, 280 skills, 94
commands from the `full` profile), curated for Be Media Class's magic-prompt project: general
engineering baseline (planning, review, security, TDD, docs) plus BMC's content/marketing/AI-media
focus. No language-specific stack was installed since this repo has no code yet — see
"Reinstalling library items" below.

**Version:** 2.1.0 (trimmed)

## Core Principles

1. **Agent-First** — Delegate to specialized agents for domain tasks
2. **Test-Driven** — Write tests before implementation, 80%+ coverage required
3. **Security-First** — Never compromise on security; validate all inputs
4. **Immutability** — Always create new objects, never mutate existing ones
5. **Plan Before Execute** — Plan complex features before writing code

## Available Agents

| Agent | Purpose | When to Use |
|-------|---------|-------------|
| planner | Implementation planning | Complex features, refactoring |
| architect | System design and scalability | Architectural decisions |
| tdd-guide | Test-driven development | New features, bug fixes |
| code-reviewer | Code quality and maintainability | After writing/modifying code |
| security-reviewer | Vulnerability detection | Before commits, sensitive code |
| refactor-cleaner | Dead code cleanup | Code maintenance |
| doc-updater | Documentation and codemaps | Updating docs |
| performance-optimizer | Bottleneck/perf analysis | Slow code, bundle size, runtime perf |
| silent-failure-hunter | Swallowed errors, bad fallbacks | Reviewing error handling |
| marketing-agent | Campaign planning, copy, positioning | BMC content/marketing work |
| seo-specialist | Technical SEO, structured data, Core Web Vitals | Site/content SEO |

No language-specific reviewer/build-resolver agents (TypeScript, Python, Go, Rust, Java, etc.) are
installed — none matched actual code in this repo. Reinstall the one you need once the stack is
chosen (see bottom of this file).

## Agent Orchestration

Use agents proactively without user prompt:
- Complex feature requests → **planner**
- Code just written/modified → **code-reviewer**
- Bug fix or new feature → **tdd-guide**
- Architectural decision → **architect**
- Security-sensitive code → **security-reviewer**

Use parallel execution for independent operations — launch multiple agents simultaneously.

## Security Guidelines

**Before ANY commit:**
- No hardcoded secrets (API keys, passwords, tokens)
- All user inputs validated
- SQL injection prevention (parameterized queries)
- XSS prevention (sanitized HTML)
- CSRF protection enabled
- Authentication/authorization verified
- Rate limiting on all endpoints
- Error messages don't leak sensitive data

**Secret management:** NEVER hardcode secrets. Use environment variables or a secret manager. Validate required secrets at startup. Rotate any exposed secrets immediately.

**If security issue found:** STOP → use security-reviewer agent → fix CRITICAL issues → rotate exposed secrets → review codebase for similar issues.

## Coding Style

**Immutability (CRITICAL):** Always create new objects, never mutate. Return new copies with changes applied.

**File organization:** Many small files over few large ones. 200-400 lines typical, 800 max. Organize by feature/domain, not by type. High cohesion, low coupling.

**Error handling:** Handle errors at every level. Provide user-friendly messages in UI code. Log detailed context server-side. Never silently swallow errors.

**Input validation:** Validate all user input at system boundaries. Use schema-based validation. Fail fast with clear messages. Never trust external data.

**Code quality checklist:**
- Functions small (<50 lines), files focused (<800 lines)
- No deep nesting (>4 levels)
- Proper error handling, no hardcoded values
- Readable, well-named identifiers

## Testing Requirements

**Minimum coverage: 80%**

Test types (all required):
1. **Unit tests** — Individual functions, utilities, components
2. **Integration tests** — API endpoints, database operations
3. **E2E tests** — Critical user flows

**TDD workflow (mandatory):**
1. Write test first (RED) — test should FAIL
2. Write minimal implementation (GREEN) — test should PASS
3. Refactor (IMPROVE) — verify coverage 80%+

Troubleshoot failures: check test isolation → verify mocks → fix implementation (not tests, unless tests are wrong).

## Development Workflow

1. **Plan** — Use planner agent, identify dependencies and risks, break into phases
2. **TDD** — Use tdd-guide agent, write tests first, implement, refactor
3. **Review** — Use code-reviewer agent immediately, address CRITICAL/HIGH issues
4. **Capture knowledge in the right place**
   - Personal debugging notes, preferences, and temporary context → auto memory
   - Team/project knowledge (architecture decisions, API changes, runbooks) → the project's existing docs structure
   - If the current task already produces the relevant docs or code comments, do not duplicate the same information elsewhere
   - If there is no obvious project doc location, ask before creating a new top-level file
5. **Commit** — Conventional commits format, comprehensive PR summaries

## Workflow Surface Policy

- `skills/` is the canonical workflow surface.
- New workflow contributions should land in `skills/` first.
- `commands/` is a legacy slash-entry compatibility surface and should only be added or updated when a shim is still required for migration or cross-harness parity.

## Git Workflow

**Commit format:** `<type>: <description>` — Types: feat, fix, refactor, docs, test, chore, perf, ci

**PR workflow:** Analyze full commit history → draft comprehensive summary → include test plan → push with `-u` flag.

## Architecture Patterns

**API response format:** Consistent envelope with success indicator, data payload, error message, and pagination metadata.

**Repository pattern:** Encapsulate data access behind standard interface (findAll, findById, create, update, delete). Business logic depends on abstract interface, not storage mechanism.

**Skeleton projects:** Search for battle-tested templates, evaluate with parallel agents (security, extensibility, relevance), clone best match, iterate within proven structure.

## Performance

**Context management:** Avoid last 20% of context window for large refactoring and multi-file features. Lower-sensitivity tasks (single edits, docs, simple fixes) tolerate higher utilization.

**Build troubleshooting:** once a language-specific build-resolver is reinstalled, use it → analyze errors → fix incrementally → verify after each fix.

## Project Structure (trimmed install)

```
agents/          — 11 stack-agnostic + BMC-relevant subagents (of 67 upstream)
skills/          — 26 curated skills (of 280 upstream)
commands/        — 25 slash commands (of 94 upstream)
hooks/           — Trigger-based automations (installed, not wired into settings.json)
rules/           — common/ only — no language-specific rule packs installed
scripts/         — Cross-platform Node.js utilities (hook implementations)
mcp-configs/     — MCP server configuration templates
```

`commands/` remains in the repo for compatibility, but the long-term direction is skills-first.

## Reinstalling library items

Everything not installed here still exists upstream in [affaan-m/ECC](https://github.com/affaan-m/ECC)
and is one command away. Once magic-prompt's stack is decided, pull in the matching pieces, e.g.:

```bash
git clone https://github.com/affaan-m/ECC.git /tmp/ecc-src && cd /tmp/ecc-src && npm install
# Rules + reviewer/build-resolver agent for one language:
node scripts/install-apply.js --target claude-project --modules framework-language --with typescript
# A single skill by id:
node scripts/install-apply.js --target claude-project --skills react-patterns
```

Run from the magic-prompt repo root (or pass an absolute path to the script) so files land in
`./.claude/`. See `.claude/rules/ecc/README.md` and `node scripts/install-apply.js --help` in the
ECC checkout for the full module/skill catalog.

## Success Metrics

- All tests pass with 80%+ coverage
- No security vulnerabilities
- Code is readable and maintainable
- Performance is acceptable
- User requirements are met
