# Fungsi/AHP.py
import pandas as pd
import streamlit as st

def hitung_ahp_ranking(data_alternatif, bobot, tipe_kriteria):
    """Menghitung peringkat menggunakan metode AHP."""
    st.header("Metode Analytic Hierarchy Process (AHP)")
    
    data_normalisasi = data_alternatif.copy()
    
    st.subheader("Langkah 1: Normalisasi Matriks Keputusan (R)")
    st.write("Rumus Normalisasi:")
    st.latex(r'''r_{ij} = \frac{a_{ij}}{\sum_{k=1}^{n} a_{kj}} ''')
    
# Menghitung jumlah dari setiap kolom kriteria
    column_sums = data_alternatif.sum()
    # Melakukan normalisasi dengan membagi setiap elemen dengan jumlah kolomnya
    data_normalisasi = data_alternatif.div(column_sums)
    # --- AKHIR BAGIAN YANG DIUBAH ---
            
    st.write("Matriks Ternormalisasi:")
    st.dataframe(data_normalisasi)

    st.subheader("Langkah 2: Menghitung Nilai Preferensi (V)")
    st.write("Nilai preferensi untuk setiap alternatif dihitung dengan menjumlahkan hasil perkalian antara matriks ternormalisasi dengan vektor bobot.")
    st.latex(r''' V_i = \sum_{j=1}^{n} w_j r_{ij} ''')

    hasil_akhir = data_normalisasi.dot(bobot)
    # Mempertahankan index (primary key) dari data asli
    hasil_df = pd.DataFrame(hasil_akhir, columns=['Nilai Akhir'], index=data_alternatif.index)
    
    hasil_df['Peringkat'] = hasil_df['Nilai Akhir'].rank(ascending=False, method='min').astype('Int64')
    st.write("Hasil Akhir dan Peringkat:")
    st.dataframe(hasil_df.sort_values(by='Peringkat'))
    
    return hasil_df