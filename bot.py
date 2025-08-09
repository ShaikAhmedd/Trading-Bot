import os
import sys
import logging
from decimal import Decimal, InvalidOperation, ROUND_DOWN
from dotenv import load_dotenv
from binance.client import Client
from binance.enums import *
from binance.exceptions import BinanceAPIException, BinanceRequestException


def setup_logger():
    log_level = os.getenv("LOG_LEVEL", "INFO").upper()
    logger = logging.getLogger("basic_bot")
    logger.setLevel(getattr(logging, log_level, logging.INFO))
    if not logger.handlers:
        fmt = logging.Formatter("%(asctime)s | %(levelname)s | %(message)s", datefmt="%Y-%m-%d %H:%M:%S")
        sh = logging.StreamHandler(sys.stdout)
        sh.setFormatter(fmt)
        logger.addHandler(sh)
    return logger

def parse_decimal(value: str, field_name: str) -> Decimal:
    value = value.replace(",", "")
    try:
        d = Decimal(value)
    except (InvalidOperation, ValueError):
        raise ValueError(f"Invalid {field_name}: {value}")
    if d <= 0:
        raise ValueError(f"{field_name} must be > 0")
    return d

class BasicBot:
    def __init__(self, api_key, api_secret, logger, use_testnet=True):
        self.logger = logger
        self.client = Client(api_key, api_secret, testnet=use_testnet)
        self.exchange_info_cache = self.exchange_info()
        self.logger.info(f"Bot initialized (testnet={use_testnet})")

    def exchange_info(self):
        return self.client.futures_exchange_info()

    def get_symbol_info(self, symbol: str):
        for s in self.exchange_info_cache["symbols"]:
            if s["symbol"] == symbol:
                return s
        raise ValueError(f"Symbol not found: {symbol}")

    def adjust_qty(self, symbol: str, qty: Decimal):
        info = self.get_symbol_info(symbol)
        for f in info["filters"]:
            if f["filterType"] == "LOT_SIZE":
                step = Decimal(f["stepSize"])
                exp = step.normalize().as_tuple().exponent
                adj = qty.quantize(Decimal((0, (1,), exp)), rounding=ROUND_DOWN)
                if adj <= 0:
                    raise ValueError("Quantity too small after rounding")
                return adj
        return qty

    def market_buy(self, symbol: str, qty: Decimal):
        qty = self.adjust_qty(symbol, qty)
        return self.client.futures_create_order(
            symbol=symbol, side=SIDE_BUY, type=FUTURE_ORDER_TYPE_MARKET, quantity=str(qty)
        )

    def market_sell(self, symbol: str, qty: Decimal):
        qty = self.adjust_qty(symbol, qty)
        return self.client.futures_create_order(
            symbol=symbol, side=SIDE_SELL, type=FUTURE_ORDER_TYPE_MARKET, quantity=str(qty)
        )

def main():
    load_dotenv()
    logger = setup_logger()

    api_key = os.getenv("BINANCE_API_KEY")
    api_secret = os.getenv("BINANCE_API_SECRET")
    use_testnet = os.getenv("USE_TESTNET", "true").lower() == "true"

    if not api_key or not api_secret:
        logger.error("Missing API credentials in .env")
        sys.exit(1)

    bot = BasicBot(api_key, api_secret, logger, use_testnet)

    print("Binance Futures Testnet Bot (type 'help' for commands)")

    while True:
        try:
            cmd = input("> ").strip().lower()
        except (EOFError, KeyboardInterrupt):
            print("\nExiting...")
            break

        if cmd in ("quit", "exit"):
            break
        if cmd == "help":
            print("Commands:\n  market_buy SYMBOL QTY\n  market_sell SYMBOL QTY\n  quit")
            continue

        parts = cmd.split()
        try:
            if parts[0] == "market_buy" and len(parts) == 3:
                symbol = parts[1].upper()
                qty = parse_decimal(parts[2], "quantity")
                order = bot.market_buy(symbol, qty)
                print(order)
            elif parts[0] == "market_sell" and len(parts) == 3:
                symbol = parts[1].upper()
                qty = parse_decimal(parts[2], "quantity")
                order = bot.market_sell(symbol, qty)
                print(order)
            else:
                print("Invalid command. Type 'help'.")
        except Exception as e:
            logger.error(e)

if __name__ == "__main__":
    main()
