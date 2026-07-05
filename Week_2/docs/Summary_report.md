# Netflix data

## Handling missing values
- director (**2634** missing - 29.91%) - Deleting rows would lose too much data. Using *Unknown* preserves the record
- country (**831** missing - 9.44%) - Replaced with *Unknown*
- cast (**825** missing - 9.37%) - Replaced with *Not Available*
- date_added (10 missing - 0.11%) - Dropping was cleaner
- rating (4 missing - 0.05%) - Dropped the 4 rows
- duration (3 missing - 0.03%) - Dropped the 3 rows

## Duplicate records
No duplicate rows were found

# Challenges
```python
FileNotFoundError: [Errno 2] No such file or directory: '../Week_1/data/netflix_titles.csv'
```
- I set working directory as root using chdir