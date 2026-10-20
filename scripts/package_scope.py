"""Catch known execution examples and unintended skills before packaging.

This content check supplements human review. It does not establish directory acceptance.
"""
import re
from pathlib import Path

SKILLS = {'dwellir', 'evm', 'substrate', 'hyperliquid-data'}
EXECUTION = re.compile(
    r'eth_send(?:Raw)?Transaction|author_(?:submit\w*|rotateKeys|insertKey)'
    r'|signAndSend|api\.tx\.|exchange\.(?:order|cancel)\s*\(|/exchange\b',
    re.IGNORECASE,
)

LEGACY_TOOLS = re.compile(r"\b(?:rpc_methods|rpc_call|hyperliquid_info|capture_stream)\b")


def validate_scope(skills: Path) -> None:
    if {p.name for p in skills.iterdir()} != SKILLS:
        raise ValueError('Unexpected skill directories in submission package')
    for path in sorted(skills.rglob('*')):
        if path.is_symlink():
            raise ValueError(f'Symlink in submission skills: {path}')
        if not path.is_file():
            continue
        if path.name != 'LICENSE' and path.suffix != '.md':
            raise ValueError(f'Unexpected executable or asset in submission skills: {path}')
        content = path.read_text()
        if LEGACY_TOOLS.search(content):
            raise ValueError(f'Removed generic MCP tool in submission skills: {path}')
        if EXECUTION.search(content):
            raise ValueError(f'Execution example in submission skills: {path}')
