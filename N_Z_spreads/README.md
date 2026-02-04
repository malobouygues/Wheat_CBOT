# SRW Wheat July–December Spread Analysis

This project analyzes the seasonality of CBOT Soft Red Winter Wheat through the lens of a physical operator, prioritizing Term Structure over directional price.

**Objective**: To replicate the decision-making metrics of merchandising teams by visualizing Cost of Carry dynamics and identifying historical Contango/Backwardation anomalies.

## 1. Context & Rationale

The logic behind this project stems from a limitation I found in static reporting. While reports like the USDA's WASDE provide crucial snapshots of the Balance Sheet (Ending Stocks, Production), they remain monthly static data points. I needed a dynamic tool to visualize how these fundamentals translate into price action over time.

**The Question** Is the current market structure (Contango/Backwardation) abnormal relative to historical seasonal norms?

**The Pivot** Initially, I focused on directional price ("Flat Price"). I realized this was a mistake for a fundamental analysis approach.

- **Why?** Flat Price is heavily polluted by macro factors (USD, Inflation).
- **Rationale**: For a storage operator, the critical variable is not the price, but the Carry (the price difference that remunerates storage).

## 2. Adapting the Code to Market Realities (Evolution of Logic)

Writing this code was about correcting my initial assumptions to fit the biological and logistical realities of the Wheat market over a 10-year historical dataset. Here is how my thinking evolved:

### A. Defining the "Biological Year"

My first iteration used a standard Year-to-Date (Jan-Dec) analysis. I realized this creates false signals in grains because resetting data on January 1st splits the storage season in half.

- **The Problem**: A Jan-1st reset ignores the cost of carry accumulated since the summer harvest.
- **The Fix**: The code forces a June 1st start date.
- **Why June 1st?** It aligns with the SRW Harvest start. This captures the full lifecycle from the "Supply Reset" (Harvest pressure) to the "Storage Depletion" (Winter/Spring).

### B. Selecting the Right Spread (July - December)

I specifically chose to model the July (N) vs. December (Z) spread.

- **July (N)**: The anchor of the new crop. Harvest pressure creates a supply glut.
- **December (Z)**: The storage phase.

**The Thesis**: I wanted to visualize the "Cash & Carry" incentive. In a normal year, this spread should trade in Contango (December > July) to pay merchants to store the grain.

### C. The "Price Level" Bias (Normalization)

One of my biggest realizations came when comparing raw price data between decades.

- **Realization**: A $0.50 move in 2000 (when Wheat was ~$2.50) is statistically crushed by daily volatility in 2022 (when Wheat was ~$8.00). Recent high-priced years were disproportionately influencing the average.
- **Correction**: I switched to Base-100 Indexing.
- **Result**: This allows the model to compare percentage returns and relative volatility rather than nominal dollar moves, ensuring 2000 and 2022 are mathematically comparable.

### D. Filtering Historical Noise (The "Black Swan" Problem)

When backtesting, a simple mean calculation was useless because of three specific structural breaks in the 10-year dataset:

- **2008 (Agflation)**: A speculative bubble where the index doubled (100 to 200).
- **2010 (Russian Drought)**: A sharp supply shock spike in July/August due to the export ban.
- **2022 (Ukraine War)**: A massive geopolitical premium starting late Feb (Day 50) and peaking in March.

**The Fix**: I switched to a Median-based approach. This naturally filters out these extreme tails to reveal the recurring behavior of a "standard year" (trading the rule, not the exception).

### E. Operational Safety: Delivery Logic & First Notice Day

My initial analysis failed to account for the physical reality of contract expiration. Data during the delivery month is driven by logistical convergence, not broad seasonality.

- **The Risk**: Holding the front-month contract into the delivery period exposes the trader to "Delivery Risk" (getting assigned physical wheat).
- **The Rule**: The analysis must stop before the First Notice Day (FND).

**Implementation**:

- According to the CME Group Calendar, the FND is the last business day of the month preceding the contract month.
- **Example**: For the July 2026 contract (WN26), the CME schedule confirms the First Notice Day is June 30, 2026.
- The code calculates this date dynamically and cuts the data series 3 days prior to ensure the model only tracks liquid, speculative risk.

https://www.cmegroup.com/markets/agriculture/grains/wheat.calendar.html

## 3. Technical Implementation

This project prioritizes data integrity and reproducibility.

- **Language**: Python 3.9+
- **Data Acquisition**: tvDatafeed (TradingView API wrapper).
  - **Reasoning**: Chosen over scraping CME HTML (fragile) or Yahoo Finance (poor handling of futures rollovers).
- **Core Libraries**:
  - **Pandas**: Vectorized operations for Marketing Year realignment and Base-100 indexing.
  - **Scipy (ndimage)**: Implementation of a Gaussian Filter (Sigma=3) to smooth high-frequency daily volatility without the lag associated with Simple Moving Averages.
- **Data Storage**: Local CSV serialization with ISO-formatted dates.
