import os
import warnings

import numpy as np
import pandas as pd
import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
import seaborn as sns
import folium
import streamlit as st
from folium.plugins import HeatMap
from streamlit_folium import st_folium

warnings.filterwarnings('ignore')

# ─────────────────────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────────────────────
# Konfigurasi halaman
# Set title halaman, layout, dan initial sidebar state
# Page title: judul title halaman
# Layout: wide/normal, wide jika ingin menggunakan lebar yang lebar
# Initial sidebar state: expanded/collapsed, expanded jika ingin membuat sidebar terbuka saat pertama kali dibuka
st.set_page_config(
    page_title="Beijing Air Quality Dashboard",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────────────────────
# CUSTOM CSS
# ─────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Sans:wght@300;400;500&display=swap');

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
}

/* Header */
.main-header {
    background: linear-gradient(135deg, #0f0c29, #302b63, #24243e);
    padding: 2.5rem 2rem;
    border-radius: 16px;
    margin-bottom: 2rem;
    position: relative;
    overflow: hidden;
}
.main-header::before {
    content: '';
    position: absolute;
    top: -50%;
    left: -50%;
    width: 200%;
    height: 200%;
    background: radial-gradient(circle at 30% 50%, rgba(99,179,237,0.15) 0%, transparent 50%),
                radial-gradient(circle at 70% 50%, rgba(236,72,153,0.1) 0%, transparent 50%);
}
.main-header h1 {
    font-family: 'Syne', sans-serif;
    font-weight: 800;
    font-size: 2.4rem;
    color: #ffffff;
    margin: 0;
    position: relative;
}
.main-header p {
    color: rgba(255,255,255,0.65);
    font-size: 0.95rem;
    margin: 0.4rem 0 0;
    position: relative;
}

/* Metric cards */
.metric-card {
    background: #ffffff;
    border: 1px solid #e8edf3;
    border-radius: 12px;
    padding: 1.2rem 1.4rem;
    box-shadow: 0 2px 8px rgba(0,0,0,0.06);
}
.metric-card .label {
    font-size: 0.78rem;
    color: #6b7280;
    font-weight: 500;
    letter-spacing: 0.05em;
    text-transform: uppercase;
}
.metric-card .value {
    font-family: 'Syne', sans-serif;
    font-size: 2rem;
    font-weight: 700;
    color: #111827;
    line-height: 1.1;
    margin-top: 0.2rem;
}
.metric-card .sub {
    font-size: 0.8rem;
    color: #9ca3af;
    margin-top: 0.15rem;
}

/* Section title */
.section-title {
    font-family: 'Syne', sans-serif;
    font-size: 1.3rem;
    font-weight: 700;
    color: white;
    border-left: 4px solid #3b82f6;
    padding-left: 0.75rem;
    margin: 1.5rem 0 1rem;
}

/* Badge */
.badge {
    display: inline-block;
    padding: 0.2rem 0.7rem;
    border-radius: 9999px;
    font-size: 0.75rem;
    font-weight: 600;
}
.badge-red    { background:#fee2e2; color:#b91c1c; }
.badge-orange { background:#ffedd5; color:#c2410c; }
.badge-yellow { background:#fef3c7; color:#b45309; }
.badge-green  { background:#d1fae5; color:#065f46; }

/* Insight box */
.insight-box {
    background: #f0f9ff;
    border-left: 4px solid #0ea5e9;
    border-radius: 0 10px 10px 0;
    padding: 1rem 1.25rem;
    margin: 1rem 0;
    font-size: 0.88rem;
    color: #0c4a6e;
    line-height: 1.6;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background: #0f172a;
}
[data-testid="stSidebar"] * {
    color: #e2e8f0 !important;
}
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────
# KONSTANTA
# ─────────────────────────────────────────────────────────────
DATA_DIR = "source/dirty"   # sesuaikan path

STATIONS = [
    'Aotizhongxin','Changping','Dingling','Dongsi',
    'Guanyuan','Gucheng','Huairou','Nongzhanguan',
    'Shunyi','Tiantan','Wanliu','Wanshouxigong',
]

STATION_COORDS = {
    'Aotizhongxin' : (39.9824, 116.3976),
    'Changping'    : (40.2149, 116.2310),
    'Dingling'     : (40.2900, 116.2200),
    'Dongsi'       : (39.9290, 116.4170),
    'Guanyuan'     : (39.9290, 116.3390),
    'Gucheng'      : (39.9140, 116.1840),
    'Huairou'      : (40.3280, 116.6280),
    'Nongzhanguan' : (39.9370, 116.4610),
    'Shunyi'       : (40.1270, 116.6550),
    'Tiantan'      : (39.8860, 116.4070),
    'Wanliu'       : (39.9870, 116.2870),
    'Wanshouxigong': (39.8780, 116.3520),
}

AQI_BINS   = [0, 12, 35.4, 55.4, 150.4, 250.4, float('inf')]
AQI_LABELS = ['Good','Moderate','Sensitive Groups','Unhealthy','Very Unhealthy','Hazardous']
AQI_COLORS = {
    'Good':'#00e400','Moderate':'#ffff00','Sensitive Groups':'#ff7e00',
    'Unhealthy':'#ff0000','Very Unhealthy':'#8f3f97','Hazardous':'#7e0023',
}

BULAN = {1:'Jan',2:'Feb',3:'Mar',4:'Apr',5:'Mei',6:'Jun',
         7:'Jul',8:'Agu',9:'Sep',10:'Okt',11:'Nov',12:'Des'}


# ─────────────────────────────────────────────────────────────
# LOAD & CLEAN DATA
# ─────────────────────────────────────────────────────────────
@st.cache_data(show_spinner="Memuat dan membersihkan data...")
def load_data(data_dir):
    dfs = []
    for station in STATIONS:
        path = os.path.join(data_dir, f"PRSA_Data_{station}_20130301-20170228.csv")
        df = pd.read_csv(path)
        dfs.append(df)

    df_all = pd.concat(dfs, ignore_index=True)

    # Handle missing values
    target_cols = ['PM2.5','PM10','SO2','NO2','CO','O3','TEMP','PRES','DEWP','RAIN','WSPM']
    cols = [c for c in target_cols if c in df_all.columns]

    df_all['datetime'] = pd.to_datetime(df_all[['year','month','day','hour']])
    df_all = df_all.set_index('datetime').sort_index()
    df_all[cols] = df_all[cols].interpolate(method='time', limit_direction='both')
    df_all[cols] = df_all[cols].ffill().bfill()
    if 'wd' in df_all.columns:
        df_all['wd'] = df_all['wd'].ffill().bfill()
    df_all = df_all.reset_index()

    # Derived columns
    df_all['Risk_Score'] = (
        df_all['PM2.5'] * 0.4 + df_all['PM10'] * 0.2 +
        df_all['NO2']   * 0.2 + df_all['CO']   * 0.1 +
        df_all['SO2']   * 0.1
    ) / (df_all['WSPM'].replace(0, 0.1))

    df_all['AQI_Category'] = pd.cut(df_all['PM2.5'], bins=AQI_BINS,
                                     labels=AQI_LABELS, right=True)
    return df_all


# ─────────────────────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("##Beijing AQ")
    st.markdown("---")
    menu = st.radio(
        "Navigasi",
        ["Overview",
         "Pertanyaan 1 — Lalu Lintas",
         "Pertanyaan 2 — Logistik",
         "Pertanyaan 3 — Asuransi",
         "Analisis Lanjutan"],
        label_visibility="collapsed",
    )
    st.markdown("---")
    st.markdown("**Filter Global**")
    sel_stations = st.multiselect(
        "Pilih Stasiun", STATIONS, default=STATIONS,
    )
    sel_years = st.multiselect(
        "Pilih Tahun", [2013,2014,2015,2016,2017], default=[2013,2014,2015,2016,2017],
    )
    st.markdown("---")
    st.markdown("**Jumlah Data Ditampilkan**")
    n_rows = st.slider("Maks. baris tabel", min_value=5, max_value=100, value=12, step=5)

    st.markdown("---")
    st.markdown("**Keterangan Warna**")
    st.markdown("""
<div style="font-size:0.8rem;line-height:2.2">
  <span style="background:#e74c3c;border-radius:4px;padding:2px 8px;color:white">■</span> Bahaya / Kritis / Tinggi<br>
  <span style="background:#e67e22;border-radius:4px;padding:2px 8px;color:white">■</span> Awas-Tinggi / Berbahaya<br>
  <span style="background:#f1c40f;border-radius:4px;padding:2px 8px;color:#333">■</span> Awas / Waspada<br>
  <span style="background:#27ae60;border-radius:4px;padding:2px 8px;color:white">■</span> Aman / Rendah<br>
  <hr style="border-color:#334155;margin:6px 0">
  <b>AQI PM2.5:</b><br>
  <span style="background:#00e400;border-radius:4px;padding:2px 8px;color:#333">■</span> Good (0–12)<br>
  <span style="background:#ffff00;border-radius:4px;padding:2px 8px;color:#333">■</span> Moderate (12–35)<br>
  <span style="background:#ff7e00;border-radius:4px;padding:2px 8px;color:white">■</span> Sensitive (35–55)<br>
  <span style="background:#ff0000;border-radius:4px;padding:2px 8px;color:white">■</span> Unhealthy (55–150)<br>
  <span style="background:#8f3f97;border-radius:4px;padding:2px 8px;color:white">■</span> Very Unhealthy (150–250)<br>
  <span style="background:#7e0023;border-radius:4px;padding:2px 8px;color:white">■</span> Hazardous (250+)
</div>
""", unsafe_allow_html=True)

    st.markdown("---")
    st.markdown(
        "<small style='color:#64748b'>PRSA Dataset · Beijing 2013–2017<br>"
        "Nama: 📪M Ns</small>",
        unsafe_allow_html=True,
    )


# ─────────────────────────────────────────────────────────────
# LOAD DATA
# ─────────────────────────────────────────────────────────────
df_raw = load_data(DATA_DIR)
df = df_raw[
    (df_raw['station'].isin(sel_stations)) &
    (df_raw['year'].isin(sel_years))
].copy()


# ─────────────────────────────────────────────────────────────
# HEADER
# ─────────────────────────────────────────────────────────────
st.markdown("""
<div class="main-header">
  <h1>Beijing Air Quality Dashboard</h1>
  <p>PRSA Multi-Site Dataset · Maret 2013 – Februari 2017 · 12 Stasiun Pemantauan</p>
</div>
""", unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════
# PAGE: OVERVIEW
# ═══════════════════════════════════════════════════════════════
if menu == "Overview":

    # KPI metrics
    c1, c2, c3, c4, c5 = st.columns(5)
    with c1:
        st.markdown(f"""<div class="metric-card">
            <div class="label">Total Records</div>
            <div class="value">{len(df):,}</div>
            <div class="sub">baris data</div></div>""", unsafe_allow_html=True)
    with c2:
        st.markdown(f"""<div class="metric-card">
            <div class="label">Rata-rata PM2.5</div>
            <div class="value">{df['PM2.5'].mean():.1f}</div>
            <div class="sub">µg/m³</div></div>""", unsafe_allow_html=True)
    with c3:
        st.markdown(f"""<div class="metric-card">
            <div class="label">Rata-rata PM10</div>
            <div class="value">{df['PM10'].mean():.1f}</div>
            <div class="sub">µg/m³</div></div>""", unsafe_allow_html=True)
    with c4:
        st.markdown(f"""<div class="metric-card">
            <div class="label">Stasiun Aktif</div>
            <div class="value">{df['station'].nunique()}</div>
            <div class="sub">stasiun</div></div>""", unsafe_allow_html=True)
    with c5:
        pct_unhealthy = (df['PM2.5'] > 55.4).mean() * 100
        st.markdown(f"""<div class="metric-card">
            <div class="label">% Tidak Sehat</div>
            <div class="value">{pct_unhealthy:.1f}%</div>
            <div class="sub">jam PM2.5 > 55.4</div></div>""", unsafe_allow_html=True)

    st.markdown("")

    # Tren tahunan PM2.5
    col1, col2 = st.columns([3, 2])
    with col1:
        st.markdown('<div class="section-title">Tren Bulanan PM2.5 & PM10</div>', unsafe_allow_html=True)
        monthly = df.groupby(['year','month'])[['PM2.5','PM10']].mean().reset_index()
        monthly['period'] = monthly['year'].astype(str) + '-' + monthly['month'].astype(str).str.zfill(2)
        monthly = monthly.sort_values('period')

        fig, ax = plt.subplots(figsize=(10, 4))
        ax.plot(monthly['period'], monthly['PM2.5'], color='#e74c3c', lw=2, label='PM2.5')
        ax.plot(monthly['period'], monthly['PM10'],  color='#e67e22', lw=2, label='PM10', alpha=0.8)
        ax.fill_between(monthly['period'], monthly['PM2.5'], alpha=0.15, color='#e74c3c')
        tick_idx = list(range(0, len(monthly), 6))
        ax.set_xticks([monthly['period'].iloc[i] for i in tick_idx])
        ax.set_xticklabels([monthly['period'].iloc[i] for i in tick_idx], rotation=30, ha='right', fontsize=8)
        ax.set_ylabel('µg/m³')
        ax.legend(); ax.grid(alpha=0.2)
        fig.tight_layout()
        st.pyplot(fig)
        plt.close()

    with col2:
        st.markdown('<div class="section-title">Distribusi AQI</div>', unsafe_allow_html=True)
        aqi_dist = df['AQI_Category'].value_counts().reindex(AQI_LABELS).fillna(0)
        aqi_pct  = aqi_dist / aqi_dist.sum() * 100

        fig, ax = plt.subplots(figsize=(5, 4))
        bars = ax.barh(AQI_LABELS, aqi_pct.values,
                       color=[AQI_COLORS[l] for l in AQI_LABELS],
                       edgecolor='white', linewidth=0.5)
        ax.set_xlabel('%')
        for bar, pct in zip(bars, aqi_pct.values):
            ax.text(bar.get_width() + 0.3, bar.get_y() + bar.get_height()/2,
                    f'{pct:.1f}%', va='center', fontsize=8)
        ax.grid(axis='x', alpha=0.2)
        fig.tight_layout()
        st.pyplot(fig)
        plt.close()

    # Heatmap rata-rata PM2.5 per stasiun per jam
    st.markdown('<div class="section-title">Heatmap PM2.5 — Stasiun × Jam</div>', unsafe_allow_html=True)
    pivot = df.groupby(['station','hour'])['PM2.5'].mean().unstack()
    fig, ax = plt.subplots(figsize=(16, 5))
    sns.heatmap(pivot, cmap='YlOrRd', annot=False, fmt='.0f',
                linewidths=0.3, ax=ax, cbar_kws={'label':'µg/m³'})
    ax.set_xlabel('Jam'); ax.set_ylabel('')
    fig.tight_layout()
    st.pyplot(fig)
    plt.close()


# ═══════════════════════════════════════════════════════════════
# PAGE: PERTANYAAN 1 — LALU LINTAS
# ═══════════════════════════════════════════════════════════════
elif menu == "Pertanyaan 1 — Lalu Lintas":
    st.markdown('<div class="section-title">Manajemen Lalu Lintas Berbasis PM2.5 & PM10</div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="insight-box">
    Bagaimana cara mengintegrasikan data historis konsentrasi PM2.5 dan PM10
    ke dalam sistem manajemen lalu lintas untuk membatasi volume kendaraan
    di zona dengan tingkat polusi tinggi?
    </div>""", unsafe_allow_html=True)

    # Klasifikasi zona
    station_pollution = df.groupby('station')[['PM2.5','PM10']].mean().round(2)
    station_pollution['Avg_Particulate'] = (station_pollution['PM2.5'] + station_pollution['PM10']) / 2

    def classify_zone(val):
        if val >= 100: return 'Bahaya'
        elif val >= 60: return 'Awas'
        else: return 'Aman'

    station_pollution['Status'] = station_pollution['Avg_Particulate'].apply(classify_zone)
    station_pollution_sorted = station_pollution.sort_values('Avg_Particulate', ascending=False)

    # Metrics
    c1, c2, c3 = st.columns(3)
    n_bahaya = (station_pollution['Status'] == 'Bahaya').sum()
    n_awas   = (station_pollution['Status'] == 'Awas').sum()
    n_aman   = (station_pollution['Status'] == 'Aman').sum()
    with c1:
        st.markdown(f"""<div class="metric-card">
            <div class="label">🔴 Zona Bahaya</div>
            <div class="value">{n_bahaya}</div>
            <div class="sub">stasiun ≥ 100 µg/m³</div></div>""", unsafe_allow_html=True)
    with c2:
        st.markdown(f"""<div class="metric-card">
            <div class="label">🟡 Zona Awas</div>
            <div class="value">{n_awas}</div>
            <div class="sub">stasiun 60–100 µg/m³</div></div>""", unsafe_allow_html=True)
    with c3:
        st.markdown(f"""<div class="metric-card">
            <div class="label">🟢 Zona Aman</div>
            <div class="value">{n_aman}</div>
            <div class="sub">stasiun &lt; 60 µg/m³</div></div>""", unsafe_allow_html=True)

    st.markdown("")
    col1, col2 = st.columns(2)

    with col1:
        st.markdown('<div class="section-title">Klasifikasi Zona per Stasiun</div>', unsafe_allow_html=True)
        zone_colors = {'Bahaya':'#e74c3c','Awas':'#f39c12','Aman':'#27ae60'}
        colors = [zone_colors[s] for s in station_pollution_sorted['Status']]
        fig, ax = plt.subplots(figsize=(7, 5))
        ax.barh(station_pollution_sorted.index, station_pollution_sorted['Avg_Particulate'], color=colors)
        ax.axvline(100, color='red',    linestyle='--', lw=1.2, label='Batas Bahaya (100)')
        ax.axvline(60,  color='orange', linestyle='--', lw=1.2, label='Batas Awas (60)')
        ax.set_xlabel('µg/m³'); ax.invert_yaxis()
        ax.legend(fontsize=8); ax.grid(alpha=0.2)
        fig.tight_layout(); st.pyplot(fig); plt.close()

    with col2:
        st.markdown('<div class="section-title">Pola Polusi per Jam</div>', unsafe_allow_html=True)
        hourly = df.groupby('hour')[['PM2.5','PM10']].mean()
        fig, ax = plt.subplots(figsize=(7, 5))
        ax.plot(hourly.index, hourly['PM2.5'], color='#e74c3c', lw=2, label='PM2.5')
        ax.plot(hourly.index, hourly['PM10'],  color='#e67e22', lw=2, label='PM10', alpha=0.8)
        ax.fill_between(hourly.index, hourly['PM2.5'], alpha=0.15, color='#e74c3c')
        peak = hourly['PM2.5'].quantile(0.75)
        for h in hourly[hourly['PM2.5'] >= peak].index:
            ax.axvspan(h-0.4, h+0.4, alpha=0.1, color='red')
        ax.set_xlabel('Jam'); ax.set_ylabel('µg/m³')
        ax.set_xticks(range(0,24)); ax.legend(); ax.grid(alpha=0.2)
        fig.tight_layout(); st.pyplot(fig); plt.close()

    # Tabel rekomendasi
    st.markdown('<div class="section-title">Rekomendasi Manajemen Lalu Lintas</div>', unsafe_allow_html=True)
    def get_action(status):
        if status == 'Bahaya': return '🔴 Ganjil-genap + Larangan truk besar'
        elif status == 'Awas': return '🟡 Pantau real-time + Siaga pengalihan'
        else: return '🟢 Normal, monitoring rutin'

    station_pollution_sorted['Rekomendasi'] = station_pollution_sorted['Status'].apply(get_action)
    st.dataframe(
        station_pollution_sorted[['PM2.5','PM10','Avg_Particulate','Status','Rekomendasi']].round(2).head(n_rows),
        use_container_width=True,
    )

    st.markdown("""<div class="insight-box">
    <b>💡 Insight:</b> Hanya <b>Gucheng</b> yang berstatus Bahaya (101.67 µg/m³).
    Jam puncak polusi terjadi pukul <b>20.00–01.00</b> — waktu kritis untuk
    menerapkan pembatasan kendaraan berat.
    </div>""", unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════
# PAGE: PERTANYAAN 2 — LOGISTIK
# ═══════════════════════════════════════════════════════════════
elif menu == "Pertanyaan 2 — Logistik":
    st.markdown('<div class="section-title">Korelasi Meteorologi & Polusi untuk Rute Logistik</div>', unsafe_allow_html=True)
    st.markdown("""<div class="insight-box">
    Bagaimana cara mengukur korelasi antara variabel meteorologi dan tingkat polusi
    udara untuk mengalihkan rute pengiriman guna menekan paparan polutan
    terhadap pekerja lapangan?
    </div>""", unsafe_allow_html=True)

    meteo_cols    = ['TEMP','PRES','DEWP','RAIN','WSPM']
    pollutant_cols = ['PM2.5','PM10','SO2','NO2','CO','O3']
    corr = df[meteo_cols + pollutant_cols].corr().loc[meteo_cols, pollutant_cols]

    safe_hours = df.groupby('hour')['Risk_Score'].mean()
    safest   = sorted(safe_hours.nsmallest(5).index.tolist())
    riskiest = sorted(safe_hours.nlargest(5).index.tolist())
    station_risk = df.groupby('station')['Risk_Score'].mean().sort_values()

    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown(f"""<div class="metric-card">
            <div class="label">Jam Paling Aman</div>
            <div class="value" style="font-size:1.2rem">{safest}</div>
            <div class="sub">untuk pengiriman</div></div>""", unsafe_allow_html=True)
    with c2:
        st.markdown(f"""<div class="metric-card">
            <div class="label">Jam Paling Berisiko</div>
            <div class="value" style="font-size:1.2rem">{riskiest}</div>
            <div class="sub">hindari pengiriman</div></div>""", unsafe_allow_html=True)
    with c3:
        safest_st = station_risk.index[0]
        st.markdown(f"""<div class="metric-card">
            <div class="label">Rute Paling Aman</div>
            <div class="value" style="font-size:1.3rem">{safest_st}</div>
            <div class="sub">Risk Score: {station_risk.iloc[0]:.1f}</div></div>""", unsafe_allow_html=True)

    st.markdown("")
    col1, col2 = st.columns(2)

    with col1:
        st.markdown('<div class="section-title">Heatmap Korelasi Meteorologi vs Polutan</div>', unsafe_allow_html=True)
        fig, ax = plt.subplots(figsize=(7, 4))
        sns.heatmap(corr, annot=True, fmt='.2f', cmap='RdYlGn_r',
                    center=0, linewidths=0.5, ax=ax,
                    annot_kws={'size':9})
        fig.tight_layout(); st.pyplot(fig); plt.close()

    with col2:
        st.markdown('<div class="section-title">Indeks Risiko Pengiriman per Jam</div>', unsafe_allow_html=True)
        fig, ax = plt.subplots(figsize=(7, 4))
        ax.plot(safe_hours.index, safe_hours.values, color='#8e44ad', lw=2)
        ax.fill_between(safe_hours.index, safe_hours.values, alpha=0.2, color='#8e44ad')
        for h in safest:
            ax.axvline(h, color='green', linestyle='--', alpha=0.6)
        ax.set_xlabel('Jam'); ax.set_ylabel('Risk Score')
        ax.set_xticks(range(0, 24)); ax.grid(alpha=0.2)
        fig.tight_layout(); st.pyplot(fig); plt.close()

    st.markdown('<div class="section-title">Ranking Risiko Stasiun (Teraman → Terberbahaya)</div>', unsafe_allow_html=True)
    risk_df = station_risk.reset_index()
    risk_df.columns = ['Stasiun','Risk Score']
    risk_df['Risk Score'] = risk_df['Risk Score'].round(1)
    risk_df['Rank'] = range(1, len(risk_df)+1)
    risk_df = risk_df[['Rank','Stasiun','Risk Score']]

    fig, ax = plt.subplots(figsize=(12, 4))
    colors_risk = ['#27ae60' if i < 3 else '#e67e22' if i < 9 else '#e74c3c'
                   for i in range(len(risk_df))]
    ax.barh(risk_df['Stasiun'], risk_df['Risk Score'], color=colors_risk)
    ax.invert_yaxis(); ax.set_xlabel('Risk Score'); ax.grid(alpha=0.2)
    fig.tight_layout(); st.pyplot(fig); plt.close()

    st.markdown("""<div class="insight-box">
    <b>Insight:</b> <b>WSPM (kecepatan angin)</b> adalah faktor terkuat menekan NO2 (r = -0.396).
    Jadwalkan pengiriman pukul <b>12.00–16.00</b> dan prioritaskan rute melalui
    <b>Dingling & Huairou</b>.
    </div>""", unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════
# PAGE: PERTANYAAN 3 — ASURANSI
# ═══════════════════════════════════════════════════════════════
elif menu == "Pertanyaan 3 — Asuransi":
    st.markdown('<div class="section-title">Model Premi Asuransi Berbasis SO2 & NO2</div>', unsafe_allow_html=True)
    st.markdown("""<div class="insight-box">
    Bagaimana menganalisis fluktuasi SO2 dan NO2 untuk memodelkan potensi
    lonjakan klaim penyakit pernapasan dan merancang struktur premi
    berdasarkan lokasi pemukiman nasabah?
    </div>""", unsafe_allow_html=True)

    so2_no2 = df.groupby('station')[['SO2','NO2']].agg(
        ['mean','std','max', lambda x: x.quantile(0.95)]
    ).round(2)
    so2_no2.columns = ['SO2_mean','SO2_std','SO2_max','SO2_p95',
                        'NO2_mean','NO2_std','NO2_max','NO2_p95']

    so2_norm = (so2_no2['SO2_mean'] - so2_no2['SO2_mean'].min()) / \
               (so2_no2['SO2_mean'].max() - so2_no2['SO2_mean'].min())
    no2_norm = (so2_no2['NO2_mean'] - so2_no2['NO2_mean'].min()) / \
               (so2_no2['NO2_mean'].max() - so2_no2['NO2_mean'].min())
    risk_index = (so2_norm * 0.6 + no2_norm * 0.4) * 100

    BASE = 500_000
    def tier_info(score):
        if score >= 75:   return 'Tinggi',      '#e74c3c', BASE * 2.0
        elif score >= 50: return 'Awas-Tinggi', '#e67e22', BASE * 1.5
        elif score >= 25: return 'Awas',        '#f1c40f', BASE * 1.2
        else:             return 'Rendah',      '#27ae60', BASE * 1.0

    premi_df = pd.DataFrame({
        'Risk Index': risk_index.round(1),
    })
    premi_df['Tier']       = premi_df['Risk Index'].apply(lambda x: tier_info(x)[0])
    premi_df['Premi/Bulan'] = premi_df['Risk Index'].apply(lambda x: f"Rp {tier_info(x)[2]:,.0f}")
    premi_df = premi_df.sort_values('Risk Index', ascending=False)

    c1, c2, c3, c4 = st.columns(4)
    for col, tier, clr, cnt_label in zip(
        [c1,c2,c3,c4],
        ['Tinggi','Awas-Tinggi','Awas','Rendah'],
        ['#e74c3c','#e67e22','#f1c40f','#27ae60'],
        ['Rp 1.000.000','Rp 750.000','Rp 600.000','Rp 500.000']
    ):
        n = (premi_df['Tier'] == tier).sum()
        with col:
            st.markdown(f"""<div class="metric-card" style="border-left:4px solid {clr}">
                <div class="label">{tier}</div>
                <div class="value">{n} stasiun</div>
                <div class="sub">{cnt_label}/bulan</div></div>""", unsafe_allow_html=True)

    st.markdown("")
    col1, col2 = st.columns(2)

    with col1:
        st.markdown('<div class="section-title">Risk Index per Stasiun</div>', unsafe_allow_html=True)
        ri_sorted = risk_index.sort_values(ascending=False)
        bar_colors = ['#e74c3c' if s>=75 else '#e67e22' if s>=50 else '#f1c40f' if s>=25
                      else '#27ae60' for s in ri_sorted]
        fig, ax = plt.subplots(figsize=(7, 5))
        ax.bar(ri_sorted.index, ri_sorted.values, color=bar_colors, edgecolor='white')
        ax.axhline(75, color='red',    linestyle='--', lw=1, label='Tier Tinggi')
        ax.axhline(50, color='orange', linestyle='--', lw=1, label='Tier Awas-Tinggi')
        ax.axhline(25, color='gold',   linestyle='--', lw=1, label='Tier Awas')
        ax.set_xticklabels(ri_sorted.index, rotation=40, ha='right', fontsize=8)
        ax.set_ylabel('Risk Index (0-100)')
        ax.legend(fontsize=8); ax.grid(axis='y', alpha=0.2)
        fig.tight_layout(); st.pyplot(fig); plt.close()

    with col2:
        st.markdown('<div class="section-title">Tren Bulanan SO2 & NO2</div>', unsafe_allow_html=True)
        monthly_trend = df.groupby('month')[['SO2','NO2']].mean()
        high_risk_months = monthly_trend[
            (monthly_trend['SO2'] > monthly_trend['SO2'].mean()) |
            (monthly_trend['NO2'] > monthly_trend['NO2'].mean())
        ].index.tolist()
        fig, ax = plt.subplots(figsize=(7, 5))
        ax.plot(monthly_trend.index, monthly_trend['SO2'], color='#c0392b', lw=2, marker='o', label='SO2')
        ax.plot(monthly_trend.index, monthly_trend['NO2'], color='#2980b9', lw=2, marker='s', label='NO2')
        for m in high_risk_months:
            ax.axvspan(m-0.4, m+0.4, alpha=0.1, color='red')
        ax.set_xticks(range(1,13))
        ax.set_xticklabels([BULAN[m] for m in range(1,13)], fontsize=8)
        ax.set_ylabel('µg/m³'); ax.legend(); ax.grid(alpha=0.2)
        fig.tight_layout(); st.pyplot(fig); plt.close()

    st.markdown('<div class="section-title">Struktur Premi per Stasiun</div>', unsafe_allow_html=True)
    st.dataframe(premi_df.head(n_rows), use_container_width=True)

    st.markdown("""<div class="insight-box">
    <b>Insight:</b> <b>Wanliu</b> (Risk Index: 97.0) memerlukan premi tertinggi Rp 1.000.000/bulan.
    Siapkan cadangan klaim <b>20–30% lebih besar</b> pada bulan <b>Oktober–Maret</b>
    (musim dingin — SO2 & NO2 melonjak akibat pembakaran pemanas).
    </div>""", unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════
# PAGE: ANALISIS LANJUTAN
# ═══════════════════════════════════════════════════════════════
elif menu == "Analisis Lanjutan":
    tab1, tab2, tab3, tab4 = st.tabs([
        "RFM Analysis",
        "Manual Grouping",
        "Geospatial",
        "AQI Binning",
    ])

    # ── TAB 1: RFM ──────────────────────────────────────────
    with tab1:
        st.markdown('<div class="section-title">RFM-Style Analysis — Risiko Polusi PM2.5</div>', unsafe_allow_html=True)
        st.markdown("""<div class="insight-box">
        Adaptasi RFM: <b>Recency</b> = hari sejak spike terakhir |
        <b>Frequency</b> = jumlah hari terjadi spike (PM2.5 > 150 µg/m³) |
        <b>Magnitude</b> = rata-rata PM2.5 saat spike
        </div>""", unsafe_allow_html=True)

        df_rfm = df.copy()
        df_rfm['date']     = df_rfm['datetime'].dt.date
        df_rfm['is_spike'] = df_rfm['PM2.5'] > 150
        spike_df = df_rfm[df_rfm['is_spike']]
        ref_date = pd.to_datetime(df_rfm['date'].max())

        rfm_list = []
        for station, grp in spike_df.groupby('station'):
            rfm_list.append({
                'station'  : station,
                'Recency'  : (ref_date - pd.to_datetime(grp['date'].max())).days,
                'Frequency': grp['date'].nunique(),
                'Magnitude': round(grp['PM2.5'].mean(), 2),
            })
        rfm = pd.DataFrame(rfm_list).set_index('station')

        r_bins = pd.qcut(rfm['Recency'],   q=3, labels=False, duplicates='drop')
        f_bins = pd.qcut(rfm['Frequency'], q=3, labels=False, duplicates='drop')
        m_bins = pd.qcut(rfm['Magnitude'], q=3, labels=False, duplicates='drop')
        rfm['R_score'] = (r_bins.max() - r_bins + 1).astype(int)
        rfm['F_score'] = (f_bins + 1).astype(int)
        rfm['M_score'] = (m_bins + 1).astype(int)
        rfm['RFM_Total'] = rfm['R_score'] + rfm['F_score'] + rfm['M_score']

        def rfm_segment(s):
            if s >= 8: return 'Zona Kritis'
            elif s >= 6: return 'Zona Berbahaya'
            elif s >= 4: return 'Zona Waspada'
            else: return 'Zona Aman'

        rfm['Segment'] = rfm['RFM_Total'].apply(rfm_segment)
        rfm_sorted = rfm.sort_values('RFM_Total', ascending=False)

        seg_colors = {'Zona Kritis':'#e74c3c','Zona Berbahaya':'#e67e22',
                      'Zona Waspada':'#f1c40f','Zona Aman':'#27ae60'}
        colors = [seg_colors[rfm_sorted.loc[s,'Segment']] for s in rfm_sorted.index]

        fig, axes = plt.subplots(1, 3, figsize=(16, 5))
        fig.suptitle("RFM Analysis — Risiko Polusi PM2.5", fontweight='bold')
        for ax, (label, col) in zip(axes, [
            ('Recency (hari)','Recency'),
            ('Frequency (hari spike)','Frequency'),
            ('Magnitude (µg/m³)','Magnitude')
        ]):
            ax.barh(rfm_sorted.index, rfm_sorted[col], color=colors)
            ax.set_title(label); ax.invert_yaxis(); ax.grid(alpha=0.2)
        handles = [mpatches.Patch(color=c, label=l) for l, c in seg_colors.items()]
        fig.legend(handles=handles, loc='lower center', ncol=4, fontsize=9, bbox_to_anchor=(0.5,-0.04))
        fig.tight_layout(); st.pyplot(fig); plt.close()
        st.dataframe(rfm_sorted.head(n_rows), use_container_width=True)

    # ── TAB 2: MANUAL GROUPING ──────────────────────────────
    with tab2:
        st.markdown('<div class="section-title">Clustering Manual Grouping</div>', unsafe_allow_html=True)

        profile = df.groupby('station').agg(
            PM25_mean=('PM2.5','mean'), PM10_mean=('PM10','mean'),
            NO2_mean=('NO2','mean'),   SO2_mean=('SO2','mean'),
        ).round(2)

        def assign_group(row):
            if row['PM25_mean'] > 80 and row['NO2_mean'] > 60:
                return 'Klaster A — Polusi Tinggi'
            elif row['PM25_mean'] > 60 and row['NO2_mean'] > 45:
                return 'Klaster B — Polusi Sedang'
            elif row['PM25_mean'] > 50:
                return 'Klaster C — Polusi Rendah-Sedang'
            else:
                return 'Klaster D — Polusi Rendah'

        profile['Klaster'] = profile.apply(assign_group, axis=1)
        profile_sorted = profile.sort_values('PM25_mean', ascending=False)

        kl_colors = {
            'Klaster A — Polusi Tinggi'       : '#e74c3c',
            'Klaster B — Polusi Sedang'       : '#e67e22',
            'Klaster C — Polusi Rendah-Sedang': '#f1c40f',
            'Klaster D — Polusi Rendah'       : '#27ae60',
        }
        colors = [kl_colors[profile_sorted.loc[s,'Klaster']] for s in profile_sorted.index]

        col1, col2 = st.columns(2)
        with col1:
            fig, ax = plt.subplots(figsize=(7, 5))
            ax.barh(profile_sorted.index, profile_sorted['PM25_mean'], color=colors)
            ax.axvline(80, color='red',    linestyle='--', lw=1, label='Batas A (80)')
            ax.axvline(60, color='orange', linestyle='--', lw=1, label='Batas B (60)')
            ax.axvline(50, color='gold',   linestyle='--', lw=1, label='Batas C (50)')
            ax.set_xlabel('PM2.5 µg/m³'); ax.invert_yaxis()
            ax.legend(fontsize=8); ax.grid(alpha=0.2)
            fig.tight_layout(); st.pyplot(fig); plt.close()

        with col2:
            fig, ax = plt.subplots(figsize=(7, 5))
            for st_name, row in profile.iterrows():
                c = kl_colors[row['Klaster']]
                ax.scatter(row['PM25_mean'], row['NO2_mean'], color=c, s=120, zorder=3)
                ax.annotate(st_name, (row['PM25_mean'], row['NO2_mean']),
                            fontsize=7, xytext=(3,3), textcoords='offset points')
            ax.set_xlabel('PM2.5 µg/m³'); ax.set_ylabel('NO2 µg/m³')
            ax.set_title('Scatter PM2.5 vs NO2'); ax.grid(alpha=0.2)
            handles = [mpatches.Patch(color=c, label=l) for l, c in kl_colors.items()]
            ax.legend(handles=handles, fontsize=7)
            fig.tight_layout(); st.pyplot(fig); plt.close()

        st.dataframe(profile_sorted.head(n_rows), use_container_width=True)

    # ── TAB 3: GEOSPATIAL ──────────────────────────────────
    with tab3:
        st.markdown('<div class="section-title">Peta Distribusi Polusi per Stasiun</div>', unsafe_allow_html=True)

        station_avg = df.groupby('station').agg(
            PM25=('PM2.5','mean'), PM10=('PM10','mean'),
            NO2=('NO2','mean'),   SO2=('SO2','mean'),
            CO=('CO','mean'),     O3=('O3','mean'),
        ).round(2)

        def mk_color(pm25):
            if pm25 > 80: return 'red'
            elif pm25 > 60: return 'orange'
            elif pm25 > 50: return 'beige'
            else: return 'green'

        m = folium.Map(location=[39.95, 116.39], zoom_start=10, tiles='CartoDB positron')
        heat_data = []
        for station, row in station_avg.iterrows():
            if station not in STATION_COORDS: continue
            lat, lon = STATION_COORDS[station]
            color = mk_color(row['PM25'])
            folium.CircleMarker(
                [lat, lon], radius=row['PM25']*0.35,
                color=color, fill=True, fill_color=color, fill_opacity=0.45, weight=1.5,
            ).add_to(m)
            popup_html = f"""<div style="font-family:Arial;font-size:12px;width:190px">
                <b>{station}</b><hr>
                PM2.5: <b>{row['PM25']} µg/m³</b><br>
                PM10: {row['PM10']} | NO2: {row['NO2']}<br>
                SO2: {row['SO2']} | CO: {row['CO']} | O3: {row['O3']}
            </div>"""
            folium.Marker(
                [lat, lon],
                popup=folium.Popup(popup_html, max_width=210),
                tooltip=f"{station} | PM2.5: {row['PM25']}",
                icon=folium.Icon(color=color, icon='cloud', prefix='fa'),
            ).add_to(m)
            heat_data.append([lat, lon, row['PM25']])

        HeatMap(heat_data, radius=40, blur=25, min_opacity=0.3,
                gradient={0.4:'blue',0.65:'lime',0.85:'orange',1.0:'red'}).add_to(m)

        st_folium(m, width=None, height=500)

        st.markdown("""<div class="insight-box">
        <b></b> Klik marker untuk melihat detail polutan per stasiun.
        Lingkaran lebih besar = PM2.5 lebih tinggi.
        Warna merah = polusi tinggi, hijau = polusi rendah.
        </div>""", unsafe_allow_html=True)

    # ── TAB 4: BINNING AQI ─────────────────────────────────
    with tab4:
        st.markdown('<div class="section-title">Clustering Binning — Kategori AQI PM2.5</div>', unsafe_allow_html=True)

        df_bin = df.copy()
        df_bin['AQI_Category'] = pd.cut(df_bin['PM2.5'], bins=AQI_BINS,
                                          labels=AQI_LABELS, right=True)
        global_dist = df_bin['AQI_Category'].value_counts().reindex(AQI_LABELS).fillna(0)
        global_pct  = (global_dist / global_dist.sum() * 100).round(2)

        col1, col2 = st.columns(2)
        with col1:
            fig, ax = plt.subplots(figsize=(7, 5))
            ax.barh(AQI_LABELS, global_pct.values,
                    color=[AQI_COLORS[l] for l in AQI_LABELS], edgecolor='white')
            for i, pct in enumerate(global_pct.values):
                ax.text(pct+0.3, i, f'{pct:.1f}%', va='center', fontsize=9)
            ax.set_xlabel('%'); ax.set_title('Distribusi AQI Global')
            ax.grid(axis='x', alpha=0.2)
            fig.tight_layout(); st.pyplot(fig); plt.close()

        with col2:
            station_dist = (
                df_bin.groupby(['station','AQI_Category'], observed=True)
                      .size().unstack(fill_value=0)
                      .reindex(columns=AQI_LABELS, fill_value=0)
            )
            station_pct = station_dist.div(station_dist.sum(axis=1), axis=0) * 100
            fig, ax = plt.subplots(figsize=(7, 5))
            bottom = np.zeros(len(station_pct))
            for cat in AQI_LABELS:
                vals = station_pct[cat].values if cat in station_pct.columns else np.zeros(len(station_pct))
                ax.bar(station_pct.index, vals, bottom=bottom,
                       color=AQI_COLORS[cat], label=cat, edgecolor='white', lw=0.3)
                bottom += vals
            ax.set_xticklabels(station_pct.index, rotation=35, ha='right', fontsize=8)
            ax.set_ylabel('%'); ax.set_title('% AQI per Stasiun')
            ax.legend(fontsize=7, loc='upper right')
            ax.grid(axis='y', alpha=0.2)
            fig.tight_layout(); st.pyplot(fig); plt.close()

        # Summary table
        summary_df = pd.DataFrame({
            'Kategori': AQI_LABELS,
            'Jumlah Jam': global_dist.values.astype(int),
            'Persentase (%)': global_pct.values,
        })
        st.dataframe(summary_df.head(n_rows), use_container_width=True, hide_index=True)