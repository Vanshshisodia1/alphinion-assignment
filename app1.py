import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

# fetch nifty 50 stocks
nifty50_tickers = ["ADANIENT.NS", "ADANIPORTS.NS", "APOLLOHOSP.NS", "ASIANPAINT.NS", "AXISBANK.NS", 
                   "BAJAJ-AUTO.NS", "BAJFINANCE.NS", "BAJAJFINSV.NS", "BEL.NS", "BPCL.NS", "BHARTIARTL.NS", 
                   "BRITANNIA.NS", "CIPLA.NS", "COALINDIA.NS", "DRREDDY.NS", "EICHERMOT.NS", "GRASIM.NS", 
                   "HCLTECH.NS", "HDFCBANK.NS", "HDFCLIFE.NS", "HEROMOTOCO.NS", "HINDALCO.NS", "HINDUNILVR.NS", 
                   "ICICIBANK.NS", "ITC.NS", "INDUSINDBK.NS", "INFY.NS", "JSWSTEEL.NS", "KOTAKBANK.NS", "LT.NS", 
                   "M&M.NS", "MARUTI.NS", "NTPC.NS", "NESTLEIND.NS", "ONGC.NS", "POWERGRID.NS", "RELIANCE.NS", 
                   "SBILIFE.NS", "SHRIRAMFIN.NS", "SBIN.NS", "SUNPHARMA.NS", "TCS.NS", "TATACONSUM.NS", 
                   "TATAMOTORS.NS", "TATASTEEL.NS", "TECHM.NS", "TITAN.NS", "TRENT.NS", "ULTRACEMCO.NS", "WIPRO.NS"]

# define time period
start_date = "2022-01-01" 
end_date = datetime.today().strftime('%Y-%m-%d')

def fetch_stock_data(tickers, start, end):
    """fetch historical stock data for given tickers."""
    data = yf.download(tickers, start=start, end=end, progress=False)['Close']
    return data.dropna()

# fetch data
stock_data = fetch_stock_data(nifty50_tickers, start_date, end_date)

def calculate_ewmac(df, short_period, long_period):
 short_ewma = df.ewm(span=short_period, adjust=False).mean()
 long_ewma = df.ewm(span=long_period, adjust=False).mean()
 rolling_std=df.rolling(window=short_period).std()
 ewmac = (short_ewma - long_ewma) / rolling_std
 return ewmac

# calculate ewmac(4,16) and ewmac(8,32)
ewmac_4_16=calculate_ewmac(stock_data, 4, 16)
ewmac_8_32=calculate_ewmac(stock_data, 8, 32)

# generate buy signals (both ewmac indicators should be > 0)
buy_signals=(ewmac_4_16>0)&(ewmac_8_32>0)

# track when each stock first entered positive ewmac zone
entry_dates=buy_signals.apply(lambda x:x[x].index.min(), axis=0)

def allocate_weights(entry_dates,current_date):
    """allocate higher weights to max 10 stocks that recently turned positive."""
    time_since_entry = (current_date - entry_dates).dt.days // 7  # convert days to weeks
    valid_stocks = time_since_entry.dropna().sort_values().index[:10]  # select top 10 recent stocks
    weights=1/(time_since_entry[valid_stocks]+1)  # inverse proportional allocation
    weights=weights/weights.sum()  # normalize to 100%
    return weights

# weekly rebalancing
rebalance_dates=pd.date_range(start=start_date, end=end_date, freq='W-MON')
portfolio_weights={}
for date in rebalance_dates:
    portfolio_weights[date]=allocate_weights(entry_dates,date)

# convert to dataframe
portfolio_weights_df=pd.DataFrame(portfolio_weights).T.fillna(0)

# backtesting: compute portfolio returns
portfolio_returns=(portfolio_weights_df.shift(1)*stock_data.pct_change()).sum(axis=1)
cumulative_returns=(1+portfolio_returns).cumprod()

def sharpe_ratio(returns, risk_free_rate=0.02):
 return (returns.mean()-risk_free_rate/252)/returns.std()*np.sqrt(252)

def max_drawdown(cumulative_returns):
 rolling_max=cumulative_returns.cummax()
 drawdown=(cumulative_returns-rolling_max)/rolling_max
 return drawdown.min()

def value_at_risk(returns, confidence_level=0.95):
 return np.percentile(returns,(1-confidence_level)*100)

def cagr(cumulative_returns, start_date, end_date):
 years=(pd.to_datetime(end_date)-pd.to_datetime(start_date)).days/365.25
 return (cumulative_returns.iloc[-1]**(1/years))-1

sharpe= sharpe_ratio(portfolio_returns)
mdd= max_drawdown(cumulative_returns)
var_95= value_at_risk(portfolio_returns)
cagr_value= cagr(cumulative_returns,start_date,end_date)

print(f"Sharpe Ratio: {sharpe:.2f}")
print(f"Maximum Drawdown: {mdd:.2%}")
print(f"Value at Risk (95%): {var_95:.2%}")
print(f"CAGR: {cagr_value:.2%}")

latest_portfolio= portfolio_weights_df.iloc[-1]
print("Portfolio Allocation on",portfolio_weights_df.index[-1])
print(latest_portfolio.apply(lambda x:f"{x*100:.2f}%"))

plt.figure(figsize=(12,6))
plt.plot(cumulative_returns,label='EWMAC Strategy',color='b')
plt.axhline(y=1,color='r',linestyle='--',alpha=0.7)
plt.title('EWMAC Strategy Backtest Performance')
plt.xlabel('Date')
plt.ylabel('Cumulative Returns')
plt.legend()
plt.show()

