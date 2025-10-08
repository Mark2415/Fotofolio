# Fungsi/Bobot.py
import numpy as np
import pandas as pd
import streamlit as st

# Rasio Indeks Konsistensi (RI) dari Saaty
RI_TABLE = {
    1: 0, 2: 0, 3: 0.58, 4: 0.90, 5: 1.12, 
    6: 1.24, 7: 1.32, 8: 1.41, 9: 1.45, 10: 1.49,
    11: 1.51, 12: 1.48, 13: 1.56, 14: 1.57, 15: 1.59
}

def hitung_bobot_ahp(matriks_perbandingan):
    """
    Menghitung bobot kriteria dari matriks perbandingan berpasangan menggunakan metode AHP.
    Fungsi ini juga melakukan pengecekan konsistensi.
    """
    st.subheader("Langkah 1: Normalisasi Matriks Perbandingan dan Hitung Bobot")
    
    # Konversi ke numpy array
    matriks = np.array(matriks_perbandingan, dtype=float)
    n = matriks.shape[0]

    # Menjumlahkan setiap kolom
    sum_of_cols = np.sum(matriks, axis=0)
    st.write("Jumlah setiap kolom:")
    st.dataframe(pd.DataFrame(sum_of_cols.reshape(1, -1), columns=matriks_perbandingan.columns, index=['Total']))

    # Normalisasi matriks
    matriks_normalisasi = matriks / sum_of_cols
    st.write("Matriks Ternormalisasi (setiap elemen dibagi dengan total kolomnya):")
    st.dataframe(pd.DataFrame(matriks_normalisasi, columns=matriks_perbandingan.columns, index=matriks_perbandingan.index))

    # Menghitung bobot (rata-rata setiap baris)
    bobot = np.mean(matriks_normalisasi, axis=1)
    st.write("Bobot Prioritas Kriteria (rata-rata dari setiap baris matriks ternormalisasi):")
    st.dataframe(pd.DataFrame(bobot, index=matriks_perbandingan.index, columns=['Bobot']))

    st.subheader("Langkah 2: Uji Konsistensi")
    # Menghitung Lambda Max
    weighted_sum_vector = np.dot(matriks, bobot)
    lambda_max_vector = weighted_sum_vector / bobot
    lambda_max = np.mean(lambda_max_vector)
    
    st.write(r"Menghitung $\lambda_{max}$")
    st.latex(r''' \lambda_{max} = \frac{1}{n} \sum_{i=1}^{n} \frac{(A \cdot w)_i}{w_i} ''')
    st.write(f"Nilai $\lambda_{max}$ = **{lambda_max:.4f}**")
    
    # Menghitung Indeks Konsistensi (CI)
    st.write("Menghitung Consistency Index (CI)")
    st.latex(r''' CI = \frac{\lambda_{max} - n}{n - 1} ''')
    ci = (lambda_max - n) / (n - 1)
    st.write(f"CI = ({lambda_max:.4f} - {n}) / ({n} - 1) = **{ci:.4f}**")

    # Mendapatkan Rasio Indeks (RI)
    st.write("Mendapatkan Random Index (RI) dari Tabel")
    if n not in RI_TABLE:
        st.warning(f"Tidak ada nilai RI standar untuk n={n}. Uji konsistensi tidak dapat diselesaikan.")
        return bobot, False
    
    ri = RI_TABLE[n]
    st.write(f"Untuk n = {n}, nilai RI adalah **{ri}**")

    # Menghitung Rasio Konsistensi (CR)
    st.write("Menghitung Consistency Ratio (CR)")
    st.latex(r''' CR = \frac{CI}{RI} ''')
    if ri == 0:
        cr = 0 # Asumsi konsisten jika n=1 atau n=2
    else:
        cr = ci / ri
    st.write(f"CR = {ci:.4f} / {ri} = **{cr:.4f}**")

    # Pengecekan hasil
    if cr < 0.10:
        st.success(f"Rasio Konsistensi (CR) adalah {cr:.4f}, yang berada di bawah 0.10. Matriks perbandingan Anda KONSISTEN. ✅")
        is_consistent = True
    else:
        st.error(f"Rasio Konsistensi (CR) adalah {cr:.4f}, yang melebihi 0.10. Matriks perbandingan Anda TIDAK KONSISTEN. ❌")
        st.warning("Mohon perbaiki nilai-nilai dalam matriks perbandingan berpasangan Anda.")
        is_consistent = False

    return bobot, is_consistent