import os
import json
import anthropic
import re
from dotenv import load_dotenv

load_dotenv()

client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))


def clean_json(text):
    text = text.replace("```json", "").replace("```", "")
    match = re.search(r"\{.*\}", text, re.DOTALL)
    return match.group(0) if match else None


def parse_command(command):
    prompt = f"""
You are an ERC20 token agent. Convert the user's command into a JSON action object.

Command: {command}

Available actions and their JSON formats:

READ actions (no confirmation needed):
- Get your own token balance:
  {{"action": "get_balance"}}

- Get balance of a specific address:
  {{"action": "get_balance", "address": "0x..."}}

- Get token name:
  {{"action": "get_name"}}

- Get token symbol:
  {{"action": "get_symbol"}}

- Get token decimals:
  {{"action": "get_decimals"}}

- Get total supply:
  {{"action": "get_total_supply"}}

- Get token info (name, symbol, supply):
  {{"action": "get_info"}}

- Get allowance (how much spender can spend on behalf of owner):
  {{"action": "get_allowance", "owner": "0x...", "spender": "0x..."}}

- Get my allowance for a spender (owner = my wallet):
  {{"action": "get_allowance", "spender": "0x..."}}

WRITE actions (will ask for confirmation):
- Transfer tokens to an address:
  {{"action": "transfer", "to": "0x...", "amount": <number>}}

- Approve a spender to spend tokens on your behalf:
  {{"action": "approve", "spender": "0x...", "amount": <number>}}

- Transfer tokens from one address to another (requires prior approval):
  {{"action": "transfer_from", "from": "0x...", "to": "0x...", "amount": <number>}}

Rules:
- amount must be a plain number (e.g. 10, 50.5)
- addresses must start with 0x
- ONLY return valid JSON, nothing else
"""

    response = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=300,
        messages=[{"role": "user", "content": prompt}]
    )

    content = response.content[0].text
    json_text = clean_json(content)
    return json.loads(json_text)
