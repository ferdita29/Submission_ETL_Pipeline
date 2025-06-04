import pandas as pd
import psycopg2
from googleapiclient.discovery import build
from google.oauth2 import service_account

# Fungsi untuk menyimpan data ke file CSV
def save_to_csv(df, filename='products.csv'):
    """
    Fungsi untuk menyimpan DataFrame ke dalam file CSV.
    :param df: DataFrame yang berisi data produk
    :param filename: Nama file CSV untuk menyimpan data
    """
    try:
        df.to_csv(filename, index=False)  # Menyimpan data ke dalam CSV
        print(f"Data berhasil disimpan ke {filename}")
    except Exception as e:
        print(f"Terjadi kesalahan saat menyimpan data ke CSV: {e}")

# Fungsi untuk menyimpan data ke PostgreSQL
def save_to_postgresql(df, db_config, table_name="products"):
    """
    Fungsi untuk menyimpan DataFrame ke dalam PostgreSQL.
    :param df: DataFrame yang berisi data produk
    :param db_config: Konfigurasi koneksi ke PostgreSQL
    :param table_name: Nama tabel di PostgreSQL (default 'products')
    """
    try:
        # Membuat koneksi ke PostgreSQL
        conn = psycopg2.connect(**db_config)
        cursor = conn.cursor()

        # Membuat tabel jika belum ada
        create_table_query = f"""
        CREATE TABLE IF NOT EXISTS {table_name} (
            id SERIAL PRIMARY KEY,
            title TEXT,
            price FLOAT,
            rating FLOAT,
            colors INT,
            size TEXT,
            gender TEXT,
            timestamp TIMESTAMP,
        );
        """
        cursor.execute(create_table_query)
        conn.commit()

        # Menyimpan data ke tabel PostgreSQL
        for _, row in df.iterrows():
            cursor.execute(
                f"INSERT INTO {table_name} (title, price, rating, colors, size, gender, timestamp) "
                "VALUES (%s, %s, %s, %s, %s, %s, %s)",
                (row['Title'], row['Price'], row['Rating'], row['Colors'], row['Size'], row['Gender'], row['Timestamp'])
            )
        conn.commit()
        print(f"Data berhasil disimpan ke PostgreSQL ke tabel {table_name}")
    except Exception as e:
        print(f"Terjadi kesalahan saat menyimpan data ke PostgreSQL: {e}")
    finally:
        if conn:
            conn.close()


# Fungsi untuk menyimpan data ke Google Sheets
def save_to_google_sheets(df, spreadsheet_id, range_name, credentials_file='utils/google-sheets-api.json'):
    """
    Fungsi untuk mengupload DataFrame ke Google Sheets.
    :param df: DataFrame yang berisi data produk
    :param spreadsheet_id: ID dari spreadsheet Google Sheets
    :param range_name: Rentang tempat data akan dimasukkan (e.g., "Sheet1!A1")
    :param credentials_file: File JSON kredensial untuk Google Sheets API
    """
    if df.empty:
        print("Tidak ada data untuk diupload ke Google Sheets.")
        return

    try:
        # Membaca kredensial dari file JSON
        creds = service_account.Credentials.from_service_account_file(credentials_file)
        service = build('sheets', 'v4', credentials=creds)
        sheet = service.spreadsheets()

        # Mengonversi DataFrame menjadi list of lists untuk Google Sheets
        values = [df.columns.tolist()] + df.values.tolist()
        body = {'values': values}

        # Update data ke Google Sheets
        sheet.values().update(
            spreadsheetId=spreadsheet_id,
            range=range_name,
            valueInputOption="RAW",
            body=body
        ).execute()

        print(f"Data berhasil disimpan ke Google Sheets di {spreadsheet_id}")

    except FileNotFoundError:
        print(f"File kredensial {credentials_file} tidak ditemukan.")
    except Exception as e:
        print(f"Terjadi kesalahan saat mengupload data ke Google Sheets: {e}")