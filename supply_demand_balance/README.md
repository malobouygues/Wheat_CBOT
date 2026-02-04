# Wheat Fundamentals and WASDE Revision Cycles

This project analyzes the fundamental Supply & Demand balance of Global and US Wheat using historical USDA WASDE data.

**Objective**: To move beyond headline "Ending Stocks" numbers and visualize the true tightness of the balance sheet through Stocks-to-Use ratios and historical revision trends.

## 1. Context & Rationale

The monthly WASDE (World Agricultural Supply and Demand Estimates) report is the benchmark for grain fundamentals. However, looking at the raw report has a major flaw: it provides a static snapshot in time.

https://www.usda.gov/about-usda/general-information/staff-offices/office-chief-economist/commodity-markets/wasde-report

**The Objective** I wanted to answer a specific fundamental question: Is the balance sheet actually tightening, or is the market just reacting to nominal inventory noise?

**The Pivot** Initially, I tracked raw Ending Stocks (in Million Metric Tons). I realized this was a "Retail" error.

- **Why?** A 600M bushel carryout in 2010 is not comparable to a 600M bushel carryout in 2023, as global consumption has risen significantly.
- **Rationale**: For a fundamental analyst, the critical metric is the Stocks-to-Use Ratio (S/U). This measures the "Days of Consumption" available. It is the only normalized metric that defines real scarcity.

## 2. Adapting the Code to Market Realities (Evolution of Logic)

My focus shifted from simply plotting data to understanding the seasonality of USDA estimates. The USDA follows a behavioral pattern in how they revise numbers throughout the marketing year.

### A. The Metric: Stocks-to-Use vs. Absolute Stocks

My first iteration simply visualized the decline in ending stocks.

- **The Trap**: Focusing on nominal volume ignores demand destruction or demand rationing.
- **The Fix**: I implemented a calculated field in ratios.py:

```python
stocks_to_use = ending_stocks / total_use
```

- **Why?** This converts the data into a percentage of tightness. It allows me to compare the US balance sheet (historically tight) vs. the World balance sheet (historically heavy due to Russia/China stocks) on the same relative scale.

### B. The Baseline: "Long-Run" vs. "5-Year" Average

The script deliberately plots two distinct averages: the full historical average and the rolling 5-year average.

- **Observation**: The global wheat flow changed structurally after 2020 (Covid logistics, Black Sea war). Comparing current tightness to 2016 data is often irrelevant.
- **Realization**: The market has a "short memory."
- **Correction**: I added a specific 5-Year Average line. This represents the "New Normal." If current Stocks-to-Use is below the 5-year average, it signals acute tightness regardless of the 10-year historical floor.

### C. The "Revision Seasonality" (USDA Bias)

The code groups data by month (Marketing Year timeline) rather than just a linear time series.

- **The Problem**: The USDA tends to be conservative. They often overestimate yield early in the season (May/June) and slowly downgrade production/increase exports as the harvest is realized.
- **The Logic**: By visualizing the curve of stocks_to_use month by month (from May forecasts to final numbers), I can identify the Direction of Travel.
- **Insight**: If the January ratio is trending below the seasonal average of previous Januarys, it confirms that the "Tail" of the crop year will be tighter than the market anticipates.

## 3. Technical Implementation

This tool prioritizes clean data structure to separate calculation logic from visualization.

- **Language**: Python 3.9+
- **Architecture**: Modular approach (ratios.py for business logic, main.py for execution).
- **Data Handling**:
  - **Pandas**: Used for datetime conversion and groupby operations to calculate monthly seasonal averages.
  - **Calculated Fields**: Dynamic computation of ratios ensures that if the source CSV is updated with new raw data, the relative metrics update automatically.
- **Source**: Historical WASDE CSV dataset (2016-Present), manually curated to ensure column consistency between US and World datasets.
