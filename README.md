# Dwellir developer plugin

Connect Dwellir's hosted MCP server and load skills for blockchain data workflows.
The package includes portable OpenAI manifests and Codex, Claude Code, and Cursor compatibility manifests.
Grok Bot uses Cursor's plugin infrastructure and needs a separate client check before submission.

## What you can do

- Discover blockchain endpoints and query supported chain state.
- Inspect account usage and manage API keys with dashboard-approved access.
- Read Hyperliquid market data and sample WebSocket streams.
- Build read-only EVM, Substrate, and Hyperliquid data applications.

The package does not execute trades, transfer assets, sign transactions, or change billing.
Key-management access applies to Dwellir API keys. It does not authorize blockchain writes.
Queries and stream captures consume the connected Dwellir account's quota.

## Skills

| Skill | Use |
| --- | --- |
| `dwellir` | Account connection, endpoint discovery, usage, permissions, and project configuration |
| `evm` | EVM state, contract reads, transaction analysis, and subscriptions |
| `substrate` | Polkadot and Substrate storage, blocks, events, and Sidecar queries |
| `hyperliquid-data` | HyperEVM state, market snapshots, order books, and data streams |

`hyperliquid-data` comes unchanged from the pinned canonical Hyperliquid repository.
The package excludes that repository's general trading skill and execution examples.

## Connect

Add this remote Streamable HTTP server in your client's MCP settings:

```text
https://mcp.dwellir.com/mcp
```

Start the client's browser authorization flow.
The Dwellir dashboard offers **Read only** or **Manage keys** within the client's requested scopes.
No API key belongs in the MCP configuration.

See [client setup](https://www.dwellir.com/docs/agents/mcp) and [plugin installation](https://github.com/dwellir-public/dwellir-skill/blob/main/PLUGIN.md).
A skills-only installation does not configure MCP or authorize an account.

## Try it

- "Find the Ethereum mainnet endpoint and read the latest block number."
- "Summarize my Dwellir RPC usage."
- "Read this account's Polkadot balance."
- "Sample the ETH order book on Hyperliquid."
- "Build a read-only Hyperliquid market data stream."

For application credentials, the `dwellir` skill checks CLI capabilities before using project setup.
Project setup requires released CLI 0.2.0 or later.
Keep application secrets in private environment files or a secret store, outside chat and version control.

## Data and support

MCP returns non-secret key references. Raw API keys stay on Dwellir servers.
Optional MCP analytics is off until you opt in for your connection.
Use `analytics_preferences` to inspect the setting or disable it with `enabled: false`.
Explicit opt-in expires after 30 days. A new connection starts with analytics off.
The control tool is never captured. Opt-out does not delete existing events.

When enabled, PostHog receives tool names, timings, outcomes, normalized client labels, and hashed connection and session identifiers.
Inferred intent uses selected RPC methods, Info query types, stream subscriptions, usage intervals, and public documentation paths.
Complete arguments, responses, credentials, and raw errors are excluded.
Revoke the connection from the dashboard's Agents page, then remove its local client configuration.

- [Documentation](https://www.dwellir.com/docs/agents)
- [Privacy policy](https://www.dwellir.com/privacy-policy)
- [Terms of service](https://www.dwellir.com/terms-of-service)
- Public support: support@dwellir.com

## Development

See [PLUGIN.md](https://github.com/dwellir-public/dwellir-skill/blob/main/PLUGIN.md) in the source repository for build, validation, release, and submission steps.
The public upload excludes that development guide and private reviewer credentials.
Version 0.2.1 includes five positive and three negative review cases, unrestricted country availability, and no commerce declaration.
A verified demo URL and published privacy coverage remain required before OpenAI submission.
Directory acceptance and publication require separate review.

## License

MIT. See [LICENSE.md](LICENSE.md) and the bundled Hyperliquid license.
