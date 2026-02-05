# SRW Wheat July–December Spread Analysis

This project analyzes the seasonality of CBOT Soft Red Winter Wheat through the lens of a physical operator, prioritizing Term Structure over directional price.

**Objective**: To analyze the seasonality of CBOT Soft Red Winter Wheat through Term Structure, and to identify historical contango/backwardation anomalies

## 1. Context & Rationale

The logic behind this project comes from a limitation I found in static reporting. While reports like the USDA's WASDE provide crucial snapshots of the Balance Sheet (Ending Stocks, Production), they remain monthly static data points. I wanted to visualize how these fundamentals translate into price action over time.

**Question**: How does the SRW wheat curve typically behave ahead of harvest, and does the current structure deviate from its historical seasonal profile?

**Initial Mistake** I focused on directional price (flat price), but realized this was a mistake for a fundamental analysis approach

- **Why?**: Flat price is heavily polluted by macro factors (USD, inflation, geopolitics, ...)
- **Rationale**: For a storage operator, the critical variable is not the price, but the carry (the price difference that remunerates storage)

## 2. Building the Model (How My Thinking Evolved)

### A. The Biological Year

My first iteration used a standard YtD (Jan-Dec) analysis. I realized this creates false signals in grains because resetting data on January 1st splits the storage season in half.

- **Problem**: A Jan-1st reset ignores the cost of carry accumulated since the summer harvest
- **Why June 1st?** It aligns with the SRW Harvest start. This captures the full lifecycle from the harvest pressure to the storage depletion (winter)

### B. Selecting the Right Spread (July - December)

I specifically chose to model the July (N) vs. December (Z) spread.

- **July (N)**: First contract of the new crop; harvest increases supply
- **December (Z)**: The storage phase

**Thesis**: I wanted to visualize the cash & carry motivation; in a normal year, this spread should trade in Contango (December > July) to pay merchants to store the grain

### C. The Price Level Bias (Normalization)

One of my biggest realizations came when comparing raw price data between decades.

- **Problem**: A $0.50 move in 2000 (when wheat was around $2.50/bushel) is statistically crushed by daily volatility in 2022 (when wheat was around $8.00/bushel)
- **Solution**: I switched to base-100 indexing to compare percentage returns and relative volatility, ensuring 2000 and 2022 are comparable

### D. Filtering Historical Noise

When backtesting, a simple mean calculation was useless because of three specific structural breaks in the 10-year dataset:

- **2008**: Speculative bubble where the index doubled (100 to 200)
- **2010 (russian ban)**: Supply shock spike in July/August due to the export ban
- **2022 (ukraine war)**: Geopolitical rise starting late February and peaking in March

**Solution**: I switched to a median approach to filter out these extreme tails

### E. Delivery & First Notice Day

My initial analysis failed to account for the physical reality of contract expiration. Data during the delivery month is driven by logistical convergence, not only seasonality.

- **Risk**: Holding the front-month contract into the delivery period exposes to a delivery risk (getting assigned physical wheat)

**Solution**:

- According to the CME Group Calendar, the FND is the last business day of the month preceding the contract month.
- **Example**: For the July 2026 contract (WN26), the CME schedule confirms the First Notice Day is June 30, 2026.
- The code calculates this date dynamically and cuts the data series 3 days prior to ensure the model only tracks liquid, speculative risk.

https://www.cmegroup.com/markets/agriculture/grains/wheat.calendar.html

## 3. Technical Stack

- **Language**: Python 3.9+
- **Data**: tvDatafeed (TradingView API)
- **Core Libraries**:
  - **Pandas**: Vectorized operations for marketing year realignment and base-100 indexing
  - **Scipy**: Gaussian Filter (sigma=3) to smooth high-frequency daily volatility
- **Data**: Local CSV serialization with ISO dates