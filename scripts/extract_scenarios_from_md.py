#!/usr/bin/env python3
"""
Extract scenario blocks from all index.md files in the Scenario Library
and output JSON objects matching data/scenarios.json schema.
Run from repo root: python scripts/extract_scenarios_from_md.py
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

SCENARIO_LIBRARY = Path(__file__).resolve().parent.parent / "📘 DOCTOR TWIN — SCENARIO LIBRARY (RAG INDEXED)"


def _slug(s: str) -> str:
    """Convert intent-like string to snake_case."""
    if not s:
        return "general"
    s = s.strip().lower()
    s = re.sub(r"[^\w\s-]", "", s)
    s = re.sub(r"[\s-]+", "_", s)
    return s or "general"


def _section_text(block: str, header: str, next_headers: list[str]) -> str:
    """Extract lines under a section until next section."""
    lines = block.splitlines()
    found = False
    out = []
    for line in lines:
        line_strip = line.strip()
        if line_strip.upper().startswith(header.upper()) and (len(line_strip) == len(header) or line_strip[len(header):len(header)+1] in (" ", "\t", "")):
            found = True
            rest = line_strip[len(header):].strip()
            if rest:
                out.append(rest)
            continue
        if found:
            if any(line_strip.upper().startswith(h.upper()) for h in next_headers):
                break
            if line_strip.startswith("# ") or line_strip.startswith("SCENARIO ID:"):
                break
            if line_strip:
                out.append(line_strip)
    return " ".join(out).strip() if out else ""


def _bullets(block: str, header: str) -> list[str]:
    """Extract bullet lines under section (lines starting with -)."""
    lines = block.splitlines()
    found = False
    out = []
    for line in lines:
        stripped = line.strip()
        if stripped.upper().startswith(header.upper()):
            found = True
            continue
        if found:
            if stripped.startswith("#") or "SCENARIO ID:" in stripped:
                break
            if stripped.startswith("-"):
                item = stripped[1:].strip().strip('"')
                if item:
                    out.append(item)
    return out


def _first_line_after(block: str, header: str) -> str:
    """First non-empty line after header (for Script)."""
    lines = block.splitlines()
    found = False
    for line in lines:
        stripped = line.strip()
        if stripped.upper().startswith(header.upper()):
            found = True
            continue
        if found and stripped and not stripped.startswith("#") and "SCENARIO ID:" not in stripped:
            return stripped.strip('"')
    return ""


def parse_block(block: str, default_brain: str = "receptionist") -> dict | None:
    """Parse one scenario block into JSON-like dict."""
    m = re.search(r"SCENARIO ID:\s*([A-Za-z0-9_-]+)", block)
    if not m:
        return None
    scenario_id = m.group(1).strip()

    intent_raw = ""
    for line in block.splitlines():
        if re.match(r"INTENT:\s*", line, re.I):
            intent_raw = line.split(":", 1)[1].strip()
            break
    intent = _slug(intent_raw) if intent_raw else _slug(scenario_id.replace("-", " "))

    risk = "low"
    for line in block.splitlines():
        if re.match(r"RISK(?:\s+LEVEL)?:\s*", line, re.I):
            r = line.split(":", 1)[1].strip().lower()
            if "critical" in r or "high" in r:
                risk = "high"
            elif "moderate" in r or "reputation" in r:
                risk = "moderate"
            elif "variable" in r:
                risk = "variable"
            else:
                risk = "low"
            break

    brain = default_brain
    for line in block.splitlines():
        if re.match(r"BRAIN:\s*", line, re.I):
            brain = line.split(":", 1)[1].strip().lower().replace(" ", "_")
            break

    triggers = _bullets(block, "Trigger")
    if not triggers:
        trigger_text = _section_text(block, "Trigger", ["Script", "Actions", "Hard Stop", "Required", "Verification", "Step", "Decision", "Script (", "Draft Response", "Immediate"])
        if trigger_text:
            triggers = [t.strip().strip('"') for t in re.split(r"[-•]\s*", trigger_text) if t.strip()][:10]
    if not triggers:
        triggers = [scenario_id.replace("-", " ").lower(), intent.replace("_", " ")]

    script = _section_text(block, "Script", ["Actions", "Hard Stop", "Required", "Follow-Up", "Explanation", "Note ", "Delivery", "Safety", "Resolution", "Coding", "Summary", "Actions"])
    if not script:
        script = _first_line_after(block, "Script")
    if not script:
        script = "I'll help you with that. Let me process your request."

    actions = _bullets(block, "Actions")
    if not actions:
        act_text = _section_text(block, "Actions", ["Hard Stop", "#", "Safety", "ENGINEERING"])
        if act_text:
            actions = [a.strip().strip("- ") for a in re.split(r"\n|;", act_text) if a.strip()][:8]
    if not actions:
        actions = ["Log request", "Route to appropriate department"]

    hard_stop = _section_text(block, "Hard Stop", ["Actions", "#"])
    if not hard_stop:
        hard_stop = _first_line_after(block, "Safety Rule")
    if not hard_stop:
        hard_stop = None

    department = brain if brain else "reception"
    if "scheduling" in brain or "SCH-" in scenario_id:
        department = "scheduling"
    elif "billing" in brain or "BILL-" in scenario_id:
        department = "billing"
    elif "medical_assistant" in brain or "MA-" in scenario_id:
        department = "medical_assistant"
    elif "physician" in brain or "PA-" in scenario_id or "RX-" in scenario_id:
        department = "pharmacy" if "RX-" in scenario_id else "prior_auth"
    elif "back" in brain or "BACK-" in scenario_id:
        department = "back_office"
    elif "admin" in brain or "ADMIN-" in scenario_id:
        department = "admin"
    elif "doc" in brain or "DOC-" in scenario_id:
        department = "records"
    elif "clin" in brain or "CLIN-" in scenario_id:
        department = "clinical"
    elif "safe" in brain or "SAFE-" in scenario_id:
        department = "safety"
    elif "lang" in brain or "LANG-" in scenario_id:
        department = "multilingual"
    elif "spa" in brain or "SPA-" in scenario_id:
        department = "medspa"
    elif "msg" in scenario_id or "MSG-" in scenario_id:
        department = "messaging"
    elif "lab" in scenario_id or "img" in scenario_id.lower():
        department = "lab_imaging"

    return {
        "scenario_id": scenario_id,
        "intent": intent,
        "risk": risk,
        "triggers": triggers[:15],
        "script": script[:2000] if script else "",
        "actions": actions,
        "hard_stop": hard_stop,
        "metadata": {
            "intent": intent,
            "risk_level": risk,
            "department": department,
            "brain": brain,
        },
    }


def main() -> int:
    repo_root = Path(__file__).resolve().parent.parent
    existing_path = repo_root / "data" / "scenarios.json"
    existing: dict[str, dict] = {}
    existing_order: list[str] = []
    if existing_path.exists():
        with open(existing_path, encoding="utf-8") as f:
            for obj in json.load(f):
                sid = obj["scenario_id"]
                existing[sid] = obj
                existing_order.append(sid)

    parsed_by_id: dict[str, dict] = {}
    for md_path in sorted(SCENARIO_LIBRARY.rglob("index.md")):
        if "RAG Scenario Pattern" in str(md_path) or "14. PATTERN" in str(md_path):
            continue
        try:
            text = md_path.read_text(encoding="utf-8")
        except Exception as e:
            print(f"Skip {md_path}: {e}", file=sys.stderr)
            continue
        blocks = re.split(r"(?=SCENARIO ID:)", text)
        default_brain = "receptionist"
        if "BILL" in text:
            default_brain = "billing_assistant"
        elif "BACK" in text or "10." in str(md_path):
            default_brain = "workflow_coordinator"
        elif "ADMIN" in text or "09." in str(md_path):
            default_brain = "office_manager"
        elif "DOC" in text or "07." in str(md_path):
            default_brain = "records_assistant"
        elif "CLIN" in text or "06." in str(md_path):
            default_brain = "clinical_assistant"
        elif "SAFE" in text or "11." in str(md_path):
            default_brain = "safety"
        elif "LANG" in text or "13" in str(md_path):
            default_brain = "multilingual"
        elif "SPA" in text or "12" in str(md_path):
            default_brain = "medspa"
        elif "LAB" in text or "IMG" in text or "03." in str(md_path):
            default_brain = "medical_assistant"
        elif "MSG" in text or "04." in str(md_path):
            default_brain = "physician_assistant"
        for blk in blocks:
            if "SCENARIO ID:" not in blk:
                continue
            obj = parse_block(blk, default_brain)
            if not obj:
                continue
            sid = obj["scenario_id"]
            if sid not in parsed_by_id:
                parsed_by_id[sid] = obj

    # Merge: prefer existing entry when we have it, else use parsed. Order: existing order then new ids.
    seen = set()
    merged: list[dict] = []
    for sid in existing_order:
        if sid in parsed_by_id or sid in existing:
            seen.add(sid)
            merged.append(existing.get(sid) or parsed_by_id[sid])
    for sid in sorted(parsed_by_id.keys()):
        if sid not in seen:
            merged.append(existing.get(sid) or parsed_by_id[sid])

    json.dump(merged, sys.stdout, indent=2, ensure_ascii=False)
    return 0


if __name__ == "__main__":
    sys.exit(main())
