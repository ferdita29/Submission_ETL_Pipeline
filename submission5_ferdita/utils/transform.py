import pandas as pd
import re

EXCHANGE_RATE = 16000  # Nilai tukar USD ke IDR

def transform_data(data):
    """
    Membersihkan dan mengubah format data

    Proses transformasi mencakup:
    - Konversi Price ke mata uang rupiah
    - Mengubah Rating menjadi tipe data float
    - Mengubah Colors ke tipe data integer
    - Menghapus data duplikat dan data tidak valid

    Parameters:
    data (list of dict): Raw data hasil scraping

    Returns:
    pd.DataFrame: Data yang telah ditransformasi
    """
    try:
        df = pd.DataFrame(data).copy()

        if df.empty:
            print("Data kosong setelah scraping")
            return df

        # Memeriksa kolom yang diperlukan ada dalam data
        required_columns = {"Price", "Rating", "Colors"}
        if not required_columns.issubset(df.columns):
            missing_cols = required_columns - set(df.columns)
            print(f"Terdapat kolom yang tidak ditemukan: {missing_cols}")
            return pd.DataFrame()

        # Membersihkan baris dengan data tidak valid (seperti "Unknown Product", "Price Unavailable")
        df = df[~df['Price'].str.contains('Price Unavailable', na=False)]
        df = df[~df['Rating'].str.contains('Invalid Rating', na=False)]
        df = df[df['Title'] != 'Unknown Product']

        # Konversi Price menjadi Rupiah, pastikan hanya angka yang diproses
        df["Price"] = pd.to_numeric(df["Price"].str.replace('$', '', regex=False), errors='coerce')  # Menggunakan 'coerce' untuk menangani nilai yang tidak valid
        df["Price"] = df["Price"] * EXCHANGE_RATE

        # Mengubah Rating menjadi tipe data float dan menangani format yang tidak valid
        df["Rating"] = df["Rating"].apply(
            lambda x: float(re.search(r"(\d+(\.\d+)?)", str(x)).group()) if re.search(r"(\d+(\.\d+)?)", str(x)) else None
        )

        # Mengonversi Colors menjadi tipe data integer, jika tidak dapat dikonversi set ke 0
        df["Colors"] = pd.to_numeric(df["Colors"].apply(
            lambda x: re.search(r"\d+", str(x)).group() if re.search(r"\d+", str(x)) else None
        ), errors='coerce')

        # Hapus data yang tidak valid (NaN) di Rating, Colors, dan Price
        df.dropna(subset=["Rating", "Price", "Colors"], inplace=True)

        # Hapus data duplikat berdasarkan 'Title' untuk memastikan hanya produk unik
        df.drop_duplicates(subset=["Title"], keep="first", inplace=True)

        print("Proses transformasi selesai.")
        return df

    except Exception as e:
        print(f"Error saat proses transformasi: {e}")
        return pd.DataFrame()
