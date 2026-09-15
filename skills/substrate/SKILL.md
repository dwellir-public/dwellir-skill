---
name: substrate
description: >
  Use when reading Substrate and Polkadot data through Dwellir endpoints:
  @polkadot/api connection setup, core RPC methods (system_*, chain_*, state_*),
  storage queries, WebSocket subscriptions, Sidecar REST APIs, and best practices.
  Use when working with Polkadot, Kusama, Substrate chains, parachains,
  extrinsics, or Sidecar REST endpoints through Dwellir.
  Triggers on mentions of polkadot, kusama, substrate, parachain, xcm,
  moonbeam, astar, acala, @polkadot/api, extrinsic, pallet, GRANDPA,
  sidecar, asset hub, bridge hub, or Substrate chain names.
---

# Substrate / Polkadot Ecosystem Reference

Use Dwellir for blockchain reads, storage queries, and read-only application development.
This skill does not sign or submit extrinsics, transfer assets, or modify node keys.
An existing wallet or a rejected MCP method does not authorize an alternate execution route.

Discover endpoints with `list_endpoints` and supported MCP methods with `rpc_methods` before calling `rpc_call`.
The direct RPC examples below describe application code; MCP supports a smaller method set.
Read credentials from environment variables or a secret store. Never print authenticated URLs or raw connection errors.

## Overview

Substrate chains are WebSocket-native. While HTTP works for individual queries, **WSS is the preferred protocol** for Substrate — it supports subscriptions and is more efficient for the stateful connection model Substrate expects.

- **Protocol:** JSON-RPC 2.0 over WSS (preferred) and HTTPS
- **Authentication:** API key in URL path
- **WSS format:** `wss://api-{chain}.n.dwellir.com/{API_KEY}`
- **HTTPS format:** `https://api-{chain}.n.dwellir.com/{API_KEY}`

## Connection Setup

### @polkadot/api (JavaScript/TypeScript)

The standard SDK for Substrate chains.

```typescript
import { ApiPromise, WsProvider } from '@polkadot/api';

const wsProvider = new WsProvider(
  `wss://api-polkadot.n.dwellir.com/${process.env.DWELLIR_API_KEY}`
);
const api = await ApiPromise.create({ provider: wsProvider });

// Chain info
const chain = await api.rpc.system.chain();
const version = await api.rpc.system.version();
console.log(`Connected to ${chain} v${version}`);
```

### py-substrate-interface (Python)

```python
from substrateinterface import SubstrateInterface
import os

substrate = SubstrateInterface(
    url=f"wss://api-polkadot.n.dwellir.com/{os.environ['DWELLIR_API_KEY']}"
)

result = substrate.query("System", "Account", [address])
print(f"Free balance: {result.value['data']['free']}")
```

### subxt (Rust)

```rust
use subxt::{OnlineClient, PolkadotConfig};

#[tokio::main]
async fn main() -> Result<(), Box<dyn std::error::Error>> {
    let api_key = std::env::var("DWELLIR_API_KEY")?;
    let url = format!("wss://api-polkadot.n.dwellir.com/{}", api_key);
    let api = OnlineClient::<PolkadotConfig>::from_url(&url)
        .await.map_err(|_| "Dwellir connection failed")?;

    let block = api.blocks().at_latest().await.map_err(|_| "Dwellir block query failed")?;
    println!("Latest block: #{}", block.number());
    Ok(())
}
```

### Raw WebSocket

```javascript
import WebSocket from 'ws';

const ws = new WebSocket(
  `wss://api-polkadot.n.dwellir.com/${process.env.DWELLIR_API_KEY}`
);

ws.on('open', () => {
  ws.send(JSON.stringify({
    jsonrpc: '2.0',
    method: 'chain_getBlock',
    params: [],
    id: 1,
  }));
});

ws.on('message', (data) => {
  console.log(JSON.parse(data));
});
```

## Supported Parachains

Dwellir provides deep coverage of the Polkadot and Kusama ecosystems.

### Relay Chains

| Chain | Endpoint Slug | Protocols |
|-------|---------------|-----------|
| Polkadot | `api-polkadot` | HTTPS, WSS |
| Kusama | `api-kusama` | HTTPS, WSS |

### Polkadot Parachains

| Chain | Endpoint Slug | Description |
|-------|---------------|-------------|
| Asset Hub Polkadot | `api-asset-hub-polkadot` | Native asset management (formerly Statemint) |
| Bridge Hub Polkadot | `api-bridge-hub-polkadot` | Cross-chain bridging |
| Acala | `api-acala` | DeFi hub — stablecoins, DEX, liquid staking |
| Astar | `api-astar` | Multi-VM smart contracts (EVM + WASM) |
| Bifrost | `api-bifrost-polkadot` | Liquid staking for multiple chains |
| Centrifuge | `api-centrifuge` | Real-world asset tokenization |
| Hydration | `api-hydration` | Omnipool DEX — single-sided liquidity |
| KILT | `api-kilt` | Decentralized identity and credentials |
| Moonbeam | `api-moonbeam` | Ethereum-compatible smart contracts |

### Kusama Parachains

| Chain | Endpoint Slug | Description |
|-------|---------------|-------------|
| Asset Hub Kusama | `api-asset-hub-kusama` | Asset management on Kusama |
| Bridge Hub Kusama | `api-bridge-hub-kusama` | Cross-chain bridging on Kusama |
| Moonriver | `api-moonriver` | Moonbeam's canary network |

### Testnets

| Chain | Endpoint Slug |
|-------|---------------|
| Moonbase Alpha | `api-moonbase-alpha` |

Full and current list: [dwellir.com/docs/getting-started/supported-chains](https://www.dwellir.com/docs/getting-started/supported-chains)

## Core RPC Methods

### system_* — Node & Network Info

| Method | Description |
|--------|-------------|
| `system_chain` | Chain name |
| `system_name` | Node implementation name |
| `system_version` | Node version |
| `system_health` | Node health (peers, syncing) |
| `system_properties` | Chain properties (SS58 prefix, token decimals, token symbol) |
| `system_peers` | Connected peer list |
| `system_localPeerId` | Local node peer ID |
| `system_nodeRoles` | Roles of the node (full, authority, light) |

### chain_* — Block & Header Access

| Method | Description | Params |
|--------|-------------|--------|
| `chain_getBlock` | Get block by hash (latest if omitted) | `[blockHash?]` |
| `chain_getBlockHash` | Get block hash by number | `[blockNumber?]` |
| `chain_getHeader` | Get block header | `[blockHash?]` |
| `chain_getFinalizedHead` | Hash of latest finalized block | `[]` |

### state_* — Storage & Runtime

| Method | Description | Params |
|--------|-------------|--------|
| `state_getStorage` | Read a storage entry | `[storageKey, blockHash?]` |
| `state_getStorageAt` | Read storage at specific block | `[storageKey, blockHash]` |
| `state_queryStorage` | Query storage changes over range | `[keys, fromBlock, toBlock?]` |
| `state_queryStorageAt` | Query storage at a block | `[keys, blockHash?]` |
| `state_getMetadata` | Runtime metadata (types, pallets, calls) | `[blockHash?]` |
| `state_getRuntimeVersion` | Runtime spec and impl version | `[blockHash?]` |
| `state_getKeys` | List storage keys with prefix | `[prefix, blockHash?]` |
| `state_getKeysPaged` | Paginated storage key listing | `[prefix, count, startKey?, blockHash?]` |
| `state_call` | Execute a runtime API call | `[method, data, blockHash?]` |

### grandpa_* — Finality

| Method | Description |
|--------|-------------|
| `grandpa_roundState` | Current GRANDPA round state |
| `grandpa_proveFinality` | Prove finality of a block |

## Storage Queries

Substrate storage is key-value based. The `@polkadot/api` provides high-level wrappers.

### Query Account Balance

```typescript
// Using @polkadot/api
const { data: { free, reserved } } = await api.query.system.account(address);
console.log(`Free: ${free.toHuman()}, Reserved: ${reserved.toHuman()}`);
```

### Query Multiple Accounts

```typescript
const accounts = ['5GrwvaEF...', '5FHneW46...'];
const balances = await api.query.system.account.multi(accounts);
balances.forEach((balance, i) => {
  console.log(`${accounts[i]}: ${balance.data.free.toHuman()}`);
});
```

### Read Arbitrary Storage

```typescript
// Pallet: Staking, Storage: Validators
const validators = await api.query.staking.validators.entries();
validators.forEach(([key, prefs]) => {
  console.log(`Validator: ${key.args[0].toString()}, Commission: ${prefs.commission.toHuman()}`);
});
```

### Raw Storage Query

```json
{
    "jsonrpc": "2.0",
    "method": "state_getStorage",
    "params": ["0x26aa394eea5630e07c48ae0c9558cef7b99d880ec681799c0cf30e8886371da9..."],
    "id": 1
  }
```

## Runtime Calls

### Get Metadata

```typescript
const metadata = await api.rpc.state.getMetadata();
const pallets = metadata.asLatest.pallets.map(p => p.name.toString());
console.log('Pallets:', pallets);
```

### Runtime API Calls

```typescript
// Check transaction payment info
const info = await api.call.transactionPaymentApi.queryInfo(extrinsic, extrinsic.length);
console.log(`Estimated fee: ${info.partialFee.toHuman()}`);
```

## WebSocket Subscriptions

Subscriptions are the primary way to receive real-time data from Substrate chains.

### Subscribe to New Block Headers

```typescript
const unsub = await api.rpc.chain.subscribeNewHeads((header) => {
  console.log(`New block #${header.number}: ${header.hash.toHex()}`);
});

// Later: unsub();
```

### Subscribe to Finalized Heads

```typescript
const unsub = await api.rpc.chain.subscribeFinalizedHeads((header) => {
  console.log(`Finalized #${header.number}: ${header.hash.toHex()}`);
});
```

### Subscribe to Storage Changes

```typescript
// Watch balance changes for an account
const unsub = await api.query.system.account(address, ({ data }) => {
  console.log(`Balance changed — Free: ${data.free.toHuman()}`);
});
```

### Subscribe to All Events

```typescript
const unsub = await api.query.system.events((events) => {
  events.forEach(({ event }) => {
    console.log(`${event.section}.${event.method}: ${event.data.toString()}`);
  });
});
```

### Raw WebSocket Subscriptions

```json
// Subscribe to new heads
{"jsonrpc":"2.0","method":"chain_subscribeNewHeads","params":[],"id":1}

// Subscribe to finalized heads
{"jsonrpc":"2.0","method":"chain_subscribeFinalizedHeads","params":[],"id":1}

// Subscribe to storage changes
{"jsonrpc":"2.0","method":"state_subscribeStorage","params":[["0x..."]],"id":1}

// Unsubscribe
{"jsonrpc":"2.0","method":"chain_unsubscribeNewHeads","params":["subscriptionId"],"id":1}
```

## Code Examples

### Query Staking Info

```typescript
const api = await ApiPromise.create({
  provider: new WsProvider(`wss://api-polkadot.n.dwellir.com/${process.env.DWELLIR_API_KEY}`),
});

// Active era
const activeEra = await api.query.staking.activeEra();
console.log(`Active era: ${activeEra.unwrap().index.toString()}`);

// Total staked
const totalIssuance = await api.query.balances.totalIssuance();
console.log(`Total issuance: ${totalIssuance.toHuman()}`);
```

### Cross-Chain (XCM) Query — Asset Hub Balance

```typescript
const assetHubApi = await ApiPromise.create({
  provider: new WsProvider(
    `wss://api-asset-hub-polkadot.n.dwellir.com/${process.env.DWELLIR_API_KEY}`
  ),
});

// Query foreign asset balance
const balance = await assetHubApi.query.system.account(address);
console.log(`Asset Hub balance: ${balance.data.free.toHuman()}`);
```

### Monitor Moonbeam EVM Events

Moonbeam is an EVM-compatible parachain — you can use both Substrate and EVM methods.

```typescript
import { JsonRpcProvider } from 'ethers';

// EVM-style access to Moonbeam
const provider = new JsonRpcProvider(
  `https://api-moonbeam.n.dwellir.com/${process.env.DWELLIR_API_KEY}`
);

const blockNumber = await provider.getBlockNumber();
console.log(`Moonbeam block: ${blockNumber}`);
```

## Sidecar REST API

Substrate API Sidecar provides a REST interface for querying chain data. Availability depends on the account and endpoint.

### Available Sidecar Endpoints

| Chain | Endpoint Slug |
|-------|---------------|
| Polkadot | `api-polkadot-sidecar` |
| Kusama | `api-kusama-sidecar` |
| Asset Hub Polkadot | `api-asset-hub-polkadot-sidecar` |
| Asset Hub Kusama | `api-asset-hub-kusama-sidecar` |
| Centrifuge | `api-centrifuge-sidecar` |
| KILT | `api-kilt-sidecar` |

### Sidecar URL Format

```
https://api-{chain}-sidecar.n.dwellir.com/{API_KEY}
```

### Key Sidecar Routes

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

## Best Practices

1. **Use WebSocket** — Substrate chains are designed for persistent connections. WSS is more efficient than HTTP for multi-call workflows and required for subscriptions.

2. **Cache metadata** — Runtime metadata is large (~500KB+). Cache it and only refresh on runtime upgrades (check `state_getRuntimeVersion`).

3. **Handle runtime upgrades** — Substrate chains can upgrade at any block. Listen for `system.events` containing `system.CodeUpdated` to refresh metadata.

4. **Use type registries** — `@polkadot/api` auto-detects types from metadata. For custom pallets, provide type definitions in the `ApiPromise.create({ types: {...} })` call.

5. **Batch storage queries** — Use `api.query.*.multi()` or `api.queryMulti()` instead of individual queries to reduce round trips.

6. **Watch finalized blocks** — For reliable data, subscribe to `chain_subscribeFinalizedHeads` rather than `chain_subscribeNewHeads`. Finalized blocks are guaranteed not to be reverted.

7. **Clean up subscriptions** — Always call the unsubscribe function returned by subscription methods to avoid resource leaks.

8. **Use Sidecar for REST needs** — If your application prefers REST over WebSocket, use the Sidecar add-on instead of wrapping JSON-RPC calls.

## Documentation Links

- Polkadot docs: [dwellir.com/docs/polkadot](https://www.dwellir.com/docs/polkadot)
- Kusama docs: [dwellir.com/docs/kusama](https://www.dwellir.com/docs/kusama)
- Moonbeam docs: [dwellir.com/docs/moonbeam](https://www.dwellir.com/docs/moonbeam)
- Acala docs: [dwellir.com/docs/acala](https://www.dwellir.com/docs/acala)
- Astar docs: [dwellir.com/docs/astar](https://www.dwellir.com/docs/astar)
- @polkadot/api docs: [polkadot.js.org/docs/api](https://polkadot.js.org/docs/api)
- Substrate JSON-RPC spec: [paritytech.github.io/json-rpc-interface-spec](https://paritytech.github.io/json-rpc-interface-spec)
- Sidecar docs: [paritytech.github.io/substrate-api-sidecar/dist](https://paritytech.github.io/substrate-api-sidecar/dist)
