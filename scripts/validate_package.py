"""Check that Git installations and the release archive contain the same plugin."""
import argparse
import json
import zipfile
from pathlib import Path

from package_scope import validate_scope

root = Path(__file__).resolve().parents[1]
parser = argparse.ArgumentParser()
parser.add_argument('--mcp-url', help='Expected staging URL override')
args = parser.parse_args()
package = root / 'dist' / 'dwellir'
validate_scope(root / 'skills')
validate_scope(package / 'skills')
manifest_paths = [f'.{client}-plugin/plugin.json' for client in ('codex', 'claude', 'cursor')]
for path in manifest_paths:
    manifest = json.loads((package / path).read_text())
    assert manifest['name'] == 'dwellir', path
    assert manifest['version'] == json.loads((package / manifest_paths[0]).read_text())['version'], path
    assert (root / path).read_bytes() == (package / path).read_bytes(), path
    assert (package / manifest.get('mcpServers', '.mcp.json')).is_file(), path

expected_mcp = json.loads((root / '.mcp.json').read_text())
if args.mcp_url:
    expected_mcp['mcpServers']['dwellir']['url'] = args.mcp_url
packaged_mcp = json.loads((package / '.mcp.json').read_text())
assert packaged_mcp == expected_mcp, 'Packaged MCP configuration differs from its source'
mcp = packaged_mcp['mcpServers']['dwellir']
assert mcp['type'] == 'http'
assert mcp['url'].startswith('https://')
marketplace = json.loads((package / '.claude-plugin/marketplace.json').read_text())
assert marketplace['plugins'][0]['name'] == 'dwellir'
assert marketplace['plugins'][0]['source'] == './'
for skill in ('dwellir', 'evm', 'substrate', 'hyperliquid-data'):
    path = package / 'skills' / skill / 'SKILL.md'
    assert path.read_text().startswith(f'---\nname: {skill}\n'), path
for path in (root / 'skills').rglob('*'):
    if path.is_file():
        assert path.read_bytes() == (package / path.relative_to(root)).read_bytes(), path
assert (package / 'skills/hyperliquid-data/LICENSE').is_file()
assert (package / 'assets/dwellir-logo.svg').is_file()
with zipfile.ZipFile(root / 'dist/dwellir-plugin.zip') as archive:
    files = {p.relative_to(package).as_posix(): p.read_bytes() for p in package.rglob('*') if p.is_file()}
    assert set(archive.namelist()) == set(files)
    for name, content in files.items():
        assert archive.read(name) == content, name
print(f'Validated {len(manifest_paths)} manifests, 4 skills, and {len(files)} archive files')
