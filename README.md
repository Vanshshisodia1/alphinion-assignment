# alphinion-assignment
This project implements an Exponentially Weighted Moving Average Crossover (EWMAC) trading strategy on Nifty 50 stocks. It fetches historical data, calculates EWMAC values, generates buy signals, allocates weights to stocks, and performs weekly rebalancing. Key metrics such as Sharpe Ratio and CAGR are included for performance evaluation.
Here’s a GitHub description for your code that highlights its functionality and key features:

---

# EWMAC Trading Strategy for Nifty 50

This Python project implements an Exponentially Weighted Moving Average Crossover (EWMAC) trading strategy on Nifty 50 stocks using historical data fetched from Yahoo Finance. The strategy involves calculating two EWMAs, generating buy signals, and performing weekly portfolio rebalancing to optimize returns.

## Features

- **Data Fetching**: Retrieves historical closing prices of Nifty 50 stocks from January 1, 2022, to the present using the `yfinance` library.
- **EWMAC Calculation**: Computes EWMAs for specified short and long periods and calculates the EWMAC value to determine market trends.
- **Buy Signal Generation**: Identifies buy signals when both EWMAC(4, 16) and EWMAC(8, 32) indicators are positive, indicating potential upward momentum.
- **Weight Allocation**: Allocates portfolio weights to the top 10 recently positive stocks, ensuring diversified investment.
- **Weekly Rebalancing**: Updates portfolio weights every week based on the latest buy signals.
- **Backtesting**: Evaluates the strategy’s performance through various metrics, including:
  - **Sharpe Ratio**: Measures risk-adjusted returns.
  - **Maximum Drawdown**: Assesses the largest drop from a peak in the cumulative return.
  - **Value at Risk (VaR)**: Estimates potential losses in the portfolio under normal market conditions.
  - **Compound Annual Growth Rate (CAGR)**: Calculates the mean annual growth rate of the investment.

## Installation

To run this project, ensure you have the following Python packages installed:

```bash
pip install yfinance pandas numpy matplotlib
```

## Usage

Run the script to see the performance of the EWMAC strategy, including a plot of cumulative returns and the final portfolio allocation. The results include key financial metrics that help evaluate the effectiveness of the trading strategy.

## Contributing

Contributions are welcome! If you have suggestions for improvements or additional features, feel free to fork the repository and submit a pull request.

