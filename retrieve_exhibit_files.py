import requests
from sec_api import QueryApi
import pprint
import sqlite3
import copy
from dotenv import dotenv_values
import os

# Load environment variables from .env file to protect sensitive information. (SEC_API_KEY)
env_variables = dotenv_values(".env")

# Get SEC_API_KEY and ENDPOINT from environment variables.
SEC_API_ENDPOINT = env_variables.get("SEC_API_ENDPOINT")
SEC_API_KEY = env_variables.get("SEC_API_KEY")
print(SEC_API_KEY)
if SEC_API_KEY is None:
    raise ValueError("SEC_API_KEY environment variable is not set.")


#, "NKE", "AATC", "GTX", "MLRT"
COMPANIES = ["AMGN"]



# Function to fetch filing URLs and Ticker's from SEC API.
def get_filings_url(api_key, ticker):
    # Define query parameters for SEC filings search

    """
    query = {
        "query": {
                "query_string": {
                    "query": f"ticker:\"{ticker}\" AND filedAt:[1900-01-01 TO 2023-01-01] AND documentFormatFiles.type:\"EX-2\"",
                "time_zone": "America/New_York"
            }
        },
        "from": "0",
        "size": "500",
        "sort": [
            {
                "field": "filedAt",
                "order": "desc"
            }
        ]
    }
    """
    query = {
        "query": {"query_string": {
            "query": f"ticker:{ticker} AND filedAt:[1900-01-01 TO 2021-12-31] AND documentFormatFiles.type:\"EX-2\"",
            "time_zone": "America/New_York"
        }},
        "from": "0",
        "size": "10",
        "sort": [{"filedAt": {"order": "desc"}}]
    }

    pprint.pprint(query)

    try:
        query_api = QueryApi(api_key=api_key)

        response = query_api.get_filings(query)

        urls = []
        added_tickers = set()

        for filing in response.get("filings", []):
            ticker = filing.get("ticker")
            url = filing.get("filingUrl")

            if ticker and url and ticker not in added_tickers:
                urls.append({"ticker": ticker, "url": url})
                added_tickers.add(ticker)

        return urls
    except Exception as e:
        print("An error occurred while fetching filings:", e)
        return []


# Function to create SQLite database and table
def create_db():
    db = sqlite3.connect("exhibit_files_urls.db")
    cursor = db.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS exhibit_files_urls (ticker TEXT, url TEXT)")
    db.commit()
    db.close()


# Function to add values to SQLite database
def add_value_to_db(ticker, url):
    try:
        db = sqlite3.connect("exhibit_files_urls.db")
        cursor = db.cursor()
        cursor.execute("INSERT INTO exhibit_files_urls VALUES (?, ?)", (ticker, url))
        db.commit()
        db.close()
    except Exception as e:
        print("An error occurred while adding value to database:", e)


# Main function to process companies' filings
def process_companies(companies):
    create_db()
    for ticker in companies:
        try:
            urls = get_filings_url(SEC_API_KEY, ticker)

            if urls:
                data = urls[0]
                add_value_to_db(data["ticker"], data["url"])
        except Exception as e:
            print(f"An error occurred for company {ticker}:", e)




if __name__ == "__main__":
    process_companies(COMPANIES)