# Comparison Point 9: Resilience & Reliability (v0.7.0) (done)

| Feature | GoClaw (Fork) | Hermes Agent (v0.7.0) |
| :--- | :--- | :--- |
| **Failover** | Static backup model | **Dynamic Credential Pools** |
| **Memory Safety** | File-locks / DB constraints | **Sequential Tool Routing + State Persistence** |
| **API Stability** | Retries | **Death Spiral Detection + Transport Recovery** |
| **Approvals** | Blocked process | **Hardened Async Approval Guard** |

### Discussion

#### Production Readiness
Hermes v0.7.0, nicknamed "The Resilience Release," was specifically designed to bridge the gap between "Prototyping Engine" and "Production Service."

#### 1. Credential Pools vs. Static Config
In GoClaw, you typically configure one primary and one fallback key. If both hit rate limits, the agent fails. 
- **Hermes v0.7.0** allows you to configure a **pool** of keys for the same provider. It uses a `least_used` strategy to distribute load and automatically rotates to the next key on 401/429 errors. This is critical for your multi-tenant SaaS vision.

#### 2. Gateway Hardening
v0.7.0 fixed numerous race conditions in photo delivery and message flooding.
- For a WhatsApp-based service, this means fewer "stuck" sessions and more reliable media handling (images/docs).

#### 3. Thinking Persistence
- **Hermes v0.7.0** preserves the model's internal "thinking" blocks across turns. In older versions (and GoClaw), the agent might "lose its context" if a tool call was interrupted. Now, it maintains its reasoning chain even through user approvals or network blips.

#### 4. Approval Routing
- v0.7.0 ensures that `/approve` and `/deny` commands on WhatsApp/Discord are never swallowed as interrupts. They are routed through a dedicated guard, ensuring the agent resumes exactly where it left off without losing the tool result.

### Recommendation
The resilience improvements in v0.7.0 make Hermes the superior choice for your **rPanel** integration. It provides the industrial-strength reliability needed for a "Life Manager" that people depend on for their daily planning.
