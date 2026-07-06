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