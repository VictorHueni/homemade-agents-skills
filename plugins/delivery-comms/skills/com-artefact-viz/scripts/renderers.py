"""
renderers.py — normalized model -> HTML fragment (com-artefact-viz).

Each renderer returns a dict with:
  kind_label : short uppercase chip text
  meta       : one-line description under the title
  toolbar    : HTML for the toolbar controls (may be "")
  view_css   : CSS scoped to this view (token-driven; never hard-codes colour)
  content    : the main HTML fragment

render.py drops these into templates/base.html.tmpl. All visual styling flows
through CSS custom properties defined in templates/tokens.fallback.css (or a
project sheet), so renderers reference var(--token) and never literal colours.
"""

import html


def esc(s):
    return html.escape(s or "", quote=True)


# --------------------------------------------------------------------------- #
# Capability map
# --------------------------------------------------------------------------- #

def render_capability_map(model, options):
    axis = options.get("left_axis_label") or model.get("left_axis_label") or "Capabilities"
    arrow = options.get("left_axis_arrow", "▼")

    def importance_badge(imp):
        if not imp:
            return ""
        label = imp.capitalize()
        return f'<span class="cap-imp cap-imp--{esc(imp)}">{esc(label)}</span>'

    def render_cap(node):
        kids = node.get("children", [])
        body = ""
        if node.get("definition"):
            body += f'<p class="cap-def">{esc(node["definition"])}</p>'
        if kids:
            body += '<div class="cap-children">' + "".join(render_cap(k) for k in kids) + "</div>"
        return (
            f'<div class="cap-card cap-l{node["level"]}">'
            f'<div class="cap-head">'
            f'<span class="cap-id">{esc(node["id"])}</span>'
            f'<span class="cap-name">{esc(node["label"]) or "&nbsp;"}</span>'
            f'{importance_badge(node.get("importance"))}'
            f"</div>{body}</div>"
        )

    groups = "".join(
        f'<section class="cap-group">'
        f'<header class="cap-group-head"><span class="cap-id cap-id--l0">{esc(root["id"])}</span>'
        f'<span class="cap-name">{esc(root["label"])}</span></header>'
        f'<div class="cap-group-body">'
        + "".join(render_cap(child) for child in root.get("children", []))
        + "</div></section>"
        for root in model["tree"]
    )
    if not groups:
        content = '<p class="viz-empty">No capabilities found in the source map.</p>'
    else:
        content = (
            '<div class="cap-layout">'
            f'<div class="cap-axis" title="L0 axis"><span class="cap-axis-text">{esc(axis)} {esc(arrow)}</span></div>'
            f'<div class="cap-groups">{groups}</div>'
            "</div>"
        )

    view_css = """
.cap-layout { display: flex; gap: var(--space-md); align-items: stretch; }
.cap-axis { flex: 0 0 2.4rem; background: var(--surface-2); border-radius: var(--card-radius);
  display: flex; align-items: center; justify-content: center; }
.cap-axis-text { writing-mode: vertical-rl; transform: rotate(180deg); font-family: var(--font-mono);
  font-size: 0.78rem; letter-spacing: 0.12em; text-transform: uppercase; color: var(--muted); white-space: nowrap; }
.cap-groups { display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: var(--space-md); flex: 1; }
.cap-group { background: var(--surface-2); border-radius: var(--card-radius); padding: var(--space-sm); }
.cap-group-head { display: flex; gap: 0.4rem; align-items: baseline; padding: 0.3rem 0.4rem 0.6rem; }
.cap-group-head .cap-name { font-weight: 700; }
.cap-group-body { display: flex; flex-direction: column; gap: var(--space-sm); }
.cap-card { background: var(--surface); border: 1px solid var(--border); border-radius: var(--node-radius);
  padding: 0.55rem 0.7rem; box-shadow: var(--shadow); }
.cap-head { display: flex; gap: 0.45rem; align-items: baseline; flex-wrap: wrap; }
.cap-id { font-family: var(--font-mono); font-size: 0.72rem; color: var(--accent); font-weight: 700; }
.cap-id--l0 { color: var(--ink); }
.cap-name { font-size: 0.92rem; }
.cap-def { margin: 0.4rem 0 0; font-size: 0.8rem; color: var(--muted); }
.cap-children { margin-top: 0.5rem; padding-left: 0.6rem; border-left: 2px solid var(--surface-2);
  display: flex; flex-direction: column; gap: 0.4rem; }
.cap-imp { margin-left: auto; font-size: 0.62rem; text-transform: uppercase; letter-spacing: 0.04em;
  padding: 0.05rem 0.4rem; border-radius: 999px; color: var(--accent-ink); font-weight: 700; }
.cap-imp--differentiator { background: var(--differentiator); }
.cap-imp--necessary { background: var(--necessary); }
.cap-imp--commodity { background: var(--commodity); }
"""
    return {
        "kind_label": "capability map",
        "meta": f'{len(model["tree"])} L0 groups · grouped by axis "{esc(axis)}"',
        "toolbar": "",
        "view_css": view_css,
        "content": content,
    }


# --------------------------------------------------------------------------- #
# FBS — collapsible tree, horizontal/vertical
# --------------------------------------------------------------------------- #

def render_fbs(model, options):
    def status_dot(status):
        return f'<span class="st-dot st--{esc(status)}" title="{esc(status)}"></span>'

    def render_func(f):
        vs = f' <span class="fbs-vs">{esc(f["vs"])}</span>' if f.get("vs") else ""
        return (
            f'<li class="fbs-leaf">{status_dot(f["status"])}'
            f'<span class="fbs-id">{esc(f["id"])}</span>'
            f'<span class="fbs-label">{esc(f["label"]) or "&nbsp;"}</span>{vs}</li>'
        )

    def render_node(node):
        kids = node.get("children", [])
        funcs = node.get("functionalities", [])
        has_children = bool(kids or funcs)
        toggle = (
            '<button class="fbs-toggle" data-toggle aria-expanded="true" aria-label="Toggle"></button>'
            if has_children else '<span class="fbs-toggle fbs-toggle--leaf"></span>'
        )
        inner = ""
        if has_children:
            child_html = "".join(render_node(k) for k in kids)
            func_html = ("<ul class='fbs-funcs'>" + "".join(render_func(f) for f in funcs) + "</ul>") if funcs else ""
            inner = f'<div class="fbs-children" data-children><ul class="fbs-list">{child_html}</ul>{func_html}</div>'
        count = ""
        if funcs:
            count = f' <span class="fbs-count">{len(funcs)}</span>'
        return (
            f'<li class="fbs-node fbs-l{node["level"]}" data-node>'
            f'<div class="fbs-row">{toggle}'
            f'<span class="fbs-id">{esc(node["id"])}</span>'
            f'<span class="fbs-label">{esc(node["label"]) or "&nbsp;"}</span>{count}</div>'
            f"{inner}</li>"
        )

    nodes = "".join(render_node(n) for n in model["tree"])
    content = (
        f'<div class="fbs-tree tree--vertical" data-tree>'
        f'<ul class="fbs-list fbs-root">{nodes}</ul></div>'
    ) if nodes else '<p class="viz-empty">No capabilities found in the source FBS.</p>'

    c = model.get("counts", {})
    legend = (
        '<div class="fbs-legend">'
        f'{_count_chip("shipped", c.get("shipped", 0))}'
        f'{_count_chip("planned", c.get("planned", 0))}'
        f'{_count_chip("backlog", c.get("backlog", 0))}'
        "</div>"
    )
    toolbar = (
        '<button class="viz-btn" data-action="orient" aria-pressed="false">Orientation: vertical</button>'
        '<button class="viz-btn" data-action="expand-all">Expand all</button>'
        '<button class="viz-btn" data-action="collapse-all">Collapse all</button>'
        + legend
    )

    view_css = """
.fbs-legend { display: inline-flex; gap: 0.4rem; align-items: center; margin-left: auto; }
.count-chip { display: inline-flex; gap: 0.3rem; align-items: center; font-size: 0.72rem; color: var(--muted); }
.count-chip .st-dot { width: 0.6rem; height: 0.6rem; }
.st-dot { display: inline-block; width: 0.7rem; height: 0.7rem; border-radius: 50%; flex: 0 0 auto; }
.st--shipped { background: var(--status-shipped); }
.st--planned { background: var(--status-planned); }
.st--backlog { background: var(--status-backlog); }
.fbs-id { font-family: var(--font-mono); font-size: 0.72rem; color: var(--accent); font-weight: 700; }
.fbs-label { font-size: 0.9rem; }
.fbs-count { font-family: var(--font-mono); font-size: 0.68rem; color: var(--muted);
  background: var(--surface-2); border-radius: 999px; padding: 0 0.4rem; }
.fbs-vs { font-size: 0.68rem; color: var(--muted); font-style: italic; }
.fbs-list { list-style: none; margin: 0; padding: 0; }
.fbs-row { display: flex; align-items: center; gap: 0.45rem; padding: 0.3rem 0.5rem;
  background: var(--surface); border: 1px solid var(--border); border-radius: var(--node-radius);
  box-shadow: var(--shadow); }
.fbs-toggle { width: 1rem; height: 1rem; flex: 0 0 auto; border: none; background: transparent;
  cursor: pointer; padding: 0; position: relative; }
.fbs-toggle:not(.fbs-toggle--leaf)::before { content: "▾"; color: var(--muted); font-size: 0.8rem; }
.fbs-node.is-collapsed > .fbs-row > .fbs-toggle::before { content: "▸"; }
.fbs-node.is-collapsed > .fbs-children { display: none; }
.fbs-funcs { list-style: none; margin: 0.3rem 0 0; padding: 0; display: flex; flex-direction: column; gap: 0.25rem; }
.fbs-leaf { display: flex; align-items: center; gap: 0.4rem; font-size: 0.82rem;
  padding: 0.2rem 0.5rem; }

/* vertical: indented nested lists */
.tree--vertical .fbs-node { margin: 0.3rem 0; }
.tree--vertical .fbs-children { margin-left: 1.1rem; padding-left: 0.6rem;
  border-left: 2px solid var(--surface-2); margin-top: 0.3rem; }

/* horizontal: each node's children laid out as a column to the right */
.tree--horizontal .fbs-root { display: flex; gap: 1.5rem; align-items: flex-start; }
.tree--horizontal .fbs-node { display: flex; flex-direction: column; }
.tree--horizontal .fbs-children { display: flex; gap: 1.5rem; margin-top: 0.6rem; }
.tree--horizontal .fbs-children > .fbs-list { display: flex; gap: 1rem; }
.tree--horizontal .fbs-row { white-space: nowrap; }
.tree--horizontal .fbs-funcs { min-width: 180px; }
"""
    return {
        "kind_label": "FBS",
        "meta": f'{sum(model.get("counts", {}).values())} functionalities · '
                f'{c.get("shipped", 0)} shipped · {c.get("planned", 0)} planned · {c.get("backlog", 0)} backlog',
        "toolbar": toolbar,
        "view_css": view_css,
        "content": content,
    }


def _count_chip(status, n):
    return f'<span class="count-chip"><span class="st-dot st--{status}"></span>{n} {status}</span>'


# --------------------------------------------------------------------------- #
# Delivery roadmap — phase-column timeline
# --------------------------------------------------------------------------- #

def render_roadmap(model, options):
    ws = model.get("walking_skeleton", {})
    ws_html = ""
    if ws.get("hypothesis") or ws.get("can") or ws.get("cannot"):
        can = "".join(f"<li>{esc(x)}</li>" for x in ws.get("can", []))
        cannot = "".join(f"<li>{esc(x)}</li>" for x in ws.get("cannot", []))
        cols = ""
        if can:
            cols += f'<div class="ws-col"><h4 class="ws-h ws-h--can">Can do</h4><ul>{can}</ul></div>'
        if cannot:
            cols += f'<div class="ws-col"><h4 class="ws-h ws-h--cannot">Cannot yet</h4><ul>{cannot}</ul></div>'
        hyp = f'<p class="ws-hyp"><strong>Hypothesis:</strong> {esc(ws["hypothesis"])}</p>' if ws.get("hypothesis") else ""
        vs = f'<p class="ws-vs">End-to-end value stream: {esc(ws["value_stream"])}</p>' if ws.get("value_stream") else ""
        ws_html = f'<section class="ws-band"><h3 class="ws-title">Walking skeleton — MVP</h3>{hyp}{vs}<div class="ws-cols">{cols}</div></section>'

    def epic_card(epic):
        pain = epic.get("pain")
        pain_cls = f" epic--{pain}" if pain else ""
        chips = []
        if epic.get("personas"):
            chips.append(f'<span class="epic-chip">{esc(epic["personas"])}</span>')
        if epic.get("capabilities"):
            chips.append(f'<span class="epic-chip">{esc(epic["capabilities"])}</span>')
        if epic.get("status"):
            chips.append(f'<span class="epic-chip st--{esc(epic["status"])}">{esc(epic["status"])}</span>')
        chip_html = f'<div class="epic-chips">{"".join(chips)}</div>' if chips else ""
        vstmt = f'<p class="epic-vstmt">{esc(epic["value_statement"])}</p>' if epic.get("value_statement") else ""
        scope = epic.get("fbs_scope", [])
        scope_html = ""
        disclose = ""
        if scope:
            items = "".join(
                f'<li><span class="st-dot st--{esc(s["status"])}"></span>'
                f'<span class="fbs-id">{esc(s["id"])}</span> {esc(s["label"])}</li>'
                for s in scope
            )
            scope_html = f'<ul class="epic-scope">{items}</ul>'
            disclose = f'<button class="epic-disclose" data-disclose>{len(scope)} features ▾</button>'
        return (
            f'<article class="epic-card{pain_cls}" data-card>'
            f'<header class="epic-head"><span class="epic-id">{esc(epic["id"])}</span>'
            f'<span class="epic-name">{esc(epic["name"])}</span></header>'
            f'{vstmt}{chip_html}{disclose}{scope_html}</article>'
        )

    columns = ""
    for p in model["phases"]:
        cards = "".join(epic_card(e) for e in p.get("epics", []))
        if not cards:
            cards = '<p class="phase-empty">—</p>'
        sub = []
        if p.get("vs_operational"):
            sub.append(f'<span class="phase-vs">VS operational: {esc(p["vs_operational"])}</span>')
        goal = f'<p class="phase-goal">{esc(p["goal"])}</p>' if p.get("goal") else ""
        columns += (
            f'<div class="phase-col">'
            f'<header class="phase-head"><span class="phase-name">{esc(p["name"])}</span>'
            f'{"".join(sub)}</header>{goal}'
            f'<div class="phase-epics">{cards}</div></div>'
        )
    timeline = f'<div class="timeline">{columns}</div>' if columns else '<p class="viz-empty">No phases found in the roadmap.</p>'
    content = ws_html + timeline

    view_css = """
.ws-band { background: var(--surface-2); border-radius: var(--card-radius); padding: var(--space-md);
  margin-bottom: var(--space-lg); border-left: 4px solid var(--accent); }
.ws-title { margin: 0 0 0.4rem; font-size: 1rem; }
.ws-hyp, .ws-vs { margin: 0.2rem 0; font-size: 0.85rem; color: var(--ink); }
.ws-vs { color: var(--muted); }
.ws-cols { display: flex; gap: var(--space-lg); margin-top: 0.6rem; flex-wrap: wrap; }
.ws-col { flex: 1 1 240px; }
.ws-col ul { margin: 0.3rem 0 0; padding-left: 1.1rem; font-size: 0.82rem; }
.ws-h { margin: 0; font-size: 0.78rem; text-transform: uppercase; letter-spacing: 0.05em; }
.ws-h--can { color: var(--status-shipped); }
.ws-h--cannot { color: var(--pain-high); }

.timeline { display: flex; gap: var(--space-md); overflow-x: auto; padding-bottom: 0.5rem;
  position: relative; }
.timeline::before { content: ""; position: absolute; top: 1.4rem; left: 0; right: 0; height: 2px;
  background: var(--border); z-index: 0; }
.phase-col { flex: 1 0 260px; min-width: 260px; position: relative; z-index: 1; }
.phase-head { display: flex; flex-direction: column; gap: 0.15rem; padding: 0.3rem 0; }
.phase-name { font-weight: 700; font-size: 0.95rem; display: inline-flex; align-items: center; gap: 0.4rem; }
.phase-name::before { content: ""; width: 0.8rem; height: 0.8rem; border-radius: 50%;
  background: var(--accent); display: inline-block; }
.phase-vs { font-size: 0.7rem; color: var(--muted); }
.phase-goal { font-size: 0.78rem; color: var(--muted); margin: 0.2rem 0 0.6rem; }
.phase-epics { display: flex; flex-direction: column; gap: var(--space-sm); }
.phase-empty { color: var(--muted); }
.epic-card { background: var(--surface); border: 1px solid var(--border); border-left: 4px solid var(--border);
  border-radius: var(--node-radius); padding: 0.6rem 0.7rem; box-shadow: var(--shadow); }
.epic-card.epic--critical { border-left-color: var(--pain-critical); }
.epic-card.epic--high { border-left-color: var(--pain-high); }
.epic-card.epic--medium { border-left-color: var(--pain-medium); }
.epic-card.epic--low { border-left-color: var(--pain-low); }
.epic-head { display: flex; gap: 0.4rem; align-items: baseline; }
.epic-id { font-family: var(--font-mono); font-size: 0.72rem; color: var(--accent); font-weight: 700; }
.epic-name { font-size: 0.9rem; font-weight: 600; }
.epic-vstmt { font-size: 0.8rem; color: var(--muted); margin: 0.35rem 0 0.4rem; }
.epic-chips { display: flex; flex-wrap: wrap; gap: 0.3rem; }
.epic-chip { font-size: 0.66rem; font-family: var(--font-mono); background: var(--surface-2);
  color: var(--ink); border-radius: 999px; padding: 0.05rem 0.45rem; }
.epic-chip.st--shipped { background: var(--status-shipped); color: var(--accent-ink); }
.epic-chip.st--planned { background: var(--status-planned); color: var(--accent-ink); }
.epic-chip.st--backlog { background: var(--status-backlog); color: var(--accent-ink); }
.epic-disclose { margin-top: 0.45rem; font: inherit; font-size: 0.72rem; cursor: pointer;
  background: transparent; border: none; color: var(--accent); padding: 0; }
.epic-scope { display: none; list-style: none; margin: 0.4rem 0 0; padding: 0;
  font-size: 0.76rem; flex-direction: column; gap: 0.2rem; }
.epic-scope li { display: flex; align-items: center; gap: 0.35rem; }
.epic-card.is-open .epic-scope { display: flex; }
.st-dot { display: inline-block; width: 0.6rem; height: 0.6rem; border-radius: 50%; flex: 0 0 auto; }
.st--shipped { background: var(--status-shipped); } .st--planned { background: var(--status-planned); }
.st--backlog { background: var(--status-backlog); }
.fbs-id { font-family: var(--font-mono); font-size: 0.7rem; color: var(--accent); }
"""
    return {
        "kind_label": "delivery roadmap",
        "meta": f'{len(model["phases"])} phases · {model.get("epic_count", 0)} epics',
        "toolbar": "",
        "view_css": view_css,
        "content": content,
    }


# --------------------------------------------------------------------------- #
# Business Model Canvas / Lean Canvas
# --------------------------------------------------------------------------- #

BMC_TEMPLATE = '"kp ka vp cr cs" "kp kr vp ch cs" "cost cost cost rev rev"'
LEAN_TEMPLATE = '"prob sol uvp adv cs" "prob metrics uvp ch cs" "cost cost cost rev rev"'


def render_bmc(model, options):
    blocks = model["blocks"]

    def block_cell(b):
        conf = b.get("confidence")
        conf_html = (
            f'<span class="bmc-conf bmc-conf--{esc(conf)}" title="confidence: {esc(conf)}">{esc(conf)}</span>'
            if conf else ""
        )
        bullets = "".join(f"<li>{esc(x)}</li>" for x in b["bullets"]) or '<li class="bmc-empty">—</li>'
        return (
            f'<section class="bmc-cell" style="grid-area: {esc(b["area"])}">'
            f'<header class="bmc-cell-head"><span class="bmc-key">{esc(b["key"])}</span>'
            f'<span class="bmc-name">{esc(b["name"])}</span>{conf_html}</header>'
            f'<ul class="bmc-bullets">{bullets}</ul></section>'
        )

    cells = "".join(block_cell(b) for b in blocks)
    template = LEAN_TEMPLATE if model["variant"] == "Lean Canvas" else BMC_TEMPLATE
    content = (
        f'<div class="bmc-grid" style="grid-template-areas: {template};">{cells}</div>'
        if cells else '<p class="viz-empty">No canvas blocks found.</p>'
    )

    view_css = """
.bmc-grid { display: grid; grid-template-columns: repeat(5, 1fr); gap: 2px;
  background: var(--border); border: 1px solid var(--border); border-radius: var(--card-radius); overflow: hidden; }
.bmc-cell { background: var(--surface); padding: 0.6rem 0.7rem; display: flex; flex-direction: column; min-height: 120px; }
.bmc-cell-head { display: flex; gap: 0.4rem; align-items: baseline; margin-bottom: 0.4rem; flex-wrap: wrap; }
.bmc-key { font-family: var(--font-mono); font-size: 0.7rem; color: var(--accent); font-weight: 700; }
.bmc-name { font-size: 0.82rem; font-weight: 700; }
.bmc-conf { margin-left: auto; font-size: 0.6rem; text-transform: uppercase; letter-spacing: 0.04em;
  padding: 0.05rem 0.4rem; border-radius: 999px; color: var(--accent-ink); }
.bmc-conf--assumed { background: var(--conf-assumed); }
.bmc-conf--tested { background: var(--conf-tested); }
.bmc-conf--validated { background: var(--conf-validated); }
.bmc-bullets { margin: 0; padding-left: 1rem; font-size: 0.78rem; display: flex; flex-direction: column; gap: 0.2rem; }
.bmc-empty { list-style: none; margin-left: -1rem; color: var(--muted); }
@media (max-width: 900px) {
  .bmc-grid { grid-template-columns: 1fr 1fr; grid-template-areas: none !important; }
  .bmc-cell { grid-area: auto !important; }
}
"""
    return {
        "kind_label": model["variant"].lower(),
        "meta": f'{model["variant"]} · {len(blocks)} blocks',
        "toolbar": "",
        "view_css": view_css,
        "content": content,
    }


# --------------------------------------------------------------------------- #
# Service blueprint — swimlane grid with the line of visibility
# --------------------------------------------------------------------------- #

BAND_LABELS = {
    "evidence": "Physical / digital evidence",
    "customer": "Customer actions",
    "frontstage": "Frontstage (visible)",
    "backstage": "Backstage (invisible)",
    "systems": "Systems / automation",
    "unclassified": "Unclassified",
}
# Control line drawn ABOVE the band whose key this is (matches parsers.CONTROL_LINES).
CONTROL_LINES = {
    "frontstage": "line of interaction",
    "backstage": "line of visibility",
    "systems": "line of internal interaction",
}


def render_service_blueprint(model, options):
    phases = model["phases"]
    nph = len(phases)
    by_band = model["by_band"]
    stats = model["stats"]

    def phase_headers():
        cells = ['<div class="sb-corner"></div>']
        for p in phases:
            pain = f' sb-ph--{esc(p["pain"])}' if p.get("pain") else ""
            pid = f'<span class="sb-ph-id">{esc(p["id"])}</span>' if p.get("id") else ""
            cells.append(
                f'<div class="sb-ph{pain}">{pid}<span class="sb-ph-name">{esc(p["name"])}</span></div>'
            )
        return f'<div class="sb-row sb-row--head">{"".join(cells)}</div>'

    def step_chip(s):
        fail = " sb-step--fail" if s.get("fail") else ""
        return f'<span class="sb-step{fail}">{esc(s["label"])}</span>'

    def lane_row(lane):
        label_bits = [f'<span class="sb-lane-name">{esc(lane["name"])}</span>']
        if lane.get("persona"):
            label_bits.append(f'<span class="sb-lane-persona">{esc(lane["persona"])}</span>')
        if lane.get("band") == "unclassified":
            label_bits.append('<span class="sb-badge sb-badge--warn" title="could not resolve a persona type — classify in the source persona doc">unclassified</span>')
        if lane.get("fail"):
            label_bits.append('<span class="sb-badge sb-badge--fail" title="named in a §9 pain point">⚠ pain</span>')
        cells = [f'<div class="sb-lane-label">{"".join(label_bits)}</div>']
        for pi in range(nph):
            chips = "".join(step_chip(s) for s in lane["cells"][pi]) if lane.get("cells") else ""
            cells.append(f'<div class="sb-cell">{chips}</div>')
        return f'<div class="sb-row">{"".join(cells)}</div>'

    def evidence_row():
        ev = model.get("evidence", [])
        if not ev:
            return ""
        chips = "".join(f'<span class="sb-evidence">{esc(x)}</span>' for x in ev)
        body = f'<div class="sb-cell sb-cell--span" style="grid-column: 2 / {nph + 2};">{chips}</div>'
        label = f'<div class="sb-lane-label"><span class="sb-lane-name">{esc(BAND_LABELS["evidence"])}</span></div>'
        return f'<div class="sb-row">{label}{body}</div>'

    def control_line(text):
        return (
            f'<div class="sb-line" style="grid-column: 1 / {nph + 2};">'
            f'<span class="sb-line-label">{esc(text)}</span></div>'
        )

    rows = [phase_headers(), evidence_row()]
    # ordered bands below evidence, inserting a control line above the marked ones
    for band in ("customer", "frontstage", "backstage", "systems", "unclassified"):
        lanes = by_band.get(band, [])
        if not lanes:
            continue
        if band in CONTROL_LINES:
            rows.append(control_line(CONTROL_LINES[band]))
        rows.append(f'<div class="sb-band-tag">{esc(BAND_LABELS[band])}</div>')
        rows.extend(lane_row(l) for l in lanes)

    # comms spine — the cross-actor handoffs ("the dance")
    spine = ""
    if model.get("connectors"):
        chips = "".join(
            f'<span class="sb-handoff">{esc(c["from"])} <span class="sb-arrow">→</span> '
            f'{esc(c["to"])}<span class="sb-handoff-obj">{esc(c["object"])}</span></span>'
            for c in model["connectors"]
        )
        spine = (
            '<section class="sb-spine"><h3 class="sb-spine-title">Notification / comms spine — handoffs</h3>'
            f'<div class="sb-spine-chips">{chips}</div></section>'
        )

    has_grid = any(by_band.get(b) for b in by_band) or model.get("evidence")
    if not has_grid:
        grid = '<p class="viz-empty">No actors found in the source process docs.</p>'
    else:
        grid = (
            f'<div class="sb-grid" style="grid-template-columns: var(--sb-lane-w) repeat({nph}, minmax(120px, 1fr));">'
            + "".join(rows) + "</div>"
        )
    content = grid + spine

    toolbar = ""
    if stats["unclassified"]:
        toolbar = (
            f'<span class="sb-note">⚠ {stats["unclassified"]} of {stats["actors"]} actors unclassified — '
            f'derived from persona type; set <code>Persona type</code> in the source persona doc to place them.</span>'
        )

    view_css = """
:root { --sb-lane-w: 190px; }
.sb-grid { display: grid; gap: 2px; background: var(--border); border: 1px solid var(--border);
  border-radius: var(--card-radius); overflow: hidden; }
.sb-row { display: contents; }
.sb-corner { background: var(--surface-2); }
.sb-ph { background: var(--surface-2); padding: 0.5rem 0.6rem; display: flex; flex-direction: column; gap: 0.1rem; }
.sb-ph-id { font-family: var(--font-mono); font-size: 0.62rem; color: var(--accent); font-weight: 700; }
.sb-ph-name { font-size: 0.82rem; font-weight: 700; }
.sb-ph--critical { box-shadow: inset 0 -3px 0 var(--pain-critical); }
.sb-ph--high { box-shadow: inset 0 -3px 0 var(--pain-high); }
.sb-ph--medium { box-shadow: inset 0 -3px 0 var(--pain-medium); }
.sb-ph--low { box-shadow: inset 0 -3px 0 var(--pain-low); }
.sb-band-tag { grid-column: 1 / -1; background: var(--surface-2); color: var(--muted);
  font-size: 0.66rem; text-transform: uppercase; letter-spacing: 0.08em; font-weight: 700;
  padding: 0.25rem 0.6rem; }
.sb-lane-label { background: var(--surface); padding: 0.5rem 0.6rem; display: flex; flex-direction: column;
  gap: 0.15rem; border-right: 2px solid var(--surface-2); }
.sb-lane-name { font-size: 0.82rem; font-weight: 600; }
.sb-lane-persona { font-size: 0.66rem; color: var(--muted); font-style: italic; }
.sb-cell { background: var(--surface); padding: 0.4rem; display: flex; flex-wrap: wrap; gap: 0.3rem;
  align-content: flex-start; }
.sb-cell--span { align-items: center; }
.sb-step { font-size: 0.72rem; background: var(--surface-2); border: 1px solid var(--border);
  border-radius: var(--node-radius); padding: 0.15rem 0.45rem; }
.sb-step--fail { border-color: var(--pain-high); box-shadow: inset 3px 0 0 var(--pain-high); }
.sb-evidence { font-size: 0.72rem; background: var(--surface); border: 1px dashed var(--accent);
  border-radius: 999px; padding: 0.15rem 0.55rem; color: var(--ink); }
.sb-line { background: var(--canvas-bg); border-top: 2px dashed var(--muted); height: 1.4rem;
  display: flex; align-items: center; }
.sb-line-label { font-size: 0.62rem; text-transform: uppercase; letter-spacing: 0.1em;
  color: var(--muted); font-weight: 700; padding: 0 0.6rem; }
.sb-badge { font-size: 0.58rem; text-transform: uppercase; letter-spacing: 0.04em; font-weight: 700;
  border-radius: 999px; padding: 0.05rem 0.4rem; width: fit-content; }
.sb-badge--warn { background: var(--pain-medium); color: var(--accent-ink); }
.sb-badge--fail { background: var(--pain-high); color: var(--accent-ink); }
.sb-spine { margin-top: var(--space-lg); background: var(--surface-2); border-radius: var(--card-radius);
  padding: var(--space-md); border-left: 4px solid var(--accent); }
.sb-spine-title { margin: 0 0 0.5rem; font-size: 0.95rem; }
.sb-spine-chips { display: flex; flex-wrap: wrap; gap: 0.4rem; }
.sb-handoff { font-size: 0.72rem; background: var(--surface); border: 1px solid var(--border);
  border-radius: var(--node-radius); padding: 0.2rem 0.5rem; display: inline-flex; align-items: center; gap: 0.3rem; }
.sb-arrow { color: var(--accent); font-weight: 700; }
.sb-handoff-obj { font-family: var(--font-mono); font-size: 0.62rem; color: var(--muted);
  background: var(--surface-2); border-radius: 999px; padding: 0 0.4rem; margin-left: 0.2rem; }
.sb-note { font-size: 0.74rem; color: var(--muted); }
"""
    meta = (
        f'{stats["phases"]} phases · {stats["actors"]} actors across {stats["procs"]} '
        f'process doc{"s" if stats["procs"] != 1 else ""} · {stats["classified"]} classified'
        + (f' · {stats["unclassified"]} unclassified' if stats["unclassified"] else "")
        + ("" if model["derived_phases"] else " · phase columns derived from §6 step order (no value stream supplied)")
    )
    return {
        "kind_label": "service blueprint",
        "meta": meta,
        "toolbar": toolbar,
        "view_css": view_css,
        "content": content,
    }


RENDERERS = {
    "capability-map": render_capability_map,
    "fbs": render_fbs,
    "delivery-roadmap": render_roadmap,
    "bmc": render_bmc,
    "service-blueprint": render_service_blueprint,
}
