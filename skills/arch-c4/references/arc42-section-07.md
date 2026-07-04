# arc42 §7 — Deployment View (embedded reference)

Extracted from the arc42 v9.0 template (July 2025). Use as the authoritative spec when writing `docs/architecture/arc42/07-deployment.md`.

Upstream: [docs.arc42.org/section-7](https://docs.arc42.org/section-7/).

---

## Content

> The deployment view describes:
> 1. technical infrastructure used to execute your system, with infrastructure elements like geographical locations, environments, computers, processors, channels and net topologies as well as other infrastructure elements and
> 2. mapping of (software) building blocks to that infrastructure elements.
>
> Often systems are executed in different environments, e.g. development environment, test environment, production environment. In such cases you should document all relevant environments.
>
> Especially document a deployment view if your software is executed as distributed system with more than one computer, processor, server or container or when you design and construct your own hardware processors and chips.
>
> From a software perspective it is sufficient to capture only those elements of an infrastructure that are needed to show a deployment of your building blocks. Hardware architects can go beyond that and describe an infrastructure to any level of detail they need to capture.

## Motivation

> Software does not run without hardware. This underlying infrastructure can and will influence a system and/or some cross-cutting concepts. Therefore, there is a need to know the infrastructure.

## Form

> Maybe a highest level deployment diagram is already contained in section 3.2. as technical context with your own infrastructure as ONE black box. In this section one can zoom into this black box using additional deployment diagrams:
> - UML offers deployment diagrams to express that view. Use it, probably with nested diagrams, when your infrastructure is more complex.
> - When your (hardware) stakeholders prefer other kinds of diagrams rather than a deployment diagram, let them use any kind that is able to show nodes and channels of the infrastructure.

**Kit application:** the C4 Deployment view replaces UML deployment diagrams. One C4 deployment view per `deploymentEnvironment` in the DSL — rendered as `deployment-<env-slug>.svg`.

---

## §7.1 — Infrastructure Level 1

### Per-environment required content

> Describe (usually in a combination of diagrams, tables, and text):
> - distribution of a system to multiple locations, environments, computers, processors, …, as well as physical connections between them
> - important justifications or motivations for this deployment structure
> - quality and/or performance features of this infrastructure
> - mapping of software artifacts to elements of this infrastructure
>
> For multiple environments or alternative deployments please copy and adapt this section of arc42 for all relevant environments.

---

## §7.2 — Infrastructure Level 2 (optional)

> Here you can include the internal structure of (some) infrastructure elements from level 1.
>
> Please copy the structure from level 1 for each selected element.

**Kit application:** §7.2 nested structure is rare. Use it only when a single deployment node (e.g. "Production Kubernetes Cluster") has internal substructure worth surfacing (e.g. node groups, namespaces, autoscaling groups).

---

## Kit-specific rules for §7

1. **One §7.x sub-subsection per environment.** Production, Staging, Development — each rendered as its own SVG via a separate `deployment SYS_NN "<EnvName>" "deployment-<slug>"` view in the DSL.

2. **Each environment subsection must contain:**
   - Embedded `deployment-<env-slug>.svg`
   - Motivation paragraph — why this deployment structure (e.g. "Multi-AZ for SLA compliance; single region to control egress costs")
   - Quality/Performance features — references `QA-XXNN` from `spec-quality-attributes`
   - Mapping table — one row per `CON-NN` instance: `Container ID / Deployment Node / Instance count / Region / Notes`

3. **Reference infrastructure ADRs.** If `arch-adr` decisions exist for hosting choice / runtime platform / database provisioning, link them in the Motivation paragraph.

4. **Do not confuse C4 Containers with Docker containers.** A C4 Container `CON-02 Claims API` might run as 3 Docker container replicas in production — that multiplicity is captured in the Mapping table's `Instance count` column. The C4 model itself records the *role*, not the count.

5. **Quality/Performance is the bridge to §10.** Where §10 Quality Requirements lists `QA-PE03 — Claims API 99th percentile latency < 200ms`, §7 says *how the deployment achieves it* (e.g. 3 pods minimum, HPA at 70% CPU, latency-routing CDN in front).

6. **§7 is appended on subsequent `deployment` mode invocations** when a new environment is added; existing environment subsections are overwritten on re-invocation for that environment.

---

## Acceptance criteria — when §7 is "done" (for a given system snapshot)

- [ ] `docs/architecture/arc42/07-deployment.md` exists with standard frontmatter
- [ ] §7.1 contains an overview paragraph naming all documented environments
- [ ] At least one §7.x environment subsection exists (Production at minimum)
- [ ] Each environment subsection has: embedded SVG + Motivation + Quality/Performance features + Mapping table
- [ ] Mapping table includes every `CON-NN` defined in the container view; absent containers explicitly listed as "not deployed in this environment"
- [ ] Infrastructure ADRs referenced (or a `decision-gap` row filed to the central ledger if missing)
- [ ] Quality/Performance section references `QA-XXNN` where they exist
