# Fungsi/WP.py
import pandas as pd
import numpy as np
import streamlit as st

def hitung_wp(data_alternatif, bobot, tipe_kriteria):
    """Menghitung peringkat menggunakan metode WP."""
    st.header("Metode Weighted Product (WP)")

    st.subheader("Langkah 1: Normalisasi Bobot")
    st.write("Bobot dinormalisasi sehingga totalnya menjadi 1.")
    bobot_normal = bobot / np.sum(bobot)
    st.write(bobot_normal)

    st.subheader("Langkah 2: Modifikasi Pangkat Sesuai Tipe Kriteria")
    st.write("Untuk kriteria 'cost', bobotnya diubah menjadi negatif.")
    pangkat = []
    for i, tipe in enumerate(tipe_kriteria):
        if tipe.lower() == 'cost':
            pangkat.append(-bobot_normal[i])
        else: # benefit
            pangkat.append(bobot_normal[i])
            
    pangkat_df = pd.DataFrame([pangkat], columns=data_alternatif.columns, index=['Pangkat (w)'])
    st.dataframe(pangkat_df)

    st.subheader("Langkah 3: Menghitung Vektor S")
    st.latex(r''' S_i = \prod_{j=1}^{n} x_{ij}^{w_j} ''')
    vektor_s = np.prod(data_alternatif.astype(float).pow(pangkat), axis=1)
    vektor_s_df = pd.DataFrame(vektor_s, columns=['Vektor S'])
    st.dataframe(vektor_s_df)

    st.subheader("Langkah 4: Menghitung Vektor V (Nilai Preferensi)")
    st.latex(r''' V_i = \frac{S_i}{\sum_{k=1}^{m} S_k} ''')
   
    vektor_v = vektor_s / np.sum(vektor_s)
    # Mempertahankan index (primary key) dari data asli
    hasil_df = pd.DataFrame(vektor_v, columns=['Nilai Akhir'], index=data_alternatif.index)
    
    hasil_df['Peringkat'] = hasil_df['Nilai Akhir'].rank(ascending=False, method='min').astype('Int64')
    st.write("Hasil Akhir dan Peringkat:")
    st.dataframe(hasil_df.sort_values(by='Peringkat'))
    
    return hasil_df