# ERC20 Blockchain Agent

An AI-powered CLI agent for interacting with ERC20 smart contracts on blockchain networks using natural language commands. Powered by [Claude](https://www.anthropic.com/claude) and [Web3.py](https://web3py.readthedocs.io/).

## Overview

Instead of manually constructing blockchain transactions or learning contract ABIs, you can type plain English commands like _"send 100 tokens to 0xABC..."_ or _"what's my balance?"_ — the agent uses Claude AI to parse your intent and execute the appropriate on-chain action.

```
You: What's my balance?
Agent: 💰 Balance: 1000.0 tokens

You: Send 50 tokens to 0xAbC1234...
⚠️  WRITE action detected: transfer {'to': '0xAbC1234...', 'amount': 50.0}
Confirm? (yes/no): yes
Agent: ✅ TX sent: 0xdeadbeef...
```

## Features

- **Natural language interface** — no need to know contract ABIs or transaction formats
- **All standard ERC20 operations** — transfer, approve, transferFrom, balanceOf, allowance, and more
- **Safety confirmations** — write operations (transfers, approvals) require explicit confirmation before broadcasting
- **Automatic unit conversion** — handles token decimals transparently
- **Secure transaction signing** — signs and broadcasts transactions using your private key

## Architecture

```
User Input (Natural Language)
        ↓
    main.py  ── CLI loop & action dispatcher
        ↓
    agent.py ── Claude AI parses input → JSON action
        ↓
blockchain.py ── Web3.py executes contract call or transaction
        ↓
    Output   ── Balance, TX hash, or token info
```

| File | Role |
|------|------|
| `main.py` | Interactive CLI loop; routes parsed actions to blockchain functions |
| `agent.py` | Calls Claude API to convert natural language into structured JSON actions |
| `blockchain.py` | Web3.py integration; reads from and writes to the ERC20 contract |

## Prerequisites

- Python 3.8+
- An [Anthropic API key](https://console.anthropic.com/)
- A blockchain RPC endpoint (e.g., [Infura](https://infura.io/), [Alchemy](https://www.alchemy.com/))
- A wallet private key with funds for gas
- The address of an ERC20 contract to interact with

## Installation

1. **Clone the repository**

   ```bash
   git clone https://github.com/sjma21/ERC20_Blockchain_agent.git
   cd ERC20_Blockchain_agent
   ```

2. **Install dependencies**

   ```bash
   pip install anthropic web3 python-dotenv
   ```

3. **Configure environment variables**

   Create a `.env` file in the project root:

   ```env
   ANTHROPIC_API_KEY=sk-ant-...
   RPC_URL=https://mainnet.infura.io/v3/YOUR_PROJECT_ID
   PRIVATE_KEY=0xYOUR_PRIVATE_KEY
   ERC20_ADDRESS=0xTOKEN_CONTRACT_ADDRESS
   WALLET_ADDRESS=0xYOUR_WALLET_ADDRESS   # optional, derived from PRIVATE_KEY if omitted
   ```

   > **Security warning:** Never commit your `.env` file or expose your private key. Add `.env` to your `.gitignore`.

## Usage

```bash
python main.py
```

The agent starts an interactive session. Type commands in plain English:

### Read Operations (no confirmation required)

| Example Command | Action |
|-----------------|--------|
| `What's my balance?` | Returns your token balance |
| `Check balance of 0xABC...` | Returns balance of a specific address |
| `What's the token name?` | Returns the token name |
| `What's the symbol?` | Returns the token symbol |
| `What's the total supply?` | Returns total token supply |
| `What's the allowance from 0xABC... to 0xDEF...?` | Returns spending allowance |
| `Give me token info` | Returns name, symbol, and total supply |

### Write Operations (require "yes" confirmation)

| Example Command | Action |
|-----------------|--------|
| `Send 100 tokens to 0xABC...` | Transfers tokens to an address |
| `Approve 0xABC... to spend 50 tokens` | Approves a spender allowance |
| `Transfer 25 tokens from 0xABC... to 0xDEF...` | Executes transferFrom |

Type `exit` or `quit` to stop the agent.

## Supported ERC20 Actions

The agent recognizes the following structured actions (parsed automatically from your natural language input):

| Action | Type | Parameters |
|--------|------|------------|
| `get_balance` | Read | `address` (optional) |
| `get_name` | Read | — |
| `get_symbol` | Read | — |
| `get_decimals` | Read | — |
| `get_total_supply` | Read | — |
| `get_allowance` | Read | `owner`, `spender` |
| `get_info` | Read | — |
| `transfer` | Write | `to`, `amount` |
| `approve` | Write | `spender`, `amount` |
| `transfer_from` | Write | `from`, `to`, `amount` |

## Security Considerations

- Your private key is loaded from the `.env` file and used only for local transaction signing — it is never transmitted anywhere except to your RPC endpoint as a signed transaction.
- Write operations always display the parsed action and parameters before asking for confirmation.
- Review the displayed action carefully before typing `yes`.

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you'd like to change.

## License

[MIT](https://choosealicense.com/licenses/mit/)
