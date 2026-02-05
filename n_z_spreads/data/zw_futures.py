import os
import pandas as pd
from datetime import datetime
from tvDatafeed import TvDatafeed, Interval

def download_zw_futures():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.makedirs(script_dir, exist_ok=True)
    
    tv = TvDatafeed()
    now = datetime.now()
    
    start_year = 2015
    end_year = 2015
    
    for year in range(start_year, end_year + 1):
        ticker = f"ZWN{year}"
        filename = f"ZWN{year}.csv"
        filepath = os.path.join(script_dir, filename)
        
        df = None
        try:
            df = tv.get_hist(
                symbol=ticker,
                exchange="CBOT",
                interval=Interval.in_daily,
                n_bars=5000
            )
        except Exception as e:
            df = None
        
        if df is not None and not df.empty:
            df = df.reset_index()
            df['datetime'] = pd.to_datetime(df['datetime']).dt.date
            df = df[['datetime', 'close', 'volume']]
            df.to_csv(filepath, index=False, header=False)
            print(f"{filename}: {len(df)} rows saved (ticker: {ticker})")
        else:
            print(f"{filename}: No data available (ticker: {ticker})")

if __name__ == "__main__":
    download_zw_futures()
