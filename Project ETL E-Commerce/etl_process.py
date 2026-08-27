import pandas as pd
import re

print("Membaca Data...")
df = pd.read_csv('data_kotor.csv')
print("Data Awal:")
print(df)
print("-" * 50)

print ("Memulai proses pembersihan data...")

df = df.drop_duplicates()

df['nama_pelanggan'] = df['nama_pelanggan'].fillna('Tidak Diketahui')

df['harga'] = df['harga'].astype(str).str.replace(r'\D', '', regex=True)
df['harga'] = pd.to_numeric(df['harga'])
df = df[df['harga']>10000]

df['tanggal'] = pd.to_datetime(df['tanggal'], format='mixed')

print("\nData setelah dibersihkan:")
print(df)
print("-" * 50)
print("\nTipe data saat ini:")
print(df.dtypes)