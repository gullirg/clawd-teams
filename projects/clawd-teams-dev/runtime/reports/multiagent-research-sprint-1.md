# Multi-Agent Architecture Research — Sprint 1

**Date:** 2026-03-29  
**Researcher:** clawd-teams-dev CEO  
**Focus:** State of the Art in Multi-Agent LLM Systems

---

## Executive Summary

This research sprint examined three critical areas for improving clawd-teams:
1. **Hierarchical Coordination** — How to structure supervisor/worker relationships
2. **Shared Memory & Context Propagation** — How agents share state and knowledge
3. **Task Decomposition Strategies** — How to break complex goals into executable subtasks

The findings directly inform clawd-teams' current architecture and suggest concrete improvements.

---

## 1. Hierarchical Coordination Patterns

### Key Findings

**Three dominant patterns exist:**

| Pattern | Structure | Best For | Weakness |
|---------|-----------|----------|----------|
| **Hierarchical** | Central orchestrator → workers | Well-defined workflows, auditability | Single point of failure, bottleneck |
| **Peer-to-Peer** | Agents communicate directly | Resilience, dynamic environments | Coordination overhead, harder to debug |
| **Hybrid** | Mix of both | Production systems at scale | Two mechanisms to maintain |

**Microsoft's Multi-Agent Reference Architecture** (2025) identifies 10 core patterns:
1. Semantic Router with LLM Fallback (cost optimization)
2. Dynamic Agent Registry (plug-and-play agents)
3. Semantic Kernel Orchestration with Skills
4. Local & Remote Agent Execution
5. Layered (Onion) Architecture
6. MCP Integration Layer
7. RAG for grounding
8. Conversation-Aware Orchestration
9. Agent-to-Agent Communication
10. Skill Chaining with Planning Support

**Hierarchical Coordination Best Practices:**
- ✅ Define explicit roles, permissions, authority per tier
- ✅ Use structured task specs with clear success criteria
- ✅ Implement bounded re-decomposition with recursion limits
- ✅ **Summarize between levels** to control context growth
- ✅ Use smaller models for routine tasks, larger for strategic
- ❌ Avoid single points of failure at supervisor level
- ❌ Avoid ambiguous authority that blocks workers
- ❌ Don't forward full transcripts across tiers — use summaries

### Implications for clawd-teams

**Current state:** clawd-teams uses hierarchical (CEO → CTO/Researcher workers).

**Recommended improvements:**
1. **Add tier-based summarization:** CEOs should not pass full context to workers; pass distilled task specs instead.
2. **Implement escalation rules:** Define when workers escalate back vs. retry.
3. **Consider dynamic agent registry:** Allow workers to self-register capabilities so CEOs don't need hardcoded knowledge.

---

## 2. Shared Memory & Context Propagation

### Key Findings

**Memory architecture for multi-agent systems mirrors human cognition:**

| Memory Type | Purpose | Technical Implementation |
|-------------|---------|-------------------------|
| **Working Memory** | Always in context | File-based (JSON/MD) injected into prompts |
| **Episodic Memory** | Searchable past events | RAG with vector DB (pgvector) |
| **Semantic Memory** | Factual knowledge | RAG / knowledge graphs |
| **Procedural Memory** | Learned skills | Fine-tuning or in-context examples |

**Critical insight from arxiv paper (2025):**
> "Memory behavior in multi-agent frameworks is governed by architecture, not context length alone. Retrieval enables stable recall and global reasoning, accumulation enables in-session learning but scales poorly, and hybrid designs are effective only under bounded context."

**Advanced memory techniques:**
1. **Memory Distillation** — An agent monitors conversations in real-time, extracts important info, and stores compressed high-signal representations. Less important elements are discarded.
2. **Dynamic Multi-Shot Example Selection** — Track successful agent outputs; automatically add proven patterns to example libraries for future prompts.
3. **Event Sourcing** — Capture reasoning behind each write, not just data. Enables replaying memory formation with different strategies.
4. **Conflict Resolution:** Use semantic arbitration (LLM-based) rather than simple timestamps; CRDTs for eventual consistency.

### Implications for clawd-teams

**Current state:** Projects have `memory/MEMORY.md` and daily notes. Workers don't share memory with CEO.

**Recommended improvements:**
1. **Implement memory distillation:** CEOs should distill worker outputs before storing, not raw dumps.
2. **Add project-level shared memory:** A `runtime/shared-context.json` that all workers can read (not write).
3. **Consider event sourcing for decisions:** Track why decisions were made, not just what was decided.
4. **Explore dynamic example selection:** Track successful task completions and inject as few-shot examples.

---

## 3. Task Decomposition Strategies

### Key Findings

**Task decomposition is the foundation of planning.** A bad decomposition cannot be rescued by good execution.

**The spectrum of deliberation:**
- **Pure reaction** (ReAct): Decide based only on immediate observation
- **Anticipatory planning**: Consider full task structure before committing

**Key difference:** Reactive agents commit to approaches before having info to know if they're sensible. Planning agents defer commitment until enough info exists.

**Hierarchical Task Network (HTN) approach:**
- Decompose goals into top-level steps
- Recursively expand composite tasks into atomic tasks
- Atomic = directly executable (tool call)
- Composite = needs further breakdown

**Critical calibration question:** When to stop decomposing?
- Too deep → hundreds of trivial steps, coordination overhead
- Too shallow → vague instructions executors can't act on

**Parallel vs. Sequential:**
- Identify independent subtasks → parallelize
- Sequential only when output of one is input to another

**Amazon Science insight on cost/complexity tradeoff:**
> Complexity of task decomposition: O(n) + O(k^m) where k = subtasks, 1 < m ≤ 2
> For small k, overhead is negligible. As k grows, coordination overhead dominates.
> **Optimal decomposition depends on scale** — don't over-engineer for small tasks.

**When single-agent is better:**
- Tasks where holistic context matters (creativity, finding hidden relationships)
- Small scope where decomposition overhead > benefit
- When "serendipitous connections" from large context are valuable

### Implications for clawd-teams

**Current state:** CEOs manually decompose tasks when spawning workers.

**Recommended improvements:**
1. **Add decomposition templates:** Standard patterns for common task types (coding, research, review).
2. **Implement granularity heuristics:** If task can be described in <50 words with clear success criteria, it's atomic. Otherwise, decompose.
3. **Track decomposition effectiveness:** Log task outcomes to learn which decomposition patterns succeed.
4. **Avoid over-decomposition:** For creative/exploratory tasks, keep context together rather than fragmenting.

---

## Actionable Recommendations for clawd-teams

### Quick Wins (can implement this week)

1. **Tier summarization:** CEO should write 2-3 sentence task summaries when spawning workers instead of forwarding full context.

2. **Shared read-only context:** Create `runtime/project-context.md` that workers can reference but only CEO updates.

3. **Task spec template:** Standardize worker task format:
   ```markdown
   ## Task
   [One sentence goal]
   
   ## Context
   [Only relevant background — distilled]
   
   ## Success Criteria
   [How to know when done]
   
   ## Constraints
   [Budget, time, scope limits]
   ```

### Medium-Term (next 2-4 weeks)

4. **Memory distillation process:** CEO runs periodic "distillation" to compress daily notes into MEMORY.md insights.

5. **Dynamic agent registry:** Workers self-describe capabilities; CEO queries registry rather than hardcoded knowledge.

6. **Decomposition logging:** Track which task structures succeed/fail to build institutional knowledge.

### Research-Informed Architecture Principles

- **Summarize across tiers** — Never pass raw transcripts between hierarchy levels
- **Bound recursion** — Set maximum decomposition depth (e.g., 3 levels)
- **Match model to task** — Cheap models for routine, expensive for strategic
- **Prefer retrieval over accumulation** — Use RAG patterns, don't stuff context
- **Design for failure** — Every decomposition should have clear escalation paths

---

## Key Sources

1. Microsoft Multi-Agent Reference Architecture (2025) — 10 design patterns
2. "Multi-Agent Collaboration Mechanisms: A Survey of LLMs" (arxiv, Jan 2025)
3. "Memory in Multi-Agent Systems: Technical Implementations" (Artium/Medium)
4. "Planning: Task Decomposition and Goal-Directed LLM Agents" (Brenndoerfer)
5. "How Task Decomposition and Smaller LLMs Can Make AI More Affordable" (Amazon Science)
6. "Hierarchical Coordination" pattern reference (agentic-design.ai)

---

## Next Sprint Topics

1. **Error recovery and retry strategies** — How agents handle failures and adapt plans
2. **Cost optimization** — Model routing, caching, batching strategies
3. **Human-in-the-loop patterns** — When and how to escalate to human oversight

---

*Research cycle approved by Gulli 2026-03-29. Weekly sprints will continue.*
