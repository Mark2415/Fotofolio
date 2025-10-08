# Fungsi/SAW.py
import pandas as pd
import streamlit as st

def hitung_saw(data_alternatif, bobot, tipe_kriteria):
    """Menghitung peringkat menggunakan metode SAW."""
    st.header("Metode Simple Additive Weighting (SAW)")
    
    data_normalisasi = data_alternatif.copy()
    
    st.subheader("Langkah 1: Normalisasi Matriks Keputusan (R)")
    st.write("Rumus Normalisasi:")
    st.latex(r''' r_{ij} = \begin{cases} \frac{x_{ij}}{\max(x_{ij})} & \text{jika j adalah atribut keuntungan (benefit)} \\ \frac{\min(x_{ij})}{x_{ij}} & \text{jika j adalah atribut biaya (cost)} \end{cases} ''')
    
    for i, kriteria in enumerate(data_alternatif.columns):
        if tipe_kriteria[i].lower() == 'benefit':
            max_val = data_alternatif[kriteria].max()
            data_normalisasi[kriteria] = data_alternatif[kriteria] / max_val
        elif tipe_kriteria[i].lower() == 'cost':
            min_val = data_alternatif[kriteria].min()
            data_normalisasi[kriteria] = min_val / data_alternatif[kriteria]
            
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