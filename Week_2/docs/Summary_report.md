# DATA CLEANING SUMMARY REPORT

## 1. NETFLIX DATASET

|Issue Found|Action Taken|Details|Impact|
|---|---|---|---|
|**Missing Values - Director**|Filled with "Unknown"|2,634 missing values replaced|Preserved 29.9% of rows that would otherwise be lost|
|**Missing Values - Cast**|Filled with "Not Available"|825 missing values replaced|Maintained data integrity with clear placeholder|
|**Missing Values - Country**|Filled with "Unknown"|831 missing values replaced|Preserved 9.4% of records for geographical analysis|
|**Missing Values - Date Added**|Dropped rows|10 rows removed (0.11% of data)|Clean date column for time-series analysis|
|**Missing Values - Rating**|Filled with mode|4 missing values filled with most common rating|Maintained rating distribution integrity|
|**Missing Values - Duration**|Dropped rows|3 rows removed (0.03% of data)|Ensured duration data completeness|
|**Date Format**|Standardized to YYYY-MM-DD|Converted from "September 25, 2021" to "2021-09-25"|Enabled proper sorting and time-series analysis|
|**Text Formatting**|Standardized strings|Used `.str.strip()` to remove whitespace|Ensured consistency across all text columns|
|**Duplicates**|Checked|`duplicated().sum()` = 0|No duplicate records found|
|**Data Types**|Converted date|`pd.to_datetime()` with `errors='coerce'`|Proper datetime format for date_added column|

### Netflix Final Results:

- **Original Shape:** 8,807 rows × 12 columns
- **Cleaned Shape:** 8,790 rows × 12 columns
- **Total Rows Removed:** 17 (10 date_added + 3 duration + 4 rating filled instead of removed)
- **Rows with Missing Values Fixed (not removed):** 4,294 (director + cast + country + rating)

# Challenges
```python
FileNotFoundError: [Errno 2] No such file or directory: '../Week_1/data/netflix_titles.csv'
```
- I set working directory as root using chdir

## RETAIL DATASET 

|**Issue Found**|**Action Taken**|**Details**|**Count Affected**|**Status**|
|---|---|---|---|---|
|**MISSING VALUES**|||||
|Missing CustomerID|Filled with 0|Sales Analytics Version: Filled 135,080 missing values with 0|135,080 rows|✅ Completed|
|Missing CustomerID|Dropped rows|Customer Analytics Version: Kept only 406,829 rows with CustomerID (75.1%)|135,080 rows removed|✅ Completed|
|Missing Description|Filled with "Unknown"|Replaced 1,454 missing product descriptions|1,454 rows|✅ Completed|
|**DUPLICATES**|||||
|Duplicate Records|Removed|Removed 5,268 exact duplicate rows while keeping first occurrence|5,268 rows removed|✅ Completed|
|**INVALID VALUES**|||||
|Zero Quantity|Removed|Removed rows with quantity = 0 (no business meaning)|0 rows found|✅ None Found|
|Invalid Unit Price (≤ 0)|Removed|Removed 2,512 rows with invalid or negative prices|2,512 rows removed|✅ Completed|
|Negative Quantity|Preserved|Kept 10,587 rows as valid returns/cancellations|10,587 rows|✅ Preserved|
|**STANDARDIZATION**|||||
|Date Format|Converted to datetime|Standardized from "12/1/2010 8:26" to datetime format with components|All 534,129 rows|✅ Applied|
|Text Formatting|UPPERCASE & Title Case|Description → UPPERCASE, Country → Title Case|All rows|✅ Applied|
|Column Names|Renamed to snake_case|Converted all column names to consistent format (e.g., InvoiceNo → invoice_no)|8 columns|✅ Applied|
|Data Types|Optimized|Converted categorical columns (stock_code, description, country) for memory efficiency|3 columns|✅ Applied|
|**DERIVED COLUMNS**|||||
|Total Price|Added|Calculated as quantity × unit_price|New column|✅ Created|
|Return Flag|Added|Boolean flag for negative quantities (is_return)|New column|✅ Created|
|Cancelled Flag|Added|Boolean flag for invoices starting with 'C' (is_cancelled)|New column|✅ Created|
|**VALIDATION**|||||
|Cancelled Invoices|Flagged|Identified 9,251 rows with invoices starting with 'C' for separate analysis|9,251 rows flagged|✅ Flagged|
|Outlier Prices|Identified|Found 4,789 rows with prices > 99th percentile|4,789 rows|✅ Flagged|

---

## DATASET QUALITY METRICS

|**Metric**|**Before Cleaning**|**After Cleaning**|**Improvement**|
|---|---|---|---|
|Total Rows|541,909|534,129|7,780 rows removed (98.56% kept)|
|Missing Values|136,534 (25.19%)|132,565 (24.82%)|3,969 missing values handled|
|Duplicates|5,268|0|100% removed|
|Invalid Prices|2,512|0|100% removed|
|Memory Usage|173.13 MB|64.71 MB|108.42 MB saved (62.6% reduction)|
|Date Format|Mixed/Inconsistent|Standardized (datetime)|100% consistent|
|Column Names|Mixed case|snake_case|100% standardized|

---

## DETAILED ISSUE BREAKDOWN

### 1. Missing Values

|Column|Missing Count|% Missing|Action|Method Rationale|
|---|---|---|---|---|
|CustomerID|135,080|24.93%|Filled with 0 / Dropped|Created 2 versions: Sales (keep all) & Customer Analytics (keep only IDs)|
|Description|1,454|0.27%|Filled with "Unknown"|Only 0.27% missing; "Unknown" clearly indicates missing data|

### 2. Duplicate Records

|Type|Count|Action|Impact|
|---|---|---|---|
|Exact Duplicate Rows|5,268|Removed|Prevented overcounting of transactions|

### 3. Invalid Entries

|Issue|Count|Action|Business Meaning|
|---|---|---|---|
|Zero Quantity|0|Removed|No business value|
|Invalid Unit Price (≤ 0)|2,512|Removed|Data entry errors or adjustments|
|Negative Quantity (Returns)|10,587|Preserved|Valid return/cancellation transactions|
|Cancelled Invoices|9,251|Flagged|Invoices starting with 'C' - exclude from revenue|

### 4. Standardization Applied

|Component|Original Format|Standardized Format|Benefit|
|---|---|---|---|
|InvoiceDate|"12/1/2010 8:26"|datetime64[us]|Time-series analysis, sorting, trend detection|
|Description|Mixed case with spaces|UPPERCASE, stripped spaces|Consistent text matching|
|Country|Mixed case|Title Case|Consistent grouping|
|Column Names|PascalCase (InvoiceNo)|snake_case (invoice_no)|Code readability|
|StockCode|Object|Category|Memory optimization (categorical)|
|Description|Object|Category|Memory optimization (categorical)|
|Country|Object|Category|Memory optimization (categorical)|

---

## ANALYSIS VERSIONS CREATED

|Version|Purpose|Shape|Key Features|
|---|---|---|---|
|**Version A: Customer Analytics**|RFM, Segmentation, CLV|401,564 × 15|Only rows with CustomerID; 4,371 unique customers|
|**Version B: Sales Analytics**|Sales trends, Products, Revenue|534,129 × 15|All transactions; missing CustomerID filled with 0|
|**Version C: Returns Analytics**|Returns, Quality issues|9,251 × 15|Only return transactions (negative quantity)|
|**Version D: Revenue Analytics**|Accurate revenue calculation|524,878 × 15|Excludes cancelled invoices|

---

## VALIDATION RESULTS

|Validation Check|Status|Finding|
|---|---|---|
|Missing Values|✅ Complete|All missing values handled|
|Duplicates|✅ Complete|5,268 duplicates removed|
|Data Types|✅ Optimized|3 columns converted to categorical|
|Date Format|✅ Standardized|All dates in datetime format|
|Text Case|✅ Standardized|Consistent UPPERCASE and Title Case|
|Column Names|✅ Standardized|Snake_case applied|
|Invalid Prices|✅ Removed|2,512 rows removed|
|Zero Quantity|✅ None|No zero quantity rows found|
|Outliers|✅ Flagged|4,789 high-price outliers identified|
|Cancelled Invoices|✅ Flagged|9,251 rows flagged for separate analysis|

---

## 💾 MEMORY OPTIMIZATION SUMMARY

|Component|Before|After|Savings|
|---|---|---|---|
|Memory Usage|173.13 MB|64.71 MB|108.42 MB (62.6%)|
|Data Types Optimized|Object types|Categorical types|Memory reduced|

---

## KEY INSIGHTS FROM CLEANING

1. **Significant Missing Customer Data**: 24.93% missing requires careful handling depending on analysis goals
2. **Valid Returns Identified**: 10,587 transactions (1.95%) are returns - valuable for customer behavior analysis
3. **Substantial Memory Improvement**: 62.6% memory reduction through data type optimization
4. **Clean Dataset Achieved**: From 541,909 rows with issues to 534,129 rows fully cleaned
5. **Multiple Analysis Ready**: 4 versions created for different business questions

# EDA FINDINGS
### Netflix Dataset — Key Findings

- **Content mix:** Movies make up 69.6% of the catalog, while TV shows account for the remaining 30.4%.
- **Growth trend:** The number of titles added to Netflix began trending upward in 2015, continued growing through 2020, and has been declining since.
- **Top content producers:** The USA leads content production by a wide margin, followed by India and the UK.
- **Rating distribution:** TV-MA is the most common rating, indicating a strong focus on mature audience content.
- **Top genre:** International Movies is the most represented genre in the catalog.

---

### Retail Dataset — Key Findings

- **Top-selling products:** Products like "Paper Craft, Little Birdie" ranked among the top 10 best-sellers by volume.
- **Revenue by country:** The UK dominates all other countries in total revenue generated.
- **Seasonal trend:** Sales show an upward trend through August, followed by a decline starting in November.
- **Best-selling product by order count:** The "White Hanging Heart T-Light Holder" was the most frequently purchased product by number of orders.
- **Customer segmentation:** There's a small group of high-value, high-frequency customers alongside a much larger group of low-spend, occasional buyers.

Linkedin post: [Week 1&2](https://www.linkedin.com/posts/chacha-marwa-dev-355394257_dataanalytics-dataengineering-datacleaning-share-7480813507412836352-_F1F/?utm_source=share&utm_medium=member_desktop&rcm=ACoAAD89CfEBNsxI5MZDtHou_-KbuyNL-oBOBWg)
