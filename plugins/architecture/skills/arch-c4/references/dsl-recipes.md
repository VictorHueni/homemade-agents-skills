# DSL recipes per mode

Copy-pasteable Structurizr DSL fragments for the four `arch-c4` modes. The grammar itself (brace placement, no forward refs, identifier rules) lives in `arch-structurizr/references/dsl-conventions.md` — skim it first if you haven't already.

---

## Recipe 1 — `context` mode (arc42 §3)

Add the primary system + actors + external systems. Inside `model { ... }`:

```
// Actors — reuse P-NN IDs from business-persona where they exist
P_01 = person "P-01 — Claims Handler" "Insurance employee triaging claims" {
    tags "internal"
}

P_02 = person "P-02 — Customer" "Person submitting a claim" {
    tags "external"
}

// The primary system being documented
SYS_01 = softwareSystem "SYS-01 — Claims Platform" "Internal platform managing the claim lifecycle from submission to disbursement" {
    tags "core"
    // Containers added later by `container` mode
}

// External systems
SYS_02 = softwareSystem "SYS-02 — Payment Gateway" "Third-party disbursement provider" {
    tags "external"
}

SYS_03 = softwareSystem "SYS-03 — Identity Provider" "Corporate SSO (Azure AD)" {
    tags "external"
}

// Relationships — declare AFTER all referenced identifiers
P_01 -> SYS_01 "Triages claims via" "HTTPS/Web UI"
P_02 -> SYS_01 "Submits claims via" "HTTPS/Web UI"
SYS_01 -> SYS_02 "Initiates disbursement on" "HTTPS/JSON"
SYS_01 -> SYS_03 "Authenticates via" "OIDC"
```

Inside `views { ... }`:

```
systemContext SYS_01 "systemContext" {
    include *
    autolayout lr
    description "SYS-01 system context — actors and neighbouring systems (arc42 §3)."
}
```

Render: `./render.sh systemContext`.

---

## Recipe 2 — `container` mode (arc42 §5.1)

Add containers as nested elements inside the primary system:

```
SYS_01 = softwareSystem "SYS-01 — Claims Platform" "..." {
    tags "core"

    CON_01 = container "CON-01 — Customer Portal" "Self-service claim submission UI" "React 18 + Vite" {
        tags "web"
    }

    CON_02 = container "CON-02 — Claims API" "Domain command + query surface" "Node.js 20 + Fastify" {
        tags "core"
    }

    CON_03 = container "CON-03 — Claims Database" "Persistent state for Claim aggregate" "PostgreSQL 16" {
        tags "database"
    }

    CON_04 = container "CON-04 — Event Bus" "Domain event distribution" "Kafka 3.7" {
        tags "queue"
    }

    CON_05 = container "CON-05 — Notification Service" "Outbound email + SMS" "Node.js 20" {
        tags "core"
    }
}
```

Inter-container relationships (still inside `model { ... }`, after all containers are declared):

```
CON_01 -> CON_02 "Sends claim commands to" "HTTPS/JSON"
CON_02 -> CON_03 "Reads from + writes to" "SQL/TCP"
CON_02 -> CON_04 "Publishes ClaimSubmitted, ClaimApproved to" "Kafka protocol"
CON_05 -> CON_04 "Consumes ClaimSubmitted from" "Kafka protocol"
CON_02 -> SYS_02 "Initiates disbursement on" "HTTPS/JSON"
```

Note: cross-system relationships (e.g. `CON_02 -> SYS_02`) replace the corresponding system-level relationship (`SYS_01 -> SYS_02`) automatically in Structurizr — the container view will surface the more-specific edge.

Inside `views { ... }`:

```
container SYS_01 "containers" {
    include *
    autolayout lr
    description "SYS-01 containers — process-level building blocks (arc42 §5.1)."
}
```

Render: `./render.sh containers`.

---

## Recipe 3 — `component` mode (arc42 §5.2)

Add components inside one container at a time. The `properties.implements` field is **mandatory** (or explicitly empty) — see `boundary-discipline.md`.

```
CON_02 = container "CON-02 — Claims API" "..." "Node.js 20 + Fastify" {
    tags "core"

    CMP_01 = component "CMP-01 — Submit Claim Endpoint" "HTTP POST /claims handler" "Fastify route" {
        tags "endpoint"
        properties {
            "implements" "none"
            "code-path" "src/claims/http/SubmitClaimRoute.ts"
        }
    }

    CMP_02 = component "CMP-02 — Claim Command Handler" "Translates HTTP → domain commands on Claim aggregate" "TypeScript command bus" {
        tags "core"
        properties {
            "implements" "BC-01.AGG-02"
            "code-path" "src/claims/application/ClaimCommandHandler.ts"
        }
    }

    CMP_03 = component "CMP-03 — Claim Aggregate Repository" "Persists/loads Claim aggregate state" "TypeORM" {
        tags "persistence"
        properties {
            "implements" "BC-01.AGG-02"
            "code-path" "src/claims/infrastructure/ClaimRepository.ts"
        }
    }

    CMP_04 = component "CMP-04 — Claim Event Publisher" "Publishes domain events to Kafka" "kafkajs" {
        tags "core"
        properties {
            "implements" "BC-01.AGG-02"
            "code-path" "src/claims/infrastructure/ClaimEventPublisher.ts"
        }
    }
}
```

Intra-container relationships:

```
CMP_01 -> CMP_02 "Dispatches command via" ""
CMP_02 -> CMP_03 "Loads + saves aggregates via" ""
CMP_02 -> CMP_04 "Publishes events via" ""
```

(Technology label is optional for intra-process method calls — leave empty `""`.)

Inside `views { ... }`:

```
component CON_02 "components-CON-02" {
    include *
    autolayout lr
    description "CON-02 internal components (arc42 §5.2)."
}
```

Render: `./render.sh components-CON-02`.

---

## Recipe 4 — `deployment` mode (arc42 §7)

Map containers onto infrastructure for one or more environments. Inside `model { ... }`, after the containers are defined:

```
deploymentEnvironment "Production" {

    DN_01 = deploymentNode "DN-01 — AWS eu-west-1" "Primary region" {

        DN_02 = deploymentNode "DN-02 — Production Kubernetes" "EKS 1.30" {
            tags "kubernetes"

            // containerInstance references a Container by DSL identifier
            CON_02_INSTANCE = containerInstance CON_02 {
                instances 3
                tags "primary"
            }

            CON_05_INSTANCE = containerInstance CON_05 {
                instances 2
            }
        }

        DN_03 = deploymentNode "DN-03 — RDS for PostgreSQL" "AWS RDS Multi-AZ" {
            tags "managed-database"
            CON_03_INSTANCE = containerInstance CON_03 {
                instances 1
            }
        }

        DN_04 = deploymentNode "DN-04 — MSK" "AWS Managed Streaming for Kafka, 3 brokers" {
            tags "managed-queue"
            CON_04_INSTANCE = containerInstance CON_04
        }

        DN_05 = deploymentNode "DN-05 — CloudFront" "Global edge cache" {
            tags "cdn"
            CON_01_INSTANCE = containerInstance CON_01
        }
    }
}

deploymentEnvironment "Staging" {
    // Same structure as Production with reduced instance counts; copy + edit
}
```

Inside `views { ... }`:

```
deployment SYS_01 "Production" "deployment-production" {
    include *
    autolayout lr
    description "SYS-01 production deployment (arc42 §7.x)."
}

deployment SYS_01 "Staging" "deployment-staging" {
    include *
    autolayout lr
}
```

Render: `./render.sh deployment-production` and `./render.sh deployment-staging`.

---

## Common patterns

### A container that's also a database

Use `tags "database"` for cylinder styling. Technology should name the engine + version (`"PostgreSQL 16"`, `"MongoDB 7"`).

### A container that's an event bus

Use `tags "queue"` for pipe styling. Technology names the broker + version (`"Kafka 3.7"`, `"RabbitMQ 3.13"`).

### A SaaS / third-party system that's effectively an external Container

If a third-party SaaS is the *only* way to satisfy a capability (e.g. Stripe for payments), model it as an external **softwareSystem** (`SYS-NN`, tagged `external`), not as a Container of your own system. Containers belong inside the C4 system boundary.

### A scheduled job / cron / batch worker

Model it as a Container with technology like `"Kubernetes CronJob"` or `"AWS EventBridge + Lambda"`. The fact that it runs on a schedule rather than in response to requests doesn't change its C4 classification.

### Frontends that share a backend

If you have a web app and a mobile app talking to the same API, both are separate Containers (`CON-01 Web App`, `CON-02 Mobile App`) — they have different technologies and different deployments.

---

## What NOT to do

- ❌ **Defining a Container with no technology label** — empty `technology` makes the §5.1 table column blank.
- ❌ **Defining Components without `properties.implements`** — boundary discipline check will flag it. Use `"none"` if the component is tech-only.
- ❌ **Using empty `""` for any property value** — Structurizr DSL rejects this at validation. Use a sentinel like `"none"` or `"_TODO_"`.
- ❌ **Putting Components inside the top-level `model { ... }` instead of inside their parent `container { ... }`** — Structurizr parses this but the component won't be reachable from the container view.
- ❌ **Reusing a DSL identifier across blocks** — identifiers must be unique within the workspace.
- ❌ **Using `:latest` in `containerInstance` properties or anywhere else** — the kit forbids unpinned references.
