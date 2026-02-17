# Dwellir Blockchain Skills

AI agent skills for blockchain development, powered by [Dwellir](https://www.dwellir.com).

## What are Skills?

Skills are structured knowledge files that give AI coding agents (like Claude Code) deep context about specific tools, APIs, and infrastructure. Instead of searching docs or guessing at API patterns, agents load the relevant skill and get immediate access to endpoint formats, code examples, method references, and best practices.

**This skill enables agents to:**
- Connect to 140+ blockchain networks via Dwellir RPC endpoints
- Write correct code for EVM, Substrate/Polkadot, and non-EVM chains
- Use trace/debug APIs for transaction analysis
- Set up WebSocket subscriptions for real-time data
- Build on Hyperliquid — gRPC streaming, order book data, Info/Exchange APIs, trading patterns
- Work with premium endpoints (Hyperliquid gRPC, Orderbook, Sidecar APIs)
- Follow best practices for retry logic, caching, and connection management

## Available Skills

| Skill | Description |
|-------|-------------|
| **dwellir** | Dwellir blockchain RPC infrastructure — 140+ chains, EVM & Substrate endpoints, trace/debug APIs, WebSocket subscriptions, premium endpoints, and dedicated nodes |

## Installation

```bash
npx skills add dwellir-public/dwellir-skill
```

## Usage

Once installed, the skill activates automatically when you mention blockchain-related topics. Example prompts:

- "Get the ETH balance for this wallet using Dwellir"
- "Set up a WebSocket subscription for new Ethereum blocks"
- "Query the Polkadot staking info for this account"
- "Trace this failed transaction to find the revert reason"
- "Connect to Moonbeam and read a smart contract"
- "What Substrate parachains does Dwellir support?"
- "Set up a multi-chain provider for Ethereum, Polygon, and Arbitrum"
- "Stream Hyperliquid order book data via WebSocket"
- "Build a funding rate monitor for Hyperliquid perpetuals"

## Dwellir Integration

### RPC Endpoints (140+ chains)

High-performance JSON-RPC access to EVM chains, Substrate/Polkadot parachains, and non-EVM networks (Aptos, Sui, TON, TRON, Starknet, and more).

```
https://api-{network}.n.dwellir.com/{API_KEY}
wss://api-{network}.n.dwellir.com/{API_KEY}
```

### Trace & Debug APIs

Full EVM execution tracing — `debug_traceTransaction`, `debug_traceCall`, `trace_block`, and more. Available on Developer plan and above.

### WebSocket Subscriptions

Real-time data via WSS — new blocks, pending transactions, contract events, storage changes. Native support for both EVM and Substrate subscription patterns.

### Premium Endpoints

- **Hyperliquid gRPC** ($299/mo) — high-frequency trading data streaming
- **Hyperliquid Orderbook** ($199/mo) — real-time L2 order book via WSS
- **Sidecar REST APIs** ($100/mo each) — Polkadot, Kusama, AssetHub, Centrifuge, KILT

### Dedicated Nodes

Single-tenant infrastructure for Ethereum, Base, BSC, Hyperliquid, Monad, EOS, Waves, and Acala. Starting at $248/month.

## Skill Structure

```
dwellir-skill/
├── .claude-plugin/
│   └── marketplace.json          # Plugin manifest
├── skills/
│   └── dwellir/
│       ├── SKILL.md              # Main skill definition
│       └── references/
│           ├── rpc-reference.md              # EVM + general RPC methods
│           ├── substrate-reference.md        # Polkadot/Substrate ecosystem
│           ├── hyperliquid-reference.md      # Hyperliquid L1, HyperEVM, trading APIs
│           └── premium-endpoints-reference.md # Sidecar, dedicated nodes, pricing
├── README.md
├── LICENSE.md
└── .gitignore
```

## Getting Started with Dwellir

1. **Sign up** at [dashboard.dwellir.com/register](https://dashboard.dwellir.com/register) (no credit card required)
2. **Create an API key** in the dashboard
3. **Set environment variable:**
   ```bash
   export DWELLIR_API_KEY="your-uuid-key"
   export DWELLIR_RPC_URL="https://api-ethereum-mainnet.n.dwellir.com/${DWELLIR_API_KEY}"
   ```
4. **Start building** — the skill handles the rest

## Contributing

1. Fork this repository
2. Create a feature branch
3. Add or update skill content
4. Test by loading the skill in Claude Code
5. Submit a pull request

## License

MIT — see [LICENSE.md](LICENSE.md)
