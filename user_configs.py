# User configurations
# A configuration should have a list exchanges and a list of asset tickers

from .constants import (
    BINANCE_US_ID,
    COINBASE_ID,
    KRAKEN_ID,
    OKCOIN_ID,
    FTX_US_ID,
    CRYPTO_COM_ID,
)

USER1_CONFIG = {
    'exchanges': [BINANCE_US_ID, COINBASE_ID, KRAKEN_ID],
    'assets': ['BTC', 'ETH', 'REP', 'SCRT']
}
