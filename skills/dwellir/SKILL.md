---
name: dwellir
description: Connect Dwellir accounts, inspect RPC usage, manage API keys, query blockchain state, and configure developer projects. Use for Dwellir infrastructure, blockchain RPC setup, EVM, Substrate, Solana, and Hyperliquid projects.
---

# Build with Dwellir

Use the hosted Dwellir MCP tools for account access and bounded chain queries.
Use the CLI to configure credentials for projects that run independently.
For Hyperliquid architecture, trading patterns, and streaming protocols, load the bundled `hyperliquid` skill.
For detailed EVM or Substrate references, load `evm` or `substrate` when available.

## Connect and query

Connect the Dwellir MCP server through the client's account connection flow.
The browser shows the requesting application and access level.
Users can create a Dwellir account during browser login.

1. Discover the chain, network, node type, and transport with `list_endpoints`.
2. Use `list_keys` to select an enabled key by name and non-secret reference.
3. Create a named key with `create_key` when the task requires one.
4. Use `rpc_methods` before `rpc_call`; supported methods vary by endpoint.
5. Use `hyperliquid_info` for supported Info queries and `capture_stream` for short WebSocket samples.
6. Use `usage_summary` or `usage_history` to inspect account consumption.

Queries consume the connected account's quota.
Direct tools keep API key values on Dwellir servers.
A key reference identifies a key within MCP; it is not a credential for application code.
Disabling or deleting a key interrupts projects that use it.

## Configure a project

Check `dwellir --version` and `dwellir project setup --help` first.
If the command is unavailable, follow the current installation instructions at https://github.com/dwellir-public/cli.
Do not invent installation commands or package names.

Run `dwellir auth login` for a local browser callback.
Use `dwellir auth login --device-code` for remote terminals and containers.
The user approves access in a browser; the CLI saves its account credential locally.

Discover exact chain, network, and node-type values with `dwellir endpoints --help` and the endpoint command.
Run setup inside the project directory:

```sh
dwellir project setup --chain ethereum --network mainnet --create-key my-project
```

Use `--key-name` to select an existing key by its unique name.
Use `--env-file .env.local` when the framework expects that file.
Use `--replace` only when replacing existing Dwellir configuration is intended.
Quota flags apply to newly created keys; check `--help` for current options.

Setup writes `DWELLIR_API_KEY`, `DWELLIR_RPC_URL`, and `DWELLIR_WSS_URL` into a private environment file.
It also adds an ignore rule and refuses tracked environment files.
Generate project code that reads those variables.
Do not print, read back into chat, commit, or pass raw credentials as command arguments.
For hosted projects, use the deployment provider's secret store.

Verify configuration through a bounded chain request that reports only the result.
For continuous streams, gRPC, or unsupported methods, build application code using the canonical protocol references.
The MCP provides short samples, not persistent subscriptions.

## Current documentation

Use `search_docs` and `get_docs` for current Dwellir endpoint capabilities.
Keep public API fallbacks explicit when a Hyperliquid query is unavailable through Dwellir.
Do not silently switch providers or imply that fallback requests use Dwellir infrastructure.
