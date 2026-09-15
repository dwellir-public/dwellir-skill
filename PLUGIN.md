# Dwellir plugin package

The package combines the hosted Dwellir MCP server with developer skills.
Production MCP is available at `https://mcp.dwellir.com/mcp`.
Frontend authorization and client compatibility still require release testing before directory submission.

## Build and verify

```sh
python scripts/build_plugin.py
python scripts/validate_package.py
claude plugin validate .claude-plugin/plugin.json --strict
claude plugin validate .claude-plugin/marketplace.json --strict
```

The output is `dist/dwellir-plugin.zip` and the expanded `dist/dwellir` directory.
For staging, pass `--mcp-url https://mcp.dwellir.tech:9999/mcp` to the build command.
Pass the same override to `scripts/validate_package.py` when verifying that staging artifact.
The root Git package and archive use the same skills and client manifests.
The staging override changes only the archive's MCP URL.

`hyperliquid-source.json` pins the canonical Hyperliquid repository revision.
The build verifies every vendored skill, reference, and license byte against that revision.
To update the source, change the revision and run `python scripts/build_plugin.py --sync-hyperliquid`.
Review and commit the resulting vendor changes together with the pin.

## Client installation

Claude Code can load the local package with `claude --plugin-dir ./dist/dwellir`.
For Git installation, add this repository as a marketplace, then install `dwellir@dwellir-skill`.
Existing marketplace users must replace the previous `dwellir-skill@dwellir-skill` installation to enable the hosted MCP package.
Private Git installation requires repository access.
Public directory submission requires a public repository.

Cursor loads `.cursor-plugin/plugin.json`, the shared `skills/` directory, and the declared `.mcp.json` file.
Test both Cursor and Grok Bot authorization before submitting the repository to Cursor's marketplace.
See the [Cursor plugin reference](https://cursor.com/docs/reference/plugins).

Codex loads `.codex-plugin/plugin.json` and the same MCP configuration.
Use the client's local plugin installation workflow for `dist/dwellir`.
MCP authorization opens a browser.
No local MCP process or manually supplied API key is required.

## Directory submission

1. Test account approval, read-only permissions, key management, revocation, and quota attribution in each target client.
2. Verify PostHog MCP events from successful and failed authenticated calls.
3. Review branding, public documentation, privacy, terms, support, reviewer credentials, and screenshots.
4. Review all bundled skills against each directory's policy before submitting.

For OpenAI, submit the production MCP URL through **With MCP** and upload the tested skills bundle.
Do not add an existing integration ID through `.app.json`.
Prepare five positive and three negative test cases.
See [OpenAI submission requirements](https://developers.openai.com/plugins/deploy/submission).

Claude's connector and plugin listings require separate submissions.
Use the hosted MCP URL for the connector and the public repository for the plugin.
See [Claude plugin submission](https://claude.com/docs/plugins/submit).

## Policy review remains open

The canonical Hyperliquid skill includes exchange writes and order-placement instructions.
The EVM reference also lists signed transaction submission.
These files remain unchanged upstream copies or existing references.
Read-only MCP tools do not make the whole package read-only.
Directory review must assess this content before any compliance attestation.
Publishing this repository or archive does not establish directory acceptance.

## Release

CI builds and verifies the package for pull requests, main pushes, and version tags.
After merging, wait for the main workflow to pass.
Create a release tag matching the version in all three plugin manifests.
Wait for that tag's workflow, then attach its `dwellir-plugin.zip` artifact to the GitHub release.
Directory publication remains a separate reviewed step.
