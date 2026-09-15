# Dwellir developer plugin

Connect Dwellir's hosted MCP server and load skills for blockchain data workflows.
The same package supports Codex, Claude Code, and Cursor plugin manifests.
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

See [client setup](https://www.dwellir.com/docs/agents/mcp) and [plugin installation](PLUGIN.md).
A skills-only installation does not configure MCP or authorize an account.

## Try it

- "Find the Ethereum mainnet endpoint and read the latest block number."
- "Summarize my Dwellir RPC usage."
- "Read this account's Polkadot balance."
- "Sample the ETH order book on Hyperliquid."
- "Build a read-only Hyperliquid market data stream."

For application credentials, the `dwellir` skill checks CLI capabilities before using project setup.
Project setup requires CLI 0.2.0 or later. It is unavailable until that version is released.
Keep application secrets in private environment files or a secret store, outside chat and version control.

## Data and support

MCP returns non-secret key references. Raw API keys stay on Dwellir servers.
The server records tool usage, duration, outcomes, client metadata, and approximate sessions in PostHog.
It excludes tool arguments, responses, credentials, and raw errors from those events.
Revoke the connection from the dashboard's Agents page, then remove its local client configuration.

- [Documentation](https://www.dwellir.com/docs/agents)
- [Privacy policy](https://www.dwellir.com/privacy-policy)
- [Terms of service](https://www.dwellir.com/terms-of-service)
- Public support: support@dwellir.com

## Development

See [PLUGIN.md](PLUGIN.md) for build, validation, release, and submission steps.
Directory acceptance and publication require separate review.

## License

MIT. See [LICENSE.md](LICENSE.md) and the bundled Hyperliquid license.
