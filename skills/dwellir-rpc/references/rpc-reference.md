# RPC Endpoints Reference

Complete reference for Dwellir's JSON-RPC endpoints covering EVM chains, debug/trace APIs, WebSocket subscriptions, batch requests, non-EVM chains, and best practices.

## Overview

- **Protocol:** JSON-RPC 2.0 over HTTPS and WSS
- **Authentication:** API key in URL path
- **Endpoint format:** `https://api-{network}.n.dwellir.com/{API_KEY}`
- **WebSocket format:** `wss://api-{network}.n.dwellir.com/{API_KEY}`

## Connection Setup

All examples use the `DWELLIR_RPC_URL` environment variable. Set it to your full endpoint URL including API key.

### ethers.js (v6)

```typescript
import { JsonRpcProvider, WebSocketProvider } from 'ethers';

// HTTP
const provider = new JsonRpcProvider(process.env.DWELLIR_RPC_URL);

// WebSocket
const wsProvider = new WebSocketProvider(process.env.DWELLIR_WSS_URL);
```

### viem

```typescript
import { createPublicClient, http, webSocket } from 'viem';
import { mainnet } from 'viem/chains';

// HTTP
const client = createPublicClient({
  chain: mainnet,
  transport: http(process.env.DWELLIR_RPC_URL),
});

// WebSocket
const wsClient = createPublicClient({
  chain: mainnet,
  transport: webSocket(process.env.DWELLIR_WSS_URL),
});
```

### web3.js

```javascript
import Web3 from 'web3';
const web3 = new Web3(process.env.DWELLIR_RPC_URL);
```

### web3.py

```python
from web3 import Web3
import os

w3 = Web3(Web3.HTTPProvider(os.environ["DWELLIR_RPC_URL"]))
print(w3.is_connected())
```

### curl

```bash
curl -X POST ${DWELLIR_RPC_URL} \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","method":"eth_blockNumber","params":[],"id":1}'
```

## EVM RPC Methods

### Account Methods

| Method | Description | Params |
|--------|-------------|--------|
| `eth_getBalance` | Get account balance in wei | `[address, block]` |
| `eth_getTransactionCount` | Get account nonce | `[address, block]` |
| `eth_getCode` | Get contract bytecode | `[address, block]` |
| `eth_getStorageAt` | Get storage value at position | `[address, position, block]` |

### Block Methods

| Method | Description | Params |
|--------|-------------|--------|
| `eth_blockNumber` | Latest block number | `[]` |
| `eth_getBlockByNumber` | Get block by number | `[blockNumber, fullTx]` |
| `eth_getBlockByHash` | Get block by hash | `[blockHash, fullTx]` |
| `eth_getBlockReceipts` | Get all receipts for a block | `[blockNumber]` |

### Transaction Methods

| Method | Description | Params |
|--------|-------------|--------|
| `eth_getTransactionByHash` | Get transaction by hash | `[txHash]` |
| `eth_getTransactionReceipt` | Get transaction receipt | `[txHash]` |
| `eth_sendRawTransaction` | Submit signed transaction | `[signedTxData]` |
| `eth_getTransactionByBlockNumberAndIndex` | Get tx by block and index | `[blockNumber, index]` |

### Call & Simulation Methods

| Method | Description | Params |
|--------|-------------|--------|
| `eth_call` | Execute read-only call | `[txObject, block]` |
| `eth_estimateGas` | Estimate gas for transaction | `[txObject, block]` |
| `eth_createAccessList` | Generate access list for tx | `[txObject, block]` |

### Log & Filter Methods

| Method | Description | Params |
|--------|-------------|--------|
| `eth_getLogs` | Get matching log entries | `[filterObject]` |
| `eth_newFilter` | Create log filter | `[filterObject]` |
| `eth_newBlockFilter` | Create block filter | `[]` |
| `eth_getFilterChanges` | Poll filter for changes | `[filterId]` |
| `eth_getFilterLogs` | Get all logs for filter | `[filterId]` |
| `eth_uninstallFilter` | Remove filter | `[filterId]` |

### Gas & Fee Methods

| Method | Description | Params |
|--------|-------------|--------|
| `eth_gasPrice` | Current gas price | `[]` |
| `eth_maxPriorityFeePerGas` | Suggested priority fee (EIP-1559) | `[]` |
| `eth_feeHistory` | Historical fee data | `[blockCount, newestBlock, rewardPercentiles]` |

### Network Methods

| Method | Description | Params |
|--------|-------------|--------|
| `eth_chainId` | Chain ID | `[]` |
| `net_version` | Network ID | `[]` |
| `eth_syncing` | Sync status | `[]` |
| `web3_clientVersion` | Client version string | `[]` |

### Subscription Methods (WebSocket)

| Method | Description | Params |
|--------|-------------|--------|
| `eth_subscribe` | Start subscription | `[type, options]` |
| `eth_unsubscribe` | Stop subscription | `[subscriptionId]` |

Subscription types: `newHeads`, `logs`, `newPendingTransactions`, `syncing`.

## Debug & Trace Methods

Available on Developer plan and above.

### debug_traceTransaction

Trace a single transaction by hash. Returns detailed execution trace.

```bash
curl -X POST ${DWELLIR_RPC_URL} \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "method": "debug_traceTransaction",
    "params": [
      "0x...",
      {"tracer": "callTracer"}
    ],
    "id": 1
  }'
```

### debug_traceCall

Trace a call without submitting a transaction.

```bash
curl -X POST ${DWELLIR_RPC_URL} \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "method": "debug_traceCall",
    "params": [
      {
        "from": "0x...",
        "to": "0x...",
        "data": "0x..."
      },
      "latest",
      {"tracer": "callTracer"}
    ],
    "id": 1
  }'
```

### debug_traceBlockByNumber

Trace all transactions in a block.

```bash
curl -X POST ${DWELLIR_RPC_URL} \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "method": "debug_traceBlockByNumber",
    "params": ["0x...", {"tracer": "callTracer"}],
    "id": 1
  }'
```

### trace_transaction (Parity-style)

```bash
curl -X POST ${DWELLIR_RPC_URL} \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "method": "trace_transaction",
    "params": ["0x..."],
    "id": 1
  }'
```

### trace_block (Parity-style)

```bash
curl -X POST ${DWELLIR_RPC_URL} \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "method": "trace_block",
    "params": ["0x..."],
    "id": 1
  }'
```

### Tracer Types

#### callTracer

Returns a tree of calls made during execution.

```json
{
  "tracer": "callTracer",
  "tracerConfig": {
    "onlyTopCall": false
  }
}
```

Response includes: `type`, `from`, `to`, `value`, `gas`, `gasUsed`, `input`, `output`, `error`, `calls` (nested).

#### prestateTracer

Shows account state before execution.

```json
{
  "tracer": "prestateTracer",
  "tracerConfig": {
    "diffMode": true
  }
}
```

With `diffMode: true`, returns `pre` and `post` state for each account showing balance, code, storage, and nonce changes.

#### 4byteTracer

Maps 4-byte function selectors to call counts.

```json
{
  "tracer": "4byteTracer"
}
```

Response: `{"0xa9059cbb-64": 1, "0x095ea7b3-64": 2}` — each key is `selector-calldataSize`, value is count.

#### Custom JavaScript Tracer

Define custom analysis logic:

```json
{
  "tracer": "{result: [], fault: function(log) {}, step: function(log) { if(log.op.toString() === 'SSTORE') this.result.push(log.stack.peek(0)); }, result: function() { return this.result; }}"
}
```

## Code Examples

### Get Account Balance

```typescript
import { JsonRpcProvider, formatEther } from 'ethers';

const provider = new JsonRpcProvider(process.env.DWELLIR_RPC_URL);
const balance = await provider.getBalance('0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045');
console.log(`Balance: ${formatEther(balance)} ETH`);
```

### Get Logs (ERC-20 Transfers)

```typescript
import { JsonRpcProvider } from 'ethers';

const provider = new JsonRpcProvider(process.env.DWELLIR_RPC_URL);
const logs = await provider.getLogs({
  address: '0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48', // USDC
  topics: [
    '0xddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef' // Transfer
  ],
  fromBlock: 'latest',
});
console.log(`Found ${logs.length} transfers`);
```

### Call Contract (Read-Only)

```typescript
import { createPublicClient, http, parseAbi } from 'viem';
import { mainnet } from 'viem/chains';

const client = createPublicClient({
  chain: mainnet,
  transport: http(process.env.DWELLIR_RPC_URL),
});

const totalSupply = await client.readContract({
  address: '0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48',
  abi: parseAbi(['function totalSupply() view returns (uint256)']),
  functionName: 'totalSupply',
});
```

### Trace a Transaction

```typescript
const result = await provider.send('debug_traceTransaction', [
  '0x...txhash...',
  { tracer: 'callTracer' }
]);
console.log('Top-level call:', result.type, result.from, '->', result.to);
console.log('Internal calls:', result.calls?.length ?? 0);
```

### WebSocket — Subscribe to New Blocks

```typescript
import { WebSocketProvider } from 'ethers';

const provider = new WebSocketProvider(process.env.DWELLIR_WSS_URL);

provider.on('block', async (blockNumber) => {
  const block = await provider.getBlock(blockNumber);
  console.log(`Block ${blockNumber}: ${block.transactions.length} txs`);
});
```

### WebSocket — Subscribe to Contract Events

```typescript
import { WebSocketProvider, Contract, parseAbi } from 'ethers';

const provider = new WebSocketProvider(process.env.DWELLIR_WSS_URL);
const usdc = new Contract(
  '0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48',
  parseAbi(['event Transfer(address indexed from, address indexed to, uint256 value)']),
  provider
);

usdc.on('Transfer', (from, to, value) => {
  console.log(`USDC Transfer: ${from} -> ${to}: ${value}`);
});
```

## Batch Requests

Send multiple JSON-RPC calls in a single HTTP request:

```bash
curl -X POST ${DWELLIR_RPC_URL} \
  -H "Content-Type: application/json" \
  -d '[
    {"jsonrpc":"2.0","method":"eth_blockNumber","params":[],"id":1},
    {"jsonrpc":"2.0","method":"eth_gasPrice","params":[],"id":2},
    {"jsonrpc":"2.0","method":"eth_chainId","params":[],"id":3}
  ]'
```

```typescript
// ethers.js batch via FetchRequest
const [blockNumber, gasPrice, chainId] = await Promise.all([
  provider.getBlockNumber(),
  provider.getFeeData(),
  provider.getNetwork(),
]);
```

## WebSocket Subscription Patterns

### newHeads — New Block Headers

```json
{"jsonrpc":"2.0","method":"eth_subscribe","params":["newHeads"],"id":1}
```

### logs — Contract Events

```json
{
  "jsonrpc":"2.0",
  "method":"eth_subscribe",
  "params":[
    "logs",
    {
      "address": "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48",
      "topics": ["0xddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef"]
    }
  ],
  "id":1
}
```

### newPendingTransactions

```json
{"jsonrpc":"2.0","method":"eth_subscribe","params":["newPendingTransactions"],"id":1}
```

### Unsubscribe

```json
{"jsonrpc":"2.0","method":"eth_unsubscribe","params":["0x...subscriptionId"],"id":1}
```

## Non-EVM Chains

### Aptos

Aptos uses a REST API rather than JSON-RPC. Endpoint format is the same.

```bash
# Get ledger info
curl ${DWELLIR_RPC_URL}/v1

# Get account resources
curl ${DWELLIR_RPC_URL}/v1/accounts/0x1/resources

# Get account balance
curl ${DWELLIR_RPC_URL}/v1/accounts/{address}/resource/0x1::coin::CoinStore%3C0x1::aptos_coin::AptosCoin%3E
```

### Sui

Sui uses JSON-RPC 2.0.

```bash
# Get latest checkpoint
curl -X POST ${DWELLIR_RPC_URL} \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","method":"sui_getLatestCheckpointSequenceNumber","params":[],"id":1}'

# Get object
curl -X POST ${DWELLIR_RPC_URL} \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","method":"sui_getObject","params":["0x..."],"id":1}'
```

### TON

TON uses its own HTTP API.

```bash
# Get address info
curl "${DWELLIR_RPC_URL}/getAddressInformation?address=EQ..."
```

### TRON

TRON uses a REST-style HTTP API.

```bash
# Get account info
curl -X POST ${DWELLIR_RPC_URL}/wallet/getaccount \
  -H "Content-Type: application/json" \
  -d '{"address": "T..."}'
```

### Starknet

Starknet uses JSON-RPC 2.0 with `starknet_` prefixed methods.

```bash
curl -X POST ${DWELLIR_RPC_URL} \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","method":"starknet_blockNumber","params":[],"id":1}'
```

## Best Practices

1. **Retry with exponential backoff** — handle 429 (rate limited) and 5xx responses:
   ```typescript
   async function rpcWithRetry(fn, maxRetries = 3) {
     for (let i = 0; i < maxRetries; i++) {
       try {
         return await fn();
       } catch (err) {
         if (i === maxRetries - 1) throw err;
         await new Promise(r => setTimeout(r, 1000 * 2 ** i));
       }
     }
   }
   ```

2. **Cache block data** — blocks are immutable once finalized; cache `getBlock` results.

3. **Use `latest` carefully** — `latest` changes every block. For consistency within a workflow, fetch the block number once and reference it explicitly.

4. **Prefer `eth_getBlockReceipts`** — more efficient than individual `eth_getTransactionReceipt` calls for full-block analysis.

5. **Limit `eth_getLogs` range** — use narrow block ranges (≤2000 blocks). Overly broad queries may time out.

6. **Connection pooling** — reuse HTTP connections and WebSocket clients rather than opening new ones per request.

7. **Archive vs full nodes** — trace/debug methods and historical state queries require archive data, which Dwellir provides on paid plans.

## Troubleshooting

| Error | Cause | Fix |
|-------|-------|-----|
| `429 Too Many Requests` | Rate limit exceeded | Add backoff/retry or upgrade plan |
| `401 Unauthorized` | Invalid API key | Check key is correct UUID in URL path |
| `method not found` | Method unavailable on this chain | Verify chain supports this RPC method |
| `missing trie node` | Historical state unavailable | Ensure trace/debug APIs are enabled on your plan |
| `execution timeout` | Trace/call too complex | Narrow the scope or use `onlyTopCall: true` |
| `block range too large` | `eth_getLogs` range too wide | Reduce block range to ≤2000 blocks |
| Connection reset | WebSocket idle timeout | Implement reconnection logic with backoff |

## Documentation Links

- Dwellir docs: [dwellir.com/docs](https://www.dwellir.com/docs)
- Tracing guide: [dwellir.com/docs/getting-started/tracing](https://www.dwellir.com/docs/getting-started/tracing)
- Per-chain docs: `https://www.dwellir.com/docs/{chain}` — e.g., [ethereum](https://www.dwellir.com/docs/ethereum), [arbitrum](https://www.dwellir.com/docs/arbitrum), [base](https://www.dwellir.com/docs/base), [polygon](https://www.dwellir.com/docs/polygon)
- Ethereum JSON-RPC spec: [ethereum.org/en/developers/docs/apis/json-rpc](https://ethereum.org/en/developers/docs/apis/json-rpc)
