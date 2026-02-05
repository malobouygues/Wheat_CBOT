# Wheat WASDE Supply & Demand

This project analyzes the fundamental supply & demand balance of Global and US wheat using historical USDA WASDE data.

**Objective**: To move beyond headline "Ending Stocks" numbers and have the tightness of the balance sheet through Stocks-to-Use ratios.

## 1. Context & Rationale

The monthly WASDE (World Agricultural Supply and Demand Estimates) report is the benchmark for grain fundamentals. 

https://www.usda.gov/about-usda/general-information/staff-offices/office-chief-economist/commodity-markets/wasde-report

**Question**: Is the balance sheet actually tightening or is the market just reacting to inventory noise?

## 2. Building the Model (How My Thinking Evolved)

My focus shifted from simply plotting data to understanding the seasonality of USDA estimates. The USDA follows a behavioral pattern in how they revise numbers throughout the marketing year.

### A. The Metric: Stocks-to-Use vs. Absolute Stocks

**Mistake** I tracked raw Ending Stocks (in million metric tons)
My first iteration simply visualized the decline in ending stocks.

- **Why?**: Focusing on nominal volume ignores demand destruction or demand rationing.
- **Solution**: I did a calculated field in ratios.py:

```python
stocks_to_use = ending_stocks / total_use
```

-> It allows me to compare the US balance sheet (historically tight) vs. the World balance sheet (historically heavy due to Russia/China stocks) on the same relative scale

### B. The revision (USDA Bias)

The code groups data by month rather than just a linear time series.

- The USDA tends to be conservative and overestimate yield early in the season (May/June)
- If the January ratio is trending below the seasonal average of previous Januarys, the crop year will be tighter than the market anticipates
- **Logic**: By visualizing the curve of stocks_to_use month by month, I can identify a direction

## 3. Technical Stack

This tool prioritizes clean data structure to separate calculation logic from visualization.

- **Language**: Python 3.9+
- **Data**:
  - **Pandas**: Groupby operations
  - **Calculated Fields**: Dynamic computation of ratios (automatically updated in case of new raw data)
- **Source**: Historical WASDE csv (2016-Present)