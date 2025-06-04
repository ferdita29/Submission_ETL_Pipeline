import pandas as pd
from utils.extract import scrape_all_pages
from utils.transform import transform_data
from utils.load import save_to_csv
from utils.load import save_to_postgresql
from utils.load import save_to_google_sheets
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError

# Memuat variabel lingkungan dari file .env
load_dotenv()

def save_to_postgresql(df, db_config):
    """Menyimpan DataFrame ke PostgreSQL"""
    try:
        # Membuat string koneksi menggunakan SQLAlchemy
        connection_string = f"postgresql://{db_config['user']}:{db_config['password']}@{db_config['host']}:{db_config['port']}/{db_config['dbname']}"
        engine = create_engine(connection_string)

        # Menyimpan DataFrame ke PostgreSQL
        df.to_sql('products_table', con=engine, if_exists='replace', index=False)
        print("\nData berhasil disimpan ke PostgreSQL.")

    except SQLAlchemyError as e:
        print(f"\nError saat menyimpan data ke PostgreSQL: {e}")
        raise

def main():
    """Main function untuk menjalankan seluruh proses ETL"""
    try:
        print("Memulai proses ETL...\n")

        # 1. Menjalankan Extract
        print("Menjalankan Extract...")
        raw_data = scrape_all_pages(start_page=1, end_page=50)  # Scraping data dari halaman 1 sampai 50
        
        if raw_data is None or len(raw_data) == 0:
            raise ValueError("Extract gagal: Tidak ada data yang ditemukan")

        print(f"Data yang diterima dari Extract (contoh):\n{raw_data[:5]}")  # Menampilkan beberapa produk pertama

        # 2. Menjalankan Transformasi
        print("\nMenjalankan Transformasi...")
        transformed_df = transform_data(raw_data)
        
        if transformed_df.empty:
            raise ValueError("Transformasi gagal: Tidak ada data valid")

        print(f"Data yang diterima setelah transformasi (contoh):\n{transformed_df.head()}")  # Menampilkan data yang sudah ditransformasi

        # 3. Menyimpan data
        print("\nMenyimpan data...")

        # Mendapatkan file output CSV dari file .env jika ada
        output_csv = os.getenv("OUTPUT_CSV", "products.csv")
        save_to_csv(transformed_df, output_csv)

        # Konfigurasi untuk menyimpan ke PostgreSQL
        db_config = {
            "dbname": os.getenv("DB_NAME", "db_fashion"),
            "user": os.getenv("DB_USER", "postgres"),
            "password": os.getenv("DB_PASSWORD", "290104"),
            "host": os.getenv("DB_HOST", "localhost"),
            "port": os.getenv("DB_PORT", "5432")
        }

        save_to_postgresql(transformed_df, db_config)

         # Mendapatkan kredensial dan spreadsheet ID 
        spreadsheet_id = "1nxXwrsQT8pC8IW62W37XfkN9HpcFdk29Hs2s7kp2jVU" 
        range_name = 'Sheet1!A1'
        save_to_google_sheets(transformed_df, spreadsheet_id, range_name)

        print("\nProses ETL selesai")

    except Exception as e:
        print(f"\nError dalam proses ETL: {e}")


if __name__ == "__main__":
    main()
