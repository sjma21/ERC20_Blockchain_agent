from agent import parse_command
from blockchain import *

WRITE_ACTIONS = {"transfer", "approve", "transfer_from"}


def confirm(prompt):
    answer = input(f"⚠️  {prompt}\nType 'yes' to confirm: ").strip().lower()
    return answer == "yes"


def handle(data):
    action = data.get("action")

    # ── READ ──────────────────────────────────────────────
    if action == "get_balance":
        addr = data.get("address", WALLET_ADDRESS)
        bal = get_balance(addr)
        return f"💰 Balance of {addr}: {bal} {get_symbol()}"

    if action == "get_name":
        return f"Token name: {get_name()}"

    if action == "get_symbol":
        return f"Token symbol: {get_symbol()}"

    if action == "get_decimals":
        return f"Decimals: {get_decimals()}"

    if action == "get_total_supply":
        return f"Total supply: {get_total_supply()} {get_symbol()}"

    if action == "get_info":
        return (f"Name: {get_name()} | Symbol: {get_symbol()} | "
                f"Decimals: {get_decimals()} | Supply: {get_total_supply()}")

    if action == "get_allowance":
        owner = data.get("owner", WALLET_ADDRESS)
        spender = data.get("spender")
        if not spender:
            return "❌ Missing spender address."
        allowance = get_allowance(owner, spender)
        return f"✅ Allowance: {allowance} {get_symbol()} (owner: {owner}, spender: {spender})"

    # ── WRITE ─────────────────────────────────────────────
    if action == "transfer":
        to = data.get("to")
        amount = data.get("amount")
        if not to or amount is None:
            return "❌ Missing 'to' address or 'amount'."
        if not confirm(f"Transfer {amount} {get_symbol()} to {to}?"):
            return "❌ Cancelled."
        tx = transfer(to, float(amount))
        return f"✅ Transfer sent! TX: {tx}"

    if action == "approve":
        spender = data.get("spender")
        amount = data.get("amount")
        if not spender or amount is None:
            return "❌ Missing 'spender' address or 'amount'."
        if not confirm(f"Approve {spender} to spend {amount} {get_symbol()}?"):
            return "❌ Cancelled."
        tx = approve(spender, float(amount))
        return f"✅ Approval sent! TX: {tx}"

    if action == "transfer_from":
        from_addr = data.get("from")
        to = data.get("to")
        amount = data.get("amount")
        if not from_addr or not to or amount is None:
            return "❌ Missing 'from', 'to', or 'amount'."
        if not confirm(f"TransferFrom {from_addr} → {to} of {amount} {get_symbol()}?"):
            return "❌ Cancelled."
        tx = transfer_from(from_addr, to, float(amount))
        return f"✅ TransferFrom sent! TX: {tx}"

    return f"❌ Unknown action: '{action}'"


print("🤖 ERC20 Agent ready. Type your command (or 'quit' to exit).")
while True:
    try:
        cmd = input("\n👉 ").strip()
        if cmd.lower() in ("quit", "exit"):
            break
        data = parse_command(cmd)
        print(f"🧠 Parsed: {data}")
        print(handle(data))
    except KeyboardInterrupt:
        break
    except Exception as e:
        print(f"❌ Error: {e}")
