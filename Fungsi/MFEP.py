# Fungsi/MFEP.py
import pandas as pd
import streamlit as st

def hitung_mfep(data_alternatif, bobot, tipe_kriteria=None):
    """Menghitung peringkat menggunakan metode MFEP."""
    st.header("Metode Multi-Factor Evaluation Process (MFEP)")
    st.info("Catatan: Proses MFEP secara matematis identik dengan SAW. Perbedaannya terletak pada terminologi, di mana bobot disebut 'Bobot Faktor' dan data alternatif disebut 'Skor Evaluasi'.")

    st.subheader("Langkah 1: Menghitung Skor Tertimbang")
    st.write("Skor setiap kriteria dikalikan dengan bobot faktor yang sesuai.")
    st.latex(r''' \text{Skor Total}_i = \sum_{j=1}^{n} (\text{Bobot Faktor}_j \times \text{Skor Evaluasi}_{ij}) ''')
    
    # Prosesnya sama persis dengan SAW, tanpa normalisasi eksplisit
    # karena skor evaluasi (data_alternatif) diasumsikan sudah dalam skala yang sama.
    # Jika tidak, normalisasi seperti SAW harus dilakukan terlebih dahulu.
    # Untuk kesederhanaan, kita anggap ini adalah weighted sum langsung.
    
    hasil_akhir = data_alternatif.dot(bobot)
    #Mempertahankan index (primary key) dari data asli
    hasil_df = pd.DataFrame(hasil_akhir, columns=['Nilai Akhir'], index=data_alternatif.index)
    
    hasil_df['Peringkat'] = hasil_df['Nilai Akhir'].rank(ascending=False, method='min').astype('Int64')
    st.write("Hasil Akhir dan Peringkat:")
    st.dataframe(hasil_df.sort_values(by='Peringkat'))
    
    return hasil_df