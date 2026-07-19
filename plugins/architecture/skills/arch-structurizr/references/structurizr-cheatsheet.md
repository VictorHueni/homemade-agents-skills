# Structurizr DSL cheatsheet

Copy-paste-able DSL fragments for the common patterns `arch-c4` produces. Read alongside `dsl-conventions.md` (which adds the kit's identifier + view-key rules on top of this raw grammar).

Authoritative reference: [docs.structurizr.com/dsl](https://docs.structurizr.com/dsl). The DSL grammar is unchanged in the consolidated [Structurizr vNext](https://www.patreon.com/posts/introducing-146923136) tool — only the rendering image (`structurizr/structurizr:<pin>-playwright`) differs from the EOL `structurizr-cli`. This file is the **subset** the kit uses.

---

## Top-level skeleton

```
workspace "Project Name" "Project description" {

    model {
        // people, software systems, containers, components, deployment environments
    }

    views {
        // systemContext, container, component, deployment, dynamic — plus styles
        theme default
    }
}
```

---

## People (arc42 §3 actors)

```
P_01 = person "P-01 — Claims Handler" "Insurance employee who triages claims" {
    tags "internal"
}

P_02 = person "P-02 — Customer" "Person submitting a claim" {
    tags "external"
}
```

Reuse `P-NN` IDs from the kit's `business-persona` skill — DSL identifier is `P_NN`, display name carries the hyphen.

---

## Software systems (arc42 §3 — System Context)

```
SYS_01 = softwareSystem "SYS-01 — Claims Platform" "Internal platform handling claim lifecycle" {
    tags "core"

    // Containers nest inside the system
}

SYS_02 = softwareSystem "SYS-02 — Payment Gateway" "External vendor for disbursements" {
    tags "external"
}
```

---

## Containers (arc42 §5 Level 1 — Building Block)

```
SYS_01 = softwareSystem "SYS-01 — Claims Platform" "..." {

    CON_01 = container "CON-01 — Customer Portal" "Self-service claim submission" "React 18 + Vite" {
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
}
```

The four positional arguments are: `identifier = container "<name>" "<description>" "<technology>"`.

---

## Components (arc42 §5 Level 2/3)

Only define components **inside** containers — the DSL parses them as nested elements.

```
CON_02 = container "CON-02 — Claims API" "..." "Node.js 20 + Fastify" {

    CMP_01 = component "CMP-01 — Submit Claim Endpoint" "HTTP POST /claims" "Fastify route" {
        tags "endpoint"
    }

    CMP_02 = component "CMP-02 — Claim Command Handler" "Translates HTTP → domain commands" "TypeScript" {
        tags "core"
    }

    CMP_03 = component "CMP-03 — Claim Aggregate Repository" "Persists Claim aggregate state" "TypeORM" {
        tags "persistence"
    }
}
```

The kit's **boundary discipline** (see `arch-c4` SKILL.md): every Component card in the rendered markdown must declare which `BC-NN.AGG-NN` domain aggregate it implements. In the DSL, encode this via a property:

```
CMP_03 = component "CMP-03 — Claim Aggregate Repository" "Persists Claim aggregate state" "TypeORM" {
    tags "persistence"
    properties {
        "implements" "BC-01.AGG-02"
    }
}
```

`arch-c4` extracts the `properties.implements` value when generating the arc42 §5 markdown.

---

## Relationships (`->`)

After all referenced identifiers are declared:

```
P_02 -> CON_01 "Submits claim via" "HTTPS"
CON_01 -> CON_02 "Calls" "HTTPS/JSON"
CON_02 -> CON_03 "Reads from + writes to" "SQL/TCP"
CON_02 -> CON_04 "Publishes ClaimSubmitted to" "Kafka protocol"
CON_02 -> SYS_02 "Initiates payment via" "HTTPS/JSON"
```

The four positional arguments are: `<source> -> <destination> "<description>" "<technology>"`.

Relationships can be defined either inside a parent block (between siblings) or at the top of the model block (between any pair).

---

## Deployment environments (arc42 §7)

```
deploymentEnvironment "Production" {

    DN_01 = deploymentNode "DN-01 — AWS eu-west-1" {

        DN_02 = deploymentNode "DN-02 — Production Kubernetes" "EKS 1.30" {

            CON_02_INSTANCE = containerInstance CON_02 {
                tags "primary"
            }
        }

        DN_03 = deploymentNode "DN-03 — RDS for PostgreSQL" "AWS RDS" {
            CON_03_INSTANCE = containerInstance CON_03
        }
    }
}

deploymentEnvironment "Staging" {
    // mirror Production with smaller node sizes
}
```

`containerInstance` is the deployment-side reference to a `container` defined in the model. The DSL identifier is local to the deploymentNode tree.

---

## Views

### System Context (arc42 §3)

```
views {
    systemContext SYS_01 "systemContext" {
        include *
        autolayout lr
        description "SYS-01 system context — actors and neighbouring systems."
    }
}
```

The second argument (`"systemContext"`) is the **view key** — it becomes the rendered filename `views/systemContext.svg`.

### Containers (arc42 §5.1)

```
container SYS_01 "containers" {
    include *
    autolayout lr
    description "SYS-01 containers — process-level building blocks."
}
```

### Components (arc42 §5.2/§5.3 — one per drilled container)

```
component CON_02 "components-CON-02" {
    include *
    autolayout lr
    description "CON-02 internal components."
}
```

### Deployment (arc42 §7 — one per environment)

```
deployment SYS_01 "Production" "deployment-production" {
    include *
    autolayout lr
}
```

### Dynamic (arc42 §6 — runtime scenarios; produced by `arch-runtime-view`, not `arch-c4`)

```
dynamic SYS_01 "dynamic-RV-01" {
    title "RV-01 — Customer submits a claim"
    P_02 -> CON_01 "Submits claim"
    CON_01 -> CON_02 "POST /claims"
    CON_02 -> CON_03 "Persists Claim aggregate"
    CON_02 -> CON_04 "Publishes ClaimSubmitted"
    autolayout lr
}
```

---

## Styling

The seed `workspace.dsl` ships with these styles. `arch-c4` adds new tag → style rules as needed.

```
views {
    styles {
        element "Person" {
            shape Person
            background #08427B
            color #ffffff
        }
        element "Software System" {
            background #1168BD
            color #ffffff
        }
        element "external" {
            background #999999
            color #ffffff
        }
        element "Container" {
            background #438DD5
            color #ffffff
        }
        element "database" {
            shape Cylinder
        }
        element "queue" {
            shape Pipe
        }
        element "web" {
            shape WebBrowser
        }
        element "mobile" {
            shape MobileDeviceLandscape
        }
        element "Component" {
            background #85BBF0
            color #000000
        }
    }
    theme default
}
```

---

## `!include` (only if you split workspace.dsl)

```
!include models/bc-01-claims.dsl
!include models/bc-02-policy.dsl
```

Paths are relative to the file containing the `!include`. See `dsl-conventions.md` §5 for when splitting is appropriate.

---

## Properties (used by the kit for cross-references)

```
CMP_03 = component "CMP-03 — Claim Aggregate Repository" "..." "TypeORM" {
    properties {
        "implements" "BC-01.AGG-02"
        "code-path" "src/claims/infrastructure/ClaimRepository.ts"
        "owner" "claims-team"
    }
}
```

`properties` are arbitrary key-value pairs. The kit uses `"implements"` (domain aggregate ID), `"code-path"`, and `"owner"`. Add more as needed.
