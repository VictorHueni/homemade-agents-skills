# Exoscale provider reference

Provider: [`exoscale/exoscale`](https://registry.terraform.io/providers/exoscale/exoscale/latest/docs) · pinned `~> 0.69` (latest at authoring: 0.69.2). Background reading: [Terraform on Exoscale](https://www.exoscale.com/blog/terraform-with-exoscale/), [community provider reference](https://community.exoscale.com/reference/terraform/provider/).

## Authentication

Credentials come from environment variables only — never literals in `.tf`/`.tfvars`:

```bash
export EXOSCALE_API_KEY="EXO..."
export EXOSCALE_API_SECRET="..."
```

Accepted env vars: `EXOSCALE_API_KEY` (or `EXOSCALE_KEY`) and `EXOSCALE_API_SECRET` (or `EXOSCALE_SECRET`). Optional: `EXOSCALE_ENDPOINT`/`EXOSCALE_COMPUTE_ENDPOINT`, `EXOSCALE_DNS_ENDPOINT`, `EXOSCALE_TIMEOUT`, `EXOSCALE_CONFIG`, `EXOSCALE_REGION`.

The provider block is therefore left credential-less:

```hcl
provider "exoscale" {}
```

Create the key in the portal under **IAM → API Keys**. Prefer a **scoped IAM key** (least privilege for the resources this config manages) over the unrestricted root key.

## Zones

`ch-gva-2` (Geneva), `ch-dk-2` (Zurich), `de-fra-1` (Frankfurt), `de-muc-1` (Munich), `at-vie-1` and `at-vie-2` (Vienna), `bg-sof-1` (Sofia). Always carry the zone as a variable.

## Instance types (common)

Format `<family>.<size>`. Families: `standard`, `cpu` (compute-optimised), `memory` (memory-optimised), `gpu*`, `storage`. Sizes: `micro`, `tiny`, `small`, `medium`, `large`, `extra-large`, `huge`, `mega`, `titan`. Example: `standard.medium`. Resolve programmatically when unsure rather than guessing; keep the chosen type in a variable.

## Resource catalogue

| Resource | Purpose |
| :--- | :--- |
| `exoscale_compute_instance` | VM. **Use this — `exoscale_compute` is deprecated.** |
| `exoscale_ssh_key` | SSH keypair registration. |
| `exoscale_anti_affinity_group` | Spread instances across hosts. |
| `exoscale_private_network` | Private L2/L3 network (managed or unmanaged). |
| `exoscale_security_group` | Firewall group (rules are separate resources). |
| `exoscale_security_group_rule` | One ingress/egress rule. |
| `exoscale_nlb` / `exoscale_nlb_service` | Network load balancer + backend service. |
| `exoscale_sks_cluster` / `exoscale_sks_nodepool` | Managed Kubernetes (SKS). |
| `exoscale_database` | Managed DBaaS (PostgreSQL, MySQL, Redis, Kafka, OpenSearch, Grafana). |
| `exoscale_block_storage_volume` | Block storage volume. |
| `exoscale_iam_role` / `exoscale_iam_api_key` | IAM. |
| `exoscale_domain` / `exoscale_domain_record` | DNS. |
| `data.exoscale_template` | Resolve an OS template ID (don't hardcode image IDs). |

## Recipes

### Compute instance (with template lookup)

```hcl
data "exoscale_template" "os" {
  zone = var.zone
  name = var.template_name # e.g. "Linux Ubuntu 24.04 LTS 64-bit"
}

resource "exoscale_compute_instance" "app" {
  name        = var.instance_name
  zone        = var.zone
  type        = var.instance_type        # e.g. standard.medium
  template_id = data.exoscale_template.os.id
  disk_size   = var.disk_size            # GB
  ssh_keys    = [exoscale_ssh_key.deploy.name]

  security_group_ids = [exoscale_security_group.app.id]
  network_interface {
    network_id = exoscale_private_network.app.id
  }
}
```

### Security group + rule (least privilege)

```hcl
resource "exoscale_security_group" "app" {
  name = "${var.instance_name}-sg"
}

resource "exoscale_security_group_rule" "ssh" {
  security_group_id = exoscale_security_group.app.id
  type              = "INGRESS"
  protocol          = "TCP"
  start_port        = 22
  end_port          = 22
  cidr              = var.admin_cidr # NOT 0.0.0.0/0
}
```

### Private network

```hcl
resource "exoscale_private_network" "app" {
  zone        = var.zone
  name        = "${var.instance_name}-net"
  netmask     = "255.255.255.0"
  start_ip    = "10.0.0.20"
  end_ip      = "10.0.0.250"
}
```

### SKS cluster + nodepool (sketch)

```hcl
resource "exoscale_sks_cluster" "k8s" {
  zone    = var.zone
  name    = var.cluster_name
  version = var.k8s_version
}

resource "exoscale_sks_nodepool" "default" {
  zone           = var.zone
  cluster_id     = exoscale_sks_cluster.k8s.id
  name           = "default"
  instance_type  = var.instance_type
  size           = var.node_count
  security_group_ids = [exoscale_security_group.app.id]
}
```

## Gotchas

- `exoscale_compute` is **deprecated** — always `exoscale_compute_instance`.
- Security-group rules are **separate resources** (`exoscale_security_group_rule`), not inline blocks.
- Resolve templates via `data.exoscale_template`; image IDs differ per zone and rotate.
- Never open SSH (`22`) to `0.0.0.0/0`; bind to an admin CIDR variable.
- Some resources are zone-scoped — keep `zone` consistent (or explicit) across dependent resources.
