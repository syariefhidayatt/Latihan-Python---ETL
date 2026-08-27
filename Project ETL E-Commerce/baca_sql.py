import sqlite3
import pandas as pd

print("menghubungkan ke database...")
koneksi = sqlite3.connect('database_ecommerce.db')

query = "select * from transaksi_bersih"

df_dari_sql = pd.read_sql(query, koneksi)

koneksi.close()

print("\n=== Data dari database sql===")
print(df_dari_sql)