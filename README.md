# Proyek Analisis data
melakukan analisis data dari https://github.com/marceloreis/HTI/tree/master (akses tanggal 10 april 2026 19:00)

## Cara Menjalankan

### 1. Install Python 3.11 (jika belum terinstall)
bash
winget install Python.Python.3.11

### 2. Uninstall library lama (disarankan agar tidak ada conflict)
bash
pip uninstall -r requirements.txt -y

### 3. Install semua dependency
bash
pip install -r requirements.txt

### 4. Jalankan dashboard
bash
streamlit run dashboard.py

### 5. Buka di browser
Setelah perintah di atas dijalankan, Streamlit akan otomatis membuka browser. Jika tidak terbuka, akses manual di:

http://localhost:8501

## Struktur Folder
├── chart/
│   ├── analisis_1_perencana_...png
│   ├── analisis_2_logistik.png
│   └── analisis_3_asuransi.png
│
├── dashboard/
│   ├── dashboard.py
│   ├── requirements.txt
│   └── runtime.txt
│
├── output_analisis_lanjutan/
│   ├── maps/
│   │   └── M3_geospatial_pm2...html
│   └── plots/
│       ├── M2_manual_groupin...png
│       ├── M3_geospatial_stati...png
│       └── M4_binning_aqi.png
│
├── source/
│   └── dirty/
        ├── PRSA_Data_Aotizhongxin_20130301-20170228.csv
        ├── PRSA_Data_Changping_20130301-20170228.csv
        ├── PRSA_Data_Dingling_20130301-20170228.csv
        ├── PRSA_Data_Dongsi_20130301-20170228.csv
        ├── PRSA_Data_Guanyuan_20130301-20170228.csv
        ├── PRSA_Data_Gucheng_20130301-20170228.csv
        ├── PRSA_Data_Huairou_20130301-20170228.csv
        ├── PRSA_Data_Nongzhanguan_20130301-20170228.csv
        ├── PRSA_Data_Shunyi_20130301-20170228.csv
        ├── PRSA_Data_Tiantan_20130301-20170228.csv
        ├── PRSA_Data_Wanliu_20130301-20170228.csv
        └── PRSA_Data_Wanshouxigong_20130301-20170228.csv
│
├── .gitignore
├── how_to_run.txt
├── Proyek_Analisis_Data.ipynb
├── README.md
├── requirements.txt
└── link.txt

## Requirements

streamlit
streamlit_folium==0.27.1
pandas==2.2.3
matplotlib==3.9.4
seaborn==0.13.2
numpy==2.2.6
folium==0.20.0

## Troubleshooting

| Masalah | Solusi |
|---------|--------|
| `ModuleNotFoundError` | Jalankan ulang `pip install -r requirements.txt` |
| `FileNotFoundError` CSV | Pastikan folder `source/dirty/` berisi 12 file CSV |
| Port 8501 sudah dipakai | Jalankan `streamlit run dashboard.py --server.port 8502` |
| Browser tidak terbuka otomatis | Buka manual `http://localhost:8501` |
| Tampilan tidak update | Tekan `R` di terminal atau `Ctrl+C` lalu jalankan ulang |

## Informasi Proyek

| | |
|-|-|
| **Nama** | M Ns |
| **Email** | cdcc325d6y0626@student.devacademy.id |
| **Dataset** | PRSA Multi-Site Air Quality, Beijing 2013–2017 |
| **Sumber** | [UCI Machine Learning Repository](https://archive.ics.uci.edu/dataset/501/beijing+multi+site+air+quality+data) |