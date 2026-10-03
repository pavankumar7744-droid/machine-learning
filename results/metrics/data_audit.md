# Data Audit Report

## 1. Dataset Shape and Basic Checks
- **Rows:** 12330 (Expected: 12,330) - Pass
- **Columns:** 18 (Expected: 18) - Pass
- **Missing Values:** 0 (Expected: 0) - Pass
- **Exact Duplicate Rows:** 125 (Expected: 125) - Pass

## 2. Target Variable (`Revenue`)
- **Target column present:** Yes
- **Type:** bool
- **Purchase Rate (overall):** 15.47% (Expected: ~15.5%)
- **Purchase Rate (without duplicates):** 15.63% (Expected: ~15.6%)

## 3. Categorical Values Check (`Month`)
- **Months Present:** Aug, Dec, Feb, Jul, June, Mar, May, Nov, Oct, Sep
- **Status:** Pass. Matches expected months exactly (Jan and Apr absent).
