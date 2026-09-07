# Dwellir plugin package

The package combines the Dwellir hosted MCP connection with developer skills.
It is in development. The public MCP hostname and directory entry are not live yet.

Build the archive with:

```sh
python scripts/build_plugin.py
```

For staging, pass `--mcp-url https://YOUR-STAGING-HOST/mcp`.
The output is `dist/dwellir-plugin.zip` and the expanded `dist/dwellir` directory.
Install the expanded package through your client's local plugin workflow.
Do not install the repository root as the final package.

`hyperliquid-source.json` pins the canonical Hyperliquid repository revision.
The build copies its skill, references, and license unchanged.
The older repository-local Hyperliquid directory remains for existing standalone consumers.
It is excluded from this package.

The general Dwellir skill teaches hosted tools and CLI credential setup.
EVM and Substrate references remain bundled for existing developer workflows.
The Dwellir MCP connects through browser OAuth.
No local MCP process or manually supplied API key is required.

## Public directory handoff

1. Deploy and test the coordinated backend, dashboard, MCP, and CLI releases.
2. Register the HTTPS MCP endpoint through ChatGPT developer mode.
3. Add the assigned connection ID through `.app.json` and the manifest's `apps` field.
4. Add verified privacy, terms, support, logo, and screenshot metadata.
5. Test the archive in both target clients with a reviewer account.
6. Submit the Dwellir listing after release approval.

Keep the publisher and listing name Dwellir.
Use blockchain, RPC, and Hyperliquid in accurate capability descriptions and task examples.
The package references Hyperliquid support without implying publication by the Hyperliquid team.
Search placement and directory acceptance are not guaranteed.
