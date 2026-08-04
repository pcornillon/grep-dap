# PRE_CONVERSION — originals carried in unmodified

Files as they stood **before** the 2026-08-04 restructure to the project spine, moved
here with `git mv` and never edited (`claude-config` D13). They are kept so the old
file can be read beside the new one; git history is not a substitute for that.

| File | Why it is here |
|---|---|
| `CLAUDE.md` | the pre-restructure project context, 112 lines |

## What happened to its content

- The **"Interactions"** block (do not make up data; talk to me directly; be concise;
  be critical) was already global as of 2026-07-31 and is not repeated in the new
  `CLAUDE.md`. It loads from `~/.claude/CLAUDE.md` in every repo.
- **"Project Overview", "Primary context", "Potential solution", "Background",
  "Problem Context", "Framing"** — the long prose statement of what the project is and
  why — was condensed into the new `CLAUDE.md`'s *What this project is* and *The one
  idea that makes this tractable*. The original is the fuller statement and is worth
  reading; nothing in it was contradicted.
- The **"Prompt"** and **"Considerations"** sections were the framing for the original
  open-ended question to Claude ("what are plausible ways GenAI could help here?").
  They are history — the project has since answered them — and were not carried
  forward.
- **"Code guidelines"** carried across intact: reuse code, methods not classes, inline
  comments, matplotlib, the `ocean14` conda environment, pydap.
- **"Output"** — *"Place any .tex, .json or other output files in
  `~/Git_Repos/grep-dap/docs/`"* — was **rewritten**, not carried: `docs/` no longer
  exists. The new rule is in `CLAUDE.md` under *Where output goes*.

Nothing else was archived. `README.md` was rewritten in place — its predecessor was two
lines and is in git history.
