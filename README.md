# Job Offers ETL Pipeline

A Python ETL (Extract, Transform, Load) pipeline that collects job listings from the [Arbeitnow API](https://arbeitnow.com/api/job-board-api), cleans and structures the data, and loads it into a normalized SQLite database.

This project is Project 2 of a personal 8-project roadmap to build hands-on data engineering skills, following on from a simpler API data collection project.

## What it does

**Extract**
- Collects job offers from the Arbeitnow public API, handling pagination and network errors (reused from Project 1)

**Transform**
- Loads the raw JSON data into a Pandas DataFrame
- Converts Unix timestamps into readable dates
- Checks for missing values and duplicate offers
- Normalizes the data into 4 separate, related tables:
  - `companies` — unique company names
  - `offers` — job offers linked to a company via `company_id`
  - `tags` — unique tag/category names
  - `offer_tags` — a linking table representing the many-to-many relationship between offers and tags

**Load**
- Loads the 4 tables into a SQLite database (`job_offers.db`)
- Verifies the database with SQL queries using `JOIN`s across multiple tables

## Tech stack

- Python 3
- [`requests`](https://docs.python-requests.org/) — HTTP requests
- [`pandas`](https://pandas.pydata.org/) — data manipulation and transformation
- `sqlite3` — database creation and loading (standard library)
- `json` — JSON parsing (standard library)

## Database schema

```
companies (company_id, company)
    |
    | 1-to-many
    v
offers (offer_id, title, location, remote, created_at, url, company_id)
    |
    | many-to-many (via offer_tags)
    v
tags (tag_id, tag_name)
```

## How to run it

1. Clone this repository
2. Install the dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the collection script to fetch fresh data:
   ```bash
   python3 collect.py
   ```
4. Run the ETL pipeline to clean, transform, and load the data:
   ```bash
   python3 etl_pipeline.py
   ```
5. This generates `job_offers.json`, `job_offers.csv`, and `job_offers.db` in the project folder

## Example queries

Offers marked as remote, joined with their company:
```sql
SELECT offers.title, companies.company, offers.location
FROM offers
JOIN companies ON offers.company_id = companies.company_id
WHERE offers.remote = 1;
```

Offers with their associated tags (many-to-many relationship):
```sql
SELECT offers.title, tags.tag_name
FROM offers
JOIN offer_tags ON offers.offer_id = offer_tags.offer_id
JOIN tags ON offer_tags.tag_id = tags.tag_id;
```

## What I learned

- Structuring an ETL pipeline: separating extraction, transformation, and loading logic
- Using Pandas to inspect, clean, and transform tabular data (dtypes, missing values, duplicates)
- Converting Unix timestamps into readable dates
- Designing a normalized relational database schema to avoid data redundancy
- Handling a many-to-many relationship using a linking table (`.explode()` in Pandas to unnest list columns)
- Performing multi-table joins in Pandas (`.merge()`) and in SQL (`JOIN`)
- Loading DataFrames into a SQLite database with `.to_sql()`
- Writing and verifying SQL queries against the resulting database
