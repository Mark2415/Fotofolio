# Main.py
import streamlit as st
import pandas as pd
import numpy as np

# Impor fungsi dari folder Fungsi
from Fungsi import baca_data, Bobot, AHP, SAW, MFEP, WP

# --- Konfigurasi Halaman ---
st.set_page_config(
    page_title="Aplikasi SPK Interaktif",
    page_icon="📪",
    layout="wide"
)

# --- State Management ---
# Menggunakan st.session_state untuk menyimpan data antar render
if 'bobot_kriteria' not in st.session_state:
    st.session_state.bobot_kriteria = None
if 'data_alternatif' not in st.session_state:
    st.session_state.data_alternatif = None
if 'matriks_perbandingan' not in st.session_state:
    st.session_state.matriks_perbandingan = None
if 'tipe_kriteria' not in st.session_state:
    st.session_state.tipe_kriteria = None
    
# --- Tampilan Utama ---
st.title("Aplikasi Sistem Pendukung Keputusan (SPK) Interaktif")
st.write("Aplikasi ini membantu Anda mengambil keputusan dengan beberapa metode SPK populer.")

# --- Sidebar untuk Input ---
with st.sidebar:
    st.header("1. Pilihan Input Data")
    metode_input = st.radio(
        "Pilih cara memasukkan data:", 
        ("Manual", "Upload CSV"),
        key="metode_input_radio"
    )

    # Cek apakah mode input baru saja diganti oleh pengguna
    if 'current_mode' not in st.session_state:
        st.session_state.current_mode = metode_input

    if st.session_state.current_mode != metode_input:
        # Jika mode berganti, reset semua data relevan
        keys_to_reset = ['bobot_kriteria', 'data_alternatif', 'matriks_perbandingan', 'tipe_kriteria']
        for key in keys_to_reset:
            if key in st.session_state:
                del st.session_state[key]
        # Simpan mode yang baru dan jalankan ulang aplikasi dengan state bersih
        st.session_state.current_mode = metode_input
        st.rerun()


    # Inisialisasi state jika belum ada
    if 'bobot_kriteria' not in st.session_state:
        st.session_state.bobot_kriteria = None
    if 'data_alternatif' not in st.session_state:
        st.session_state.data_alternatif = None
    if 'matriks_perbandingan' not in st.session_state:
        st.session_state.matriks_perbandingan = None
    if 'tipe_kriteria' not in st.session_state:
        st.session_state.tipe_kriteria = None

    # Sisa kode untuk input data (sama seperti sebelumnya)
    if metode_input == "Upload CSV":
        st.subheader("Upload File CSV")
        file_perbandingan = st.file_uploader("Upload Matriks Perbandingan Kriteria (CSV)", type="csv", key="file_perbandingan_uploader")
        file_alternatif = st.file_uploader("Upload Data Skor Alternatif (CSV)", type="csv", key="file_alternatif_uploader")
        
        if file_perbandingan and file_alternatif:
            st.session_state.matriks_perbandingan = baca_data.baca_csv(file_perbandingan)
            st.session_state.data_alternatif = baca_data.baca_csv(file_alternatif)
            
            if st.session_state.matriks_perbandingan is not None and st.session_state.data_alternatif is not None:
                kriteria_names = st.session_state.matriks_perbandingan.columns.tolist()
                
                try:
                    st.session_state.data_alternatif = st.session_state.data_alternatif[kriteria_names]
                except KeyError as e:
                    st.error(f"Kolom di file Data Alternatif tidak cocok! Pastikan kolom berikut ada: {e}")
                    st.session_state.data_alternatif = None 
                
                if st.session_state.data_alternatif is not None:
                    st.success("Data Kriteria dan Alternatif cocok! ✅")
                    st.session_state.tipe_kriteria = [st.selectbox(f"Tipe untuk '{k}'", ["Benefit", "Cost"], key=f"tipe_{k}") for k in kriteria_names]
    
    else: # Input Manual
        st.subheader("Input Manual")
        jml_kriteria = st.number_input("Jumlah Kriteria", min_value=2, max_value=10, value=3, step=1)
        kriteria_names = [st.text_input(f"Nama Kriteria {i+1}", f"K{i+1}") for i in range(jml_kriteria)]
        
        st.write("**Matriks Perbandingan Berpasangan Kriteria (Skala Saaty 1-9)**")
        df_perbandingan = pd.DataFrame(np.ones((jml_kriteria, jml_kriteria)), columns=kriteria_names, index=kriteria_names)
        
        edited_df_perbandingan = st.data_editor(df_perbandingan, key="editor_perbandingan")
        
        for i in range(jml_kriteria):
            for j in range(i, jml_kriteria):
                if i == j:
                    edited_df_perbandingan.iloc[i, j] = 1.0
                else:
                    if edited_df_perbandingan.iloc[i, j] != 0:
                        try:
                            edited_df_perbandingan.iloc[j, i] = 1 / edited_df_perbandingan.iloc[i, j]
                        except ZeroDivisionError:
                            edited_df_perbandingan.iloc[j, i] = np.inf
        
        st.session_state.matriks_perbandingan = edited_df_perbandingan

        st.session_state.tipe_kriteria = [st.selectbox(f"Tipe untuk '{k}'", ["Benefit", "Cost"], key=f"tipe_{k}") for k in kriteria_names]

        jml_alternatif = st.number_input("Jumlah Alternatif", min_value=2, max_value=20, value=4, step=1)
        alternatif_names = [st.text_input(f"Nama Alternatif {i+1}", f"Alt {i+1}") for i in range(jml_alternatif)]

        st.write("**Data Skor Alternatif**")
        df_alternatif = pd.DataFrame(np.zeros((jml_alternatif, jml_kriteria)), index=alternatif_names, columns=kriteria_names)
        st.session_state.data_alternatif = st.data_editor(df_alternatif, key="editor_alternatif")
        
# --- Kolom Utama untuk Proses dan Hasil ---
col1, col2 = st.columns([1, 2])

with col1:
    st.header("2. Hitung Bobot Kriteria (AHP)")
    
    if st.session_state.bobot_kriteria is not None:
        st.header("3. Pilih Metode Ranking")
        # Menggunakan fungsi baru untuk menampilkan data dengan slider
        baca_data.tampilkan_data_dengan_filter(st.session_state.data_alternatif, "Data Alternatif")
    if st.button("Hitung Bobot"):
        with st.spinner("Menghitung bobot dan konsistensi..."):
            bobot, konsisten = Bobot.hitung_bobot_ahp(st.session_state.matriks_perbandingan)
            if konsisten:
                st.session_state.bobot_kriteria = bobot
            else:
                st.session_state.bobot_kriteria = None # Reset jika tidak konsisten
    else:
        st.info("Silakan masukkan data di sidebar terlebih dahulu.")

    if st.session_state.bobot_kriteria is not None:
        st.header("3. Pilih Metode Ranking")
        st.write("Data Alternatif:")
        st.dataframe(st.session_state.data_alternatif)
        
        metode_ranking = st.selectbox(
            "Pilih metode untuk mengambil keputusan:",
            ("AHP", "SAW", "MFEP", "WP")
        )
        
        if st.button("🧮 Hitung Peringkat"):
            st.session_state.metode_terpilih = metode_ranking
        
with col2:
    st.header("Hasil Analisis dan Peringkat")
    if 'metode_terpilih' in st.session_state and st.session_state.bobot_kriteria is not None:
        metode = st.session_state.metode_terpilih
        data_alt = st.session_state.data_alternatif
        bobot = st.session_state.bobot_kriteria
        tipe = st.session_state.tipe_kriteria
        
        if metode == "SAW":
            SAW.hitung_saw(data_alt, bobot, tipe)
        elif metode == "WP":
            WP.hitung_wp(data_alt, bobot, tipe)
        elif metode == "MFEP":
            MFEP.hitung_mfep(data_alt, bobot, tipe)
        elif metode == "AHP":
            AHP.hitung_ahp_ranking(data_alt, bobot, tipe)
    else:
        st.info("Silakan hitung bobot yang konsisten dan pilih metode ranking terlebih dahulu.")