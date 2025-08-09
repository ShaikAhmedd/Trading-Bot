# Trading-Bot
Overview
A simple command-line bot to place market buy/sell orders on Binance Futures (Testnet by default) 🚀.
It:
Connects to Binance Futures using python-binance 🔌
Parses and validates decimal quantities ✅
Adjusts order quantities to symbol LOT_SIZE step 📏
Provides a small REPL with market_buy and market_sell commands ⌨️
Logs activity with configurable log level 📝

Features
Testnet support toggle via .env 🧪
LOT_SIZE-aware quantity rounding (ROUND_DOWN) 🔽
Clear error messages for invalid inputs ❗

Minimal dependencies 📦
Folder Structure
bot.py 🐍
.env 🔒
README.md 📄
requirements.txt (optional) 📃

Requirements
Python 3.9+ 🐍
A Binance API key/secret (Testnet recommended for safety) 🔑
Python packages
python-binance 📦
python-dotenv 📦
Example requirements.txt
python-binance==1.0.19
python-dotenv==1.0.1

Environment Setup
Create and activate a virtual environment 🧰
Windows (PowerShell):
python -m venv .venv
..venv\Scripts\Activate
macOS/Linux:
python3 -m venv .venv
source .venv/bin/activate

Install dependencies 📦
pip install -r requirements.txt
or
pip install python-binance python-dotenv

Create a .env file in the project root 🗝️
BINANCE_API_KEY=your_testnet_api_key
BINANCE_API_SECRET=your_testnet_api_secret

true = Binance Futures Testnet, false = live account (use with extreme caution)
USE_TESTNET=true

Optional: logging level (DEBUG, INFO, WARNING, ERROR)
LOG_LEVEL=INFO

Getting Testnet API Keys
Log in to Binance Futures Testnet and generate API keys for the Futures test environment 🔐.
Ensure Futures is enabled for the key ✅.
Keep keys secret 🙈.

How to Run
From VS Code or terminal:
python bot.py ▶️
Expected prompt:
Binance Futures Testnet Bot (type 'help' for commands)

Commands
help 
Shows available commands.
market_buy SYMBOL QTY 🟢
Places a market buy order (futures) for SYMBOL with quantity QTY.
Example: market_buy BTCUSDT 0.001
market_sell SYMBOL QTY 🔻
Places a market sell order (futures) for SYMBOL with quantity QTY.
Example: market_sell ETHUSDT 0.02
quit or exit 🚪
Exits the program.

Notes on Quantity
Quantities are parsed as Decimal 🧮.
Commas are allowed (e.g., 1,000 becomes 1000) ✅.
QTY must be > 0 ➕.
The bot rounds QTY down to the symbol LOT_SIZE step as per exchange info; if rounding makes it 0, it raises “Quantity too small after rounding” ⚠️.

Symbols
Use USDT-margined futures symbols like BTCUSDT, ETHUSDT, etc. 💱.
Symbol must exist on Binance Futures; otherwise “Symbol not found” ❌.

Logging
Controlled by LOG_LEVEL in .env (DEBUG/INFO/WARNING/ERROR) 🧭.
Logs to stdout with timestamps 🕒.

Error Handling
Invalid quantity format → “Invalid quantity: ...” ⛔.
Quantity <= 0 → “quantity must be > 0” 🚫.
Symbol not found → “Symbol not found: ...” 🔎.
Binance API errors → shown via logger with the error message 🧯.
Network issues → retried at library level; surfaced as BinanceRequestException 🌐.

Security
Never commit .env or API keys 🔐.
Use Testnet (USE_TESTNET=true) while testing 🧪.
If setting USE_TESTNET=false, you are trading live — proceed only if you fully understand the risks ⚠️.

Troubleshooting
Bot exits with “Missing API credentials in .env” 🧩
Ensure BINANCE_API_KEY and BINANCE_API_SECRET are present and not empty ✅.
“Quantity too small after rounding” ➖
Increase QTY to meet the symbol’s LOT_SIZE step 📈.
“Symbol not found” 🔤
Double-check symbol and ensure it’s a Futures symbol available on the selected environment (testnet/live) 🔁.
SSL or connection errors 🌐
Check internet and retry; consider upgrading python-binance 🔄.

Extending the Bot
Add leverage or margin mode:
client.futures_change_leverage(symbol="BTCUSDT", leverage=5) 🧰.
Add stop loss / take profit:
futures_create_order with STOP / TAKE_PROFIT types and appropriate params 🎯.
Add account balance or position checks:
client.futures_account_balance(), client.futures_position_information() 📊.

Known Limitations
Only market orders supported 🛑.
No risk management (no SL/TP) by default ⚠️.
No persistence or order tracking 🗂️🔑.

Tips

Use emoji shortcodes like :rocket:, :warning:, :lock:, etc.—GitHub will autocomplete afte
