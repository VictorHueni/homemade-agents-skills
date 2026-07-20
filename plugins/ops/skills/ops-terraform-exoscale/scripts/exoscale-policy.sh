#!/usr/bin/env bash
# exoscale-policy.sh — deterministic, dependency-free Exoscale security checks.
#
# Why native (not Trivy custom Rego): Trivy's built-in checks do not cover the
# Exoscale provider, and Trivy's custom-Rego mechanism for Terraform is
# unreliable across versions (custom `deny` rules silently fail to render).
# These checks are plain HCL pattern checks — deterministic and version-stable.
#
# Checks:
#   EXO-001 (HIGH) — exoscale_security_group_rule opens SSH (22) INGRESS to the world
#   EXO-002 (HIGH) — exoscale_security_group_rule opens any OTHER port (e.g. RDP 3389,
#                    VNC 5900, or all-ports) INGRESS to the world
#
# "the world" = 0.0.0.0/0 or ::/0. A legitimately-scoped public rule (e.g. bootstrap
# SSH from an admin /32) is NOT open to the world and does not trigger either check.
#
# Usage:  exoscale-policy.sh <dir>
# Exit:   0 = clean, 1 = at least one HIGH finding, 2 = usage error
set -euo pipefail

DIR="${1:-infra}"
[ -d "$DIR" ] || { echo "exoscale-policy: directory not found: $DIR" >&2; exit 2; }

findings=0
while IFS= read -r -d '' file; do
  # awk walks each `resource "exoscale_security_group_rule" "<n>" { ... }` block
  # (brace-depth tracked) and flags INGRESS rules open to the world (0.0.0.0/0 or
  # ::/0): SSH-22 → EXO-001, any other port/proto → EXO-002.
  awk -v fname="$file" '
    function reset() { intype=""; proto=""; sp=""; ep=""; cidr=""; rname="" }
    BEGIN { depth=0; inblock=0; reset() }
    {
      line=$0
      if (inblock==0 && match(line, /resource[ \t]+"exoscale_security_group_rule"[ \t]+"[^"]+"/)) {
        inblock=1; bdepth=0; reset()
        if (match(line, /"exoscale_security_group_rule"[ \t]+"[^"]+"/)) {
          s=substr(line,RSTART,RLENGTH); n=split(s,a,"\""); rname=a[4]
        }
      }
      if (inblock==1) {
        # collect attributes (string/number, ignore interpolations/vars)
        if (match(line, /[ \t]*type[ \t]*=[ \t]*"[^"]*"/))      { v=line; sub(/.*type[ \t]*=[ \t]*"/,"",v); sub(/".*/,"",v); intype=toupper(v) }
        if (match(line, /[ \t]*protocol[ \t]*=[ \t]*"[^"]*"/))  { v=line; sub(/.*protocol[ \t]*=[ \t]*"/,"",v); sub(/".*/,"",v); proto=toupper(v) }
        if (match(line, /[ \t]*start_port[ \t]*=[ \t]*[0-9]+/)) { v=line; sub(/.*start_port[ \t]*=[ \t]*/,"",v); sub(/[^0-9].*/,"",v); sp=v+0 }
        if (match(line, /[ \t]*end_port[ \t]*=[ \t]*[0-9]+/))   { v=line; sub(/.*end_port[ \t]*=[ \t]*/,"",v); sub(/[^0-9].*/,"",v); ep=v+0 }
        if (match(line, /[ \t]*cidr[ \t]*=[ \t]*"[^"]*"/))      { v=line; sub(/.*cidr[ \t]*=[ \t]*"/,"",v); sub(/".*/,"",v); cidr=v }

        n=gsub(/{/,"{"); m=gsub(/}/,"}"); bdepth+=n-m
        if (bdepth<=0) {
          # block closed — evaluate
          openworld=(cidr=="0.0.0.0/0" || cidr=="::/0")
          ssh=(sp!="" && ep!="" && sp+0<=22 && ep+0>=22)
          ingress=(intype=="" || intype=="INGRESS")
          tcp=(proto=="" || proto=="TCP")
          if (openworld && ingress) {
            if (ssh && tcp) {
              printf("EXO-001 (HIGH) %s: rule \"%s\" exposes SSH (22) INGRESS to %s\n", fname, rname, cidr)
              hits++
            } else {
              # any other public ingress: RDP 3389, VNC 5900, all-ports, non-TCP, etc.
              portdesc=(sp=="" && ep=="") ? "all ports" : (sp==ep ? "port " sp : "ports " sp "-" ep)
              protodesc=(proto=="") ? "ALL" : proto
              printf("EXO-002 (HIGH) %s: rule \"%s\" exposes %s/%s INGRESS to %s\n", fname, rname, protodesc, portdesc, cidr)
              hits++
            }
          }
          inblock=0
        }
      }
    }
    END { exit (hits>0 ? 1 : 0) }
  ' "$file" || findings=1
done < <(find "$DIR" -type f -name '*.tf' -not -path '*/.terraform/*' -print0)

if [ "$findings" -ne 0 ]; then
  echo "exoscale-policy: HIGH findings above. Scope each rule to a specific CIDR (e.g. an" >&2
  echo "  admin /32) or bind the service to a private/overlay network — no public ingress." >&2
  exit 1
fi
echo "exoscale-policy: no findings"
