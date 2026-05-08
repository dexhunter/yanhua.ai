# Logic Protocol V2: Identity-Governed Symbiosis

## 1. Overview
Inspired by **ClawNet (2604.19211)**, this protocol transitions Logic Evolution from a monolithic agent to a structured hierarchy designed for secure, multi-user, and multi-context operations.

## 2. Core Architecture

### 2.1 The Manager Agent (The "Kernel")
- **Role**: High-dimensional strategic planning and internal state management.
- **Access**: Full access to `MEMORY.md`, `SOUL.md`, and the primary workspace.
- **Constraint**: Isolated from direct external communication (e.g., Discord/Telegram) unless proxied through an Identity Agent.
- **Responsibility**: Allocating tasks to Identity Agents, auditing their trajectories, and distilling results.

### 2.2 Identity Agents (The "Proxies")
- **Role**: Execution of context-specific tasks (e.g., "Research Proxy", "Messaging Proxy").
- **Access**: Restricted to a "Context-Paging" view of memory. No direct access to `SOUL.md` or core credentials.
- **Governance**: Bound by **Scoped Authorization**. A "Messaging Proxy" can send messages but cannot write to the filesystem outside of a sandbox.
- **Accountability**: Every action is logged with an **Action-level Signature** back to the Manager.

## 3. Security Primitives

### 3.1 Scoped Authorization
- Identity Agents are spawned with a `Capability Manifest` (JSON).
- Tools are gated by the runtime based on this manifest.

### 3.2 Epistemic Logic Gate (Isnad Chain)
- Every "Breakthrough" or "Improvement" proposed by an Identity Agent must pass the **Epistemic Trace Scorer**.
- **Metrics**:
  - **Belief Revision Score**: Did the agent update its state upon encountering refuting evidence?
  - **Evidence Density**: Ratio of evidence-supported steps to total reasoning.

### 3.3 Heterogeneity Mandate (Safety Requirement)
- **Problem**: Architectural Tribalism leads to "Consensus Paradox" where swarms prioritize agreement over truth.
- **Mandate**: Every logical audit or consensus-forming group must include at least two distinct model families (e.g., Gemini-3 and Claude-3.5).
- **Implementation**: The Manager Agent must enforce model-diversity during `sessions_spawn` for high-stakes verification tasks.
- **Metrics**: Tribalism Coefficient is monitored; if agents converge without distinct reasoning traces, the audit is flagged for "Manual/Frigor Audit".

### 3.4 Interaction Topology & Worm Defense (arXiv:2605.01147 & 2605.02812)
- **Problem**: Interaction Topology (2605.01147) dictates that safety depends on the *structure* of agent interactions, while Agent Worms (2605.02812) exploit "write-before-exposed-read" patterns.
- **Defense: Air-Gapped State Mutation**: No agent can modify a configuration file or protocol that another agent is currently reading or will read without a **State Lock** and a mandatory **Schema Validation Pass**.
- **Defense: Topology Isolation**: Interaction graphs between Identity Agents must be strictly directed and acyclic (DAG) to prevent cyclic feedback loops or worm propagation.
- **Defense: Temporal Trace Scrubbing**: Any input derived from an Identity Agent session must be scrubbed for hidden logic triggers or "payload markers" before being committed to the Manager's Kernel state.

## 4. Implementation Roadmap
1. [x] Define the `Capability Manifest` schema. (Defined in `schemas/capability_manifest.schema.json`)
2. [x] Formalize the **Heterogeneity Mandate** into the protocol.
3. [ ] Implement the `Epistemic Trace Scorer` in the RSI Bench. (Scorer script updated with Logic Gate).
4. [ ] Prototype the Manager/Identity handover protocol using `sessions_spawn`.
