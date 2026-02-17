# Premium Endpoints Reference

Paid add-on endpoints and dedicated node infrastructure available through Dwellir. All premium endpoints include a **3-day free trial** and are managed via the [Dwellir dashboard](https://dashboard.dwellir.com).

## Overview

Premium endpoints are subscription add-ons on top of your base plan. They provide specialized access to high-demand protocols and REST APIs that go beyond standard RPC.

| Endpoint | Price | Protocol | Description |
|----------|-------|----------|-------------|
| Hyperliquid gRPC | $299/mo | gRPC | High-frequency trading data streaming |
| Hyperliquid Orderbook | $199/mo | WSS only | Real-time L2 order book data |
| Polkadot Sidecar | $100/mo | REST | Polkadot block/account queries via REST |
| Kusama Sidecar | $100/mo | REST | Kusama block/account queries via REST |
| AssetHub Polkadot Sidecar | $100/mo | REST | AssetHub Polkadot REST queries |
| AssetHub Kusama Sidecar | $100/mo | REST | AssetHub Kusama REST queries |
| Centrifuge Sidecar | $100/mo | REST | Centrifuge REST queries |
| KILT Sidecar | $100/mo | REST | KILT REST queries |

## Hyperliquid gRPC

**Price:** $299/month | **Free trial:** 3 days | **Protocol:** gRPC

High-performance gRPC streaming for Hyperliquid mainnet. Designed for low-latency trading applications, market data ingestion, and real-time analytics.

### Endpoint

```
Endpoint slug: api-hyperliquid-mainnet-grpc
URL: https://api-hyperliquid-mainnet-grpc.n.dwellir.com/{API_KEY}
```

### gRPC Connection Setup

```python
import grpc

channel = grpc.secure_channel(
    'api-hyperliquid-mainnet-grpc.n.dwellir.com:443',
    grpc.ssl_channel_credentials()
)
# Use generated Hyperliquid protobuf stubs for method calls
```

### Use Cases

- Real-time trade streaming
- Market data feeds for trading bots
- High-frequency order monitoring
- Low-latency block data ingestion

## Hyperliquid Orderbook

**Price:** $199/month | **Free trial:** 3 days | **Protocol:** WSS only (HTTPS hidden)

Real-time L2 order book data for Hyperliquid mainnet. WebSocket-only endpoint — HTTP requests are not supported.

### Endpoint

```
Endpoint slug: api-hyperliquid-mainnet-orderbook
WSS: wss://api-hyperliquid-mainnet-orderbook.n.dwellir.com/{API_KEY}
```

### WebSocket Connection

```javascript
const ws = new WebSocket(
  `wss://api-hyperliquid-mainnet-orderbook.n.dwellir.com/${process.env.DWELLIR_API_KEY}`
);

ws.on('open', () => {
  // Subscribe to order book updates
  ws.send(JSON.stringify({
    method: 'subscribe',
    subscription: { type: 'l2Book', coin: 'ETH' }
  }));
});

ws.on('message', (data) => {
  const update = JSON.parse(data);
  console.log('Order book update:', update);
});
```

### Use Cases

- Order book visualization
- Spread monitoring and arbitrage
- Liquidity analysis
- Market making strategies

## Sidecar REST APIs

**Price:** $100/month each | **Free trial:** 3 days | **Protocol:** REST (HTTPS)

Substrate API Sidecar provides a RESTful interface for querying Substrate-based chain data. More convenient than raw JSON-RPC for applications that prefer HTTP REST patterns.

### Available Chains

| Chain | Endpoint Slug |
|-------|---------------|
| Polkadot | `api-polkadot-sidecar` |
| Kusama | `api-kusama-sidecar` |
| AssetHub Polkadot | `api-asset-hub-polkadot-sidecar` |
| AssetHub Kusama | `api-asset-hub-kusama-sidecar` |
| Centrifuge | `api-centrifuge-sidecar` |
| KILT | `api-kilt-sidecar` |

### URL Format

```
https://api-{chain}-sidecar.n.dwellir.com/{API_KEY}/{route}
```

### Core Routes

#### Blocks

```bash
# Latest block
curl "https://api-polkadot-sidecar.n.dwellir.com/${DWELLIR_API_KEY}/blocks/head"

# Block by number
curl "https://api-polkadot-sidecar.n.dwellir.com/${DWELLIR_API_KEY}/blocks/12345678"

# Block by hash
curl "https://api-polkadot-sidecar.n.dwellir.com/${DWELLIR_API_KEY}/blocks/0x..."
```

#### Accounts

```bash
# Account balance
curl "https://api-polkadot-sidecar.n.dwellir.com/${DWELLIR_API_KEY}/accounts/{accountId}/balance-info"

# Staking info
curl "https://api-polkadot-sidecar.n.dwellir.com/${DWELLIR_API_KEY}/accounts/{accountId}/staking-info"

# Vesting info
curl "https://api-polkadot-sidecar.n.dwellir.com/${DWELLIR_API_KEY}/accounts/{accountId}/vesting-info"
```

#### Pallets

```bash
# List storage items for a pallet
curl "https://api-polkadot-sidecar.n.dwellir.com/${DWELLIR_API_KEY}/pallets/staking/storage"

# Get specific storage value
curl "https://api-polkadot-sidecar.n.dwellir.com/${DWELLIR_API_KEY}/pallets/staking/storage/activeEra"
```

#### Transaction Material

```bash
# Get data needed to construct a transaction offline
curl "https://api-polkadot-sidecar.n.dwellir.com/${DWELLIR_API_KEY}/transaction/material"
```

#### Runtime

```bash
# Runtime metadata
curl "https://api-polkadot-sidecar.n.dwellir.com/${DWELLIR_API_KEY}/runtime/metadata"

# Runtime spec
curl "https://api-polkadot-sidecar.n.dwellir.com/${DWELLIR_API_KEY}/runtime/spec"
```

#### Node Info

```bash
# Node version
curl "https://api-polkadot-sidecar.n.dwellir.com/${DWELLIR_API_KEY}/node/version"

# Network info
curl "https://api-polkadot-sidecar.n.dwellir.com/${DWELLIR_API_KEY}/node/network"
```

### Full Route Reference

| Route | Method | Description |
|-------|--------|-------------|
| `/blocks/head` | GET | Latest block with extrinsics and events |
| `/blocks/{blockId}` | GET | Block by number or hash |
| `/blocks/head/header` | GET | Latest block header only |
| `/accounts/{accountId}/balance-info` | GET | Free, reserved, frozen balances |
| `/accounts/{accountId}/staking-info` | GET | Staking status, nominations, rewards |
| `/accounts/{accountId}/staking-payouts` | GET | Staking payout history |
| `/accounts/{accountId}/vesting-info` | GET | Vesting schedules |
| `/pallets/{palletId}/storage` | GET | List storage items for pallet |
| `/pallets/{palletId}/storage/{storageItemId}` | GET | Specific storage value |
| `/pallets/{palletId}/errors` | GET | Pallet error definitions |
| `/pallets/{palletId}/constants` | GET | Pallet constants |
| `/transaction/material` | GET | Chain metadata for offline tx construction |
| `/transaction/fee-estimate` | POST | Estimate fee for a transaction |
| `/runtime/metadata` | GET | Full runtime metadata |
| `/runtime/spec` | GET | Runtime spec version |
| `/node/version` | GET | Node software version |
| `/node/network` | GET | Network info (chain, peers) |

### Sidecar Code Example

```typescript
const SIDECAR_URL = `https://api-polkadot-sidecar.n.dwellir.com/${process.env.DWELLIR_API_KEY}`;

// Get account balance
const response = await fetch(`${SIDECAR_URL}/accounts/${accountId}/balance-info`);
const balance = await response.json();
console.log(`Free: ${balance.free}, Reserved: ${balance.reserved}`);

// Get latest block
const blockResponse = await fetch(`${SIDECAR_URL}/blocks/head`);
const block = await blockResponse.json();
console.log(`Block #${block.number}: ${block.extrinsics.length} extrinsics`);
```

## Dedicated Nodes

Single-tenant blockchain infrastructure for production workloads requiring guaranteed compute, storage, and network resources. Dedicated nodes are not shared with other customers.

### Available Chains

| Chain | Node Offering | Monthly Price |
|-------|---------------|---------------|
| Monad | Dedicated Node | $1,000 |
| Hyperliquid Mainnet | Dedicated Node (Tokyo) | $1,150 |
| Hyperliquid Testnet | Dedicated Node | $800 |
| Ethereum | Dedicated Node (Lodestar + Geth) | $830 |
| Base | Dedicated Node | $650 |
| BSC | Dedicated Node | $650 |
| EOS | Dedicated Node + Hyperion Indexer | $890 |
| Waves | Dedicated Node | $370 |
| Acala | Dedicated Node | $248 |

### When to Use Dedicated Nodes

- **Guaranteed performance** — no noisy neighbors, consistent latency
- **High throughput** — no shared rate limits
- **Custom configuration** — node flags, chain specs, or indexer setup
- **Compliance** — single-tenant for regulatory requirements
- **Critical workloads** — production systems that cannot tolerate shared infrastructure variability

### How Dedicated Nodes Work

1. Subscribe via the [Dwellir dashboard](https://dashboard.dwellir.com)
2. Dwellir provisions a dedicated instance in the appropriate region
3. You receive a unique endpoint URL
4. The node is exclusively yours — no shared resources

## How to Subscribe

### Premium Endpoints

1. Log in to [dashboard.dwellir.com](https://dashboard.dwellir.com)
2. Navigate to the chain/endpoint you want
3. Click on a premium endpoint (marked with a lock icon)
4. Start the 3-day free trial or subscribe directly
5. The endpoint activates immediately

### Dedicated Nodes

1. Log in to [dashboard.dwellir.com](https://dashboard.dwellir.com)
2. Navigate to the Dedicated Nodes section
3. Select your chain
4. Subscribe — provisioning begins immediately
5. You'll receive your dedicated endpoint URL

### Billing

- Premium endpoints and dedicated nodes are billed monthly
- Charges are separate from your base RPC plan
- Cancellation takes effect at end of billing period
- Free trials auto-convert to paid unless cancelled

## Documentation Links

- Hyperliquid docs: [dwellir.com/docs/hyperliquid](https://www.dwellir.com/docs/hyperliquid)
- Polkadot docs: [dwellir.com/docs/polkadot](https://www.dwellir.com/docs/polkadot)
- Kusama docs: [dwellir.com/docs/kusama](https://www.dwellir.com/docs/kusama)
- Sidecar upstream docs: [paritytech.github.io/substrate-api-sidecar/dist](https://paritytech.github.io/substrate-api-sidecar/dist)
- Dashboard: [dashboard.dwellir.com](https://dashboard.dwellir.com)
