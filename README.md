# regalia

## Description
Regalia is a powerful tool designed to identify potential price differences (arbitrage opportunities) 
across various cryptocurrency exchanges. By leveraging real-time market data, this tool helps traders 
and enthusiasts capitalize on price differentials between exchanges, maximizing profit potential in 
the volatile cryptocurrency market.

### Features
- **Multi-Exchange Analysis**: Seamlessly compare prices across multiple cryptocurrency exchanges to 
uncover lucrative arbitrage opportunities.
- **Real-Time Data**: Utilize up-to-date market data to ensure accurate analysis and timely execution 
of trades.

## Project Structure
```
project-root/
│
├── tests/
│ ├── test_utils/
│   ├── test_arbitrage_explorer_v1.py
│   └── test_exchange_apis.py
│ └── test_regalia_main.py
│
├── utils/
│ ├── arbitrage_explorer_v1.py
│ ├── exchange_apis.py
│ └── ticker_constants.py
│
├── README.md
├── constants.py
├── regalia_main.py
├── requirements.txt
└── user_configs.py
```

## Usage
### Run tool
python regalia_main.py
### Run unit tests
python -m unittest

## Future Developement
- **Customizable Parameters**: Adjust parameters such as minimum price difference, trading fees, and 
minimum volume to tailor the tool to your specific trading strategy.
- **Configurable Notifications**: Receive alerts via email, SMS, or other channels when potential 
arbitrage opportunities arise.

## Authors
Henry Chu

