# Fungsi/baca_data.py
import pandas as pd
import streamlit as st

def baca_csv(file_uploader):
    """
    Membaca file CSV yang diunggah, dengan asumsi kolom pertama adalah indeks.
    Fungsi ini lebih kuat karena bisa mendeteksi pemisah (koma, titik koma, tab) secara otomatis
    dan menangani karakter BOM (Byte Order Mark) yang sering menyebabkan error.
    """
    try:
        if file_uploader is not None:
            # PERBAIKAN: Menambahkan encoding='utf-8-sig' untuk mengatasi error BOM
            df = pd.read_csv(file_uploader, index_col=0, sep=None, engine='python', encoding='utf-8-sig')
            st.success("File CSV berhasil dibaca!")
            return df
    except Exception as e:
        st.error(f"Terjadi kesalahan saat membaca file: {e}")
        st.warning("Pastikan file Anda berformat CSV dan kolom pertama adalah kolom indeks unik (contoh: 'Student No').")
        return None

def tampilkan_data_dengan_filter(df, title="Data"):
    """
    Menampilkan DataFrame di Streamlit dengan slider untuk memilih jumlah baris.
    """
    if df is not None and not df.empty:
        st.subheader(f"Pratinjau {title}")
        
        default_rows = min(5, len(df))
        
        jumlah_baris = st.slider(
            f"Pilih jumlah baris {title} yang ingin ditampilkan:",
            min_value=1,
            max_value=len(df),
            value=default_rows,
            key=f"slider_{title.lower().replace(' ', '_')}"
        )
        
        st.dataframe(df.head(jumlah_baris))
    else:
        st.info(f"{title} belum diunggah atau kosong.")