#!/usr/bin/env python3
"""Repo checks for the winotto-ou plugin marketplace. Stdlib only.

Usage: python3 scripts/check.py   (from the repo root; prints OK or the errors, exit 1)
"""
import json
import re
import sys
from pathlib import Path

ALLOWED_KEYS = {"name", "description", "license", "compatibility", "metadata", "allowed-tools"}
URL_RE = re.compile(r"^https://mcp\.winotto\.com/[a-z-]+/mcp$")
SECRET_RE = re.compile(r"(?i)(api[_-]?ke" + r"y|sec" + r"ret|pass" + r"word)\s*[:=]\s*\S{8,}")
# Built by concatenation so this file does not trip its own scan.
FORBIDDEN_STRINGS = ["/ho" + "me/", "/mnt" + "/c/", "@gmail" + ".com"]
SKIP_DIRS = {".git", "__pycache__", ".pytest_cache", "dist"}
MCP_PREFIX = "mcp" + "__"
PLUGIN_ROOT_VAR = "${CLAUDE_PLUGIN_ROOT}"


def load_json(path, errors, root):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError) as e:
        errors.append(f"{path.relative_to(root)}: cannot parse JSON ({e})")
        return None


def parse_frontmatter(text):
    """Return dict of top-level keys -> string value, or None if no frontmatter."""
    lines = text.split("\n")
    if not lines or lines[0].strip() != "---":
        return None
    end = None
    for i in range(1, len(lines)):
        if lines[i].strip() == "---":
            end = i
            break
    if end is None:
        return None
    result = {}
    key = None
    for line in lines[1:end]:
        m = re.match(r"^([A-Za-z0-9_-]+):\s*(.*)$", line)
        if m:
            key = m.group(1)
            result[key] = m.group(2).strip()
        elif key and (line.startswith(" ") or line.startswith("\t")):
            result[key] = (result[key] + " " + line.strip()).strip()
    for k, v in result.items():
        if v in (">", "|", ">-", "|-"):
            result[k] = ""
        elif v[:2] in (">-", "|-") or v[:1] in (">", "|"):
            result[k] = v.lstrip(">|-").strip()
    return result


def check_manifests(root, errors):
    mp_path = root / ".claude-plugin" / "marketplace.json"
    mp = load_json(mp_path, errors, root) if mp_path.exists() else None
    if not mp_path.exists():
        errors.append(".claude-plugin/marketplace.json: missing")
    plugin_dirs = []
    if isinstance(mp, dict):
        if mp.get("name") != "winotto-ou":
            errors.append("marketplace.json: name must be 'winotto-ou'")
        for p in mp.get("plugins", []):
            src = p.get("source") if isinstance(p, dict) else None
            label = f"marketplace.json plugin {p.get('name') if isinstance(p, dict) else p!r}"
            if not isinstance(src, str) or not src.startswith("./"):
                errors.append(f"{label}: source must be a string starting with './'")
                continue
            if ".." in src:
                errors.append(f"{label}: source must not contain '..'")
                continue
            d = root / src
            if not d.is_dir():
                errors.append(f"{label}: source folder {src} does not exist")
                continue
            pj = d / ".claude-plugin" / "plugin.json"
            if not pj.is_file():
                errors.append(f"{label}: {src}/.claude-plugin/plugin.json missing")
            else:
                load_json(pj, errors, root)
            plugin_dirs.append(d)
    return plugin_dirs


def check_mcp(plugin_dir, root, errors):
    path = plugin_dir / ".mcp.json"
    if not path.is_file():
        errors.append(f"{path.relative_to(root)}: missing (the plugin must ship its connectors)")
        return
    data = load_json(path, errors, root)
    if not isinstance(data, dict):
        return
    servers = data.get("mcpServers")
    rel = path.relative_to(root)
    if not isinstance(servers, dict):
        errors.append(f"{rel}: mcpServers must be an object")
        return
    for name, srv in servers.items():
        if not isinstance(srv, dict) or set(srv) != {"type", "url"}:
            errors.append(f"{rel}: server '{name}' must be an object with exactly the keys type and url")
            continue
        if srv["type"] != "http":
            errors.append(f"{rel}: server '{name}' type must be 'http'")
        if not isinstance(srv["url"], str) or not URL_RE.match(srv["url"]):
            errors.append(f"{rel}: server '{name}' url must match {URL_RE.pattern}")


def check_skills(plugin_dir, root, errors):
    skills = plugin_dir / "skills"
    if not skills.is_dir():
        return
    for d in sorted(p for p in skills.iterdir() if p.is_dir()):
        sk = d / "SKILL.md"
        rel = sk.relative_to(root)
        if not sk.is_file():
            errors.append(f"{d.relative_to(root)}: SKILL.md missing")
            continue
        fm = parse_frontmatter(sk.read_text(encoding="utf-8"))
        if fm is None:
            errors.append(f"{rel}: frontmatter missing")
            continue
        if fm.get("name") != d.name:
            errors.append(f"{rel}: name {fm.get('name')!r} must equal folder name {d.name!r}")
        desc = fm.get("description", "")
        if not desc:
            errors.append(f"{rel}: description is empty")
        elif len(desc) > 1024:
            errors.append(f"{rel}: description is {len(desc)} chars, limit is 1024")
        for k in sorted(set(fm) - ALLOWED_KEYS):
            errors.append(f"{rel}: frontmatter key '{k}' is not allowed")
        for f in sorted(p for p in d.rglob("*") if p.is_file()):
            try:
                text = f.read_text(encoding="utf-8")
            except (UnicodeDecodeError, OSError):
                continue
            for bad in (MCP_PREFIX, PLUGIN_ROOT_VAR):
                if bad in text:
                    errors.append(f"{f.relative_to(root)}: contains {bad}")


def check_no_bin(plugin_dir, root, errors):
    if (plugin_dir / "bin").exists():
        errors.append(f"{plugin_dir.relative_to(root)}/bin: folder bin/ is not allowed in a plugin")


def check_leaks(root, errors):
    for f in sorted(root.rglob("*")):
        if not f.is_file():
            continue
        rel = f.relative_to(root)
        if SKIP_DIRS & set(rel.parts):
            continue
        try:
            text = f.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            continue
        for s in FORBIDDEN_STRINGS:
            if s in text:
                errors.append(f"{rel}: contains forbidden text {s!r}")
        if SECRET_RE.search(text):
            errors.append(f"{rel}: looks like it contains a secret")


def run(root):
    root = Path(root).resolve()
    errors = []
    plugin_dirs = check_manifests(root, errors)
    for d in plugin_dirs:
        check_mcp(d, root, errors)
        check_skills(d, root, errors)
        check_no_bin(d, root, errors)
    check_leaks(root, errors)
    return errors


if __name__ == "__main__":
    errs = run(Path.cwd())
    if errs:
        print("\n".join(errs))
        sys.exit(1)
    print("OK")
