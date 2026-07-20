workspace "{{project_name}}" "{{project_description}}" {

    // ─────────────────────────────────────────────────────────────────
    // MODEL
    //
    // Identifiers follow the kit convention (see arch-structurizr/
    // references/dsl-conventions.md):
    //
    //   • Software systems: SYS_NN  (display "SYS-NN — Name")
    //   • Containers:       CON_NN  (display "CON-NN — Name")
    //   • Components:       CMP_NN  (display "CMP-NN — Name")
    //   • Deployment nodes: DN_NN   (display "DN-NN — Name")
    //   • People:           P_NN    (reuse P-NN IDs from business-persona)
    //
    // Grammar gotcha: forward references are NOT allowed. Declare an
    // identifier BEFORE using it in a relationship.
    // ─────────────────────────────────────────────────────────────────

    model {

        // People — replace these placeholders with real personas from
        // docs/business/01a-personas.md
        P_01 = person "P-01 — Placeholder Persona" "_TODO_ describe primary user" {
            tags "internal"
        }

        // The system this workspace documents
        SYS_01 = softwareSystem "SYS-01 — {{project_name}}" "{{project_description}}" {
            tags "core"

            // Containers — add via `arch-c4 container` mode
            // CON_01 = container "CON-01 — Web App" "..." "..." { tags "web" }
        }

        // Relationships (declare AFTER all referenced identifiers)
        P_01 -> SYS_01 "Uses"
    }

    // ─────────────────────────────────────────────────────────────────
    // VIEWS
    //
    // View keys become rendered filenames:
    //   views/<view-key>.svg
    //
    // Canonical keys (see dsl-conventions.md §3):
    //   • systemContext           → arc42 §3
    //   • containers              → arc42 §5.1
    //   • components-<CON-NN>     → arc42 §5.2/§5.3
    //   • deployment-<env>        → arc42 §7
    //   • dynamic-<RV-NN>         → arc42 §6 (arch-runtime-view)
    // ─────────────────────────────────────────────────────────────────

    views {

        systemContext SYS_01 "systemContext" {
            include *
            autolayout lr
            description "SYS-01 — System Context (arc42 §3)."
        }

        // Add container/component/deployment views via `arch-c4`.
        // container SYS_01 "containers" {
        //     include *
        //     autolayout lr
        // }

        styles {
            element "Person" {
                shape Person
                background "#08427B"
                color "#ffffff"
            }
            element "Software System" {
                background "#1168BD"
                color "#ffffff"
            }
            element "Container" {
                background "#438DD5"
                color "#ffffff"
            }
            element "Component" {
                background "#85BBF0"
                color "#000000"
            }
            element "external" {
                background "#999999"
                color "#ffffff"
            }
            element "core" {
                background "#0B6FB8"
                color "#ffffff"
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
        }

        // NOTE: `theme default` (which fetches from static.structurizr.com)
        // is intentionally NOT used here — that cloud service EOLs on
        // 2026-09-30. The styles{} block above already covers what the
        // default theme provides for the kit's tag taxonomy.
    }
}
