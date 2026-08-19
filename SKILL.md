---
name: hatch-project-context
description: Read and reconcile Hatch's internal Feishu knowledge base, public One Pager, and market-entry analysis. Use when Codex needs Hatch-specific context for product positioning, architecture, creator or customer workflows, market strategy, onboarding, internal collaboration, briefs, presentations, comparisons, or answers about what Hatch is and how it works. Do not use for generic repository work that does not depend on Hatch business or product context.
---

# Hatch Project Context

Use the live Hatch sources instead of relying on remembered project context. Read only the sources needed for the request.

## Workflow

1. Read [references/sources.md](references/sources.md) and select the relevant sources.
2. Retrieve current source content at task time. Do not treat copied excerpts or prior chat summaries as current authority.
3. Distinguish source roles:
   - Use Feishu for internal decisions, architecture, operating context, guides, and meeting history.
   - Use the One Pager for approved external positioning, business-model language, and partner messaging.
   - Use Market Analysis for market-entry hypotheses, vertical selection, and GTM framing.
4. Resolve conflicts by task intent, source role, and date. State material conflicts instead of silently blending them.
5. Produce the requested answer or artifact with links to the sources used. Label meeting notes and market claims according to their evidence level.

## Source authority

- For internal product intent, prefer the relevant Feishu canonical document over meeting notes.
- For external-facing language, prefer the current One Pager. Do not expose internal wording unless the user explicitly requests it and sharing is appropriate.
- For market selection, use Market Analysis as a working thesis, not as verified fact. Verify claims that require current or precise external evidence against primary sources.
- For current implementation, release, authentication, payment, entitlement, or runtime behavior, inspect the real product path. These content sources are not UAT or release evidence.
- When two sources disagree, report both positions with their source and date, then identify which one governs the requested task.

## Handling Feishu material

- Use authenticated `lark-cli` access described in the source reference.
- Read only. Do not move, edit, share, or change permissions unless the user explicitly asks.
- Prefer canonical product pages over AI-generated meeting summaries.
- Treat smart minutes as potentially inaccurate. Confirm consequential claims against the original transcript or a canonical document.
- Do not broadly reproduce private, personal, health, financing, credential, or access-control information.
- If authentication or a live dependency is unavailable, report the blocker. Never substitute mock data or claim the source was checked.

## Typical outputs

- Explain Hatch positioning, architecture, creator flow, customer flow, or business model.
- Prepare internal onboarding, product briefs, market plans, partner materials, or meeting preparation.
- Compare internal strategy with external messaging.
- Trace when and where a Hatch decision was made.
- Identify stale, conflicting, sensitive, or unverified project claims.
