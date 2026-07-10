#!/usr/bin/env python3
"""
Generate userapp/assets/xavier_erd_panel.html from schema.py.

Run from the userapp/ directory:
    python generate_erd.py

Called automatically by cloudbuild.yaml before docker build.
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
if HERE not in sys.path:
    sys.path.insert(0, HERE)

from schema import ENTITY_SCHEMAS, EDGES

OUT = os.path.join(HERE, "assets", "xavier_erd_panel.html")


def build_tables_js():
    tables = {}
    for key, s in ENTITY_SCHEMAS.items():
        tables[key] = {
            "label":     s["label"],
            "color":     s["color"],
            "colorBg":   s["colorBg"],
            "desc":      s["desc"],
            "required":  s["required"],
            "optional":  s["optional"],
            "system":    s["system"],
            "relations": s.get("relations", []),
        }
        if s.get("no_metadata"):
            tables[key]["junction"] = True
    return json.dumps(tables, indent=2)


def build_pos_js():
    pos = {key: s["pos"] for key, s in ENTITY_SCHEMAS.items()}
    return json.dumps(pos, indent=2)


def build_edges_js():
    return json.dumps([[a, b] for a, b in EDGES], indent=2)


HTML_TEMPLATE = """\
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Xavier LIMS — Schema Reference</title>
<style>
  *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

  :root {
    --bg: #0f1117;
    --bg2: #161b27;
    --bg3: #1e2535;
    --border: rgba(255,255,255,0.08);
    --border-hi: rgba(255,255,255,0.18);
    --text: #e2e8f0;
    --text-muted: #8892a4;
    --text-dim: #4a5568;
    --accent: #4f9cf9;
    --accent-glow: rgba(79,156,249,0.15);
    --teal: #2dd4bf;
    --amber: #fbbf24;
    --coral: #fb7185;
    --purple: #a78bfa;
    --green: #4ade80;
    --font-mono: 'JetBrains Mono', 'Fira Code', 'Cascadia Code', monospace;
    --font: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
  }

  body {
    background: var(--bg);
    color: var(--text);
    font-family: var(--font);
    font-size: 13px;
    min-height: 100vh;
    display: flex;
    flex-direction: column;
  }

  header {
    padding: 14px 20px;
    border-bottom: 1px solid var(--border);
    display: flex;
    align-items: center;
    gap: 12px;
    background: var(--bg2);
    flex-shrink: 0;
  }

  .logo {
    font-family: var(--font-mono);
    font-size: 11px;
    color: var(--accent);
    letter-spacing: 0.12em;
    text-transform: uppercase;
  }

  .logo span { color: var(--text-muted); }

  .header-hint {
    margin-left: auto;
    color: var(--text-muted);
    font-size: 12px;
  }

  .layout {
    display: flex;
    flex: 1;
    overflow: hidden;
    height: calc(100vh - 49px);
  }

  #canvas-wrap {
    flex: 1;
    position: relative;
    overflow: hidden;
    background: var(--bg);
    background-image: radial-gradient(circle at 1px 1px, rgba(255,255,255,0.03) 1px, transparent 0);
    background-size: 24px 24px;
  }

  #canvas {
    position: absolute;
    top: 0; left: 0;
    width: 100%; height: 100%;
  }

  #sidebar {
    width: 300px;
    border-left: 1px solid var(--border);
    background: var(--bg2);
    display: flex;
    flex-direction: column;
    overflow: hidden;
  }

  .sidebar-header {
    padding: 14px 16px 10px;
    border-bottom: 1px solid var(--border);
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 8px;
    flex-shrink: 0;
  }

  .sidebar-title {
    font-family: var(--font-mono);
    font-size: 10px;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    color: var(--text-muted);
    font-weight: 400;
  }

  #ingest-btn {
    display: none;
    align-items: center;
    gap: 5px;
    padding: 5px 10px;
    background: var(--accent);
    color: #fff;
    border: none;
    border-radius: 5px;
    font-size: 11px;
    font-family: var(--font);
    font-weight: 500;
    cursor: pointer;
    text-decoration: none;
    white-space: nowrap;
    transition: opacity 0.15s;
  }

  #ingest-btn:hover { opacity: 0.85; }
  #ingest-btn.visible { display: flex; }

  .sidebar-body {
    flex: 1;
    overflow-y: auto;
    padding: 12px 16px;
  }

  .placeholder {
    color: var(--text-dim);
    font-size: 12px;
    line-height: 1.6;
    margin-top: 8px;
  }

  .placeholder strong {
    display: block;
    color: var(--text-muted);
    margin-bottom: 6px;
    font-size: 11px;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    font-family: var(--font-mono);
  }

  .table-name {
    font-family: var(--font-mono);
    font-size: 13px;
    font-weight: 600;
    margin-bottom: 4px;
  }

  .table-desc {
    color: var(--text-muted);
    font-size: 12px;
    line-height: 1.5;
    margin-bottom: 12px;
  }

  .junction-note {
    padding: 6px 8px;
    background: rgba(255,255,255,0.03);
    border-radius: 4px;
    border-left: 2px solid rgba(255,255,255,0.15);
    margin-bottom: 12px;
    color: var(--text-muted);
    font-size: 11px;
    line-height: 1.5;
  }

  .section-label {
    font-family: var(--font-mono);
    font-size: 9px;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: var(--text-dim);
    margin-bottom: 5px;
    margin-top: 12px;
    display: flex;
    align-items: center;
    gap: 6px;
  }

  .section-label:first-of-type { margin-top: 0; }

  .req-dot {
    width: 6px; height: 6px;
    border-radius: 50%;
    background: var(--coral);
    flex-shrink: 0;
  }

  .opt-dot {
    width: 6px; height: 6px;
    border-radius: 50%;
    background: var(--text-dim);
    flex-shrink: 0;
  }

  .field-row {
    display: flex;
    align-items: center;
    gap: 6px;
    padding: 4px 0;
    border-bottom: 1px solid var(--border);
    font-family: var(--font-mono);
    font-size: 11px;
  }

  .field-row:last-child { border-bottom: none; }

  .field-name { color: var(--text); flex: 1; min-width: 0; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
  .field-type { color: var(--text-dim); font-size: 10px; flex-shrink: 0; }

  .badge {
    font-size: 9px;
    padding: 1px 5px;
    border-radius: 3px;
    font-family: var(--font-mono);
    letter-spacing: 0.04em;
    flex-shrink: 0;
  }

  .badge-pk  { background: rgba(251,191,36,0.15);  color: var(--amber); }
  .badge-fk  { background: rgba(79,156,249,0.12);  color: var(--accent); }
  .badge-sys { background: rgba(255,255,255,0.05); color: var(--text-dim); }

  .rel-row {
    display: flex;
    align-items: center;
    gap: 8px;
    padding: 4px 0;
    font-size: 11px;
    color: var(--text-muted);
    cursor: pointer;
    border-radius: 4px;
    transition: color 0.1s;
  }

  .rel-row:hover { color: var(--accent); }
  .rel-arrow { color: var(--text-dim); font-family: var(--font-mono); }

  .erd-node { cursor: pointer; }
  .conn-line {
    fill: none;
    stroke: rgba(255,255,255,0.07);
    stroke-width: 1.5;
    transition: stroke 0.15s;
  }
  .conn-line.highlighted {
    stroke: var(--accent);
    stroke-width: 2;
    stroke-opacity: 0.55;
  }
  .group-label {
    font-family: var(--font-mono, monospace);
    font-size: 9px;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    fill: rgba(255,255,255,0.18);
  }
</style>
</head>
<body>

<header>
  <div class="logo">Xavier<span>/</span>LIMS</div>
  <div style="width:1px;height:16px;background:var(--border)"></div>
  <span style="color:var(--text-muted);font-size:12px">Schema reference</span>
  <span class="header-hint">Click any table to explore · red = required · gray = optional</span>
</header>

<div class="layout">
  <div id="canvas-wrap">
    <svg id="canvas" xmlns="http://www.w3.org/2000/svg"></svg>
  </div>

  <div id="sidebar">
    <div class="sidebar-header">
      <span class="sidebar-title" id="sidebar-title">No table selected</span>
      <a id="ingest-btn" href="#" target="_blank">&#8599; Ingest</a>
    </div>
    <div class="sidebar-body" id="sidebar-body">
      <p class="placeholder">
        <strong>Schema explorer</strong>
        Select a table to see its fields and relationships.<br><br>
        <span style="color:var(--coral)">&#9679;</span> Required fields must be present on ingest.<br>
        <span style="color:var(--text-dim)">&#9679;</span> Optional fields default or can be omitted.<br><br>
        Click a related table to jump to it. Use the ingest button to open the data entry form for that table.
      </p>
    </div>
  </div>
</div>

<script>
const STREAMLIT_BASE = 'http://localhost:8501';

// ── Schema data (generated by generate_erd.py — do not edit manually) ─────────
const TABLES = __TABLES_DATA__;
const POS    = __POS_DATA__;
const EDGES  = __EDGES_DATA__;
// ──────────────────────────────────────────────────────────────────────────────

const NW = 152, NH = 44;
const VW = 700, VH = 720;

const svg = document.getElementById('canvas');
svg.setAttribute('viewBox', `0 0 ${VW} ${VH}`);
svg.style.width = '100%';
svg.style.height = '100%';

// defs
const defs = document.createElementNS('http://www.w3.org/2000/svg', 'defs');
defs.innerHTML = `
  <marker id="arr" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="5" markerHeight="5" orient="auto-start-reverse">
    <path d="M2 1L8 5L2 9" fill="none" stroke="rgba(255,255,255,0.18)" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
  </marker>
  <marker id="arr-hi" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="5" markerHeight="5" orient="auto-start-reverse">
    <path d="M2 1L8 5L2 9" fill="none" stroke="#4f9cf9" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
  </marker>`;
svg.appendChild(defs);

// group labels
function addGroupLabel(txt, x, y) {
  const t = document.createElementNS('http://www.w3.org/2000/svg', 'text');
  t.setAttribute('x', x); t.setAttribute('y', y);
  t.setAttribute('class', 'group-label');
  t.textContent = txt;
  svg.appendChild(t);
}
addGroupLabel('Lineage',    30,  50);
addGroupLabel('Grouping',  500,  50);
addGroupLabel('Sequencing', 30, 600);

// edges
const edgeLayer = document.createElementNS('http://www.w3.org/2000/svg', 'g');
edgeLayer.id = 'edge-layer';
svg.appendChild(edgeLayer);

function edgePath(fk, tk) {
  const f = POS[fk], t = POS[tk];
  const fx = f.x + NW / 2, fy = f.y + NH;
  const tx = t.x + NW / 2, ty = t.y;
  const my = (fy + ty) / 2;
  return `M ${fx} ${fy} C ${fx} ${my}, ${tx} ${my}, ${tx} ${ty}`;
}

const edgeEls = {};
EDGES.forEach(([from, to]) => {
  const path = document.createElementNS('http://www.w3.org/2000/svg', 'path');
  path.setAttribute('d', edgePath(from, to));
  path.setAttribute('class', 'conn-line');
  path.setAttribute('marker-end', 'url(#arr)');
  path.dataset.from = from;
  path.dataset.to = to;
  edgeLayer.appendChild(path);
  edgeEls[`${from}__${to}`] = path;
});

// nodes
const nodeEls = {};
Object.entries(POS).forEach(([key, pos]) => {
  const t = TABLES[key];
  if (!t) return;
  const isJunction = !!t.junction;

  const g = document.createElementNS('http://www.w3.org/2000/svg', 'g');
  g.setAttribute('class', 'erd-node');
  g.dataset.key = key;

  const rect = document.createElementNS('http://www.w3.org/2000/svg', 'rect');
  rect.setAttribute('x', pos.x);
  rect.setAttribute('y', pos.y);
  rect.setAttribute('width', NW);
  rect.setAttribute('height', NH);
  rect.setAttribute('rx', 6);
  rect.setAttribute('fill', t.colorBg);
  rect.setAttribute('stroke', t.color);
  rect.setAttribute('stroke-width', isJunction ? '1' : '1.5');
  rect.setAttribute('stroke-opacity', isJunction ? '0.4' : '0.7');

  const label = document.createElementNS('http://www.w3.org/2000/svg', 'text');
  label.setAttribute('x', pos.x + NW / 2);
  label.setAttribute('y', pos.y + NH / 2 - 6);
  label.setAttribute('text-anchor', 'middle');
  label.setAttribute('dominant-baseline', 'central');
  label.setAttribute('fill', t.color);
  label.setAttribute('font-family', 'JetBrains Mono, Fira Code, monospace');
  label.setAttribute('font-size', '11');
  label.setAttribute('font-weight', isJunction ? '400' : '600');
  label.textContent = t.label;

  const sub = document.createElementNS('http://www.w3.org/2000/svg', 'text');
  sub.setAttribute('x', pos.x + NW / 2);
  sub.setAttribute('y', pos.y + NH / 2 + 8);
  sub.setAttribute('text-anchor', 'middle');
  sub.setAttribute('dominant-baseline', 'central');
  sub.setAttribute('fill', 'rgba(255,255,255,0.28)');
  sub.setAttribute('font-family', 'JetBrains Mono, Fira Code, monospace');
  sub.setAttribute('font-size', '9');
  sub.textContent = isJunction
    ? `(junction · ${t.required.length} required)`
    : `${t.required.length} required · ${t.optional.length} optional`;

  g.appendChild(rect);
  g.appendChild(label);
  g.appendChild(sub);
  g.addEventListener('click', () => selectTable(key));
  svg.appendChild(g);
  nodeEls[key] = { g, rect };
});

// ── Selection ─────────────────────────────────────────────────────────────────
function selectTable(key) {
  Object.entries(nodeEls).forEach(([k, { rect }]) => {
    const isJ = !!TABLES[k].junction;
    rect.setAttribute('stroke-opacity', isJ ? '0.4' : '0.7');
    rect.setAttribute('stroke-width',   isJ ? '1'   : '1.5');
  });
  Object.values(edgeEls).forEach(p => {
    p.setAttribute('class', 'conn-line');
    p.setAttribute('marker-end', 'url(#arr)');
  });

  nodeEls[key].rect.setAttribute('stroke-opacity', '1');
  nodeEls[key].rect.setAttribute('stroke-width', '2.5');

  EDGES.forEach(([from, to]) => {
    if (from === key || to === key) {
      const el = edgeEls[`${from}__${to}`];
      if (el) {
        el.setAttribute('class', 'conn-line highlighted');
        el.setAttribute('marker-end', 'url(#arr-hi)');
      }
    }
  });

  const t = TABLES[key];

  document.getElementById('sidebar-title').textContent = t.label;

  const btn = document.getElementById('ingest-btn');
  btn.href = `${STREAMLIT_BASE}/Ingest_Data?table=${key}`;
  btn.classList.add('visible');

  let html = `<div class="table-name" style="color:${t.color}">${t.label}</div>`;
  html += `<div class="table-desc">${t.desc}</div>`;

  if (t.junction) {
    html += `<div class="junction-note">Junction table — no surrogate ID. Primary key is the composite of both foreign keys. No extra_metadata.</div>`;
  }

  if (t.required.length) {
    html += `<div class="section-label"><span class="req-dot"></span>Required fields</div>`;
    t.required.forEach(f => {
      html += `<div class="field-row"><span class="field-name">${f}</span><span class="field-type">ingest key</span></div>`;
    });
  }

  if (t.optional.length) {
    html += `<div class="section-label"><span class="opt-dot"></span>Optional fields</div>`;
    t.optional.forEach(f => {
      html += `<div class="field-row"><span class="field-name">${f}</span><span class="field-type">optional</span></div>`;
    });
  }

  if (t.system.length) {
    html += `<div class="section-label" style="margin-top:10px">
      <span style="width:6px;height:6px;border-radius:50%;background:var(--text-dim);display:inline-block;flex-shrink:0"></span>
      System fields
    </div>`;
    t.system.forEach(f => {
      const isPk = f === 'id';
      const isFk = f.endsWith('_id') && f !== 'id';
      html += `<div class="field-row">
        <span class="field-name">${f}</span>
        ${isPk ? '<span class="badge badge-pk">PK</span>' : ''}
        ${isFk ? '<span class="badge badge-fk">FK</span>' : ''}
        <span class="badge badge-sys">auto</span>
      </div>`;
    });
  }

  if (t.relations && t.relations.length) {
    html += `<div class="section-label" style="margin-top:14px">
      <span style="color:var(--accent);font-size:10px">↔</span>
      Related tables
    </div>`;
    t.relations.forEach(rel => {
      const rt = TABLES[rel];
      if (!rt) return;
      html += `<div class="rel-row" onclick="selectTable('${rel}')">
        <span class="rel-arrow">↔</span>
        <span style="color:${rt.color}">${rt.label}</span>
      </div>`;
    });
  }

  document.getElementById('sidebar-body').innerHTML = html;
}

window.selectTable = selectTable;
</script>
</body>
</html>
"""


def generate():
    html = HTML_TEMPLATE \
        .replace("__TABLES_DATA__", build_tables_js()) \
        .replace("__POS_DATA__",    build_pos_js()) \
        .replace("__EDGES_DATA__",  build_edges_js())

    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w", encoding="utf-8") as f:
        f.write(html)

    print(f"ERD generated → {OUT}")


if __name__ == "__main__":
    generate()
