import sqlite3
import requests
import pdfplumber
import os

print("selin ceren canbulut")
# İlk olarak exhibit_file_urls'de yer alan verileri indirip bir listeye kaydediyorum.
def extract_data():
    connection = sqlite3.connect("exhibit_file_urls.db")
    cursor = connection.cursor()
    table_name = "exhibit_file_url"
    cursor.execute(f"SELECT ticker, url FROM {table_name}")
    url_ticker_list = cursor.fetchall()
    connection.close()
    print(url_ticker_list)
    return url_ticker_list

extract_data()

"""

def create_download_files_db():
    db = sqlite3.connect("extracted_text.db")
    cursor = db.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS extracted_text (ticker TEXT, pdf_text TEXT)")
    db.commit()
    db.close()

def save_text_to_db(ticker, pdf_text):
    conn = sqlite3.connect("extracted_text.db")
    cursor = text.cursor()
    cursor.execute("INSERT INTO extracted_text VALUES (?, ?)", (ticker, pdf_text))
    conn.commit()
    conn.close()

def download_data():
    create_download_files_db()
    url_ticker_list = extract_data()
    for ticker, url in url_ticker_list:
        response = requests.get(url)
        try:
            if response.status_code == 200:
                pdf_text = ""
                with pdfplumber.open(response.content) as pdf:
                    for page in pdf.pages:
                        pdf_text += page.extract_text()
                        print(pdf_text)
                save_text_to_db(ticker, pdf_text)
        except:
            print(f"Response status code for {url} is not equal to 200")


if __name__ == "__main__":
    download_data()
"""



