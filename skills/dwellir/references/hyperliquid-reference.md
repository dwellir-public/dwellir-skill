# Hyperliquid Reference

Complete reference for building on Hyperliquid through Dwellir — HyperCore L1, HyperEVM, gRPC streaming, order book data, Info API, Exchange API, and WebSocket subscriptions.

Hyperliquid is Dwellir's key competitive edge. Dwellir offers gRPC streaming, real-time L2 order book data, HyperEVM JSON-RPC, and dedicated nodes with edge servers in Singapore and Tokyo.

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

## Dwellir Hyperliquid Endpoints

### Endpoint Summary

| Endpoint | Slug | Protocol | Price | Use Case |
|----------|------|----------|-------|----------|
| HyperEVM JSON-RPC | `api-hyperliquid-mainnet` | HTTPS/WSS | Base plan | Smart contract calls, EVM state |
| L1 gRPC Streaming | `api-hyperliquid-mainnet-grpc` | gRPC | $299/mo | Block/fill streaming, low-latency data |
| L2 Orderbook | `api-hyperliquid-mainnet-orderbook` | WSS only | $199/mo | Real-time order book updates |
| Dedicated Node (Tokyo) | Custom | All | $1,150/mo | Uncapped throughput, no rate limits |
| Dedicated Node (Testnet) | Custom | All | $800/mo | Testing and development |

### HyperEVM Endpoint (Base Plan)

Standard EVM JSON-RPC for smart contract interaction on the HyperEVM layer.

```
HTTPS: https://api-hyperliquid-mainnet.n.dwellir.com/{API_KEY}
WSS:   wss://api-hyperliquid-mainnet.n.dwellir.com/{API_KEY}
```

```typescript
import { JsonRpcProvider } from 'ethers';
const provider = new JsonRpcProvider(
  `https://api-hyperliquid-mainnet.n.dwellir.com/${process.env.DWELLIR_API_KEY}`
);

const blockNumber = await provider.getBlockNumber();
const balance = await provider.getBalance('0x...');
```

### gRPC Streaming Endpoint ($299/mo)

Low-latency gRPC streaming from the Hyperliquid L1. Designed for trading bots, market data feeds, and real-time analytics.

```
Endpoint: api-hyperliquid-mainnet-grpc.n.dwellir.com:443
```

Available gRPC methods:
- `GetOrderBookSnapshot` — single order book snapshot at a timestamp
- `StreamBlocks` — real-time block streaming from a timestamp
- `StreamBlockFills` — order fill execution streams

Proto files are available upon request from support@dwellir.com.

```python
import grpc
import json

# Python gRPC connection
channel = grpc.secure_channel(
    'api-hyperliquid-mainnet-grpc.n.dwellir.com:443',
    grpc.ssl_channel_credentials()
)
# Use generated stubs from Hyperliquid proto files
```

```go
// Go gRPC connection
import (
    "google.golang.org/grpc"
    "google.golang.org/grpc/credentials"
)

creds := credentials.NewTLS(&tls.Config{})
conn, err := grpc.Dial(
    "api-hyperliquid-mainnet-grpc.n.dwellir.com:443",
    grpc.WithTransportCredentials(creds),
)
```

### Orderbook WebSocket ($199/mo)

Real-time L2 order book data. **WSS only** — HTTP requests are not supported.

```
WSS: wss://api-hyperliquid-mainnet-orderbook.n.dwellir.com/{API_KEY}
```

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
```

## Hyperliquid Data Architecture

Understanding how data flows in Hyperliquid is essential for building on it.

### Two APIs, Two Purposes

| API | URL | Purpose | Auth |
|-----|-----|---------|------|
| **Info API** | `POST /info` | Read-only market data and account queries | None |
| **Exchange API** | `POST /exchange` | Order placement, transfers, account management | Signature required |

Both use `POST` with `Content-Type: application/json`. The Info API is unauthenticated. The Exchange API requires EIP-712 signatures.

### Coin Naming Conventions

Understanding coin format is critical:

| Context | Format | Example |
|---------|--------|---------|
| Perpetual | Coin name | `"BTC"`, `"ETH"`, `"HYPE"` |
| Spot | `@{tokenIndex}` | `"@1"` (PURR), `"@150"` |
| Spot (display) | `SYMBOL/USDC` | `"PURR/USDC"` |
| HIP-3 DEX token | `dexname:SYMBOL` | `"xyz:XYZ100"` |

### Asset Indexing

Perpetual assets are identified by numeric index in the Exchange API:
- Perpetuals: asset index directly (e.g., `0` for BTC, `1` for ETH)
- Spot: `10000 + tokenIndex`

## Info API — Read-Only Queries

All requests: `POST` to the info endpoint with `Content-Type: application/json`.

When using Dwellir's HyperEVM endpoint, the Info API is accessed via the Hyperliquid native API URL. For direct L1 queries, use `https://api.hyperliquid.xyz/info`.

### Market Data

#### Get All Mid Prices

```javascript
const response = await fetch('https://api.hyperliquid.xyz/info', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ type: 'allMids' }),
});
const mids = await response.json();
// { "BTC": "113377.0", "ETH": "3245.5", "HYPE": "28.4", ... }
```

#### Get Order Book Snapshot

```javascript
const response = await fetch('https://api.hyperliquid.xyz/info', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    type: 'l2Book',
    coin: 'BTC',
    nSigFigs: null, // null = full precision, or 2/3/4/5
  }),
});
const book = await response.json();
// book.levels[0] = bids [{ px, sz, n }]
// book.levels[1] = asks [{ px, sz, n }]
```

#### Get Candle Data

```javascript
const response = await fetch('https://api.hyperliquid.xyz/info', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    type: 'candleSnapshot',
    req: {
      coin: 'BTC',
      interval: '1h', // 1m,3m,5m,15m,30m,1h,2h,4h,8h,12h,1d,3d,1w,1M
      startTime: Date.now() - 86400000, // 24h ago
      endTime: Date.now(),
    },
  }),
});
const candles = await response.json();
// [{ t: openTime, T: closeTime, o, h, l, c, v, n, s, i }]
```

### Perpetuals Metadata

#### Get Perp Universe & Asset Contexts

```javascript
const response = await fetch('https://api.hyperliquid.xyz/info', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ type: 'metaAndAssetCtxs' }),
});
const [meta, assetCtxs] = await response.json();
// meta.universe = [{ name, szDecimals, maxLeverage, ... }]
// assetCtxs = [{ funding, openInterest, prevDayPx, dayNtlVlm, premium, ... }]
```

#### Get Funding Rates

```javascript
const response = await fetch('https://api.hyperliquid.xyz/info', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    type: 'fundingHistory',
    coin: 'BTC',
    startTime: Date.now() - 86400000,
  }),
});
const history = await response.json();
// [{ coin, fundingRate, premium, time }]
```

#### Get Predicted Funding Rates

```javascript
const response = await fetch('https://api.hyperliquid.xyz/info', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ type: 'predictedFundings' }),
});
const predictions = await response.json();
// Predicted rates across venues (Binance, Bybit, etc.)
```

### Spot Metadata

#### Get Spot Universe & Contexts

```javascript
const response = await fetch('https://api.hyperliquid.xyz/info', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ type: 'spotMetaAndAssetCtxs' }),
});
const [meta, assetCtxs] = await response.json();
// meta.tokens = [{ name, tokenId, szDecimals, ... }]
// meta.universe = [{ name, tokens: [baseIdx, quoteIdx], ... }]
```

### User Account State

#### Perpetual Positions & Margin

```javascript
const response = await fetch('https://api.hyperliquid.xyz/info', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    type: 'clearinghouseState',
    user: '0x...',
  }),
});
const state = await response.json();
// state.marginSummary = { accountValue, totalNtlPos, totalRawUsd, totalMarginUsed }
// state.assetPositions = [{ position: { coin, szi, leverage, liquidationPx, ... } }]
```

#### Spot Balances

```javascript
const response = await fetch('https://api.hyperliquid.xyz/info', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    type: 'spotClearinghouseState',
    user: '0x...',
  }),
});
const state = await response.json();
// state.balances = [{ coin, hold, total, entryNtl }]
```

#### Open Orders

```javascript
const response = await fetch('https://api.hyperliquid.xyz/info', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    type: 'frontendOpenOrders',
    user: '0x...',
  }),
});
const orders = await response.json();
// [{ coin, side, limitPx, sz, oid, orderType, reduceOnly, ... }]
```

#### User Fills / Trade History

```javascript
const response = await fetch('https://api.hyperliquid.xyz/info', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    type: 'userFills',
    user: '0x...',
  }),
});
const fills = await response.json();
// [{ coin, px, sz, side, dir, closedPnl, fee, time, hash, ... }]
```

#### Order Status Check

```javascript
const response = await fetch('https://api.hyperliquid.xyz/info', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    type: 'orderStatus',
    user: '0x...',
    oid: 91490942, // order ID (uint64 or 16-byte hex cloid)
  }),
});
const result = await response.json();
// { status: "order", order: { order: {...}, status: "filled"|"open"|"canceled"|... } }
// or { status: "unknownOid" }
```

### User Financial Data

#### Fee Schedule & Rates

```javascript
const response = await fetch('https://api.hyperliquid.xyz/info', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    type: 'userFees',
    user: '0x...',
  }),
});
const fees = await response.json();
// fees.userCrossRate, fees.userAddRate (taker/maker for perps)
// fees.userSpotCrossRate, fees.userSpotAddRate (taker/maker for spot)
// fees.feeSchedule.tiers = volume-based fee tiers
```

#### Portfolio & P&L History

```javascript
const response = await fetch('https://api.hyperliquid.xyz/info', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    type: 'portfolio',
    user: '0x...',
  }),
});
const portfolio = await response.json();
// [["day", { accountValueHistory, pnlHistory, vlm }],
//  ["week", ...], ["month", ...], ["allTime", ...],
//  ["perpDay", ...], ["perpWeek", ...], ...]
```

#### Rate Limits

```javascript
const response = await fetch('https://api.hyperliquid.xyz/info', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    type: 'userRateLimit',
    user: '0x...',
  }),
});
const limits = await response.json();
// { cumVlm, nRequestsUsed, nRequestsCap, nRequestsSurplus }
```

### Staking & Delegation

```javascript
// Get delegations
const delegations = await fetch('https://api.hyperliquid.xyz/info', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ type: 'delegations', user: '0x...' }),
}).then(r => r.json());
// [{ validator, amount, lockedUntilTimestamp }]

// Get staking summary
const summary = await fetch('https://api.hyperliquid.xyz/info', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ type: 'delegatorSummary', user: '0x...' }),
}).then(r => r.json());
// { delegated, undelegated, totalPendingWithdrawal, nPendingWithdrawals }
```

### Vaults

```javascript
const vaultDetails = await fetch('https://api.hyperliquid.xyz/info', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    type: 'vaultDetails',
    vaultAddress: '0x...',
    user: '0x...', // optional — includes followerState if provided
  }),
}).then(r => r.json());
// { name, leader, apr, followers, portfolio, maxDistributable, ... }
```

### Borrow/Lend

```javascript
// User borrow/lend positions
const userState = await fetch('https://api.hyperliquid.xyz/info', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ type: 'borrowLendUserState', user: '0x...' }),
}).then(r => r.json());
// { tokenToState, health, healthFactor }

// Reserve state (interest rates, utilization)
const reserves = await fetch('https://api.hyperliquid.xyz/info', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ type: 'allBorrowLendReserveStates' }),
}).then(r => r.json());
// [[tokenIndex, { borrowYearlyRate, supplyYearlyRate, utilization, ... }], ...]
```

## Exchange API — Write Operations

All Exchange API requests require EIP-712 signatures. Use the Hyperliquid SDK or sign manually.

**Endpoint:** `POST https://api.hyperliquid.xyz/exchange`

Every request needs: `action` (operation-specific), `nonce` (timestamp ms), `signature` (EIP-712).

### Place an Order

```python
from hyperliquid.utils import constants
from hyperliquid.exchange import Exchange
from eth_account import Account

wallet = Account.from_key(os.environ["PRIVATE_KEY"])
exchange = Exchange(wallet, constants.MAINNET_API_URL)

# Limit buy 0.1 BTC at $100,000
result = exchange.order("BTC", True, 0.1, 100000, {"limit": {"tif": "Gtc"}})
print(result)  # { status: "ok", response: { type: "order", data: { statuses: [...] } } }
```

### Order Types

| Type | TIF | Description |
|------|-----|-------------|
| Limit GTC | `{"limit": {"tif": "Gtc"}}` | Good-til-canceled, rests on book |
| Limit ALO | `{"limit": {"tif": "Alo"}}` | Post-only, rejected if would cross |
| Limit IOC | `{"limit": {"tif": "Ioc"}}` | Immediate-or-cancel, fills or dies |
| Market | IOC at slippage price | Use IOC with aggressive price |
| Trigger (Stop) | `{"trigger": {"triggerPx": "...", "isMarket": true, "tpsl": "sl"}}` | Stop-loss market order |
| Trigger (TP) | `{"trigger": {"triggerPx": "...", "isMarket": true, "tpsl": "tp"}}` | Take-profit market order |
| TWAP | Separate `twapOrder` action | Time-weighted execution over duration |

### Cancel Orders

```python
# Cancel by order ID
exchange.cancel("BTC", 91490942)

# Cancel all orders for a coin
exchange.cancel_all("BTC")
```

### Modify an Order

```python
# Modify existing order (keeps queue position if price unchanged)
exchange.modify_order(oid, "BTC", True, 0.1, 101000, {"limit": {"tif": "Gtc"}})
```

### Set Leverage

```python
# Cross leverage
exchange.update_leverage(20, "BTC", is_cross=True)

# Isolated leverage
exchange.update_leverage(10, "BTC", is_cross=False)
```

### Transfer USDC

```python
# Transfer between perp and spot
exchange.usd_class_transfer(1000, True)  # perp -> spot

# Transfer to another address
exchange.usd_transfer("0xrecipient...", 100)
```

### Dead Man's Switch

Auto-cancel all orders at a future time (minimum 5 seconds ahead, max 10 triggers/day):

```python
import time
# Cancel all orders in 30 seconds if no heartbeat
exchange.schedule_cancel(int(time.time() * 1000) + 30000)
```

### Agent (API) Wallets

Hyperliquid supports "agent wallets" — separate keys authorized to trade on behalf of your account. Each account can have 1 unnamed + 3 named agents, plus 2 per subaccount.

```python
# Approve agent wallet from main account
exchange.approve_agent(agent_address)
```

## WebSocket Subscriptions

Connect to the Hyperliquid WebSocket for real-time streaming data.

**Dwellir Orderbook endpoint:** `wss://api-hyperliquid-mainnet-orderbook.n.dwellir.com/{API_KEY}`

**Native Hyperliquid WS:** `wss://api.hyperliquid.xyz/ws`

### Subscribe / Unsubscribe Pattern

```javascript
// Subscribe
ws.send(JSON.stringify({
  method: 'subscribe',
  subscription: { type: 'l2Book', coin: 'BTC' }
}));

// Unsubscribe
ws.send(JSON.stringify({
  method: 'unsubscribe',
  subscription: { type: 'l2Book', coin: 'BTC' }
}));
```

### Available Subscription Types

| Type | Params | Data Streamed |
|------|--------|---------------|
| `allMids` | `dex?` | All mid prices |
| `l2Book` | `coin` | Order book updates (bids/asks with price, size, count) |
| `trades` | `coin` | Trade executions |
| `bbo` | `coin` | Best bid/offer only (lighter than l2Book) |
| `candle` | `coin`, `interval` | OHLCV candle updates |
| `activeAssetCtx` | `coin` | Mark price, funding, OI, volume |
| `activeAssetData` | `user`, `coin` | User leverage, max trade sizes |
| `openOrders` | `user`, `dex?` | User's active orders |
| `orderUpdates` | `user` | Order status changes (fills, cancels) |
| `userEvents` | `user` | Fills, funding payments, liquidations |
| `userFills` | `user` | Trade executions with snapshots |
| `userFundings` | `user` | Funding payment snapshots |
| `userNonFundingLedgerUpdates` | `user` | Deposits, withdrawals, transfers |
| `clearinghouseState` | `user`, `dex?` | Position/margin updates |
| `twapStates` | `user`, `dex?` | TWAP order progress |
| `notification` | `user` | System notifications |
| `webData3` | `user` | Aggregate user info |

### Example: Stream Trades

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

### Example: Monitor Positions in Real-Time

```javascript
const ws = new WebSocket('wss://api.hyperliquid.xyz/ws');

ws.on('open', () => {
  ws.send(JSON.stringify({
    method: 'subscribe',
    subscription: { type: 'clearinghouseState', user: '0x...' }
  }));
});

ws.on('message', (data) => {
  const msg = JSON.parse(data);
  if (msg.channel === 'clearinghouseState') {
    const state = msg.data;
    console.log(`Account value: ${state.marginSummary.accountValue}`);
    for (const pos of state.assetPositions) {
      console.log(`${pos.position.coin}: ${pos.position.szi} @ ${pos.position.entryPx}`);
    }
  }
});
```

## Common Patterns

### Market-Making Bot Skeleton

```javascript
const ws = new WebSocket(
  `wss://api-hyperliquid-mainnet-orderbook.n.dwellir.com/${process.env.DWELLIR_API_KEY}`
);

ws.on('open', () => {
  // Subscribe to order book and best bid/offer
  ws.send(JSON.stringify({
    method: 'subscribe',
    subscription: { type: 'l2Book', coin: 'ETH' }
  }));
});

ws.on('message', (data) => {
  const msg = JSON.parse(data);
  if (msg.channel === 'l2Book') {
    const bestBid = msg.data.levels[0][0]; // { px, sz, n }
    const bestAsk = msg.data.levels[1][0];
    const spread = parseFloat(bestAsk.px) - parseFloat(bestBid.px);
    const mid = (parseFloat(bestBid.px) + parseFloat(bestAsk.px)) / 2;
    console.log(`ETH mid: ${mid.toFixed(2)}, spread: ${spread.toFixed(2)}`);
    // Place/update orders based on book state
  }
});
```

### Funding Rate Arbitrage Monitor

```javascript
// Fetch predicted funding across venues
const predictions = await fetch('https://api.hyperliquid.xyz/info', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ type: 'predictedFundings' }),
}).then(r => r.json());

// Compare Hyperliquid funding vs other venues
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

### Multi-Data Dashboard

```javascript
// Fetch all key data in parallel
const [mids, meta, book] = await Promise.all([
  fetch('https://api.hyperliquid.xyz/info', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ type: 'allMids' }),
  }).then(r => r.json()),

  fetch('https://api.hyperliquid.xyz/info', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ type: 'metaAndAssetCtxs' }),
  }).then(r => r.json()),

  fetch('https://api.hyperliquid.xyz/info', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ type: 'l2Book', coin: 'BTC' }),
  }).then(r => r.json()),
]);

console.log(`BTC mid: $${mids.BTC}`);
console.log(`BTC OI: ${meta[1][0].openInterest}`);
console.log(`BTC funding: ${meta[1][0].funding}`);
console.log(`BTC book depth: ${book.levels[0].length} bid levels`);
```

### Account Health Monitor

```javascript
async function checkAccountHealth(userAddress) {
  const state = await fetch('https://api.hyperliquid.xyz/info', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ type: 'clearinghouseState', user: userAddress }),
  }).then(r => r.json());

  const { accountValue, totalMarginUsed, totalNtlPos } = state.marginSummary;
  const marginRatio = parseFloat(totalMarginUsed) / parseFloat(accountValue);

  console.log(`Account value: $${parseFloat(accountValue).toFixed(2)}`);
  console.log(`Margin used: ${(marginRatio * 100).toFixed(1)}%`);
  console.log(`Positions: ${state.assetPositions.length}`);

  for (const { position: pos } of state.assetPositions) {
    console.log(`  ${pos.coin}: ${pos.szi} @ ${pos.entryPx} (liq: ${pos.liquidationPx})`);
  }

  if (marginRatio > 0.8) {
    console.warn('WARNING: Margin utilization above 80%');
  }
}
```

## Best Practices

1. **Use Dwellir gRPC for latency-sensitive data** — the gRPC endpoint provides lower latency than HTTP polling for block and fill streaming.

2. **Use the Orderbook WebSocket for book data** — Dwellir's Orderbook endpoint is optimized for L2 book updates with edge servers in Singapore and Tokyo.

3. **Batch Info API calls** — fetch `metaAndAssetCtxs` and `spotMetaAndAssetCtxs` in one call each rather than per-asset queries.

4. **Mind the nonce** — Exchange API uses timestamp-based nonces. Ensure your clock is synchronized.

5. **Agent wallets for bots** — use agent wallets rather than your main key for automated trading. Limits: 1 unnamed + 3 named per account.

6. **Handle rate limits proactively** — check `userRateLimit` to monitor consumption. Rate limit scales with trading volume.

7. **WebSocket reconnection** — implement automatic reconnection with backoff. Initial user subscriptions include `isSnapshot: true` for state recovery.

8. **Use `bbo` over `l2Book` when possible** — if you only need best bid/offer, `bbo` is lighter than full book updates.

9. **Pagination for fills** — `userFills` returns max 2000 entries. Use `userFillsByTime` with the last timestamp for pagination.

10. **Dead Man's Switch for safety** — use `scheduleCancel` as a heartbeat mechanism for trading bots. If your bot crashes, orders auto-cancel.

## Documentation Links

- Dwellir Hyperliquid docs: [dwellir.com/docs/hyperliquid](https://www.dwellir.com/docs/hyperliquid)
- Hyperliquid API docs: [hyperliquid.gitbook.io/hyperliquid-docs/for-developers/api](https://hyperliquid.gitbook.io/hyperliquid-docs/for-developers/api)
- Hyperliquid Info endpoint: [hyperliquid.gitbook.io/hyperliquid-docs/for-developers/api/info-endpoint](https://hyperliquid.gitbook.io/hyperliquid-docs/for-developers/api/info-endpoint)
- Hyperliquid Exchange endpoint: [hyperliquid.gitbook.io/hyperliquid-docs/for-developers/api/exchange-endpoint](https://hyperliquid.gitbook.io/hyperliquid-docs/for-developers/api/exchange-endpoint)
- Hyperliquid WebSocket: [hyperliquid.gitbook.io/hyperliquid-docs/for-developers/api/websocket](https://hyperliquid.gitbook.io/hyperliquid-docs/for-developers/api/websocket)
- Hyperliquid Python SDK: [github.com/hyperliquid-dex/hyperliquid-python-sdk](https://github.com/hyperliquid-dex/hyperliquid-python-sdk)
- Dwellir dashboard: [dashboard.dwellir.com](https://dashboard.dwellir.com)
- Dwellir support: support@dwellir.com
