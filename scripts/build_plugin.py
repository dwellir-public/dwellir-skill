"""Bundle the canonical Hyperliquid data skill without maintaining a second copy."""
import argparse
import json
import shutil
import subprocess
import tempfile
import zipfile
from pathlib import Path

from package_scope import validate_scope

root = Path(__file__).resolve().parents[1]
parser = argparse.ArgumentParser()
parser.add_argument("--mcp-url", help="Override the shared MCP URL for staging")
parser.add_argument("--sync-hyperliquid", action="store_true", help="Update the vendored skill from the pinned source")
args = parser.parse_args()
source = json.loads((root / "hyperliquid-source.json").read_text())
if source["path"] != "skills/hyperliquid-data":
    raise ValueError("Expected the canonical Hyperliquid data skill")
output = root / "dist" / "dwellir"
if output.exists():
    shutil.rmtree(output)
output.mkdir(parents=True)
for directory in (".codex-plugin", ".claude-plugin", ".cursor-plugin"):
    shutil.copytree(root / directory, output / directory)
shutil.copytree(root / "assets", output / "assets")
with tempfile.TemporaryDirectory() as temporary:
    checkout = Path(temporary) / "hyperliquid"
    subprocess.run(["git", "clone", "--quiet", "--no-checkout", source["repository"], str(checkout)], check=True)
    subprocess.run(["git", "-C", str(checkout), "checkout", "--quiet", "--detach", source["revision"]], check=True)
    actual = subprocess.check_output(["git", "-C", str(checkout), "rev-parse", "HEAD"], text=True).strip()
    if actual != source["revision"]:
        raise ValueError("Hyperliquid source revision mismatch")
    destination = checkout / "skills" / "hyperliquid-data"
    vendored = root / "skills" / "hyperliquid-data"
    if args.sync_hyperliquid:
        shutil.rmtree(vendored, ignore_errors=True)
        shutil.copytree(destination, vendored)
    canonical_files = {p.relative_to(destination): p.read_bytes() for p in destination.rglob("*") if p.is_file()}
    vendored_files = {p.relative_to(vendored): p.read_bytes() for p in vendored.rglob("*") if p.is_file()}
    if canonical_files != vendored_files:
        raise ValueError("Vendored Hyperliquid differs from its pin; run with --sync-hyperliquid")
validate_scope(root / "skills")
shutil.copytree(root / "skills", output / "skills")
mcp = json.loads((root / ".mcp.json").read_text())
if args.mcp_url:
    mcp["mcpServers"]["dwellir"]["url"] = args.mcp_url
(output / ".mcp.json").write_text(json.dumps(mcp, indent=2) + "\n")
shutil.copyfile(root / "hyperliquid-source.json", output / "hyperliquid-source.json")
shutil.copyfile(root / "LICENSE.md", output / "LICENSE.md")
for name in ("README.md", "PLUGIN.md"):
    shutil.copyfile(root / name, output / name)
with zipfile.ZipFile(root / "dist" / "dwellir-plugin.zip", "w") as archive:
    for path in sorted(output.rglob("*")):
        if path.is_file():
            entry = zipfile.ZipInfo(path.relative_to(output).as_posix())
            entry.compress_type = zipfile.ZIP_DEFLATED
            entry.external_attr = 0o100644 << 16
            archive.writestr(entry, path.read_bytes())
print(output)
