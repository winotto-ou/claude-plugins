#!/usr/bin/env bash
# Local install check: installs winotto@winotto-ou into a throwaway Claude Code
# config dir, verifies skills and MCP servers, and builds dist/winotto.zip for
# a manual claude.ai "Upload plugin" test. Never touches ~/.claude.
set -euo pipefail

repo="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$repo"

CLAUDE_CONFIG_DIR="$(mktemp -d)"
export CLAUDE_CONFIG_DIR
trap 'rm -rf "$CLAUDE_CONFIG_DIR"' EXIT

claude plugin marketplace add "$repo"
claude plugin install winotto@winotto-ou
list_out="$(claude plugin list)"
details_out="$(claude plugin details winotto@winotto-ou)"
printf '%s\n%s\n' "$list_out" "$details_out"

fail() { echo "FAIL: $*" >&2; exit 1; }

grep -q 'winotto@winotto-ou' <<<"$list_out" || fail "plugin missing from list"
grep -qE 'Skills \(4\)' <<<"$details_out" || fail "expected 4 skills"
for s in estonian-proofreading jw-search suomen-oikoluku ariregister; do
  grep -q "$s" <<<"$details_out" || fail "skill $s missing"
done
grep -qE 'MCP servers \(5\)' <<<"$details_out" || fail "expected 5 MCP servers"
for m in jw bible-lex et-proof email arireg; do
  grep -E 'MCP servers' <<<"$details_out" | grep -qE "(^|[ ,])$m([ ,]|$)" || fail "MCP server $m missing"
done

mkdir -p dist
python3 - <<'PY'
import zipfile, pathlib
root = pathlib.Path("plugins/winotto")
out = pathlib.Path("dist/winotto.zip")
out.unlink(missing_ok=True)
with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as z:
    for p in sorted(root.rglob("*")):
        if p.is_file() and "__pycache__" not in p.parts:
            z.write(p, p.relative_to(root).as_posix())
names = zipfile.ZipFile(out).namelist()
assert ".claude-plugin/plugin.json" in names, "plugin.json not at zip root"
print(f"zip: {out} ({len(names)} files)")
PY

echo "OK install winotto@winotto-ou: 4 skills, 5 MCP servers"
