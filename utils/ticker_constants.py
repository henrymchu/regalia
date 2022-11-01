# Assets with USD trading pairs

KNOWN_BINANCE_US_ASSETS = []
KNOWN_COINBASE_ASSETS = []

# Last updated 2022-10-31
KNOWN_FTX_US_ASSETS = [
    'AAVE', 'ALGO', 'AUD', 'AVAX', 'BAT', 'BCH', 'BRZ', 'BTC', 'CAD', 'CUSDT', 'DAI', 'DOGE', 'ETH', 'ETHW', 'EUR',
    'GBP', 'GRT', 'KSHIB', 'LINK', 'LTC', 'MATIC', 'MKR', 'NEAR', 'PAXG', 'SHIB', 'SOL', 'SUSHI', 'TRX', 'UNI',
    'USDT', 'WBTC', 'YFI']

KNONW_KRAKEN_ASSETS = []

# Last updated 2022-10-31
KNOWN_GEMINI_ASSETS = [
    '1INCH', 'AAVE', 'ALCX', 'ALI', 'AMP', 'ANKR', 'APE', 'API3', 'ASH', 'AUDIO', 'AVAX', 'AXS', 'BAL', 'BAT',
    'BCH', 'BICO', 'BNT', 'BOND', 'BTC', 'BUSD', 'CHZ', 'COMP', 'CRV', 'CTX', 'CUBE', 'CVC', 'DAI', 'DOGE', 'DOT',
    'DPI', 'EFIL', 'ELON', 'ENJ', 'ENS', 'ERN', 'ETH', 'EUL', 'FET', 'FIDA', 'FIL', 'FRAX', 'FTM', 'FXS', 'GAL',
    'GALA', 'GFI', 'GMT', 'GRT', 'GUSD', 'IMX', 'INDEX', 'INJ', 'IOTX', 'JAM', 'KNC', 'KP3R', 'LDO', 'LINK', 'LPT',
    'LQTY', 'LRC', 'LTC', 'LUNA', 'LUSD', 'MANA', 'MASK', 'MATIC', 'MC', 'MCO2', 'METIS', 'MIM', 'MIR', 'MKR', 'MPL',
    'NMR', 'ORCA', 'OXT', 'PAXG', 'PLA', 'QNT', 'QRDO', 'RAD', 'RARE', 'RAY', 'RBN', 'REN', 'REVV', 'RLY', 'RNDR',
    'SAMO', 'SAND', 'SBR', 'SHIB', 'SKL', 'SLP', 'SNX', 'SOL', 'SPELL', 'STORJ', 'SUSHI', 'TOKE', 'TRU', 'UMA',
    'UNI', 'USDC', 'UST', 'WCFG', 'XTZ', 'YFI', 'ZBC', 'ZEC', 'ZRX'
]

# Last updated 2022-10-31
KNOWN_OKCOIN_ASSETS = [
    'AAVE', 'ADA', 'ALGO', 'ANC', 'APE', 'API3', 'AR', 'ASTR', 'ATLAS', 'ATOM', 'AVAX', 'AXS', 'BRWL', 'BTC', 'CELO',
    'CHZ', 'COMP', 'CRO', 'CUSD', 'DAI', 'DIKO', 'DOGE', 'DOT', 'EGLD', 'ENJ', 'ENS', 'EOS', 'ETH', 'FLOW', 'FTM',
    'GALA', 'GRT', 'HASH', 'HBAR', 'HKC', 'ICP', 'ICX', 'IOTX', 'KDA', 'LINK', 'LRC', 'LTC', 'LUNA', 'LUNC', 'LUNR',
    'MAGIC', 'MANA', 'MATIC', 'MIA', 'MIM', 'MKR', 'NEAR', 'NYC', 'ONE', 'OP', 'POKT', 'UNI', 'USDT', 'SCRT', 'SHIB',
    'SLP', 'SNX', 'SOL', 'SPELL', 'STMX', 'STX', 'SUSHI', 'TRX', 'UMA', 'USDC', 'USDK', 'USTC', 'WAXP', 'WBTC', 'XCN',
    'XLM', 'XTZ', 'YFI', 'YFII', 'ZEC', 'ZEN', 'ZIL'
]

SINGLE_TICKER_IDENTIFIERS_USD = {
    'BTC': {
        'name': 'bitcoin',
        'binance.us': 'BTCUSD',
        'gemini': 'BTCUSD',
        'kraken': 'BTCUSD',
    },
    'ETH': {
        'name': 'ether',
        'binance.us': 'ETHUSD',
        'gemini': 'ETHUSD',
        'kraken': 'ETHUSD',
    },
    'FIL': {
        'name': 'filecoin',
        'binance.us': 'FILUSD',
        'coinbase': None,
        'gemini': 'FILUSD',
        'kraken': 'FILUSD',
    },
    'ILV': {
        'name': 'illuvium',
        'binance.us': 'ILVUSD',
        'coinbase': None,
    },
    'NEAR': {
        'name': 'near',
        'binance.us': 'NEARUSD',
        'coinbase': None,
        'okcoin': 'NEAR-USD',
    },
    'REP': {
        'name': 'augur',
        'binance.us': 'REPUSD',
        'coinbase': None,
        'kraken': 'REPUSD',
    },
    'SCRT': {
        'name': 'secret',
        'kraken': 'SCRTUSD',
        'okcoin': 'SCRT-USD',
    },
}
