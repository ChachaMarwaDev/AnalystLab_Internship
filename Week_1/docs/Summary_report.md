<!-- Description of the Dataset -->
# Week 1 report
## Summary of shows.ipynb
Netflix Movies & TV Shows Dataset Summary
Overview
- Size: 8,807 records with 12 features, occupying approximately 8 MB of memory.
- Content: This dataset contains a list of movies and TV shows available on Netflix, with details about their content, cast, and metadata.

Column Breakdown
1. Text-heavy: The vast majority of columns (11 out of 12) contain text data, including:
2. Identifiers & Titles: show_id, title
3. Content Classification: type (Movie/TV Show), rating, listed_in (genres), description
4. People & Places: director, cast, country
5. Dates & Duration: date_added, duration
6. Only Numeric Column: release_year is the sole numeric feature.

Data Quality Concerns
Missing Data: There are 4,307 missing values, representing 4.1% of the entire dataset.
Affected Columns: Six columns contain missing entries:
1. director
2. cast
3. country
4. date_added
5. rating
6. duration

Key Insight: The missing values are concentrated in the descriptive and categorical columns, which may require imputation or careful handling for certain analyses.
Key Features Observed (from sample data)
Contains both Movies (e.g., "Dick Johnson Is Dead") and TV Shows (e.g., "Blood & Water", "Ganglands").

Attributes include:
- Content ratings (e.g., PG-13, TV-MA)
- Release years ranging at least from 2020–2021
- Country of production (e.g., United States, South Africa)
- Genres (e.g., Documentaries, International TV Shows)
- Duration (in minutes for movies, seasons for TV shows)

## Challenges
### Shows.ipynb
1. Loaded the data from the url but only scraped the HTML page note the actual csv file
    - I opted for the Kaggle api (Kagglehub) provides easier handling of files from the urls
2. Accesing and saving the csv to the data folder
    - I opted to go with the ../ going a level up the folder I am currently on

