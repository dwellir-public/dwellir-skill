# Dwellir plugin package

The package combines the production Dwellir MCP server with four developer skills.
Native Codex authorization and authenticated read calls have passed production testing.
Each directory's remaining client and reviewer checks are separate from package validation.

## Build and verify

```sh
python -m unittest discover -s scripts -p 'test_*.py'
python scripts/build_plugin.py
python scripts/validate_package.py
claude plugin validate .claude-plugin/plugin.json --strict
claude plugin validate .claude-plugin/marketplace.json --strict
claude plugin validate skills --strict
```

The output is `dist/dwellir-plugin.zip` and the expanded `dist/dwellir` directory.
For staging, pass `--mcp-url https://mcp.dwellir.tech:9999/mcp` to both build and validation commands.
The override changes only the archive's MCP URL.
The root Git package and production archive contain identical skills and client manifests.

`hyperliquid-source.json` pins a canonical repository revision and its `skills/hyperliquid-data` directory.
The build compares every vendored skill and license byte with that revision.
To update, change the revision and run `python scripts/build_plugin.py --sync-hyperliquid`.
Review the vendor changes and pin together.

A build-time check rejects known transaction-execution examples, unexpected skills, scripts, and symlinks.
It supplements human content review. It does not establish policy compliance or directory acceptance.

## Client installation

### Claude Code

For local testing:

```sh
claude --plugin-dir ./dist/dwellir
```

For Git installation, add this repository as a marketplace, then install `dwellir@dwellir-skill`.
Private Git installation requires repository access. Directory distribution requires public source.
Use `/mcp` to authenticate Dwellir after installing.
Existing users of `dwellir-skill@dwellir-skill` must replace that legacy skills-only installation.

### Codex

Load the package through Codex's plugin marketplace workflow.
The `.codex-plugin/plugin.json` manifest references the shared skills and MCP configuration.
The package does not modify an existing standalone Dwellir MCP connection.
Use one Dwellir connection per client to avoid duplicate tools.

### Cursor and Grok Bot

Cursor reads `.cursor-plugin/plugin.json`, `skills/`, and the declared `.mcp.json`.
Test local installation and account connection in Cursor before submitting the public repository.
Test Grok Bot separately; marketplace submission alone does not prove availability in Grok Bot.
See the [Cursor plugin reference](https://cursor.com/docs/reference/plugins).

## Package scope

The bundle supports blockchain data, account usage, API key management, and read-only application development.
It excludes trade execution, asset transfers, wallet signing, automatic trading, and billing changes.
The canonical `hyperliquid-data` skill replaces the general Hyperliquid trading reference from version 0.1.0.
EVM and Substrate references exclude transaction submission examples.

**Read only** permits account inspection and chain queries.
**Manage keys** also permits Dwellir API key changes. It grants no blockchain write capability.
A permission denial must not trigger a fallback to other local credentials.

Project setup requires released CLI 0.2.0 or later and a successful capability check.
Until that release exists, the skill reports the limitation instead of installing an unreleased branch.

## Directory submission

Use the same production MCP URL and release contents for each submission.

1. Verify public source availability, publisher identity, and access to each submission portal.
2. Test each target client's installation, account approval, permissions, revocation, and quota attribution.
3. Test successful and failed calls in PostHog MCP Analytics.
4. Prepare a populated reviewer account and each directory's test cases.
5. Review public documentation, privacy, terms, support, availability, and branding.
6. Review each completed form with the publisher before selecting Submit.

Use a monitored administrative address for review correspondence and `support@dwellir.com` for public support when separate fields exist.
Verify whether a single contact field is public before choosing its address.

OpenAI accepts MCP and skills together. Prepare five positive and three negative test cases.
See [OpenAI submission requirements](https://developers.openai.com/plugins/deploy/submission).
Claude's connector and plugin listings require separate submissions.
See [Claude plugin submission](https://claude.com/docs/plugins/submit).

## Release

CI tests, builds, and verifies the package for pull requests, main pushes, and version tags.
After merging, wait for the main workflow to pass.
Create a release tag matching the version in all three plugin manifests.
Wait for the tag workflow, then attach its `dwellir-plugin.zip` artifact to the GitHub release.
Verify the release download against the CI artifact's SHA-256 checksum.
Directory submission and publication remain separate reviewed steps.
