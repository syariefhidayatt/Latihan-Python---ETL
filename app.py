from flask import Flask, request
import pandas as pd
import re
import sqlite3
import plotly.express as px

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def halaman_utama():
    if request.method == 'POST':
        file = request.files['file_csv']
        
        if file.filename == '':
            return 'Kamu belum memilih file apapun!'
        try:
            df = pd.read_csv(file)
            df = df.drop_duplicates()
            df['nama_pelanggan'] = df['nama_pelanggan'].fillna('nama pelanggan tidak diketahui')
            df['harga'] = df['harga'].astype(str).str.replace(r'\D', '', regex=True)
            df['harga'] = pd.to_numeric(df['harga'])
            df = df[df['harga'] > 1000]
            df['tanggal'] = pd.to_datetime(df['tanggal'], format='mixed')

            koneksi = sqlite3.connect('database_ecommerce.db')
            df.to_sql('transaksi_bersih', koneksi, if_exists='append', index=False)
            koneksi.close()

            df_summary= df.groupby('kategori')['harga'].sum().reset_index()

            grafik = px.bar(
                df_summary,
                x='kategori',
                y='harga',
                title='Total pendapatan per kategori barang',
                labels={'kategori': 'kategori barang', 'harga': 'Total pendapatan (Rp)'},
                color='kategori'
            )
            grafik.update_layout(yaxis_tickformat=',')

            grafik_html = grafik.to_html(full_html=False)
            tabel_html = df.to_html(index=False, border=1)

            return f'''
                <h2>Sukses! Data berhasil dibersihkan</h2>
                <p>File asal: <b>{file.filename}</b></p>
                <hr>
                <div>{grafik_html}</div>
                <h3>Hasil data yang sudah rapih:</h3>
                {tabel_html}
                <br>
                <a href="/">Kembali ke Home</a>
            '''
        except Exception as e:
              return f"Terjadi kesalahan saat memproses data: {e}"

    return '''
        <h1>Aplikasi ETL E-Commerce</h1>
        <p>Silakan upload file CSV kotor kamu di bawah ini:</p>
        
        <form method="POST" enctype="multipart/form-data">
            <input type="file" name="file_csv" accept=".csv">
            <br><br>
            <input type="submit" value="Upload dan Proses Data">
        </form>
    '''

if __name__ == '__main__':
    app.run(debug=True)