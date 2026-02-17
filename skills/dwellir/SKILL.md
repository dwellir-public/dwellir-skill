---
name: dwellir
description: >
  Dwellir blockchain RPC infrastructure including endpoints for 140+ chains
  (EVM, Substrate/Polkadot, Aptos, Sui, TON, TRON, Starknet, and more),
  HTTP & WebSocket APIs, trace/debug methods, premium endpoints
  (Hyperliquid gRPC, Hyperliquid Orderbook, HyperEVM, Substrate Sidecar APIs),
  and dedicated node infrastructure.
  Use when connecting to blockchain networks, making RPC calls,
  querying chain state, subscribing to events, or using Dwellir-specific
  endpoints. Triggers on mentions of Dwellir, RPC, blockchain,
  api key, endpoint, or chain names.
---

# Dwellir Blockchain Infrastructure

## Related Skills

For detailed chain-specific references, load the relevant skill:

| Skill | Use When |
|-------|----------|
| **evm** | Working with EVM chains (Ethereum, Arbitrum, Base, Polygon, etc.), eth_ methods, Solidity, trace/debug APIs |
| **substrate** | Working with Polkadot, Kusama, parachains, @polkadot/api, Sidecar REST APIs |
| **hyperliquid** | Working with Hyperliquid L1, HyperEVM, Info API, gRPC streaming, order book data |

## Intake Questions
- Which chain and network should Dwellir target?
- Is this read-only or does it involve submitting transactions?
- Does this need HTTP, WebSocket, or both?
- What endpoint or API key should I use (default: `DWELLIR_RPC_URL`, optional `DWELLIR_WSS_URL`)?
- Any constraints (rate limits, plan tier, region)?

## Safety Defaults
- Default to testnet/devnet when a network is not specified.
- Prefer read-only operations unless the user explicitly needs writes.
- Never ask for or accept private keys or secret keys.
- Use environment variables for API keys — never hardcode them.

## Confirm Before Write
- Require explicit confirmation before submitting transactions to any network.
- If confirmation is missing, return the exact transaction payload for review.

## Agent API Key Provisioning
Programmatic API key provisioning for AI agents is **coming soon**. For now, users must create keys manually at [dashboard.dwellir.com](https://dashboard.dwellir.com).

## x402 Status
x402 pay-per-request is **not yet supported**. Agent-based billing is on the roadmap.

## Quick Reference

| Product | Description | Use Case |
|---------|-------------|----------|
| **RPC Endpoints** | High-performance blockchain access (140+ chains) | dApp backend, wallet interactions, chain queries |
| **Trace & Debug APIs** | EVM execution tracing and debugging | Transaction analysis, gas profiling, internal calls |
| **WebSocket** | Real-time subscriptions via WSS | New blocks, pending transactions, log events |
| **Premium Endpoints** | Hyperliquid gRPC, Orderbook, Sidecar APIs | High-frequency trading, Polkadot REST queries |
| **Dedicated Nodes** | Single-tenant infrastructure | Production workloads requiring guaranteed resources |

## RPC Endpoints

Dwellir provides low-latency RPC endpoints for 140+ blockchain networks.

### Endpoint Format

```
HTTPS:  https://api-{network}.n.dwellir.com/{API_KEY}
WSS:    wss://api-{network}.n.dwellir.com/{API_KEY}
```

Examples:
```
https://api-ethereum-mainnet.n.dwellir.com/xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
wss://api-ethereum-mainnet.n.dwellir.com/xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
https://api-polkadot.n.dwellir.com/xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
```

### Authentication

API key is embedded in the URL path. No separate headers needed. Keys are UUIDs.

### Getting an API Key

1. Register at [dashboard.dwellir.com/register](https://dashboard.dwellir.com/register) (no credit card required)
2. Navigate to the API Keys section
3. Click "Create API Key"
4. Copy the UUID key into your endpoint URL

### Connection Setup

```typescript
// EVM chains (ethers.js)
import { JsonRpcProvider } from 'ethers';
const provider = new JsonRpcProvider(process.env.DWELLIR_RPC_URL);

// EVM chains (viem)
import { createPublicClient, http } from 'viem';
import { mainnet } from 'viem/chains';
const client = createPublicClient({
  chain: mainnet,
  transport: http(process.env.DWELLIR_RPC_URL),
});

// Substrate/Polkadot (@polkadot/api)
import { ApiPromise, WsProvider } from '@polkadot/api';
const wsProvider = new WsProvider(process.env.DWELLIR_WSS_URL);
const api = await ApiPromise.create({ provider: wsProvider });

// curl
curl -X POST ${DWELLIR_RPC_URL} \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","method":"eth_blockNumber","params":[],"id":1}'
```

### Supported Networks

| Category | Networks |
|----------|----------|
| **EVM L1** | Ethereum, BSC, Avalanche (C-Chain), Fantom, Gnosis, Celo, Chiliz, IoTeX, Ronin, Sonic, Viction |
| **EVM L2/Rollups** | Arbitrum (One, Nova), Base, Blast, Linea, LISK, Mantle, Manta (Atlantic, Pacific), Optimism, Polygon, Polygon zkEVM, Scroll, Unichain, zkSync Era, Zora |
| **Substrate/Polkadot** | Polkadot, Kusama, Asset Hub (Polkadot/Kusama), Acala, Astar, Bifrost, Bridge Hub, Centrifuge, Hydration, Moonbeam, Moonriver, KILT, and 20+ more parachains |
| **Non-EVM** | Aptos, Sui, TON, TRON, Celestia, Bittensor, Starknet, Hyperliquid |
| **Emerging** | Berachain, Flow (EVM Gateway), Immutable, Manta Pacific, Movement, Monad |
| **Testnets** | Ethereum Sepolia/Holesky, Arbitrum Sepolia, Base Sepolia, Blast Sepolia, BSC Testnet, Fantom Testnet, Gnosis Chiado, Linea Sepolia, LISK Sepolia, Mantle Sepolia, Moonbase Alpha, Optimism Sepolia, Polygon Amoy, Scroll Sepolia, zkSync Sepolia, Avalanche Fuji, and more |

Full list: [dwellir.com/docs/getting-started/supported-chains](https://www.dwellir.com/docs/getting-started/supported-chains)

### Rate Limits & Plans

1 RPC response = 1 API credit, applied uniformly across HTTP, WebSocket, and trace/debug operations.

| Plan | Cost/mo | Rate Limit | Monthly Credits | Trace/Debug | Autoscaling |
|------|---------|------------|-----------------|-------------|-------------|
| **Free** | $0 | 20 req/sec | 500K/day | No | No |
| **Developer** | $49 | 100 req/sec | 25M | Yes | Yes |
| **Growth** | $299 | 500 req/sec | 150M | Yes | Yes |
| **Scale** | $999 | 2,000 req/sec | 500M | Yes | Yes |
| **Enterprise** | Custom | Custom | Custom | Yes | Yes |

Extra credits: $5/M (Developer), $3/M (Growth), $2/M (Scale). Spending limits configurable per API key.

Current pricing: [dwellir.com/docs/getting-started/pricing](https://www.dwellir.com/docs/getting-started/pricing)

## Premium Endpoints

Paid add-on subscriptions with 3-day free trials. Managed via [dashboard.dwellir.com](https://dashboard.dwellir.com).

| Endpoint | Price | Protocol | Use Case |
|----------|-------|----------|----------|
| **Hyperliquid gRPC** | $299/mo | gRPC | High-frequency trading, streaming |
| **Hyperliquid Orderbook** | $199/mo | WSS only | Real-time L2 order book data |
| **Sidecar APIs** | $100/mo each | REST | Polkadot/Kusama/AssetHub/Centrifuge/KILT block and account queries |

## Dedicated Nodes

Single-tenant blockchain infrastructure for production workloads.

| Chain | Monthly Price |
|-------|---------------|
| Monad | $1,000 |
| Hyperliquid Mainnet | $1,150 |
| Hyperliquid Testnet | $800 |
| Ethereum (Lodestar + Geth) | $830 |
| Base | $650 |
| BSC | $650 |
| EOS + Hyperion Indexer | $890 |
| Waves | $370 |
| Acala | $248 |

Contact sales or subscribe via [dashboard.dwellir.com](https://dashboard.dwellir.com).

## Best Practices

1. **Use environment variables** — store `DWELLIR_RPC_URL` / `DWELLIR_WSS_URL` / `DWELLIR_API_KEY`, never hardcode keys.
2. **Retry with backoff** — use exponential backoff on 429 (rate limit) and 5xx errors.
3. **Prefer WebSocket for Substrate** — Substrate chains are WebSocket-native; HTTP works but WSS is more efficient.
4. **Batch JSON-RPC requests** — send arrays of requests to reduce round trips on EVM chains.
5. **Cache metadata** — cache chain metadata and type registries to avoid redundant fetches.
6. **Set spending limits** — configure per-key spending limits in the dashboard to prevent overages.
7. **Use testnets first** — develop and test on testnets before switching to mainnet.
8. **Monitor usage** — check the dashboard for credit consumption and approaching limits.

## Documentation Links

- Getting started: [dwellir.com/docs/getting-started](https://www.dwellir.com/docs/getting-started)
- Supported chains: [dwellir.com/docs/getting-started/supported-chains](https://www.dwellir.com/docs/getting-started/supported-chains)
- Pricing: [dwellir.com/docs/getting-started/pricing](https://www.dwellir.com/docs/getting-started/pricing)
- Tracing: [dwellir.com/docs/getting-started/tracing](https://www.dwellir.com/docs/getting-started/tracing)
- Per-chain docs: `https://www.dwellir.com/docs/{chain}` (e.g., [ethereum](https://www.dwellir.com/docs/ethereum), [polkadot](https://www.dwellir.com/docs/polkadot))
- Dashboard: [dashboard.dwellir.com](https://dashboard.dwellir.com)
