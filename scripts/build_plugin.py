"""Bundle the canonical Hyperliquid skill without maintaining a second copy."""
import argparse
import json
import shutil
import subprocess
import tempfile
from pathlib import Path

root = Path(__file__).resolve().parents[1]
parser = argparse.ArgumentParser()
parser.add_argument("--mcp-url", default="https://mcp.dwellir.com/mcp")
args = parser.parse_args()
source = json.loads((root / "hyperliquid-source.json").read_text())
output = root / "dist" / "dwellir"
if output.exists():
    shutil.rmtree(output)
output.mkdir(parents=True)
shutil.copytree(root / ".codex-plugin", output / ".codex-plugin")
shutil.copytree(root / "assets", output / "assets")
shutil.copytree(root / "skills", output / "skills", ignore=shutil.ignore_patterns("hyperliquid"))
with tempfile.TemporaryDirectory() as temporary:
    checkout = Path(temporary) / "hyperliquid"
    subprocess.run(["git", "clone", "--quiet", "--no-checkout", source["repository"], str(checkout)], check=True)
    subprocess.run(["git", "-C", str(checkout), "checkout", "--quiet", "--detach", source["revision"]], check=True)
    actual = subprocess.check_output(["git", "-C", str(checkout), "rev-parse", "HEAD"], text=True).strip()
    if actual != source["revision"]:
        raise ValueError("Hyperliquid source revision mismatch")
    destination = output / "skills" / "hyperliquid"
    destination.mkdir()
    for name in ("SKILL.md", "LICENSE"):
        shutil.copyfile(checkout / name, destination / name)
    shutil.copytree(checkout / "references", destination / "references")
(output / ".mcp.json").write_text(json.dumps({"mcpServers": {"dwellir": {"url": args.mcp_url}}}, indent=2) + "\n")
shutil.copyfile(root / "hyperliquid-source.json", output / "hyperliquid-source.json")
shutil.copyfile(root / "LICENSE.md", output / "LICENSE.md")
shutil.make_archive(str(root / "dist" / "dwellir-plugin"), "zip", output)
print(output)
