# Hyperliquid Reference

Complete reference for building on Hyperliquid through Dwellir — HyperEVM JSON-RPC, Info API proxy, gRPC L1 streaming, order book WebSocket, and dedicated nodes.

Hyperliquid is Dwellir's key competitive edge. Dwellir runs its own Hyperliquid nodes and offers infrastructure that goes beyond standard RPC: a custom gRPC gateway for Hypercore data, a real-time order book server, and a filtering Info API proxy — with edge servers in Singapore and Tokyo.

## How Hyperliquid Works

Hyperliquid is a purpose-built L1 blockchain optimized for trading. It has two layers:

**HyperCore** — The native trading layer. Fully on-chain perpetual futures and spot order books. Every order, cancellation, trade, and liquidation settles within one block. Handles ~200,000 orders/second with sub-second finality via HyperBFT consensus.

**HyperEVM** — A general-purpose EVM smart contract layer that runs alongside HyperCore. Developers can deploy Solidity contracts that interact with HyperCore's liquidity. Chain ID: **998**.

Key properties:
- All order books are fully on-chain — no off-chain matching
- Sub-second block times with one-block finality
- Native gas token: **HYPE**
- Perpetuals support up to 50x leverage
- Native spot trading with HIP-3 DEX deployment

## What Dwellir Provides

Dwellir runs full Hyperliquid infrastructure: the official HL node, plus custom software built by Dwellir and the community for serving specific data channels.

| Endpoint | What It Serves | Protocol | Pricing |
|----------|---------------|----------|---------|
| **HyperEVM JSON-RPC** | EVM state, smart contracts, blocks | HTTPS + WSS | Base plan |
| **Info API proxy** | Market data, user state, metadata | HTTPS (POST) | Base plan |
| **L1 gRPC Gateway** | Hypercore block/fill streaming | gRPC | $299/mo add-on |
| **Orderbook WebSocket** | Real-time L2 order book data | WSS only | $199/mo add-on |
| **Dedicated Node** (Tokyo) | Full stack, uncapped throughput | All | $1,150/mo |
| **Dedicated Node** (Testnet) | Full stack for testing | All | $800/mo |

### What Dwellir Does NOT Proxy

**Exchange API** — Hyperliquid's Exchange endpoint (`https://api.hyperliquid.xyz/exchange`) handles order placement, cancellation, transfers, and other write operations. These require EIP-712 signatures from your wallet and go directly to Hyperliquid's API, not through Dwellir. See [Hyperliquid Exchange API docs](https://hyperliquid.gitbook.io/hyperliquid-docs/for-developers/api/exchange-endpoint).

**Native WebSocket** — Hyperliquid's subscription WebSocket (`wss://api.hyperliquid.xyz/ws`) for user events, trades, and candles is a separate service. Dwellir's Orderbook WebSocket serves order book data specifically.

### How It Fits Together

A typical Hyperliquid application uses Dwellir for **reading data** and Hyperliquid's native API for **writing**:

```
┌─────────────────────────────────────────────────────────┐
│  Your Application                                        │
├──────────────────┬──────────────────────────────────────┤
│  READ (Dwellir)  │  WRITE (Hyperliquid native)          │
│                  │                                       │
│  EVM state ──────┤  Place orders ─── api.hyperliquid.xyz │
│  Info queries ───┤  Cancel orders    /exchange           │
│  gRPC streams ───┤  Transfers        (requires sig)      │
│  Order book ─────┤  Set leverage                         │
└──────────────────┴──────────────────────────────────────┘
```

## HyperEVM JSON-RPC (Base Plan)

Standard EVM JSON-RPC served by [Nanoreth](https://github.com/hl-archive-node/nanoreth) (a reth fork for Hyperliquid EVM data). Supports HTTP and WebSocket.

### Endpoint

```
HTTPS: https://api-hyperliquid-mainnet.n.dwellir.com/{API_KEY}
WSS:   wss://api-hyperliquid-mainnet.n.dwellir.com/{API_KEY}
```

### Connection

```typescript
import { JsonRpcProvider } from 'ethers';

const provider = new JsonRpcProvider(
  `https://api-hyperliquid-mainnet.n.dwellir.com/${process.env.DWELLIR_API_KEY}`
);

// Standard EVM methods work
const blockNumber = await provider.getBlockNumber();
const balance = await provider.getBalance('0x...');
const chainId = await provider.getNetwork(); // chainId: 998
```

```typescript
import { createPublicClient, http } from 'viem';

const client = createPublicClient({
  chain: {
    id: 998,
    name: 'Hyperliquid',
    nativeCurrency: { name: 'HYPE', symbol: 'HYPE', decimals: 18 },
    rpcUrls: {
      default: {
        http: [`https://api-hyperliquid-mainnet.n.dwellir.com/${process.env.DWELLIR_API_KEY}`],
      },
    },
  },
  transport: http(),
});
```

### Supported Methods

All standard Ethereum JSON-RPC methods: `eth_blockNumber`, `eth_getBalance`, `eth_call`, `eth_getTransactionByHash`, `eth_getBlockByNumber`, `eth_getLogs`, `eth_sendRawTransaction`, etc.

### Use Cases

- Deploy and interact with Solidity contracts on HyperEVM
- Query EVM state (balances, contract storage, logs)
- Monitor EVM-side events and transactions
- Build HyperEVM dApps that interact with HyperCore liquidity

## Info API Proxy (Base Plan)

Dwellir proxies Hyperliquid's `/info` endpoint through a [filtering REST server](https://github.com/dwellir-public/hyperliquid-rest-server). This validates requests and blocks certain high-risk query types (e.g., `fileSnapshot` is restricted on lower-tier plans).

### Endpoint

```
POST https://api-hyperliquid-mainnet.n.dwellir.com/{API_KEY}/info
Content-Type: application/json
```

All Info API requests use `POST` with a JSON body containing a `type` field.

### Market Data Queries

#### Get All Mid Prices

```javascript
const DWELLIR_INFO = `https://api-hyperliquid-mainnet.n.dwellir.com/${process.env.DWELLIR_API_KEY}/info`;

const mids = await fetch(DWELLIR_INFO, {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ type: 'allMids' }),
}).then(r => r.json());
// { "BTC": "113377.0", "ETH": "3245.5", "HYPE": "28.4", ... }
```

#### Get Order Book Snapshot

```javascript
const book = await fetch(DWELLIR_INFO, {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    type: 'l2Book',
    coin: 'BTC',
    nSigFigs: null, // null = full precision, or 2/3/4/5
  }),
}).then(r => r.json());
// book.levels[0] = bids [{ px, sz, n }], book.levels[1] = asks
```

#### Get Candle Data

```javascript
const candles = await fetch(DWELLIR_INFO, {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    type: 'candleSnapshot',
    req: {
      coin: 'BTC',
      interval: '1h', // 1m,3m,5m,15m,30m,1h,2h,4h,8h,12h,1d,3d,1w,1M
      startTime: Date.now() - 86400000,
      endTime: Date.now(),
    },
  }),
}).then(r => r.json());
// [{ t: openTime, T: closeTime, o, h, l, c, v, n, s, i }]
```

### Perpetuals Metadata

#### Universe & Asset Contexts (Funding, OI, Volume)

```javascript
const [meta, assetCtxs] = await fetch(DWELLIR_INFO, {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ type: 'metaAndAssetCtxs' }),
}).then(r => r.json());
// meta.universe = [{ name, szDecimals, maxLeverage, ... }]
// assetCtxs = [{ funding, openInterest, prevDayPx, dayNtlVlm, premium, ... }]
```

#### Funding Rate History

```javascript
const history = await fetch(DWELLIR_INFO, {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    type: 'fundingHistory',
    coin: 'BTC',
    startTime: Date.now() - 86400000,
  }),
}).then(r => r.json());
// [{ coin, fundingRate, premium, time }]
```

#### Predicted Funding Rates (Cross-Venue)

```javascript
const predictions = await fetch(DWELLIR_INFO, {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ type: 'predictedFundings' }),
}).then(r => r.json());
// Predicted rates across Hyperliquid, Binance, Bybit, etc.
```

### Spot Metadata

```javascript
const [meta, assetCtxs] = await fetch(DWELLIR_INFO, {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ type: 'spotMetaAndAssetCtxs' }),
}).then(r => r.json());
// meta.tokens = [{ name, tokenId, szDecimals, ... }]
// meta.universe = [{ name, tokens: [baseIdx, quoteIdx], ... }]
```

### User Account Queries

These require knowing the user's address (blockchain data is public).

#### Perpetual Positions & Margin

```javascript
const state = await fetch(DWELLIR_INFO, {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ type: 'clearinghouseState', user: '0x...' }),
}).then(r => r.json());
// state.marginSummary = { accountValue, totalNtlPos, totalRawUsd, totalMarginUsed }
// state.assetPositions = [{ position: { coin, szi, leverage, liquidationPx, ... } }]
```

#### Spot Balances

```javascript
const state = await fetch(DWELLIR_INFO, {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ type: 'spotClearinghouseState', user: '0x...' }),
}).then(r => r.json());
// state.balances = [{ coin, hold, total, entryNtl }]
```

#### Open Orders

```javascript
const orders = await fetch(DWELLIR_INFO, {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ type: 'frontendOpenOrders', user: '0x...' }),
}).then(r => r.json());
// [{ coin, side, limitPx, sz, oid, orderType, reduceOnly, ... }]
```

#### User Fills / Trade History

```javascript
const fills = await fetch(DWELLIR_INFO, {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ type: 'userFills', user: '0x...' }),
}).then(r => r.json());
// [{ coin, px, sz, side, dir, closedPnl, fee, time, hash, ... }]
```

#### Order Status

```javascript
const result = await fetch(DWELLIR_INFO, {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ type: 'orderStatus', user: '0x...', oid: 91490942 }),
}).then(r => r.json());
// { status: "order", order: { order: {...}, status: "filled"|"open"|"canceled"|... } }
// or { status: "unknownOid" }
```

### Available Info API Query Types

All of these are available through Dwellir's Info API proxy unless noted.

| Type | Description | Risk Level |
|------|-------------|------------|
| `meta` | Perpetuals metadata (universe, margin tables) | LOW |
| `spotMeta` | Spot token metadata and trading pairs | LOW |
| `metaAndAssetCtxs` | Combined perp metadata + live market data | LOW |
| `spotMetaAndAssetCtxs` | Combined spot metadata + live market data | LOW |
| `exchangeStatus` | Exchange status with L1 timestamp | LOW |
| `allMids` | Mid prices for all coins | LOW |
| `l2Book` | Order book snapshot (20 levels/side) | LOW |
| `candleSnapshot` | OHLCV candle data (up to 5000 candles) | LOW |
| `clearinghouseState` | User perp positions and margin | MEDIUM |
| `spotClearinghouseState` | User spot balances | MEDIUM |
| `openOrders` | User's active orders | MEDIUM |
| `frontendOpenOrders` | Active orders with extra metadata | MEDIUM |
| `orderStatus` | Single order status by ID | MEDIUM |
| `userFills` | User fill history (max 2000) | MEDIUM |
| `userFillsByTime` | Paginated fills by time range | MEDIUM |
| `historicalOrders` | Recent order history (max 2000) | MEDIUM |
| `userFunding` | User funding payment history | MEDIUM |
| `userFees` | Fee schedule, volume, discounts | MEDIUM |
| `userRateLimit` | API rate limit status | LOW |
| `fundingHistory` | Historical funding rates for a coin | LOW |
| `predictedFundings` | Predicted funding across venues | LOW |
| `activeAssetData` | User leverage, max trade sizes per coin | MEDIUM |
| `delegations` | User staking delegations | MEDIUM |
| `delegatorSummary` | Staking summary | LOW |
| `subAccounts` | User sub-account list | MEDIUM-HIGH |
| `vaultDetails` | Vault info, followers, P&L | LOW |
| `userVaultEquities` | User's vault deposits | MEDIUM |
| `portfolio` | User P&L history (day/week/month/all) | MEDIUM |
| `referral` | Referral rewards and status | MEDIUM |
| `maxBuilderFee` | Builder fee approval check | LOW |
| `perpDexs` | All HIP-3 perpetual DEXes | LOW |
| `validatorL1Votes` | Validator governance votes | LOW |
| `borrowLendUserState` | User borrow/lend positions | MEDIUM |
| `allBorrowLendReserveStates` | All reserve interest rates | LOW |
| `tokenDetails` | Token supply and deployment info | LOW |
| `fileSnapshot` | **Restricted on Free/Starter plans** — full L4 order book dump | CRITICAL |

### Coin Naming Conventions

| Context | Format | Example |
|---------|--------|---------|
| Perpetual | Coin name | `"BTC"`, `"ETH"`, `"HYPE"` |
| Spot | `@{tokenIndex}` | `"@1"` (PURR), `"@150"` |
| Spot (display) | `SYMBOL/USDC` | `"PURR/USDC"` |
| HIP-3 DEX token | `dexname:SYMBOL` | `"xyz:XYZ100"` |

## L1 gRPC Gateway (Premium — $299/mo)

Low-latency gRPC streaming from the Hyperliquid L1. This is a [Dwellir-built gateway](https://github.com/dwellir-public/hyperliquid-l1-gateway) that reads Hypercore data directly from disk and serves it via gRPC. Data not available through the native Info API (like raw block data and fill streams) is accessible here.

### Endpoint

```
Host: api-hyperliquid-mainnet-grpc.n.dwellir.com:443
Service: hyperliquid_l1_gateway.v1.HyperLiquidL1Gateway
```

3-day free trial available.

### Available gRPC Methods

| Method | Type | Description |
|--------|------|-------------|
| `GetOrderBookSnapshot` | Unary | Order book snapshot at a given timestamp |
| `StreamBlocks` | Server streaming | Real-time block data from a timestamp |
| `StreamBlockFills` | Server streaming | Order fill executions in real-time |

### Connection

Proto files are available upon request from support@dwellir.com.

```python
import grpc

channel = grpc.secure_channel(
    'api-hyperliquid-mainnet-grpc.n.dwellir.com:443',
    grpc.ssl_channel_credentials()
)
# Use generated stubs from Hyperliquid L1 gateway proto files
# stub = HyperLiquidL1GatewayStub(channel)
# response = stub.GetOrderBookSnapshot(request)
```

```go
import (
    "crypto/tls"
    "google.golang.org/grpc"
    "google.golang.org/grpc/credentials"
)

creds := credentials.NewTLS(&tls.Config{})
conn, err := grpc.Dial(
    "api-hyperliquid-mainnet-grpc.n.dwellir.com:443",
    grpc.WithTransportCredentials(creds),
)
// Use generated stubs for method calls
```

### Use Cases

- Real-time block data ingestion for analytics
- Trade/fill streaming for backtesting engines
- Order book snapshots at specific timestamps
- Building indexers and data pipelines

## Orderbook WebSocket (Premium — $199/mo)

Real-time L2 order book data served by Dwellir's [order book server](https://github.com/dwellir-public/hyperliquid-orderbook-server), which reads Hypercore data directly from disk. **WSS only** — HTTP requests are not supported.

### Endpoint

```
WSS: wss://api-hyperliquid-mainnet-orderbook.n.dwellir.com/{API_KEY}
```

3-day free trial available.

### Benchmarked Message Rates

| Data Type | Messages/sec | Monthly Messages (per pair) |
|-----------|-------------|----------------------------|
| L2 Orderbook | ~10.4 msg/s | ~27M |
| L4 Orderbook | ~9.0 msg/s | ~23M |

### Connection

```javascript
const ws = new WebSocket(
  `wss://api-hyperliquid-mainnet-orderbook.n.dwellir.com/${process.env.DWELLIR_API_KEY}`
);

ws.on('open', () => {
  ws.send(JSON.stringify({
    method: 'subscribe',
    subscription: { type: 'l2Book', coin: 'ETH' }
  }));
});

ws.on('message', (data) => {
  const update = JSON.parse(data);
  // update.levels[0] = bids, update.levels[1] = asks
  // Each level: { px: "price", sz: "size", n: numOrders }
  console.log('Book update:', update);
});

// Unsubscribe
ws.send(JSON.stringify({
  method: 'unsubscribe',
  subscription: { type: 'l2Book', coin: 'ETH' }
}));
```

### Use Cases

- Market making — monitor spreads and depth in real-time
- Arbitrage — compare order books across venues
- Liquidity analysis — track depth changes over time
- Trading signals — detect large order placement/removal

## Dedicated Nodes

Full Hyperliquid stack on single-tenant infrastructure. No shared rate limits, uncapped throughput.

| Offering | Location | Monthly Price |
|----------|----------|---------------|
| Hyperliquid Mainnet | Tokyo | $1,150 |
| Hyperliquid Testnet | — | $800 |

A dedicated node includes:
- Official Hyperliquid L1 node (HyperCore + HyperEVM)
- Nanoreth (EVM JSON-RPC via HTTP + WebSocket)
- L1 gRPC Gateway (Hypercore streaming)
- Orderbook Server (L2/L4 book data)
- REST Server (Info API proxy)

Contact sales or subscribe via [dashboard.dwellir.com](https://dashboard.dwellir.com).

## Placing Orders (via Hyperliquid Native API)

Order placement and other write operations go directly to Hyperliquid's Exchange API — they are **not** proxied by Dwellir. This is because write operations require EIP-712 signatures from your wallet.

**Exchange API endpoint:** `POST https://api.hyperliquid.xyz/exchange`

For order placement, use the [Hyperliquid Python SDK](https://github.com/hyperliquid-dex/hyperliquid-python-sdk) or sign requests manually:

```python
from hyperliquid.utils import constants
from hyperliquid.exchange import Exchange
from eth_account import Account
import os

wallet = Account.from_key(os.environ["PRIVATE_KEY"])
exchange = Exchange(wallet, constants.MAINNET_API_URL)

# Limit buy 0.1 BTC at $100,000
result = exchange.order("BTC", True, 0.1, 100000, {"limit": {"tif": "Gtc"}})

# Cancel an order
exchange.cancel("BTC", order_id)
```

For full Exchange API documentation, see: [Hyperliquid Exchange Endpoint docs](https://hyperliquid.gitbook.io/hyperliquid-docs/for-developers/api/exchange-endpoint)

## Hyperliquid Native WebSocket

For real-time user events, trades, candle updates, and position changes, use Hyperliquid's native WebSocket directly:

**WebSocket URL:** `wss://api.hyperliquid.xyz/ws`

This is separate from Dwellir's Orderbook WebSocket. Key subscription types:

| Type | Description |
|------|-------------|
| `allMids` | All mid prices |
| `trades` | Trade executions per coin |
| `candle` | OHLCV candle updates |
| `l2Book` | Order book updates |
| `bbo` | Best bid/offer (lighter than l2Book) |
| `orderUpdates` | User order status changes |
| `userEvents` | Fills, funding, liquidations |
| `userFills` | Trade executions with snapshots |
| `clearinghouseState` | Position/margin updates |

```javascript
const ws = new WebSocket('wss://api.hyperliquid.xyz/ws');

ws.on('open', () => {
  ws.send(JSON.stringify({
    method: 'subscribe',
    subscription: { type: 'trades', coin: 'BTC' }
  }));
});

ws.on('message', (data) => {
  const msg = JSON.parse(data);
  if (msg.channel === 'trades') {
    for (const trade of msg.data) {
      console.log(`${trade.side} ${trade.sz} BTC @ ${trade.px}`);
    }
  }
});
```

For full WebSocket documentation, see: [Hyperliquid WebSocket docs](https://hyperliquid.gitbook.io/hyperliquid-docs/for-developers/api/websocket)

## Common Patterns

### Market Data Dashboard (via Dwellir Info API)

```javascript
const DWELLIR_INFO = `https://api-hyperliquid-mainnet.n.dwellir.com/${process.env.DWELLIR_API_KEY}/info`;

// Fetch all key market data in parallel
const [mids, meta, book] = await Promise.all([
  fetch(DWELLIR_INFO, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ type: 'allMids' }),
  }).then(r => r.json()),

  fetch(DWELLIR_INFO, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ type: 'metaAndAssetCtxs' }),
  }).then(r => r.json()),

  fetch(DWELLIR_INFO, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ type: 'l2Book', coin: 'BTC' }),
  }).then(r => r.json()),
]);

console.log(`BTC mid: $${mids.BTC}`);
console.log(`BTC OI: ${meta[1][0].openInterest}`);
console.log(`BTC funding: ${meta[1][0].funding}`);
console.log(`BTC book: ${book.levels[0].length} bid levels`);
```

### Funding Rate Monitor

```javascript
const DWELLIR_INFO = `https://api-hyperliquid-mainnet.n.dwellir.com/${process.env.DWELLIR_API_KEY}/info`;

const predictions = await fetch(DWELLIR_INFO, {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ type: 'predictedFundings' }),
}).then(r => r.json());

// Compare Hyperliquid vs other venues
for (const [coin, venues] of Object.entries(predictions)) {
  const hlRate = venues.find(v => v.venue === 'Hyperliquid')?.rate;
  const binanceRate = venues.find(v => v.venue === 'Binance')?.rate;
  if (hlRate && binanceRate) {
    const diff = Math.abs(parseFloat(hlRate) - parseFloat(binanceRate));
    if (diff > 0.001) {
      console.log(`${coin}: HL=${hlRate} vs Binance=${binanceRate} (diff: ${diff.toFixed(6)})`);
    }
  }
}
```

### Account Health Monitor

```javascript
const DWELLIR_INFO = `https://api-hyperliquid-mainnet.n.dwellir.com/${process.env.DWELLIR_API_KEY}/info`;

async function checkAccountHealth(userAddress) {
  const state = await fetch(DWELLIR_INFO, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ type: 'clearinghouseState', user: userAddress }),
  }).then(r => r.json());

  const { accountValue, totalMarginUsed } = state.marginSummary;
  const marginRatio = parseFloat(totalMarginUsed) / parseFloat(accountValue);

  console.log(`Account value: $${parseFloat(accountValue).toFixed(2)}`);
  console.log(`Margin used: ${(marginRatio * 100).toFixed(1)}%`);

  for (const { position: pos } of state.assetPositions) {
    console.log(`  ${pos.coin}: ${pos.szi} @ ${pos.entryPx} (liq: ${pos.liquidationPx})`);
  }

  if (marginRatio > 0.8) {
    console.warn('WARNING: Margin utilization above 80%');
  }
}
```

### Market-Making with Dwellir Orderbook

```javascript
// Use Dwellir's premium orderbook for low-latency book data
const ws = new WebSocket(
  `wss://api-hyperliquid-mainnet-orderbook.n.dwellir.com/${process.env.DWELLIR_API_KEY}`
);

ws.on('open', () => {
  ws.send(JSON.stringify({
    method: 'subscribe',
    subscription: { type: 'l2Book', coin: 'ETH' }
  }));
});

ws.on('message', (data) => {
  const msg = JSON.parse(data);
  const bestBid = msg.levels[0][0]; // { px, sz, n }
  const bestAsk = msg.levels[1][0];
  const spread = parseFloat(bestAsk.px) - parseFloat(bestBid.px);
  const mid = (parseFloat(bestBid.px) + parseFloat(bestAsk.px)) / 2;

  console.log(`ETH mid: ${mid.toFixed(2)}, spread: ${spread.toFixed(2)}`);

  // Place/update orders via Hyperliquid Exchange API (not Dwellir)
  // exchange.order("ETH", true, size, mid - offset, {"limit": {"tif": "Alo"}});
  // exchange.order("ETH", false, size, mid + offset, {"limit": {"tif": "Alo"}});
});
```

## Best Practices

1. **Use Dwellir for reads, Hyperliquid native for writes** — Dwellir provides the data infrastructure; order placement requires signatures and goes through `api.hyperliquid.xyz/exchange`.

2. **Use the gRPC gateway for latency-sensitive streaming** — the gRPC endpoint reads from disk and has lower latency than HTTP polling the Info API.

3. **Use Dwellir's Orderbook WebSocket for book data** — it's optimized for order book delivery with edge servers in Singapore and Tokyo.

4. **Batch Info API queries** — fetch `metaAndAssetCtxs` or `spotMetaAndAssetCtxs` in one call rather than per-asset queries.

5. **Cache metadata** — `meta`, `spotMeta`, and `perpDexs` are semi-static. Cache for 1-5 minutes.

6. **Paginate fills** — `userFills` returns max 2000 entries. Use `userFillsByTime` with the last timestamp for pagination.

7. **Check exchange status for staleness** — query `exchangeStatus` to verify the L1 timestamp. Reject stale data.

8. **Use `l2Book` via Info API for snapshots, Orderbook WS for streaming** — the Info API gives point-in-time snapshots; the Orderbook WebSocket gives continuous updates.

## Hyperliquid Historical Data

Dwellir hosts Hyperliquid archival data in S3:

```
Endpoint: https://hyperliquid-archival-data.n.dwellir.com
Bucket: hyperliquid-historical-data
```

Available data:
- `node_fills/hourly/` — fill data by hour
- `node_fills_by_block/hourly/` — fills organized by block
- `node_trades/hourly/` — trade data by hour

Files are compressed with LZ4. Bandwidth limit: 500 Mbit shared.

## Documentation Links

- Dwellir Hyperliquid docs: [dwellir.com/docs/hyperliquid](https://www.dwellir.com/docs/hyperliquid)
- Dwellir L1 gRPC Gateway (source): [github.com/dwellir-public/hyperliquid-l1-gateway](https://github.com/dwellir-public/hyperliquid-l1-gateway)
- Dwellir Orderbook Server (source): [github.com/dwellir-public/hyperliquid-orderbook-server](https://github.com/dwellir-public/hyperliquid-orderbook-server)
- Dwellir REST Server (source): [github.com/dwellir-public/hyperliquid-rest-server](https://github.com/dwellir-public/hyperliquid-rest-server)
- Hyperliquid API docs: [hyperliquid.gitbook.io/hyperliquid-docs/for-developers/api](https://hyperliquid.gitbook.io/hyperliquid-docs/for-developers/api)
- Hyperliquid Info endpoint: [hyperliquid.gitbook.io/hyperliquid-docs/for-developers/api/info-endpoint](https://hyperliquid.gitbook.io/hyperliquid-docs/for-developers/api/info-endpoint)
- Hyperliquid Exchange endpoint: [hyperliquid.gitbook.io/hyperliquid-docs/for-developers/api/exchange-endpoint](https://hyperliquid.gitbook.io/hyperliquid-docs/for-developers/api/exchange-endpoint)
- Hyperliquid WebSocket: [hyperliquid.gitbook.io/hyperliquid-docs/for-developers/api/websocket](https://hyperliquid.gitbook.io/hyperliquid-docs/for-developers/api/websocket)
- Hyperliquid Python SDK: [github.com/hyperliquid-dex/hyperliquid-python-sdk](https://github.com/hyperliquid-dex/hyperliquid-python-sdk)
- Dwellir dashboard: [dashboard.dwellir.com](https://dashboard.dwellir.com)
- Dwellir support: support@dwellir.com
