"""

import sqlite3
import os
import requests
import pdfplumber

# Veritabanı dosyası ve hedef klasör adı
DB_FILE = "exhibit_files_urls.db"
DOWNLOAD_FOLDER = "downloaded_files"
TEXT_DB_FILE = "extracted_text.db"



# Yeni veritabanını oluşturma ve tabloyu tanımlama
def create_text_db():
    conn = sqlite3.connect(TEXT_DB_FILE)
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS extracted_text (ticker TEXT, pdf_text TEXT)")
    conn.commit()
    conn.close()

# Text verisini yeni veritabanına kaydetme
def save_text_to_db(ticker, pdf_text):
    conn = sqlite3.connect(TEXT_DB_FILE)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO extracted_text VALUES (?, ?)", (ticker, pdf_text))
    conn.commit()
    conn.close()


# Veritabanından URL'leri ve ilgili ticker'ları çekme
def download_and_read_pdfs(urls_with_tickers):
    if not os.path.exists(DOWNLOAD_FOLDER):
        os.makedirs(DOWNLOAD_FOLDER)

    for ticker, url in urls_with_tickers:
        try:
            # Önce dosyayı indir ve PDF metinini çıkar
            response = requests.get(url)
            response.raise_for_status()

            file_name = f"{ticker}_{url.split('/')[-1]}"
            file_path = os.path.join(DOWNLOAD_FOLDER, file_name)

            with open(file_path, "wb") as file:
                file.write(response.content)

            print(f"{file_name} downloaded successfully at {file_path}")

            # PDF dosyasını metin olarak okuma
            with pdfplumber.open(file_path) as pdf:
                pdf_text = ""
                for page in pdf.pages:
                    pdf_text += page.extract_text()

                # PDF metnini işleme veya kaydetme yapabilirsiniz
                print(f"Text extracted from {file_name}:\n{pdf_text}")

                # PDF metnini yeni veritabanına kaydet
                save_text_to_db(ticker, pdf_text)

        except (requests.exceptions.RequestException, pdfplumber.PDFSyntaxError) as e:
            print(f"An error occurred while processing {url}: {e}")


if __name__ == "__main__":
    urls_with_tickers = get_urls_with_tickers_from_database()
    try:
        create_text_db()  # Yeni veritabanını oluştur
    except Exception as e:
        print("An error occurred while creating text database:", e)
    download_and_read_pdfs(urls_with_tickers)

"""