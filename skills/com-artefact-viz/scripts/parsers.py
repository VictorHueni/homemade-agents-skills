"""
parsers.py — canonical Markdown -> normalized model (com-artefact-viz).

Each parser reads exactly the Markdown shape its source skill emits and returns
a plain dict ("the model"). Renderers consume the model and never touch raw
Markdown. When a source skill's output template evolves, only the matching
parser here changes — the renderer and templates stay put.

Source shapes (see references/parsing-contract.md for the full contract):
  capability map  -> business-capability-map  (docs/business/03a-capability-map.md)
  fbs             -> spec-functional-breakdown-structure (docs/product-specs/07a-fbs.md)
  delivery roadmap-> plan-delivery-roadmap     (docs/plans/delivery-roadmap.md)
  bmc / lean      -> business-model-canvas      (docs/business/02a-bmc.md | 02a-lean-canvas.md)

Standard library only.
"""

import re

# --------------------------------------------------------------------------- #
# Shared helpers
# --------------------------------------------------------------------------- #

CAP_ID = re.compile(r"\bC\d+(?:\.\d+)*\b")
FUNC_ID = re.compile(r"\bC\d+(?:\.\d+)+\.F\d+\b")
EPIC_ID = re.compile(r"\bE-\d+\b")

STATUS_MAP = {"✅": "shipped", "🔄": "planned", "⬜": "backlog"}


def strip_frontmatter(text):
    """Drop a leading YAML frontmatter block (--- ... ---) if present."""
    if text.startswith("---"):
        end = text.find("\n---", 3)
        if end != -1:
            nl = text.find("\n", end + 1)
            return text[nl + 1 :] if nl != -1 else ""
    return text


def doc_title(text):
    """First level-1 heading, with the artefact-type suffix kept verbatim."""
    for line in text.splitlines():
        if line.startswith("# "):
            return line[2:].strip()
    return "Untitled"


def is_placeholder(value):
    """True for scaffold placeholders the renderer should treat as empty."""
    if value is None:
        return True
    v = value.strip()
    if not v:
        return True
    low = v.lower()
    return (
        v == "_TODO_"
        or low in ("_todo_", "tbd", "_tbd_")
        or (v.startswith("[") and v.endswith("]"))
        or (v.startswith("{{") and v.endswith("}}"))
    )


def clean(value):
    """Strip markdown emphasis/link syntax for plain-text display."""
    if value is None:
        return ""
    v = value.strip()
    v = re.sub(r"\[([^\]]+)\]\([^)]*\)", r"\1", v)  # [text](url) -> text
    v = v.replace("**", "").replace("`", "")
    v = v.strip(" _*")
    return v


def split_h2(text):
    """Return {heading_text: body} for every level-2 (## ) section."""
    out = {}
    cur = None
    buf = []
    for line in text.splitlines():
        m = re.match(r"^##\s+(.*\S)\s*$", line)
        if m and not line.startswith("###"):
            if cur is not None:
                out[cur] = "\n".join(buf)
            cur = m.group(1).strip()
            buf = []
        else:
            if cur is not None:
                buf.append(line)
    if cur is not None:
        out[cur] = "\n".join(buf)
    return out


def find_section(sections, *keywords):
    """First section whose heading contains all keywords (case-insensitive)."""
    for head, body in sections.items():
        low = head.lower()
        if all(k.lower() in low for k in keywords):
            return body
    return None


def first_code_block(body):
    """Contents of the first fenced ``` block in a section body."""
    if body is None:
        return None
    m = re.search(r"```[^\n]*\n(.*?)```", body, re.DOTALL)
    return m.group(1) if m else None


def parse_table(body):
    """
    Parse the first GFM table in `body`. Returns (headers, rows) where each row
    is a list of cell strings aligned to headers. Header/separator rows excluded.
    """
    if not body:
        return [], []
    lines = [l for l in body.splitlines() if l.strip().startswith("|")]
    if len(lines) < 2:
        return [], []

    def cells(line):
        parts = line.strip().strip("|").split("|")
        return [c.strip() for c in parts]

    headers = cells(lines[0])
    rows = []
    for line in lines[2:]:  # skip header + separator
        if re.match(r"^\s*\|[\s:|-]+\|?\s*$", line):  # stray separator
            continue
        c = cells(line)
        if any(cell.strip() for cell in c):
            rows.append(c)
    return headers, rows


def row_dict(headers, row):
    """Zip a row to its headers (tolerating short/long rows)."""
    d = {}
    for i, h in enumerate(headers):
        d[h] = row[i] if i < len(row) else ""
    return d


def first_status_symbol(text):
    for sym, name in STATUS_MAP.items():
        if sym in text:
            return name
    return None


# --------------------------------------------------------------------------- #
# Tree from the "Global overview" ASCII block (capability map + FBS share it)
# --------------------------------------------------------------------------- #

def parse_overview_tree(code, strip_after=None):
    """
    Parse the ASCII overview block into a nested tree keyed by capability ID.
    Nesting is derived from the ID's dot-depth (C1 -> C1.1 -> C1.1.1), which is
    far more robust than counting box-drawing indentation.

    Returns a list of root nodes: {id, label, level, children: [...]}.
    `strip_after` truncates the label at that substring (FBS appends counts).
    """
    if not code:
        return []
    by_id = {}
    order = []
    for raw in code.splitlines():
        m = CAP_ID.search(raw)
        if not m:
            continue
        cid = m.group(0)
        # Label = text after the ID, minus a leading "· " separator.
        tail = raw[m.end():]
        tail = re.sub(r"^[\s·–-]+", "", tail)
        if strip_after and strip_after in tail:
            tail = tail.split(strip_after)[0]
        label = clean(tail)
        if cid in by_id:  # ignore duplicate appearances
            continue
        node = {
            "id": cid,
            "label": "" if is_placeholder(label) else label,
            "level": cid.count("."),
            "children": [],
        }
        by_id[cid] = node
        order.append(cid)

    roots = []
    for cid in order:
        node = by_id[cid]
        parent_id = cid.rsplit(".", 1)[0] if "." in cid else None
        if parent_id and parent_id in by_id:
            by_id[parent_id]["children"].append(node)
        else:
            roots.append(node)
    return roots


# --------------------------------------------------------------------------- #
# Capability map
# --------------------------------------------------------------------------- #

def parse_capability_map(text):
    text = strip_frontmatter(text)
    sections = split_h2(text)
    title = doc_title(text)

    # L0 axis label -> default left-axis arrow text (project-overridable later).
    axis = None
    m = re.search(r"\*\*Chosen axis:\*\*\s*(.+)", text)
    if m:
        axis = clean(m.group(1))
        if is_placeholder(axis):
            axis = None

    tree = parse_overview_tree(first_code_block(find_section(sections, "global", "overview")))

    # Enrich each node from the "Capability index" table.
    index = {}
    headers, rows = parse_table(find_section(sections, "capability", "index") or "")
    if headers:
        hmap = {h.lower(): i for i, h in enumerate(headers)}
        id_i = hmap.get("id", 0)
        name_i = hmap.get("name", 1)
        imp_i = next((i for h, i in hmap.items() if "importance" in h), None)
        def_i = next((i for h, i in hmap.items() if "definition" in h), None)
        for row in rows:
            rid_m = CAP_ID.search(row[id_i] if id_i < len(row) else "")
            if not rid_m:
                continue
            rid = rid_m.group(0)
            importance = None
            if imp_i is not None and imp_i < len(row):
                raw_imp = row[imp_i].lower()
                if "/" not in raw_imp and not is_placeholder(row[imp_i]):
                    for kw in ("differentiator", "necessary", "commodity"):
                        if kw in raw_imp:
                            importance = kw
                            break
            definition = ""
            if def_i is not None and def_i < len(row) and not is_placeholder(row[def_i]):
                definition = clean(row[def_i])
            index[rid] = {
                "name": clean(row[name_i]) if name_i < len(row) else "",
                "importance": importance,
                "definition": definition,
            }

    def enrich(node):
        meta = index.get(node["id"])
        if meta:
            if not node["label"] and meta["name"]:
                node["label"] = meta["name"]
            node["importance"] = meta.get("importance")
            node["definition"] = meta.get("definition", "")
        else:
            node.setdefault("importance", None)
            node.setdefault("definition", "")
        for ch in node["children"]:
            enrich(ch)

    for n in tree:
        enrich(n)

    return {
        "kind": "capability-map",
        "title": title,
        "left_axis_label": axis,
        "tree": tree,
    }


# --------------------------------------------------------------------------- #
# Functional Breakdown Structure
# --------------------------------------------------------------------------- #

def parse_fbs(text):
    text = strip_frontmatter(text)
    sections = split_h2(text)
    title = doc_title(text)

    axis = None
    m = re.search(r"\*\*Chosen axis:\*\*\s*(.+)", text)
    if m:
        axis = clean(re.sub(r"\*\(inherited.*?\)\*", "", m.group(1)))
        if is_placeholder(axis):
            axis = None

    tree = parse_overview_tree(
        first_code_block(find_section(sections, "global", "overview")),
        strip_after="(functionalities",
    )

    # Functionalities live in per-capability tables anywhere in the doc.
    funcs_by_cap = {}
    for body in sections.values():
        headers, rows = parse_table(body)
        if not headers:
            continue
        lower = [h.lower() for h in headers]
        if "id" not in lower or not any("functional" in h for h in lower):
            continue
        id_i = lower.index("id")
        name_i = next((i for i, h in enumerate(lower) if "functional" in h), 1)
        status_i = next((i for i, h in enumerate(lower) if "status" in h), None)
        vs_i = next((i for i, h in enumerate(lower) if "vs" in h or "stage" in h), None)
        for row in rows:
            fid_m = FUNC_ID.search(row[id_i] if id_i < len(row) else "")
            if not fid_m:
                continue
            fid = fid_m.group(0)
            cap_id = fid.rsplit(".F", 1)[0]
            status = None
            if status_i is not None and status_i < len(row):
                status = first_status_symbol(row[status_i])
            vs = ""
            if vs_i is not None and vs_i < len(row) and not is_placeholder(row[vs_i]):
                vs = clean(row[vs_i])
            funcs_by_cap.setdefault(cap_id, []).append({
                "id": fid,
                "label": clean(row[name_i]) if name_i < len(row) else "",
                "status": status or "backlog",
                "vs": vs,
            })

    # Attach functionalities to their leaf capability nodes.
    def attach(node):
        for ch in node["children"]:
            attach(ch)
        node["functionalities"] = funcs_by_cap.get(node["id"], [])

    for n in tree:
        attach(n)

    counts = {"shipped": 0, "planned": 0, "backlog": 0}
    for flist in funcs_by_cap.values():
        for f in flist:
            counts[f["status"]] = counts.get(f["status"], 0) + 1

    return {
        "kind": "fbs",
        "title": title,
        "left_axis_label": axis,
        "tree": tree,
        "counts": counts,
    }


# --------------------------------------------------------------------------- #
# Delivery roadmap
# --------------------------------------------------------------------------- #

def _pain_level(text):
    low = (text or "").lower()
    for level in ("critical", "high", "medium", "low"):
        if level in low:
            return level
    return None


def parse_roadmap(text):
    text = strip_frontmatter(text)
    sections = split_h2(text)
    title = doc_title(text)

    # Walking skeleton -------------------------------------------------------
    ws_body = find_section(sections, "walking", "skeleton") or ""
    ws = {"hypothesis": "", "value_stream": "", "can": [], "cannot": []}
    m = re.search(r"\*\*Hypothesis[^:]*:\*\*\s*(.+)", ws_body)
    if m and not is_placeholder(m.group(1)):
        ws["hypothesis"] = clean(m.group(1))
    m = re.search(r"\*\*Value stream[^:]*:\*\*\s*(.+)", ws_body)
    if m and not is_placeholder(m.group(1)):
        ws["value_stream"] = clean(m.group(1))
    # "can" / "cannot yet" bullet lists
    can_mode = None
    for line in ws_body.splitlines():
        cl = line.strip()
        if "can:" in cl.lower() and "cannot" not in cl.lower():
            can_mode = "can"
            continue
        if "cannot" in cl.lower():
            can_mode = "cannot"
            continue
        bullet = re.match(r"^(?:[-*]|\d+\.)\s+(.*)", cl)
        if bullet and can_mode and not is_placeholder(bullet.group(1)):
            ws[can_mode].append(clean(bullet.group(1)))

    # Phase plan -------------------------------------------------------------
    phases = []
    headers, rows = parse_table(find_section(sections, "phase", "plan") or "")
    if headers:
        lower = [h.lower() for h in headers]
        p_i = 0
        e_i = next((i for i, h in enumerate(lower) if "epic" in h), 1)
        vs_i = next((i for i, h in enumerate(lower) if "value stream" in h or "operational" in h), None)
        g_i = next((i for i, h in enumerate(lower) if "goal" in h), None)
        for row in rows:
            name = clean(row[p_i]) if p_i < len(row) else ""
            if is_placeholder(name):
                continue
            phases.append({
                "name": name,
                "epics_raw": clean(row[e_i]) if e_i < len(row) else "",
                "vs_operational": clean(row[vs_i]) if vs_i is not None and vs_i < len(row) else "",
                "goal": clean(row[g_i]) if g_i is not None and g_i < len(row) else "",
                "epics": [],
            })

    # Epic table -------------------------------------------------------------
    epics = []
    epic_by_id = {}
    headers, rows = parse_table(find_section(sections, "epic", "table") or "")
    if headers:
        lower = [h.lower() for h in headers]
        def col(*names):
            for i, h in enumerate(lower):
                if any(n in h for n in names):
                    return i
            return None
        c_id = col("id")
        c_name = col("epic name", "name")
        c_vs = col("vs anchor", "anchor")
        c_pain = col("pain")
        c_pers = col("persona")
        c_caps = col("capabilit")
        c_phase = col("phase")
        c_prd = col("prd")
        c_status = col("status")
        for row in rows:
            d = row_dict(headers, row)
            eid_m = EPIC_ID.search(row[c_id]) if c_id is not None and c_id < len(row) else None
            if not eid_m:
                continue
            eid = eid_m.group(0)
            def g(i):
                return clean(row[i]) if i is not None and i < len(row) and not is_placeholder(row[i]) else ""
            epic = {
                "id": eid,
                "name": g(c_name),
                "vs_anchor": g(c_vs),
                "pain": _pain_level(row[c_pain]) if c_pain is not None and c_pain < len(row) else None,
                "personas": g(c_pers),
                "capabilities": g(c_caps),
                "phase": g(c_phase),
                "prd": g(c_prd),
                "status": first_status_symbol(row[c_status]) if c_status is not None and c_status < len(row) else None,
                "value_statement": "",
                "fbs_scope": [],
            }
            epics.append(epic)
            epic_by_id[eid] = epic

    # Per-epic sections (### E-NN) -> value statement + FBS scope -------------
    epic_sections = re.split(r"^###\s+", find_section(sections, "epics") or "", flags=re.MULTILINE)
    for chunk in epic_sections:
        eid_m = EPIC_ID.search(chunk[:40])
        if not eid_m:
            continue
        epic = epic_by_id.get(eid_m.group(0))
        if not epic:
            continue
        m = re.search(r"\*\*Value statement:\*\*\s*(.+)", chunk)
        if m and not is_placeholder(m.group(1)):
            epic["value_statement"] = clean(m.group(1))
        _, frows = parse_table(chunk)
        for r in frows:
            fid_m = FUNC_ID.search(" ".join(r))
            if not fid_m:
                continue
            epic["fbs_scope"].append({
                "id": fid_m.group(0),
                "label": clean(r[1]) if len(r) > 1 else "",
                "status": first_status_symbol(" ".join(r)) or "backlog",
            })

    # Bucket epics into phases. Prefer the epic's own Phase column; fall back to
    # matching epic IDs named in the phase-plan row.
    def phase_key(name):
        m = re.search(r"(mvp|phase\s*\d+|\d+)", name.lower())
        return m.group(0).replace(" ", "") if m else name.lower()

    if phases:
        index = {phase_key(p["name"]): p for p in phases}
        for epic in epics:
            placed = False
            pk = phase_key(epic["phase"]) if epic["phase"] else None
            if pk and pk in index:
                index[pk]["epics"].append(epic)
                placed = True
            if not placed:
                for p in phases:
                    if epic["id"] in p["epics_raw"]:
                        p["epics"].append(epic)
                        placed = True
                        break
            if not placed and phases:
                phases[0]["epics"].append(epic)
    else:
        # No phase plan: synthesize columns from distinct Phase values.
        seen = {}
        for epic in epics:
            key = epic["phase"] or "Unscheduled"
            if key not in seen:
                seen[key] = {"name": key, "epics": [], "vs_operational": "", "goal": "", "epics_raw": ""}
                phases.append(seen[key])
            seen[key]["epics"].append(epic)

    return {
        "kind": "delivery-roadmap",
        "title": title,
        "walking_skeleton": ws,
        "phases": phases,
        "epic_count": len(epics),
    }


# --------------------------------------------------------------------------- #
# Business Model Canvas / Lean Canvas
# --------------------------------------------------------------------------- #

# grid-area name per canonical block key, for each variant.
BMC_AREAS = {
    "8": "kp", "7": "ka", "6": "kr", "2": "vp", "4": "cr",
    "3": "ch", "1": "cs", "9": "cost", "5": "rev",
}
LEAN_AREAS = {
    "8'": "prob", "7'": "sol", "6'": "metrics", "2": "uvp", "4'": "adv",
    "3": "ch", "1": "cs", "9": "cost", "5": "rev",
}


def parse_bmc(text):
    text = strip_frontmatter(text)
    title = doc_title(text)

    variant = "BMC"
    m = re.search(r"\*\*Variant chosen:\*\*\s*(.+)", text)
    if m and "lean" in m.group(1).lower():
        variant = "Lean Canvas"
    elif "lean canvas" in title.lower():
        variant = "Lean Canvas"

    # Only parse blocks before the deep-dives / VPC template sections.
    cut = len(text)
    for marker in ("## Value Proposition Deep-dives", "## Inter-block", "# VPC Companion"):
        idx = text.find(marker)
        if idx != -1:
            cut = min(cut, idx)
    body = text[:cut]

    blocks = []
    # Block headings look like "### 1 · Customer Segments" or "### 4' · Unfair Advantage".
    parts = re.split(r"^###\s+", body, flags=re.MULTILINE)
    for chunk in parts[1:]:
        head_line = chunk.splitlines()[0]
        hm = re.match(r"(\d+'?)\s*·\s*(.+)", head_line.strip())
        if not hm:
            continue
        key = hm.group(1)
        name = clean(re.sub(r"\*\(.*?\)\*", "", hm.group(2)))
        # Bullets (skip blockquote notes and italics-only guidance lines).
        bullets = []
        for line in chunk.splitlines()[1:]:
            bm = re.match(r"^\s*[-*]\s+(.*)", line)
            if not bm:
                continue
            val = bm.group(1).strip()
            if is_placeholder(val):
                continue
            bullets.append(clean(val))
        confidence = None
        cm = re.search(r"\*\*Confidence:\*\*\s*(\w+)", chunk)
        if cm:
            confidence = cm.group(1).strip().lower()
        areas = LEAN_AREAS if variant == "Lean Canvas" else BMC_AREAS
        blocks.append({
            "key": key,
            "name": name,
            "bullets": bullets,
            "confidence": confidence,
            "area": areas.get(key),
        })

    # Keep only blocks that belong to the chosen variant's grid (drop the
    # alternate variant's blocks, e.g. Lean's 4'/6'/7'/8' in a BMC doc).
    blocks = [b for b in blocks if b["area"]]

    return {
        "kind": "bmc",
        "title": title,
        "variant": variant,
        "blocks": blocks,
    }


# --------------------------------------------------------------------------- #
# Service blueprint — a COMPOSITION lens (multi-source, derived)
#
# Unlike the four single-file parsers above, this one composes several canonical
# artefacts into one cross-process customer-visibility view. It is NOT a second
# source of truth: it restates nothing — it reads the process docs (actors,
# systems, steps, handoffs, pain points), drapes them under value-stream phase
# columns, and DERIVES the only thing no source carries — the line of visibility
# — from persona type. Anything it cannot classify is surfaced, not guessed.
# Full derivation contract: references/parsing-contract.md.
# --------------------------------------------------------------------------- #

PERSONA_HEAD = re.compile(r"^###\s+(P-\d+)\s*·\s*(.+?)\s*$", re.MULTILINE)
PTYPE_KEYWORDS = ("customer", "served", "primary", "secondary", "supplemental", "negative")
VS_STAGE_HEAD = re.compile(r"^####\s+(VS-\d+\.\d+)\s*·\s*(.+?)\s*$", re.MULTILINE)
_STOPWORDS = {
    "the", "a", "an", "of", "and", "to", "in", "for", "with", "flow", "process",
    "system", "intake", "team", "dept", "department", "service", "s",
}


def _tokens(text):
    """Lower-case alphanumeric word set, stop-words removed — for fuzzy matching."""
    words = re.findall(r"[a-z0-9]+", (text or "").lower())
    return {w for w in words if w not in _STOPWORDS and len(w) > 1}


def parse_persona_index(texts):
    """
    Build {persona-id: {name, role, tokens, ptype}} from one or more persona
    docs. `ptype` is the lower-cased persona-type keyword (customer / served /
    primary / …) used to classify front/back-stage; None when absent.
    """
    index = {}
    for text in texts:
        text = strip_frontmatter(text)
        heads = list(PERSONA_HEAD.finditer(text))
        for i, m in enumerate(heads):
            pid = m.group(1)
            head_tail = m.group(2)
            # "Name — role tagline"  ->  name, role
            name, _, role = head_tail.partition("—")
            block = text[m.end(): heads[i + 1].start() if i + 1 < len(heads) else len(text)]
            ptype = None
            tm = re.search(r"\*\*Persona type:\*\*\s*([^\n|]+)", block)
            if tm and not is_placeholder(tm.group(1)):
                low = tm.group(1).lower()
                ptype = next((k for k in PTYPE_KEYWORDS if k in low), None)
            index[pid] = {
                "name": clean(name),
                "role": clean(role),
                "tokens": _tokens(name) | _tokens(role),
                "ptype": ptype,
            }
    return index


def parse_value_stream_phases(text, stream=None):
    """
    Ordered phase columns from a value-stream doc: one per `#### VS-N.M · Stage`
    heading, carrying the stage's pain index when present. `stream` (e.g. "VS-1")
    filters to a single stream; None keeps every stage in document order.
    """
    text = strip_frontmatter(text)
    heads = list(VS_STAGE_HEAD.finditer(text))
    phases = []
    for i, m in enumerate(heads):
        sid = m.group(1)
        if stream and not sid.startswith(stream + "."):
            continue
        name = clean(m.group(2))
        if is_placeholder(name):
            name = sid
        block = text[m.end(): heads[i + 1].start() if i + 1 < len(heads) else len(text)]
        pain = None
        pm = re.search(r"pain point index[^\n|]*\|\s*\**\s*(critical|high|medium|low)", block, re.I)
        if pm:
            pain = pm.group(1).lower()
        phases.append({"id": sid, "name": name, "pain": pain})
    return phases


def _section_after(text, *keywords):
    """§-body lookup that tolerates the process docs' numbered `## 3. Actors` heads."""
    return find_section(split_h2(strip_frontmatter(text)), *keywords)


def parse_process(text):
    """
    Extract the blueprint-relevant slice of one business-process doc:
    title, actors (§3), systems (§4 Data Stores), data-object handoffs (§5),
    per-actor numbered steps (§6) and pain points (§9). Defensive: every part
    degrades to empty when its section is missing or placeholder-filled.
    """
    text = strip_frontmatter(text)
    sections = split_h2(text)
    title = doc_title(text)
    slug = re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-") or "process"

    def first_col(sec_keywords):
        _, rows = parse_table(find_section(sections, *sec_keywords) or "")
        out = []
        for r in rows:
            name = clean(r[0]) if r else ""
            if name and not is_placeholder(name):
                out.append(name)
        return out

    actors = first_col(("actors",))
    systems = first_col(("data", "stores"))

    # §5 Data Objects -> handoffs (Object | Created by | Consumed by)
    objects = []
    headers, rows = parse_table(find_section(sections, "data", "objects") or "")
    if headers:
        lower = [h.lower() for h in headers]
        c_obj = 0
        c_from = next((i for i, h in enumerate(lower) if "created" in h), None)
        c_to = next((i for i, h in enumerate(lower) if "consumed" in h), None)
        for r in rows:
            d = row_dict(headers, r)
            obj = clean(r[c_obj]) if c_obj < len(r) else ""
            if not obj or is_placeholder(obj):
                continue
            objects.append({
                "object": obj,
                "from": clean(r[c_from]) if c_from is not None and c_from < len(r) else "",
                "to": clean(r[c_to]) if c_to is not None and c_to < len(r) else "",
            })

    # §6 Activities -> per-actor numbered steps (### 6.x {Actor}'s flow)
    steps_by_actor = {}
    activities = find_section(sections, "activities") or ""
    for chunk in re.split(r"^###\s+", activities, flags=re.MULTILINE)[1:]:
        head = chunk.splitlines()[0]
        actor = re.sub(r"^[0-9.]+\s*", "", head)            # drop "6.1 "
        actor = re.sub(r"['’]s\s+flow\s*$", "", actor, flags=re.I).strip()
        actor = re.sub(r"\bflow\s*$", "", actor, flags=re.I).strip()
        if not actor or is_placeholder(actor):
            continue
        steps = []
        for line in chunk.splitlines()[1:]:
            sm = re.match(r"^\s*\d+\.\s+(.*)", line)
            if not sm:
                continue
            raw = sm.group(1)
            nm = re.match(r"\*\*(.+?)\*\*\s*(?:—\s*(.*))?$", raw)
            label = clean(nm.group(1)) if nm else clean(raw)
            if label and not is_placeholder(label):
                steps.append(label)
        if steps:
            steps_by_actor[actor] = steps

    # §9 pain points -> who-experiences set (for fail flags) + the rows themselves
    pains = []
    pain_actors = set()
    headers, rows = parse_table(find_section(sections, "broken") or find_section(sections, "pain") or "")
    if headers:
        lower = [h.lower() for h in headers]
        c_pp = 0
        c_who = next((i for i, h in enumerate(lower) if "who" in h or "experien" in h), None)
        c_where = next((i for i, h in enumerate(lower) if "where" in h), None)
        for r in rows:
            pp = clean(r[c_pp]) if c_pp < len(r) else ""
            if not pp or is_placeholder(pp):
                continue
            who = clean(r[c_who]) if c_who is not None and c_who < len(r) else ""
            pains.append({
                "pain": pp,
                "who": who,
                "where": clean(r[c_where]) if c_where is not None and c_where < len(r) else "",
            })
            if who:
                pain_actors |= _tokens(who)

    return {
        "title": title,
        "slug": slug,
        "actors": actors,
        "systems": systems,
        "objects": objects,
        "steps_by_actor": steps_by_actor,
        "pains": pains,
        "pain_actors": pain_actors,
    }


# Band order, top -> bottom, with the three Shostack/Bitner control lines.
BLUEPRINT_BANDS = ["evidence", "customer", "frontstage", "backstage", "systems", "unclassified"]
CONTROL_LINES = {
    "frontstage": "line of interaction",
    "backstage": "line of visibility",
    "systems": "line of internal interaction",
}


def _resolve_persona(actor_name, persona_index):
    """Best persona match for an actor name by token overlap on name+role."""
    at = _tokens(actor_name)
    if not at:
        return None
    best, best_score = None, 0
    for pid, p in persona_index.items():
        score = len(at & p["tokens"])
        if score > best_score:
            best, best_score = p, score
    return best if best_score else None


def _looks_like_system(name):
    low = name.lower()
    return bool(re.search(r"\b(system|platform|service|api|engine|automation|bot|portal|registry|database|store)\b", low))


def parse_service_blueprint(proc_texts, vs_text=None, persona_texts=None, options=None):
    options = options or {}
    persona_index = parse_persona_index(persona_texts or [])
    phases = parse_value_stream_phases(vs_text, options.get("stream")) if vs_text else []

    procs = [parse_process(t) for t in proc_texts]
    title = options.get("title") or (
        f"Service Blueprint — {procs[0]['title']}" if procs else "Service Blueprint"
    )

    # ---- 1. Gather every actor (union of §3 + §6) with its source proc ------
    actor_order = []
    actor_seen = {}
    proc_pain_tokens = set()
    for proc in procs:
        proc_pain_tokens |= proc["pain_actors"]
        names = list(proc["actors"]) + [a for a in proc["steps_by_actor"] if a not in proc["actors"]]
        for name in names:
            key = name.lower()
            if key not in actor_seen:
                lane = {
                    "name": name, "proc": proc["slug"], "steps": [],
                    "persona": None, "ptype": None, "band": None, "fail": False,
                }
                actor_seen[key] = lane
                actor_order.append(lane)
            # steps come from the proc that documents this actor's §6 flow
            if name in proc["steps_by_actor"] and not actor_seen[key]["steps"]:
                actor_seen[key]["steps"] = proc["steps_by_actor"][name]

    # ---- 2. Resolve persona + classify into bands --------------------------
    customer_keys = set()
    for lane in actor_order:
        p = _resolve_persona(lane["name"], persona_index)
        if p:
            lane["persona"] = p["name"]
            lane["ptype"] = p["ptype"]
        if lane["ptype"] in ("customer", "served"):
            lane["band"] = "customer"
            customer_keys.add(lane["name"].lower())
        elif lane["ptype"] == "negative":
            lane["band"] = "drop"
        elif _looks_like_system(lane["name"]):
            lane["band"] = "systems"

    # touches_customer: an actor that exchanges a §5 data object with a customer
    # actor sits ABOVE the line of visibility (frontstage); otherwise backstage.
    touch = set()
    connectors = []
    for proc in procs:
        for obj in proc["objects"]:
            a, b = obj["from"].lower(), obj["to"].lower()
            if a and b:
                connectors.append({"object": obj["object"], "from": obj["from"], "to": obj["to"]})
            if a in customer_keys and b:
                touch.add(b)
            if b in customer_keys and a:
                touch.add(a)

    for lane in actor_order:
        if lane["band"] in ("customer", "systems", "drop"):
            continue
        if lane["persona"] is None and lane["ptype"] is None:
            lane["band"] = "unclassified"
        else:
            lane["band"] = "frontstage" if lane["name"].lower() in touch else "backstage"

    lanes = [l for l in actor_order if l["band"] != "drop"]

    # fail flag: actor named in any §9 "who experiences it" cell
    for lane in lanes:
        if _tokens(lane["name"]) & proc_pain_tokens:
            lane["fail"] = True

    # ---- 3. Phase columns (VS stages, else ordinal fallback) ---------------
    derived_phases = bool(phases)
    max_steps = max((len(l["steps"]) for l in lanes), default=0)
    if not phases:
        n = max_steps or 1
        phases = [{"id": None, "name": f"Step {i + 1}", "pain": None} for i in range(n)]
    nph = len(phases)

    # Place each step into a phase. VS columns: proportional ordinal mapping.
    # Synthesised columns: one step per column (direct ordinal). Deterministic —
    # no keyword guessing, so the view never silently mis-files a step.
    for lane in lanes:
        cells = [[] for _ in range(nph)]
        ns = len(lane["steps"])
        for i, step in enumerate(lane["steps"]):
            if derived_phases:
                pi = min(nph - 1, (i * nph) // ns) if ns else 0
            else:
                pi = min(i, nph - 1)
            cells[pi].append({"label": step, "fail": lane["fail"]})
        lane["cells"] = cells

    # ---- 4. Evidence band: customer-facing systems / handoff artefacts ------
    evidence = []
    seen_ev = set()
    for proc in procs:
        for obj in proc["objects"]:
            if (obj["from"].lower() in customer_keys or obj["to"].lower() in customer_keys):
                if obj["object"].lower() not in seen_ev:
                    evidence.append(obj["object"])
                    seen_ev.add(obj["object"].lower())

    # band -> ordered lanes
    by_band = {b: [l for l in lanes if l["band"] == b] for b in BLUEPRINT_BANDS}

    classified = sum(1 for l in lanes if l["band"] != "unclassified")
    return {
        "kind": "service-blueprint",
        "title": title,
        "phases": phases,
        "derived_phases": derived_phases,
        "by_band": by_band,
        "evidence": evidence,
        "connectors": connectors,
        "stats": {
            "procs": len(procs),
            "actors": len(lanes),
            "classified": classified,
            "unclassified": len(lanes) - classified,
            "personas": len(persona_index),
            "phases": nph,
        },
    }


# --------------------------------------------------------------------------- #
# Dispatch by source path / content
# --------------------------------------------------------------------------- #

PARSERS = {
    "capability-map": parse_capability_map,
    "fbs": parse_fbs,
    "delivery-roadmap": parse_roadmap,
    "bmc": parse_bmc,
}

# Multi-source kinds are handled directly by render.py (they take several files),
# so they live outside the single-text PARSERS map but are still valid --kind
# values and renderer keys.
MULTISOURCE_KINDS = ("service-blueprint",)


def detect_kind(path, text):
    """Guess the artefact type from filename, then from content headings."""
    p = path.lower()
    if "service-blueprint" in p or "service_blueprint" in p:
        return "service-blueprint"
    if "capability-map" in p or "capability_map" in p:
        return "capability-map"
    if "fbs" in p or "functional-breakdown" in p:
        return "fbs"
    if "roadmap" in p:
        return "delivery-roadmap"
    if "lean-canvas" in p or "bmc" in p or "canvas" in p:
        return "bmc"
    head = text[:4000].lower()
    if "business capability map" in head:
        return "capability-map"
    if "functional breakdown structure" in head:
        return "fbs"
    if "delivery roadmap" in head:
        return "delivery-roadmap"
    if "business model canvas" in head or "lean canvas" in head:
        return "bmc"
    return None
