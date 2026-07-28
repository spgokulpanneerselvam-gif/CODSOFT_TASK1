import os
import re
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd
import requests
import seaborn as sns
from bs4 import BeautifulSoup


BASE_DIR = Path(__file__).resolve().parent
DATASET_PATH = BASE_DIR / "products.csv"
IMAGES_DIR = BASE_DIR / "images"


def fetch_page(url: str) -> str:
    """Fetch HTML content for a given URL."""
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers, timeout=15)
    response.raise_for_status()
    return response.text


def parse_page(html: str) -> list[dict]:
    """Extract book data from the page HTML."""
    soup = BeautifulSoup(html, "html.parser")
    books = []

    for article in soup.select("article.product_pod"):
        title_tag = article.select_one("h3 a")
        title = title_tag["title"].strip() if title_tag and title_tag.has_attr("title") else None

        price_tag = article.select_one(".price_color")
        price = None
        if price_tag:
            price_text = price_tag.get_text(strip=True)
            price = float(re.sub(r"[^\d.]", "", price_text))

        rating_tag = article.select_one(".star-rating")
        rating = None
        if rating_tag:
            rating_class = rating_tag.get("class", [])
            rating_map = {
                "One": 1,
                "Two": 2,
                "Three": 3,
                "Four": 4,
                "Five": 5,
            }
            rating_name = next((cls for cls in rating_class if cls in rating_map), None)
            rating = rating_map.get(rating_name)

        availability_tag = article.select_one(".availability")
        availability = availability_tag.get_text(" ", strip=True) if availability_tag else None

        books.append(
            {
                "title": title,
                "price": price,
                "rating": rating,
                "availability": availability,
            }
        )

    return books


def scrape_books() -> pd.DataFrame:
    """Scrape all available pages from the bookstore website."""
    all_books = []
    page_number = 1

    while True:
        if page_number == 1:
            url = "https://books.toscrape.com/catalogue/page-1.html"
        else:
            url = f"https://books.toscrape.com/catalogue/page-{page_number}.html"

        html = fetch_page(url)
        page_books = parse_page(html)
        if not page_books:
            break

        all_books.extend(page_books)

        soup = BeautifulSoup(html, "html.parser")
        next_link = soup.select_one("li.next > a")
        if not next_link:
            break

        page_number += 1

    df = pd.DataFrame(all_books)
    return df


def clean_dataset(df: pd.DataFrame) -> pd.DataFrame:
    """Clean the extracted dataset by handling missing values and formatting fields."""
    cleaned = df.copy()
    cleaned["title"] = cleaned["title"].astype(str).str.strip()
    cleaned["price"] = pd.to_numeric(cleaned["price"], errors="coerce")
    cleaned["rating"] = pd.to_numeric(cleaned["rating"], errors="coerce")
    cleaned["availability"] = cleaned["availability"].fillna("Unknown").astype(str).str.strip()

    cleaned = cleaned.dropna(subset=["title"]).reset_index(drop=True)
    cleaned["availability_status"] = cleaned["availability"].str.contains("In stock", case=False, na=False)
    cleaned["availability_status"] = cleaned["availability_status"].map({True: "In stock", False: "Out of stock"})
    cleaned["rating"] = cleaned["rating"].fillna(0).astype(int)

    return cleaned


def save_charts(df: pd.DataFrame) -> None:
    """Create and save all requested visualizations."""
    IMAGES_DIR.mkdir(exist_ok=True)
    sns.set_theme(style="whitegrid")

    plt.figure(figsize=(8, 5))
    sns.histplot(df["price"], bins=20, kde=True)
    plt.title("Price Distribution")
    plt.xlabel("Price (£)")
    plt.ylabel("Frequency")
    plt.tight_layout()
    plt.savefig(IMAGES_DIR / "price_distribution.png")
    plt.close()

    plt.figure(figsize=(8, 5))
    rating_counts = df["rating"].value_counts().sort_index()
    sns.barplot(x=rating_counts.index, y=rating_counts.values, hue=rating_counts.index, legend=False, palette="viridis")
    plt.title("Rating Distribution")
    plt.xlabel("Rating (1-5)")
    plt.ylabel("Count")
    plt.tight_layout()
    plt.savefig(IMAGES_DIR / "rating_distribution.png")
    plt.close()

    plt.figure(figsize=(8, 5))
    availability_counts = df["availability_status"].value_counts()
    sns.barplot(x=availability_counts.index, y=availability_counts.values, hue=availability_counts.index, legend=False, palette="magma")
    plt.title("Availability Count")
    plt.xlabel("Availability")
    plt.ylabel("Count")
    plt.tight_layout()
    plt.savefig(IMAGES_DIR / "availability.png")
    plt.close()


def print_summary(df: pd.DataFrame) -> None:
    """Print a brief EDA summary for the scraped dataset."""
    print("\nDataset Preview:")
    print(df.head(5))

    print("\nMissing values:")
    print(df.isnull().sum())

    print("\nEDA Summary:")
    print(f"Total number of books scraped: {len(df)}")
    print(f"Average price: £{df['price'].mean():.2f}")
    most_common_rating = df["rating"].mode().iloc[0] if not df["rating"].mode().empty else "N/A"
    print(f"Most common rating: {most_common_rating}")
    in_stock_count = int((df["availability_status"] == "In stock").sum())
    print(f"Number of books in stock: {in_stock_count}")

    print("\nPrice statistics:")
    print(df["price"].describe())


def main() -> None:
    """Run the full scraping, cleaning, export, and visualization workflow."""
    print("Scraping books from Books to Scrape...")
    df = scrape_books()

    if df.empty:
        raise RuntimeError("No books were scraped. Please check the website connection.")

    print("Cleaning and preparing the dataset...")
    df = clean_dataset(df)

    print("Saving CSV data...")
    df.to_csv(DATASET_PATH, index=False)

    print("Generating charts...")
    save_charts(df)

    print("Displaying the first 5 rows...")
    print_summary(df)

    print(f"\nResults saved to {DATASET_PATH}")
    print(f"Charts saved in {IMAGES_DIR}")


if __name__ == "__main__":
    main()
