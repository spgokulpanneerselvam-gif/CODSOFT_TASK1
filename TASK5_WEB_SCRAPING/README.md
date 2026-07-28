# Web Scraping Analysis Project

This project scrapes book data from [Books to Scrape](https://books.toscrape.com/) and stores the results in a CSV file for analysis.

## What the script does
- Fetches the website using the `requests` library.
- Parses HTML with `BeautifulSoup`.
- Extracts book title, price, star rating, and availability.
- Stores the results in a Pandas DataFrame.
- Saves the data to `products.csv`.
- Generates charts for price, rating, and availability and saves them in the `images` folder.

## How to run
From the project folder, run:

```bash
python web_scraping_analysis.py
```

## Output files
- `products.csv`
- `images/price_distribution.png`
- `images/rating_distribution.png`
- `images/availability.png`
