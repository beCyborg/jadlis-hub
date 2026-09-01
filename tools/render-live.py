#!/usr/bin/env python3
"""render-live.py — render the live ~/.claude research stack FROM the plugin.

This is the INVERSE of the documented sync procedure (live -> plugin).
It takes plugins/jadlis-research as the source of truth and materialises the
personal contour in ~/.claude, undoing the plugin-specific adaptations
(placeholders, MCP name prefixes, namespaced slash-commands / agent types).

Dev tool only: it lives in the repo root `tools/` and is NOT part of the plugin.

Usage:
    tools/render-live.py --dry-run          # print the plan, change nothing
    tools/render-live.py --check            # only verify invariants
    tools/render-live.py                    # render
    tools/render-live.py --prune --yes      # render + drop stale skill files
"""

from __future__ import annotations

import argparse
import difflib
import os
import re
import shutil
import sys
from pathlib import Path

# --------------------------------------------------------------------------
# Configuration
# --------------------------------------------------------------------------

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_PLUGIN = REPO_ROOT / "plugins" / "jadlis-research"
DEFAULT_DEST = Path.home() / ".claude"

# Value the placeholders resolve to in the live contour.
LIVE_ROOT = "/Users/cyborg/.claude"
LIVE_ROOT_TILDE = "~/.claude"
# ${CLAUDE_PLUGIN_DATA} holds the verifier homes. In the live contour those
# live at $HOME/.claude/verif-homes (see ~/.claude/skills/verif/SKILL.md:62),
# so the plugin-data root maps onto $HOME/.claude itself -- NOT a verif-data dir.
PLUGIN_DATA_ROOT = "/Users/cyborg/.claude"
VAULT_PATH = "/Users/cyborg/Jadlis"

TEXT_SUFFIXES = {".md", ".js", ".py", ".sh", ".json", ".toml"}

# Directory trees rendered wholesale: (source rel, dest rel)
SKILL_TREES = [
    ("skills/full-research", "skills/full-research"),
    ("skills/search-paper", "skills/search-paper"),
    ("skills/search", "skills/search"),
    ("skills/verif", "skills/verif"),
]

# Non-skill trees rendered wholesale (never pruned): (source rel, dest rel)
ASSET_TREES = [
    # first-run deploy templates for the verifier homes
    ("assets/verif-homes", "assets/verif-homes"),
]

# Single files: (source rel, dest rel)
SINGLE_FILES = [
    ("shared/obsidian-write-contract.md", "skills/_shared/obsidian-write-contract.md"),
    ("agents/researcher-opus-xhigh.md", "agents/researcher-opus-xhigh.md"),
    ("agents/orchestrator-fable-xhigh.md", "agents/orchestrator-fable-xhigh.md"),
]

# Flat globs: (source dir, glob, dest dir)
FLAT_GLOBS = [
    ("workflows", "*.js", "workflows"),
    ("scripts", "*", "scripts"),
]

# Protocols rendered into full-research are symlinked into search-community.
PROTOCOL_SRC = "skills/full-research/protocols"
PROTOCOL_LINK_DIR = "skills/search-community/protocols"

# Extra symlinks: (link path rel to dest, target path rel to dest). The target
# must itself be rendered; the link is created only if the source exists.
EXTRA_LINKS = [
    # websearch.py moved plugin-side from skills/search/scripts/ to scripts/
    ("skills/search/scripts/websearch.py", "scripts/websearch.py"),
]

# Never rendered: plugin-only service skill.
SKIP_SOURCE_PREFIXES = ("skills/keys/",)

# Invariants
DEST_FORBIDDEN = ["plugin_jadlis-research", "CLAUDE_PLUGIN_ROOT", "{PLUGIN_ROOT}", "user_config."]
PLUGIN_FORBIDDEN = ["/Users/cyborg", "~/.claude/"]
# Deliberate exceptions: these reference the *recipient's* config, not a plugin path.
PLUGIN_EXCEPTIONS = {
    "skills/keys/SKILL.md",
    "skills/verif/SKILL.md",
    "skills/full-research/protocols/grok-web-protocol.md",
    # telemetry path of the recipient (~/.claude/telemetry/search-ab)
    "scripts/websearch.py",
    # venv path of a third-party plugin on the recipient's machine
    "scripts/yt-transcript.py",
    # recipient-side config / environment notes
    "README.md",
    "skills/verif/TESTS.md",
    "skills/verif/system-prompts/fable-verifier.md",
}
# Whole subtrees exempt from the plugin invariant (recipient-side data paths).
PLUGIN_EXCEPTION_PREFIXES = (
    "skills/search/",
)


# --------------------------------------------------------------------------
# Text substitution
# --------------------------------------------------------------------------

def substitute(text: str) -> str:
    """Apply the plugin -> live substitutions. Order matters."""
    # 1. ${CLAUDE_PLUGIN_ROOT} -> absolute live root (shared write contract lives in skills/_shared locally).
    text = text.replace("${CLAUDE_PLUGIN_ROOT}/shared/obsidian-write-contract.md", LIVE_ROOT + "/skills/_shared/obsidian-write-contract.md")
    text = text.replace("${CLAUDE_PLUGIN_ROOT}", LIVE_ROOT)

    # 2. {PLUGIN_ROOT} placeholder (protocols/references). A leading `$` means it
    #    is a JS template interpolation of the local `PLUGIN_ROOT` const, not the
    #    placeholder -- leave those alone.
    text = re.sub(r"(?<!\$)\{PLUGIN_ROOT\}/scripts/", LIVE_ROOT_TILDE + "/scripts/", text)
    text = re.sub(r"(?<!\$)\{PLUGIN_ROOT\}", LIVE_ROOT_TILDE, text)

    # 3. MCP tool names. reddit-alt BEFORE the generic rule, otherwise the
    #    generic rule eats the prefix and leaves `mcp__reddit__-alt`.
    text = text.replace("mcp__plugin_jadlis-research_reddit-alt__", "mcp__reddit-alt__")
    text = re.sub(r"mcp__plugin_jadlis-research_([A-Za-z0-9-]+?)__", r"mcp__\1__", text)

    # 4. Namespaced slash-commands and agent types.
    text = text.replace("/jadlis-research:", "/")
    text = re.sub(r"(['\"])jadlis-research:([A-Za-z0-9_-]+)\1", r"\1\2\1", text)

    # 5. Verifier data root.
    text = text.replace("${CLAUDE_PLUGIN_DATA}", PLUGIN_DATA_ROOT)

    # 6. Plugin userConfig placeholder.
    text = text.replace("${user_config.VAULT_PATH}", VAULT_PATH)

    # 7. Workflow fallbacks: in the plugin they are dry-run stubs fed by args;
    #    in the live contour there is no plugin host to supply them.
    text = text.replace("A.pluginRoot || '.'", f"A.pluginRoot || '{LIVE_ROOT}'")
    text = text.replace("A.vaultPath || ''", f"A.vaultPath || '{VAULT_PATH}'")

    return text


def is_text(path: Path) -> bool:
    return path.suffix.lower() in TEXT_SUFFIXES


# --------------------------------------------------------------------------
# Plan building
# --------------------------------------------------------------------------

class Item:
    """One rendered file."""

    def __init__(self, src: Path, dst: Path, rel: str):
        self.src = src
        self.dst = dst
        self.rel = rel          # path relative to dest root, for display
        self.status = "new"     # new | changed | same
        self.plus = 0
        self.minus = 0
        self.diff: list[str] = []

    def compute(self) -> None:
        if not self.dst.exists() or self.dst.is_symlink():
            self.status = "new"
            return
        if is_text(self.src):
            new = substitute(self.src.read_text(encoding="utf-8"))
            try:
                old = self.dst.read_text(encoding="utf-8")
            except UnicodeDecodeError:
                self.status = "changed"
                return
            if old == new:
                self.status = "same"
                return
            self.status = "changed"
            self.diff = list(
                difflib.unified_diff(
                    old.splitlines(keepends=True),
                    new.splitlines(keepends=True),
                    fromfile=f"dest/{self.rel}",
                    tofile=f"render/{self.rel}",
                )
            )
            for line in self.diff[2:]:
                if line.startswith("+") and not line.startswith("+++"):
                    self.plus += 1
                elif line.startswith("-") and not line.startswith("---"):
                    self.minus += 1
        else:
            self.status = "same" if self.dst.read_bytes() == self.src.read_bytes() else "changed"


class Link:
    """One protocol symlink in search-community."""

    def __init__(self, link: Path, target: Path, rel: str):
        self.link = link
        self.target = target
        self.rel = rel
        self.status = "new"     # new | ok | retarget | replace-file

    def compute(self) -> None:
        if self.link.is_symlink():
            self.status = "ok" if os.readlink(self.link) == str(self.target) else "retarget"
        elif self.link.exists():
            self.status = "replace-file"
        else:
            self.status = "new"


def collect(plugin: Path, dest: Path) -> tuple[list[Item], list[Link]]:
    items: list[Item] = []

    def add(src: Path, dst: Path) -> None:
        rel_src = src.relative_to(plugin).as_posix()
        if any(rel_src.startswith(p) for p in SKIP_SOURCE_PREFIXES):
            return
        items.append(Item(src, dst, dst.relative_to(dest).as_posix()))

    for src_rel, dst_rel in SKILL_TREES + ASSET_TREES:
        base = plugin / src_rel
        if not base.is_dir():
            continue
        for f in sorted(base.rglob("*")):
            if f.is_file():
                add(f, dest / dst_rel / f.relative_to(base))

    for src_rel, dst_rel in SINGLE_FILES:
        f = plugin / src_rel
        if f.is_file():
            add(f, dest / dst_rel)

    for src_dir, pattern, dst_dir in FLAT_GLOBS:
        base = plugin / src_dir
        if not base.is_dir():
            continue
        for f in sorted(base.glob(pattern)):
            if f.is_file():
                add(f, dest / dst_dir / f.name)

    links: list[Link] = []
    proto_dest = dest / "skills/full-research/protocols"
    proto_src = plugin / PROTOCOL_SRC
    if proto_src.is_dir():
        for f in sorted(proto_src.glob("*.md")):
            link = dest / PROTOCOL_LINK_DIR / f.name
            links.append(Link(link, proto_dest / f.name, link.relative_to(dest).as_posix()))

    rendered = {it.dst for it in items}
    for link_rel, target_rel in EXTRA_LINKS:
        target = dest / target_rel
        if target in rendered:
            links.append(Link(dest / link_rel, target, link_rel))

    for it in items:
        it.compute()
    for ln in links:
        ln.compute()
    return items, links


# --------------------------------------------------------------------------
# Rendering
# --------------------------------------------------------------------------

def render(items: list[Item], links: list[Link]) -> tuple[int, int]:
    written = 0
    for it in items:
        if it.status == "same":
            continue
        it.dst.parent.mkdir(parents=True, exist_ok=True)
        if it.dst.is_symlink():
            it.dst.unlink()
        if is_text(it.src):
            it.dst.write_text(substitute(it.src.read_text(encoding="utf-8")), encoding="utf-8")
        else:
            shutil.copyfile(it.src, it.dst)
        shutil.copymode(it.src, it.dst)  # preserve exec bits
        written += 1

    linked = 0
    for ln in links:
        if ln.status == "ok":
            continue
        ln.link.parent.mkdir(parents=True, exist_ok=True)
        if ln.link.is_symlink() or ln.link.exists():
            ln.link.unlink()
        ln.link.symlink_to(ln.target)
        linked += 1
    return written, linked


def prune(items: list[Item], links: list[Link], dest: Path, assume_yes: bool, dry_run: bool) -> list[Path]:
    """Files inside the rendered skill trees that the plugin no longer provides."""
    keep = {it.dst.resolve() for it in items} | {ln.link.resolve() for ln in links}
    stale: list[Path] = []
    for _, dst_rel in SKILL_TREES:
        base = dest / dst_rel
        if not base.is_dir():
            continue
        for f in sorted(base.rglob("*")):
            if f.is_file() and not f.is_symlink() and f.resolve() not in keep:
                stale.append(f)
    if not stale:
        return []
    print("\nPrune candidates (in dest, absent from plugin):")
    for f in stale:
        print(f"  - {f.relative_to(dest)}")
    if dry_run:
        return stale
    if not assume_yes:
        print("Refusing to delete without --yes.")
        return []
    for f in stale:
        f.unlink()
    print(f"Deleted {len(stale)} stale file(s).")
    return stale


# --------------------------------------------------------------------------
# Invariants
# --------------------------------------------------------------------------

def scan(path: Path, needles: list[str]) -> list[tuple[int, str, str]]:
    if not is_text(path):
        return []
    try:
        text = path.read_text(encoding="utf-8")
    except (UnicodeDecodeError, OSError):
        return []
    hits = []
    for n, line in enumerate(text.splitlines(), 1):
        for needle in needles:
            if needle not in line:
                continue
            # `${PLUGIN_ROOT}` inside workflow JS is the JS template variable, not the placeholder.
            if needle == "{PLUGIN_ROOT}" and path.suffix == ".js" and "${PLUGIN_ROOT}" in line and line.count("{PLUGIN_ROOT}") == line.count("${PLUGIN_ROOT}"):
                continue
            # Machine-local read-side telemetry hook is intentionally referenced by ~/.claude path (guarded call).
            if "full-research-telemetry.py" in line:
                continue
            hits.append((n, needle, line.strip()[:160]))
    return hits


def check(plugin: Path, dest: Path, items: list[Item]) -> tuple[int, int]:
    print("\n--- invariants: dest ---")
    dest_bad = 0
    for it in items:
        if it.dst.is_symlink() or not it.dst.exists():
            continue
        for n, needle, line in scan(it.dst, DEST_FORBIDDEN):
            print(f"{it.dst}:{n}: [{needle}] {line}")
            dest_bad += 1
    print(f"dest violations: {dest_bad}")

    print("\n--- invariants: plugin ---")
    plugin_bad = 0
    for f in sorted(plugin.rglob("*")):
        if not f.is_file():
            continue
        rel = f.relative_to(plugin).as_posix()
        if (
            rel in PLUGIN_EXCEPTIONS
            or rel.startswith(PLUGIN_EXCEPTION_PREFIXES)
            or rel.startswith(".git/")
        ):
            continue
        for n, needle, line in scan(f, PLUGIN_FORBIDDEN):
            print(f"{rel}:{n}: [{needle}] {line}")
            plugin_bad += 1
    exempt = sorted(PLUGIN_EXCEPTIONS) + [p + "**" for p in PLUGIN_EXCEPTION_PREFIXES]
    print(f"plugin violations: {plugin_bad} (exceptions: {', '.join(exempt)})")
    return dest_bad, plugin_bad


# --------------------------------------------------------------------------
# Main
# --------------------------------------------------------------------------

def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--plugin", type=Path, default=DEFAULT_PLUGIN)
    ap.add_argument("--dest", type=Path, default=DEFAULT_DEST)
    ap.add_argument("--dry-run", action="store_true", help="print the plan, change nothing")
    ap.add_argument("--check", action="store_true", help="only verify invariants")
    ap.add_argument("--prune", action="store_true", help="drop dest files the plugin no longer has")
    ap.add_argument("--yes", action="store_true", help="confirm --prune deletions")
    ap.add_argument("--verbose", action="store_true", help="full diffs instead of +/- counts")
    args = ap.parse_args()

    plugin = args.plugin.resolve()
    dest = args.dest.resolve()
    if not plugin.is_dir():
        print(f"error: plugin dir not found: {plugin}", file=sys.stderr)
        return 3

    print(f"plugin: {plugin}")
    print(f"dest:   {dest}")

    items, links = collect(plugin, dest)

    if not args.check:
        print(f"\n--- plan ({len(items)} files, {len(links)} symlinks) ---")
        for it in items:
            if it.status == "same":
                continue
            mark = "NEW    " if it.status == "new" else f"CHANGED"
            extra = "" if it.status == "new" else f"  (+{it.plus}/-{it.minus})"
            print(f"  {mark} {it.rel}{extra}")
            if args.verbose and it.diff:
                sys.stdout.writelines(it.diff)
        for ln in links:
            if ln.status != "ok":
                print(f"  SYMLINK[{ln.status}] {ln.rel} -> {ln.target}")

        n_new = sum(1 for i in items if i.status == "new")
        n_chg = sum(1 for i in items if i.status == "changed")
        n_same = sum(1 for i in items if i.status == "same")
        l_new = sum(1 for l in links if l.status == "new")
        l_re = sum(1 for l in links if l.status == "retarget")
        l_file = sum(1 for l in links if l.status == "replace-file")
        l_ok = sum(1 for l in links if l.status == "ok")
        print(
            f"\nsummary: {n_new} new, {n_chg} changed, {n_same} same | "
            f"symlinks: {l_new} new, {l_re} retarget, {l_file} replacing regular file, {l_ok} ok"
        )

    replaced: list[str] = []
    if not args.check and not args.dry_run:
        written, linked = render(items, links)
        replaced = [l.rel for l in links if l.status == "replace-file"]
        print(f"\nrendered {written} file(s), {linked} symlink(s)")
        if replaced:
            print("regular files replaced by symlinks:")
            for r in replaced:
                print(f"  - {r}")

    if args.prune:
        prune(items, links, dest, args.yes, args.dry_run or args.check)

    dest_bad, plugin_bad = check(plugin, dest, items)

    if dest_bad:
        return 1
    if plugin_bad:
        if args.dry_run:
            print("(dry-run: plugin violations are a warning only)")
            return 0
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
