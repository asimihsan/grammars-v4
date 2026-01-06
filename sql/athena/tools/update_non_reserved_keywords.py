#!/usr/bin/env python3
"""Update non_reserved_keyword rule in AthenaParser.g4 from a keyword list."""
from __future__ import annotations

import pathlib
import re
import sys

SCRIPT_DIR = pathlib.Path(__file__).resolve().parent
ROOT_DIR = SCRIPT_DIR.parent
LEXER_FILE = ROOT_DIR / "AthenaLexer.g4"
PARSER_FILE = ROOT_DIR / "AthenaParser.g4"
RESERVED_SELECT = ROOT_DIR / "reserved_select_keywords.txt"
RESERVED_DDL = ROOT_DIR / "reserved_ddl_keywords.txt"

START_MARKER = "// @non_reserved_keyword:start"
END_MARKER = "// @non_reserved_keyword:end"


def load_keywords(path: pathlib.Path) -> list[str]:
    keywords: list[str] = []
    if not path.exists():
        return keywords
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        keywords.append(line)
    return keywords


def load_lexer_tokens(path: pathlib.Path) -> set[str]:
    tokens: set[str] = set()
    token_re = re.compile(r"^([A-Z_][A-Z0-9_]*)\s*:\s*'([^']*)';")
    literal_ok = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*$")
    for line in path.read_text(encoding="utf-8").splitlines():
        match = token_re.match(line.strip())
        if not match:
            continue
        token, literal = match.group(1), match.group(2)
        if not literal_ok.match(literal):
            continue
        tokens.add(token)
    return tokens


def build_rule(keywords: list[str]) -> str:
    if not keywords:
        raise SystemExit("computed non_reserved_keyword list is empty")
    lines = ["non_reserved_keyword", "    : " + keywords[0]]
    for keyword in keywords[1:]:
        lines.append("    | " + keyword)
    lines.append("    ;")
    return "\n".join(lines)


def replace_block(text: str, replacement: str) -> str:
    start_idx = text.find(START_MARKER)
    end_idx = text.find(END_MARKER)
    if start_idx == -1 or end_idx == -1 or end_idx < start_idx:
        raise SystemExit("Markers not found in AthenaParser.g4")
    end_idx = end_idx + len(END_MARKER)
    new_block = f"{START_MARKER}\n{replacement}\n{END_MARKER}"
    return text[:start_idx] + new_block + text[end_idx:]


def main() -> int:
    lexer_tokens = load_lexer_tokens(LEXER_FILE)
    reserved_select = set(load_keywords(RESERVED_SELECT))
    reserved_ddl = set(load_keywords(RESERVED_DDL))
    unknown_reserved = sorted((reserved_select | reserved_ddl) - lexer_tokens)
    if unknown_reserved:
        print(
            "Warning: reserved keywords not present in AthenaLexer.g4: "
            + ", ".join(unknown_reserved),
            file=sys.stderr,
        )

    non_reserved = sorted(lexer_tokens - reserved_select)

    parser_text = PARSER_FILE.read_text(encoding="utf-8")
    rule_text = build_rule(non_reserved)
    updated = replace_block(parser_text, rule_text)
    if updated != parser_text:
        PARSER_FILE.write_text(updated, encoding="utf-8")
    return 0


if __name__ == "__main__":
    sys.exit(main())
