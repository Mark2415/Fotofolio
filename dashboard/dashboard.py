
import os
import warnings

import numpy as np
import pandas as pd
import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
import seaborn as sns
import folium
import streamlit as st
from scipy import stats
from scipy.stats import shapiro, f_oneway

from folium.plugins import HeatMap
from streamlit_folium import st_folium

warnings.filterwarnings('ignore')


# PAGE CONFIG

st.set_page_config(
    page_title="Beijing Air Quality Dashboard",
    page_icon=":china:",
    layout="wide",
    initial_sidebar_state="expanded",
)

# CUSTOM CSS
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Sans:wght@300;400;500&display=swap');

html, body, [class*="css"] { font-family: 'DM Sans', sans-serif; }

/* Animasi gradient bergerak */
@keyframes gradientMove {
    0% { background-position: 0% 50%; }
    50% { background-position: 100% 50%; }
    100% { background-position: 0% 50%; }
}

.main-header {
    background: linear-gradient(135deg, #0f0c29, #302b63, #24243e);
    background-size: 200% 200%;
    animation: gradientMove 12s ease infinite;
    padding: 2.5rem 2rem; border-radius: 16px; margin-bottom: 2rem;
    position: relative; overflow: hidden;
}
.main-header::before {
    content: ''; position: absolute; top: -50%; left: -50%;
    width: 200%; height: 200%;
    background: radial-gradient(circle at 30% 50%, rgba(99,179,237,0.15) 0%, transparent 50%),
                radial-gradient(circle at 70% 50%, rgba(236,72,153,0.1) 0%, transparent 50%);
}
.main-header h1 {
    font-family: 'Syne', sans-serif; font-weight: 800; font-size: 2.4rem;
    color: #ffffff; margin: 0; position: relative;
}
.main-header p {
    color: rgba(255,255,255,0.65); font-size: 0.95rem;
    margin: 0.4rem 0 0; position: relative;
}

/* Animasi hover metric-card */
.metric-card {
    background: #1e293b; border: 1px solid #334155;
    border-radius: 12px; padding: 1.2rem 1.4rem;
    box-shadow: 0 2px 8px rgba(0,0,0,0.3);
    transition: transform 0.3s ease, box-shadow 0.3s ease;
}
.metric-card:hover {
    transform: translateY(-6px) scale(1.03);
    box-shadow: 0 6px 16px rgba(0,0,0,0.4);
}

.metric-card .label {
    font-size: 0.78rem; color: #94a3b8; font-weight: 500;
    letter-spacing: 0.05em; text-transform: uppercase;
}
.metric-card .value {
    font-family: 'Syne', sans-serif; font-size: 2rem; font-weight: 700;
    color: #f1f5f9; line-height: 1.1; margin-top: 0.2rem;
}
.metric-card .sub { font-size: 0.8rem; color: #64748b; margin-top: 0.15rem; }

.section-title {
    font-family: 'Syne', sans-serif;
    font-size: 1.3rem;
    font-weight: 700;
    color: white;
    border-left: 4px solid #3b82f6;
    padding-left: 0.75rem;
    margin: 1.5rem 0 1rem;
}

.insight-box {
    background: #0f172a; border-left: 4px solid #0ea5e9;
    border-radius: 0 10px 10px 0; padding: 1rem 1.25rem; margin: 1rem 0;
    font-size: 0.88rem; color: #bae6fd; line-height: 1.6;
    transition: background 0.5s ease;
}
.insight-box:hover {
    background: #1e293b;
}

[data-testid="stSidebar"] { background: #0f172a; }
[data-testid="stSidebar"] * { color: #e2e8f0 !important; }
.stApp { background: #0f172a; }
</style>
""", unsafe_allow_html=True)

# KONSTANTA
DATA_DIR = "source/dirty"
STATIONS = [
    'Aotizhongxin','Changping','Dingling','Dongsi',
    'Guanyuan','Gucheng','Huairou','Nongzhanguan',
    'Shunyi','Tiantan','Wanliu','Wanshouxigong',
]
STATION_COORDS = {
    'Aotizhongxin':(39.9824,116.3976), 'Changping':(40.2149,116.2310),
    'Dingling':(40.2900,116.2200),     'Dongsi':(39.9290,116.4170),
    'Guanyuan':(39.9290,116.3390),     'Gucheng':(39.9140,116.1840),
    'Huairou':(40.3280,116.6280),      'Nongzhanguan':(39.9370,116.4610),
    'Shunyi':(40.1270,116.6550),       'Tiantan':(39.8860,116.4070),
    'Wanliu':(39.9870,116.2870),       'Wanshouxigong':(39.8780,116.3520),
}
AQI_BINS   = [0, 12, 35.4, 55.4, 150.4, 250.4, float('inf')]
AQI_LABELS = ['Good','Moderate','Sensitive Groups','Unhealthy','Very Unhealthy','Hazardous']
AQI_COLORS = {
    'Good':'#00e400','Moderate':'#ffff00','Sensitive Groups':'#ff7e00',
    'Unhealthy':'#ff0000','Very Unhealthy':'#8f3f97','Hazardous':'#7e0023',
}
POLLUTANTS = ['PM2.5','PM10','SO2','NO2','CO','O3']
METEO      = ['TEMP','PRES','DEWP','RAIN','WSPM']
BULAN = {1:'Jan',2:'Feb',3:'Mar',4:'Apr',5:'Mei',6:'Jun',
         7:'Jul',8:'Agu',9:'Sep',10:'Okt',11:'Nov',12:'Des'}

# Dark matplotlib style
DS = {'figure.facecolor':'#1e293b','axes.facecolor':'#1e293b',
      'axes.edgecolor':'#475569','axes.labelcolor':'#cbd5e1',
      'xtick.color':'#94a3b8','ytick.color':'#94a3b8',
      'text.color':'#f1f5f9','grid.color':'#334155',
      'legend.facecolor':'#1e293b','legend.edgecolor':'#475569'}

# LOAD & CLEAN DATA

@st.cache_data(show_spinner="Memuat dan membersihkan data...")
def load_data(data_dir):
    dfs = []
    for station in STATIONS:
        path = os.path.join(data_dir, f"PRSA_Data_{station}_20130301-20170228.csv")
        df = pd.read_csv(path)
        dfs.append(df)
    df_all = pd.concat(dfs, ignore_index=True)
    cols = [c for c in POLLUTANTS+METEO if c in df_all.columns]
    df_all['datetime'] = pd.to_datetime(df_all[['year','month','day','hour']])
    df_all = df_all.set_index('datetime').sort_index()
    df_all[cols] = df_all[cols].interpolate(method='time', limit_direction='both')
    df_all[cols] = df_all[cols].ffill().bfill()
    if 'wd' in df_all.columns:
        df_all['wd'] = df_all['wd'].ffill().bfill()
    df_all = df_all.reset_index()
    df_all['AQI_Category'] = pd.cut(df_all['PM2.5'], bins=AQI_BINS, labels=AQI_LABELS, right=True)
    return df_all

# SIDEBAR

with st.sidebar:
    st.markdown("## Beijing Air Quality Analysis")
    st.markdown("---")
    menu = st.radio("Navigasi", [
        "Overview",
        "Pertanyaan 1 — Lalu Lintas",
        "Pertanyaan 2 — Logistik",
        "Pertanyaan 3 — Asuransi",
        "Diagram tambahan",
        "Analisis Lanjutan",
    ], label_visibility="collapsed")
    st.markdown("---")
    st.markdown("**Filter Global**")
    sel_stations = st.multiselect("Pilih Stasiun", STATIONS, default=STATIONS)
    sel_years    = st.multiselect("Pilih Tahun", [2013,2014,2015,2016,2017],
                                  default=[2013,2014,2015,2016,2017])
    st.markdown("---")
    st.markdown("**Jumlah Data Ditampilkan**")
    n_rows = st.slider("Maks. baris tabel", 5, 100, 12, 5)
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
  <span style="background:#8f3f97;border-radius:4px;padding:2px 8px;color:white">■</span> Very Unhealthy<br>
  <span style="background:#7e0023;border-radius:4px;padding:2px 8px;color:white">■</span> Hazardous (250+)
</div>""", unsafe_allow_html=True)
    st.markdown("---")
    st.markdown("<small style='color:#64748b'>PRSA Dataset · Beijing 2013–2017<br>Nama: 📪M Ns</small>",
                unsafe_allow_html=True)


# LOAD + FILTER
df_raw = load_data(DATA_DIR)
df = df_raw[(df_raw['station'].isin(sel_stations))&(df_raw['year'].isin(sel_years))].copy()


# HEADER
st.markdown("""
<div class="main-header">
  <h1>Beijing Air Quality Dashboard</h1>
  <p>PRSA Multi-Site Dataset · Maret 2013 – Februari 2017 · 12 Stasiun Pemantauan</p>
</div>""", unsafe_allow_html=True)



# OVERVIEW
if menu == "Overview":
    c1,c2,c3,c4,c5 = st.columns(5)
    for col,(lbl,val,sub) in zip([c1,c2,c3,c4,c5],[
        ("Total Records",   f"{len(df):,}",             "baris data"),
        ("Rata-rata PM2.5", f"{df['PM2.5'].mean():.1f}","µg/m³"),
        ("Rata-rata PM10",  f"{df['PM10'].mean():.1f}", "µg/m³"),
        ("Stasiun Aktif",   f"{df['station'].nunique()}","stasiun"),
        ("% Tidak Sehat",   f"{(df['PM2.5']>55.4).mean()*100:.1f}%","jam PM2.5>55"),
    ]):
        with col:
            st.markdown(f"""<div class="metric-card">
                <div class="label">{lbl}</div><div class="value">{val}</div>
                <div class="sub">{sub}</div></div>""", unsafe_allow_html=True)

    st.markdown("")
    col1,col2 = st.columns([3,2])
    with col1:
        st.markdown('<div class="section-title">Tren Bulanan PM2.5 & PM10</div>', unsafe_allow_html=True)
        monthly = df.groupby(['year','month'])[['PM2.5','PM10']].mean().reset_index()
        monthly['period'] = monthly['year'].astype(str)+'-'+monthly['month'].astype(str).str.zfill(2)
        monthly = monthly.sort_values('period')
        with plt.rc_context(DS):
            fig,ax = plt.subplots(figsize=(10,4))
            ax.plot(monthly['period'],monthly['PM2.5'],color='#e74c3c',lw=2,label='PM2.5')
            ax.plot(monthly['period'],monthly['PM10'], color='#e67e22',lw=2,label='PM10',alpha=0.8)
            ax.fill_between(monthly['period'],monthly['PM2.5'],alpha=0.15,color='#e74c3c')
            tix = list(range(0,len(monthly),6))
            ax.set_xticks([monthly['period'].iloc[i] for i in tix])
            ax.set_xticklabels([monthly['period'].iloc[i] for i in tix],rotation=30,ha='right',fontsize=8)
            ax.set_ylabel('µg/m³'); ax.legend(); ax.grid(alpha=0.2)
            fig.tight_layout(); st.pyplot(fig); plt.close()
    with col2:
        st.markdown('<div class="section-title">Distribusi AQI</div>', unsafe_allow_html=True)
        aqi_dist = df['AQI_Category'].value_counts().reindex(AQI_LABELS).fillna(0)
        aqi_pct  = aqi_dist/aqi_dist.sum()*100
        with plt.rc_context(DS):
            fig,ax = plt.subplots(figsize=(5,4))
            bars = ax.barh(AQI_LABELS,aqi_pct.values,color=[AQI_COLORS[l] for l in AQI_LABELS],edgecolor='#1e293b')
            for bar,pct in zip(bars,aqi_pct.values):
                ax.text(bar.get_width()+0.3,bar.get_y()+bar.get_height()/2,f'{pct:.1f}%',va='center',fontsize=8)
            ax.set_xlabel('%'); ax.grid(axis='x',alpha=0.2)
            fig.tight_layout(); st.pyplot(fig); plt.close()

    st.markdown('<div class="section-title">Heatmap PM2.5 — Stasiun × Jam</div>', unsafe_allow_html=True)
    pivot = df.groupby(['station','hour'])['PM2.5'].mean().unstack()
    with plt.rc_context(DS):
        fig,ax = plt.subplots(figsize=(16,5))
        sns.heatmap(pivot,cmap='YlOrRd',linewidths=0.3,ax=ax,cbar_kws={'label':'µg/m³'})
        ax.set_xlabel('Jam'); ax.set_ylabel('')
        fig.tight_layout(); st.pyplot(fig); plt.close()



# Diagram tambahan

elif menu == "Diagram tambahan":
    tab_uni,tab_multi,tab_num,tab_cat = st.tabs([
        "Univariate","Multivariate","Numerikal","Kategorikal"])

    # UNIVARIATE
    with tab_uni:
        st.markdown('<div class="section-title">Histogram & KDE — Polutan Utama</div>', unsafe_allow_html=True)
        with plt.rc_context(DS):
            fig,axes = plt.subplots(2,3,figsize=(16,8))
            for ax,col in zip(axes.flatten(),POLLUTANTS):
                data = df[col].dropna()
                ax.hist(data,bins=60,color='#3498db',alpha=0.5,edgecolor='#1e293b',density=True)
                data.plot.kde(ax=ax,color='#e74c3c',linewidth=2)
                ax.set_title(col); ax.set_xlabel("µg/m³"); ax.grid(alpha=0.2)
            fig.suptitle("Distribusi Polutan — Histogram & KDE",fontweight='bold')
            fig.tight_layout(); st.pyplot(fig); plt.close()

        st.markdown('<div class="section-title">Boxplot PM2.5 per Stasiun</div>', unsafe_allow_html=True)
        with plt.rc_context(DS):
            fig,ax = plt.subplots(figsize=(14,5))
            sts = sorted(df['station'].unique())
            bp = ax.boxplot([df[df['station']==s]['PM2.5'].dropna().values for s in sts],
                            patch_artist=True, medianprops=dict(color='white',linewidth=2))
            for patch in bp['boxes']:
                patch.set_facecolor('#e74c3c'); patch.set_alpha(0.7)
            ax.set_xticklabels(sts,rotation=30,ha='right',fontsize=8)
            ax.set_ylabel("PM2.5 (µg/m³)"); ax.grid(axis='y',alpha=0.2)
            fig.tight_layout(); st.pyplot(fig); plt.close()

        st.markdown('<div class="section-title">Violin Plot — PM2.5 per Stasiun</div>', unsafe_allow_html=True)
        with plt.rc_context(DS):
            fig,ax = plt.subplots(figsize=(14,5))
            sns.violinplot(data=df,x='station',y='PM2.5',palette='RdYlGn_r',
                           order=sorted(df['station'].unique()),ax=ax,cut=0)
            ax.set_xlabel("Stasiun"); ax.set_ylabel("PM2.5 (µg/m³)")
            ax.set_xticklabels(sorted(df['station'].unique()),rotation=30,ha='right',fontsize=8)
            ax.grid(axis='y',alpha=0.2)
            fig.tight_layout(); st.pyplot(fig); plt.close()

        st.markdown('<div class="section-title">Skewness & Kurtosis</div>', unsafe_allow_html=True)
        sk_rows = []
        for col in POLLUTANTS+METEO:
            d = df[col].dropna()
            sk = d.skew(); kt = d.kurtosis()
            shape = "Simetris" if abs(sk)<0.5 else ("Skewed Kanan" if sk>0 else "Skewed Kiri")
            sk_rows.append({'Variabel':col,'Mean':round(d.mean(),2),'Std':round(d.std(),2),
                            'Skewness':round(sk,3),'Kurtosis':round(kt,3),'Bentuk':shape})
        st.dataframe(pd.DataFrame(sk_rows),use_container_width=True,hide_index=True)

    # MULTIVARIATE
    with tab_multi:
        st.markdown('<div class="section-title">Correlation Matrix Heatmap</div>', unsafe_allow_html=True)
        corr_full = df[POLLUTANTS+METEO].corr()
        with plt.rc_context(DS):
            fig,ax = plt.subplots(figsize=(12,9))
            mask = np.triu(np.ones_like(corr_full,dtype=bool))
            sns.heatmap(corr_full,mask=mask,annot=True,fmt=".2f",cmap='RdYlGn_r',
                        center=0,linewidths=0.4,ax=ax,annot_kws={'size':8})
            ax.set_title("Correlation Matrix",fontweight='bold')
            fig.tight_layout(); st.pyplot(fig); plt.close()

        st.markdown('<div class="section-title">Scatter Plot + Regression Line</div>', unsafe_allow_html=True)
        pairs = [('TEMP','O3'),('WSPM','NO2'),('PM2.5','PM10'),('TEMP','CO')]
        with plt.rc_context(DS):
            fig,axes = plt.subplots(2,2,figsize=(14,9))
            for ax,(xc,yc) in zip(axes.flatten(),pairs):
                samp = df[[xc,yc]].dropna().sample(min(3000,len(df)),random_state=42)
                ax.scatter(samp[xc],samp[yc],alpha=0.2,s=5,color='#3498db')
                slope,intercept,r,p,_ = stats.linregress(samp[xc],samp[yc])
                xr = np.linspace(samp[xc].min(),samp[xc].max(),100)
                ax.plot(xr,slope*xr+intercept,color='#e74c3c',lw=2,
                        label=f'r={r:.3f}  p={"<0.001" if p<0.001 else f"{p:.3f}"}')
                ax.set_xlabel(xc); ax.set_ylabel(yc); ax.set_title(f"{xc} vs {yc}")
                ax.legend(fontsize=8); ax.grid(alpha=0.2)
            fig.suptitle("Scatter Plot + Regression Line",fontweight='bold')
            fig.tight_layout(); st.pyplot(fig); plt.close()

        st.markdown('<div class="section-title">Joint Plot — WSPM vs NO2</div>', unsafe_allow_html=True)
        samp_jp = df[['WSPM','NO2']].dropna().sample(min(3000,len(df)),random_state=42)
        with plt.rc_context(DS):
            g = sns.jointplot(data=samp_jp,x='WSPM',y='NO2',kind='hex',
                              color='#8e44ad',marginal_kws={'bins':40,'fill':True})
            g.figure.suptitle("Joint Plot — WSPM vs NO2",y=1.02,fontweight='bold')
            g.set_axis_labels("Kecepatan Angin (m/s)","NO2 (µg/m³)")
            st.pyplot(g.figure); plt.close()

    # NUMERIKAL
    with tab_num:
        st.markdown('<div class="section-title">Percentile Analysis</div>', unsafe_allow_html=True)
        pct_levels = [5,10,25,50,75,90,95,99]
        pct_rows = []
        for col in ['PM2.5','NO2','SO2']:
            d = df[col].dropna()
            row = {'Variabel':col}
            for lvl in pct_levels:
                row[f'P{lvl}'] = round(np.percentile(d,lvl),2)
            pct_rows.append(row)
        st.dataframe(pd.DataFrame(pct_rows),use_container_width=True,hide_index=True)

        st.markdown('<div class="section-title">Q-Q Plot — Uji Normalitas</div>', unsafe_allow_html=True)
        with plt.rc_context(DS):
            fig,axes = plt.subplots(2,3,figsize=(16,9))
            for ax,col in zip(axes.flatten(),POLLUTANTS):
                samp = df[col].dropna().sample(min(5000,len(df)),random_state=42)
                stats.probplot(samp,dist="norm",plot=ax)
                ax.set_title(f"Q-Q: {col}")
                ax.get_lines()[0].set(markersize=2,alpha=0.4,color='#3498db')
                ax.get_lines()[1].set(color='#e74c3c',linewidth=1.5)
                ax.grid(alpha=0.2)
            fig.suptitle("Q-Q Plot — Normality Check",fontweight='bold')
            fig.tight_layout(); st.pyplot(fig); plt.close()

        st.markdown('<div class="section-title">Outlier Detection — IQR Method</div>', unsafe_allow_html=True)
        out_rows = []
        for col in POLLUTANTS:
            d = df[col].dropna()
            Q1,Q3 = d.quantile(0.25),d.quantile(0.75)
            IQR = Q3-Q1; lower,upper = Q1-1.5*IQR,Q3+1.5*IQR
            n_out = ((d<lower)|(d>upper)).sum()
            out_rows.append({'Variabel':col,'Q1':round(Q1,2),'Q3':round(Q3,2),'IQR':round(IQR,2),
                             'Lower':round(lower,2),'Upper':round(upper,2),
                             'Jumlah Outlier':int(n_out),'%':round(n_out/len(d)*100,2)})
        st.dataframe(pd.DataFrame(out_rows),use_container_width=True,hide_index=True)

        st.markdown('<div class="section-title">Normality Testing — Shapiro-Wilk</div>', unsafe_allow_html=True)
        sw_rows = []
        for col in POLLUTANTS+['TEMP','WSPM']:
            samp = df[col].dropna().sample(500,random_state=42)
            stat,p = shapiro(samp)
            sw_rows.append({'Variabel':col,'W-stat':round(stat,4),'p-value':round(p,6),
                            'Normal?':'✅ Ya' if p>0.05 else '❌ Tidak'})
        st.dataframe(pd.DataFrame(sw_rows),use_container_width=True,hide_index=True)

    # KATEGORIKAL
    with tab_cat:
        df_cat = df.copy()
        st_avg2 = df_cat.groupby('station')['PM2.5'].mean()
        df_cat['Status_Polusi'] = df_cat['station'].map(
            st_avg2.apply(lambda v: 'Bahaya' if v>=100 else 'Awas' if v>=60 else 'Aman').to_dict())
        so2no2_c = df_cat.groupby('station')[['SO2','NO2']].mean()
        s2n = (so2no2_c['SO2']-so2no2_c['SO2'].min())/(so2no2_c['SO2'].max()-so2no2_c['SO2'].min())
        n2n = (so2no2_c['NO2']-so2no2_c['NO2'].min())/(so2no2_c['NO2'].max()-so2no2_c['NO2'].min())
        ri2 = (s2n*0.6+n2n*0.4)*100
        def tier2(s):
            return 'Tier Tinggi' if s>=75 else 'Tier Awas-Tinggi' if s>=50 else 'Tier Awas' if s>=25 else 'Tier Rendah'
        df_cat['Tier_Premi'] = df_cat['station'].map(ri2.apply(tier2).to_dict())
        tier_order  = ['Tier Tinggi','Tier Awas-Tinggi','Tier Awas','Tier Rendah']
        tier_clr2   = {'Tier Tinggi':'#e74c3c','Tier Awas-Tinggi':'#e67e22',
                       'Tier Awas':'#f1c40f','Tier Rendah':'#27ae60'}
        status_ord2 = ['Bahaya','Awas','Aman']
        status_clr2 = {'Bahaya':'#e74c3c','Awas':'#f39c12','Aman':'#27ae60'}

        st.markdown('<div class="section-title">Distribusi Status Polusi & Tier Premi</div>', unsafe_allow_html=True)
        col1,col2 = st.columns(2)
        with col1:
            with plt.rc_context(DS):
                fig,ax = plt.subplots(figsize=(7,5))
                sc = df_cat.groupby(['station','Status_Polusi']).size().unstack(fill_value=0)
                sc = sc.reindex(columns=[c for c in status_ord2 if c in sc.columns])
                sc.plot(kind='barh',ax=ax,color=[status_clr2[c] for c in sc.columns],edgecolor='#0f172a')
                ax.set_xlabel("Jumlah Jam"); ax.legend(title='Status'); ax.grid(axis='x',alpha=0.2)
                fig.tight_layout(); st.pyplot(fig); plt.close()
        with col2:
            with plt.rc_context(DS):
                fig,ax = plt.subplots(figsize=(7,5))
                tc = df_cat['Tier_Premi'].value_counts().reindex(tier_order,fill_value=0)
                bars = ax.bar(tc.index,tc.values,color=[tier_clr2[t] for t in tc.index],edgecolor='#0f172a')
                for bar,val in zip(bars,tc.values):
                    ax.text(bar.get_x()+bar.get_width()/2,bar.get_height()+500,f'{val:,}',ha='center',fontsize=8)
                ax.set_xticklabels(tc.index,rotation=15,ha='right')
                ax.set_ylabel("Jumlah Jam"); ax.grid(axis='y',alpha=0.2)
                fig.tight_layout(); st.pyplot(fig); plt.close()

        st.markdown('<div class="section-title">Boxplot & Violin per Kategori</div>', unsafe_allow_html=True)
        col1,col2 = st.columns(2)
        with col1:
            with plt.rc_context(DS):
                fig,ax = plt.subplots(figsize=(7,5))
                sns.boxplot(data=df_cat,x='Status_Polusi',y='PM2.5',
                            order=status_ord2,palette=status_clr2,ax=ax)
                ax.set_title("PM2.5 per Status Polusi"); ax.grid(axis='y',alpha=0.2)
                fig.tight_layout(); st.pyplot(fig); plt.close()
        with col2:
            with plt.rc_context(DS):
                fig,ax = plt.subplots(figsize=(7,5))
                sns.violinplot(data=df_cat,x='Tier_Premi',y='NO2',
                               order=tier_order,palette=tier_clr2,ax=ax,cut=0)
                ax.set_xticklabels(tier_order,rotation=15,ha='right',fontsize=8)
                ax.set_title("NO2 per Tier Premi"); ax.grid(axis='y',alpha=0.2)
                fig.tight_layout(); st.pyplot(fig); plt.close()

        st.markdown('<div class="section-title">ANOVA Test</div>', unsafe_allow_html=True)
        g_st = [df_cat[df_cat['station']==s]['PM2.5'].dropna().values for s in df_cat['station'].unique()]
        f1,p1 = f_oneway(*g_st)
        g_ti = [df_cat[df_cat['Tier_Premi']==t]['NO2'].dropna().values
                for t in tier_order if t in df_cat['Tier_Premi'].unique()]
        f2,p2 = f_oneway(*g_ti)
        anova_df = pd.DataFrame([
            {'Uji':'PM2.5 antar Stasiun','F-stat':round(f1,4),'p-value':round(p1,8),
             'Kesimpulan':'✅ Signifikan' if p1<0.05 else '❌ Tidak Signifikan'},
            {'Uji':'NO2 antar Tier Premi','F-stat':round(f2,4),'p-value':round(p2,8),
             'Kesimpulan':'✅ Signifikan' if p2<0.05 else '❌ Tidak Signifikan'},
        ])
        st.dataframe(anova_df,use_container_width=True,hide_index=True)

# PERTANYAAN 1
elif menu == "Pertanyaan 1 — Lalu Lintas":
    st.markdown('<div class="section-title"> Manajemen Lalu Lintas — Q4 2016 hingga Q1 2017</div>', unsafe_allow_html=True)
    st.markdown("""<div class="insight-box">
    Bagaimana mengintegrasikan data historis PM2.5 & PM10 ke dalam sistem manajemen lalu lintas
    untuk membatasi kendaraan pada <b>Q4 2016 (Okt–Des) hingga Q1 2017 (Jan–Mar)</b>?
    </div>""", unsafe_allow_html=True)

    df_p1 = df_raw[
        ((df_raw['year']==2016)&(df_raw['month'].isin([10,11,12]))) |
        ((df_raw['year']==2017)&(df_raw['month'].isin([1,2,3])))
    ].copy()

    sp = df_p1.groupby('station')[['PM2.5','PM10']].mean().round(2)
    sp['Avg_Particulate'] = (sp['PM2.5']+sp['PM10'])/2
    sp['Status'] = sp['Avg_Particulate'].apply(lambda v: 'Bahaya' if v>=100 else 'Awas' if v>=60 else 'Aman')
    ss = sp.sort_values('Avg_Particulate', ascending=False)

    c1,c2,c3 = st.columns(3)
    for col,status,clr,note in zip([c1,c2,c3],
        ['Bahaya','Awas','Aman'],['#e74c3c','#f39c12','#27ae60'],['≥ 100 µg/m³','60–100 µg/m³','< 60 µg/m³']):
        n = (sp['Status']==status).sum()
        with col:
            st.markdown(f"""<div class="metric-card" style="border-left:4px solid {clr}">
                <div class="label">Zona {status}</div>
                <div class="value">{n}</div>
                <div class="sub">{note}</div></div>""", unsafe_allow_html=True)

    st.markdown("")
    col1,col2 = st.columns(2)
    zcm = {'Bahaya':'#e74c3c','Awas':'#f39c12','Aman':'#27ae60'}
    with col1:
        st.markdown('<div class="section-title">Klasifikasi Zona per Stasiun</div>', unsafe_allow_html=True)
        with plt.rc_context(DS):
            fig,ax = plt.subplots(figsize=(7,5))
            ax.barh(ss.index,ss['Avg_Particulate'],color=[zcm[s] for s in ss['Status']])
            ax.axvline(100,color='red',   linestyle='--',lw=1.2,label='Batas Bahaya')
            ax.axvline(60, color='orange',linestyle='--',lw=1.2,label='Batas Awas')
            ax.set_xlabel('µg/m³'); ax.invert_yaxis()
            ax.legend(fontsize=8); ax.grid(alpha=0.2)
            fig.tight_layout(); st.pyplot(fig); plt.close()
    with col2:
        st.markdown('<div class="section-title">Pola Polusi per Jam</div>', unsafe_allow_html=True)
        hp = df_p1.groupby('hour')[['PM2.5','PM10']].mean()
        pk = hp['PM2.5'].quantile(0.75)
        with plt.rc_context(DS):
            fig,ax = plt.subplots(figsize=(7,5))
            ax.plot(hp.index,hp['PM2.5'],color='#e74c3c',lw=2,label='PM2.5')
            ax.plot(hp.index,hp['PM10'], color='#e67e22',lw=2,label='PM10')
            ax.fill_between(hp.index,hp['PM2.5'],alpha=0.15,color='#e74c3c')
            for h in hp[hp['PM2.5']>=pk].index:
                ax.axvspan(h-0.4,h+0.4,alpha=0.08,color='red')
            ax.set_xlabel('Jam'); ax.set_ylabel('µg/m³')
            ax.set_xticks(range(0,24)); ax.legend(); ax.grid(alpha=0.2)
            fig.tight_layout(); st.pyplot(fig); plt.close()

    st.markdown('<div class="section-title">Rekomendasi Manajemen Lalu Lintas</div>', unsafe_allow_html=True)
    ss['Rekomendasi'] = ss['Status'].apply(
        lambda s: '🔴 Ganjil-genap + Larangan truk besar' if s=='Bahaya'
                  else '🟡 Pantau real-time + Siaga pengalihan' if s=='Awas'
                  else '🟢 Normal, monitoring rutin')
    st.dataframe(ss[['PM2.5','PM10','Avg_Particulate','Status','Rekomendasi']].round(2).head(n_rows),
                 use_container_width=True)
    st.markdown("""<div class="insight-box">
    <b>Insight:</b> <b>Gucheng</b> satu-satunya zona Bahaya (101.67 µg/m³) selama Q4 2016–Q1 2017.
    Tidak ada stasiun aman — seluruh Beijing di zona Awas saat musim dingin.
    Jam kritis: <b>pukul 20.00–01.00</b> (pola dua puncak polusi harian).
    </div>""", unsafe_allow_html=True)

# PERTANYAAN 2

elif menu == "Pertanyaan 2 — Logistik":
    st.markdown('<div class="section-title"> Korelasi Meteorologi & Polusi pada Jam 06.00–22.00</div>', unsafe_allow_html=True)
    st.markdown("""<div class="insight-box">
    Bagaimana mengukur korelasi meteorologi vs polusi untuk mengalihkan rute pengiriman
    selama <b>jam operasional puncak 06.00–22.00</b>?
    </div>""", unsafe_allow_html=True)

    df_p2 = df_raw[(df_raw['hour']>=6)&(df_raw['hour']<=22)].copy()
    df_p2['Risk_Score'] = (
        df_p2['PM2.5']*0.4+df_p2['PM10']*0.2+df_p2['NO2']*0.2+df_p2['CO']*0.1+df_p2['SO2']*0.1
    )/df_p2['WSPM'].replace(0,0.1)

    corr2  = df_p2[METEO+POLLUTANTS].corr().loc[METEO,POLLUTANTS]
    sh2    = df_p2.groupby('hour')['Risk_Score'].mean()
    safest2  = sorted(sh2.nsmallest(5).index.tolist())
    riskiest2= sorted(sh2.nlargest(5).index.tolist())
    sr2 = df_p2.groupby('station')['Risk_Score'].mean().sort_values()

    c1,c2,c3 = st.columns(3)
    with c1:
        st.markdown(f"""<div class="metric-card">
            <div class="label">Jam Paling Aman</div>
            <div class="value" style="font-size:1.1rem">{safest2}</div>
            <div class="sub">untuk pengiriman</div></div>""", unsafe_allow_html=True)
    with c2:
        st.markdown(f"""<div class="metric-card">
            <div class="label">Jam Paling Berisiko</div>
            <div class="value" style="font-size:1.1rem">{riskiest2}</div>
            <div class="sub">hindari pengiriman</div></div>""", unsafe_allow_html=True)
    with c3:
        st.markdown(f"""<div class="metric-card">
            <div class="label">Rute Paling Aman</div>
            <div class="value" style="font-size:1.2rem">{sr2.index[0]}</div>
            <div class="sub">Risk Score: {sr2.iloc[0]:.1f}</div></div>""", unsafe_allow_html=True)

    st.markdown("")
    col1,col2 = st.columns(2)
    with col1:
        st.markdown('<div class="section-title">Heatmap Korelasi (06.00–22.00)</div>', unsafe_allow_html=True)
        with plt.rc_context(DS):
            fig,ax = plt.subplots(figsize=(7,4))
            sns.heatmap(corr2,annot=True,fmt='.2f',cmap='RdYlGn_r',center=0,linewidths=0.5,ax=ax,annot_kws={'size':9})
            fig.tight_layout(); st.pyplot(fig); plt.close()
    with col2:
        st.markdown('<div class="section-title">Indeks Risiko per Jam</div>', unsafe_allow_html=True)
        with plt.rc_context(DS):
            fig,ax = plt.subplots(figsize=(7,4))
            ax.plot(sh2.index,sh2.values,color='#8e44ad',lw=2)
            ax.fill_between(sh2.index,sh2.values,alpha=0.2,color='#8e44ad')
            for h in safest2:
                ax.axvline(h,color='#27ae60',linestyle='--',alpha=0.7,
                           label='Jam Aman' if h==safest2[0] else '')
            ax.set_xlabel('Jam'); ax.set_ylabel('Risk Score')
            ax.set_xticks(range(6,23)); ax.legend(); ax.grid(alpha=0.2)
            fig.tight_layout(); st.pyplot(fig); plt.close()

    st.markdown('<div class="section-title">Ranking Risiko Stasiun (06.00–22.00)</div>', unsafe_allow_html=True)
    with plt.rc_context(DS):
        fig,ax = plt.subplots(figsize=(12,4))
        clrs = ['#27ae60' if i<3 else '#e67e22' if i<9 else '#e74c3c' for i in range(len(sr2))]
        ax.barh(sr2.index,sr2.values,color=clrs)
        ax.invert_yaxis(); ax.set_xlabel('Risk Score'); ax.grid(alpha=0.2)
        fig.tight_layout(); st.pyplot(fig); plt.close()

    st.markdown("""<div class="insight-box">
    <b>Insight:</b> <b>WSPM</b> faktor terkuat (r=-0.396 vs NO2).
    Pukul <b>06.00 pagi berisiko tinggi</b> — polutan malam belum terdispersi.
    Jadwalkan pengiriman pukul <b>12.00–16.00</b> via <b>Dingling & Huairou</b>.
    </div>""", unsafe_allow_html=True)

# PERTANYAAN 3

elif menu == "Pertanyaan 3 — Asuransi":
    st.markdown('<div class="section-title"> Proyeksi Klaim Asuransi pada Musim Dingin 2016</div>', unsafe_allow_html=True)
    st.markdown("""<div class="insight-box">
    Bagaimana menganalisis fluktuasi SO2 & NO2 selama <b>musim dingin 2016</b>
    untuk memproyeksikan lonjakan klaim dan merancang struktur premi?
    </div>""", unsafe_allow_html=True)

    df_p3 = df_raw[
        ((df_raw['year']==2015)&(df_raw['month'].isin([11,12]))) |
        ((df_raw['year']==2016)&(df_raw['month'].isin([1,2,11,12]))) |
        ((df_raw['year']==2017)&(df_raw['month'].isin([1,2])))
    ].copy()
    df_p3['period_label'] = df_p3['year'].astype(str)+'-'+df_p3['month'].astype(str).str.zfill(2)

    sn3 = df_p3.groupby('station')[['SO2','NO2']].mean()
    s2n3 = (sn3['SO2']-sn3['SO2'].min())/(sn3['SO2'].max()-sn3['SO2'].min())
    n2n3 = (sn3['NO2']-sn3['NO2'].min())/(sn3['NO2'].max()-sn3['NO2'].min())
    ri3  = (s2n3*0.6+n2n3*0.4)*100
    BASE3 = 500_000
    def ti3(s):
        if s>=75:   return 'Tinggi',    '#e74c3c',BASE3*2.0
        elif s>=50: return 'Awas-Tinggi','#e67e22',BASE3*1.5
        elif s>=25: return 'Awas',      '#f1c40f',BASE3*1.2
        else:       return 'Rendah',    '#27ae60',BASE3*1.0
    pr3 = pd.DataFrame({'Risk Index':ri3.round(1)})
    pr3['Tier']        = pr3['Risk Index'].apply(lambda x: ti3(x)[0])
    pr3['Premi/Bulan'] = pr3['Risk Index'].apply(lambda x: f"Rp {ti3(x)[2]:,.0f}")
    pr3 = pr3.sort_values('Risk Index', ascending=False)

    c1,c2,c3,c4 = st.columns(4)
    for col,tier,clr,premi in zip([c1,c2,c3,c4],
        ['Tinggi','Awas-Tinggi','Awas','Rendah'],
        ['#e74c3c','#e67e22','#f1c40f','#27ae60'],
        ['Rp 1.000.000','Rp 750.000','Rp 600.000','Rp 500.000']):
        n = (pr3['Tier']==tier).sum()
        with col:
            st.markdown(f"""<div class="metric-card" style="border-left:4px solid {clr}">
                <div class="label">{tier}</div>
                <div class="value">{n} stasiun</div>
                <div class="sub">{premi}/bulan</div></div>""", unsafe_allow_html=True)

    st.markdown("")
    col1,col2 = st.columns(2)
    with col1:
        st.markdown('<div class="section-title">Risk Index per Stasiun</div>', unsafe_allow_html=True)
        ri3s = ri3.sort_values(ascending=False)
        with plt.rc_context(DS):
            fig,ax = plt.subplots(figsize=(7,5))
            clrs = ['#e74c3c' if s>=75 else '#e67e22' if s>=50 else '#f1c40f' if s>=25 else '#27ae60' for s in ri3s]
            ax.bar(ri3s.index,ri3s.values,color=clrs,edgecolor='#0f172a')
            ax.axhline(75,color='red',   linestyle='--',lw=1,label='Tier Tinggi')
            ax.axhline(50,color='orange',linestyle='--',lw=1,label='Tier Awas-Tinggi')
            ax.axhline(25,color='gold',  linestyle='--',lw=1,label='Tier Awas')
            ax.set_xticklabels(ri3s.index,rotation=40,ha='right',fontsize=8)
            ax.set_ylabel('Risk Index (0-100)'); ax.legend(fontsize=8); ax.grid(axis='y',alpha=0.2)
            fig.tight_layout(); st.pyplot(fig); plt.close()
    with col2:
        st.markdown('<div class="section-title">Tren Bulanan SO2 & NO2</div>', unsafe_allow_html=True)
        mt3 = df_p3.groupby('period_label')[['SO2','NO2']].mean().sort_index()
        with plt.rc_context(DS):
            fig,ax = plt.subplots(figsize=(7,5))
            ax.plot(mt3.index,mt3['SO2'].values,color='#c0392b',lw=2,marker='o',label='SO2')
            ax.plot(mt3.index,mt3['NO2'].values,color='#2980b9',lw=2,marker='s',label='NO2')
            ax.set_xticklabels(mt3.index,rotation=30,ha='right',fontsize=8)
            ax.set_ylabel('µg/m³'); ax.legend(); ax.grid(alpha=0.2)
            fig.tight_layout(); st.pyplot(fig); plt.close()

    st.markdown('<div class="section-title">Struktur Premi per Stasiun</div>', unsafe_allow_html=True)
    st.dataframe(pr3.head(n_rows),use_container_width=True)
    st.markdown("""<div class="insight-box">
    <b>Insight:</b> <b>Wanliu</b> Risk Index 97.0 → premi tertinggi Rp 1.000.000/bulan.
    <b>Desember</b> = puncak NO2 (77.50 µg/m³ di 2016) — bulan klaim tertinggi.
    Cadangan klaim <b>20–30% lebih besar</b> pada Oktober–Maret.
    </div>""", unsafe_allow_html=True)

# ANALISIS LANJUTAN

elif menu == "Analisis Lanjutan":
    tab1,tab2,tab3,tab4 = st.tabs([
        "RFM Analysis","Manual Grouping","Geospatial","AQI Binning"])

    with tab1:
        st.markdown('<div class="section-title">RFM-Style Analysis — Risiko Polusi PM2.5</div>', unsafe_allow_html=True)
        st.markdown("""<div class="insight-box">
        <b>Recency</b> = hari sejak spike terakhir |
        <b>Frequency</b> = hari terjadi spike (PM2.5 > 150 µg/m³) |
        <b>Magnitude</b> = rata-rata PM2.5 saat spike
        </div>""", unsafe_allow_html=True)

        df_rfm = df.copy()
        df_rfm['date']     = df_rfm['datetime'].dt.date
        df_rfm['is_spike'] = df_rfm['PM2.5']>150
        sp_df = df_rfm[df_rfm['is_spike']]
        ref_d = pd.to_datetime(df_rfm['date'].max())
        rfm_l = []
        for stn,grp in sp_df.groupby('station'):
            rfm_l.append({'station':stn,
                          'Recency':(ref_d-pd.to_datetime(grp['date'].max())).days,
                          'Frequency':grp['date'].nunique(),
                          'Magnitude':round(grp['PM2.5'].mean(),2)})
        rfm = pd.DataFrame(rfm_l).set_index('station')
        rb = pd.qcut(rfm['Recency'],  q=3,labels=False,duplicates='drop')
        fb = pd.qcut(rfm['Frequency'],q=3,labels=False,duplicates='drop')
        mb = pd.qcut(rfm['Magnitude'],q=3,labels=False,duplicates='drop')
        rfm['R_score']   = (rb.max()-rb+1).astype(int)
        rfm['F_score']   = (fb+1).astype(int)
        rfm['M_score']   = (mb+1).astype(int)
        rfm['RFM_Total'] = rfm['R_score']+rfm['F_score']+rfm['M_score']
        rfm['Segment']   = rfm['RFM_Total'].apply(
            lambda s: 'Zona Kritis' if s>=8 else 'Zona Berbahaya' if s>=6
                      else 'Zona Waspada' if s>=4 else 'Zona Aman')
        rfm_s = rfm.sort_values('RFM_Total',ascending=False)
        sc_rfm = {'Zona Kritis':'#e74c3c','Zona Berbahaya':'#e67e22',
                  'Zona Waspada':'#f1c40f','Zona Aman':'#27ae60'}
        clrs_rfm = [sc_rfm[rfm_s.loc[s,'Segment']] for s in rfm_s.index]
        with plt.rc_context(DS):
            fig,axes = plt.subplots(1,3,figsize=(16,5))
            fig.suptitle("RFM Analysis",fontweight='bold')
            for ax,(lbl,col) in zip(axes,[('Recency (hari)','Recency'),
                                          ('Frequency (hari spike)','Frequency'),
                                          ('Magnitude (µg/m³)','Magnitude')]):
                ax.barh(rfm_s.index,rfm_s[col],color=clrs_rfm)
                ax.set_title(lbl); ax.invert_yaxis(); ax.grid(alpha=0.2)
            hnd = [mpatches.Patch(color=c,label=l) for l,c in sc_rfm.items()]
            fig.legend(handles=hnd,loc='lower center',ncol=4,fontsize=9,bbox_to_anchor=(0.5,-0.04))
            fig.tight_layout(); st.pyplot(fig); plt.close()
        st.dataframe(rfm_s.head(n_rows),use_container_width=True)

    with tab2:
        st.markdown('<div class="section-title">Clustering Manual Grouping</div>', unsafe_allow_html=True)
        prf = df.groupby('station').agg(
            PM25_mean=('PM2.5','mean'),PM10_mean=('PM10','mean'),
            NO2_mean=('NO2','mean'),  SO2_mean=('SO2','mean'),
        ).round(2)
        def ag2(row):
            if row['PM25_mean']>80 and row['NO2_mean']>60: return 'Klaster A — Polusi Tinggi'
            elif row['PM25_mean']>60 and row['NO2_mean']>45: return 'Klaster B — Polusi SDiagram tambahanng'
            elif row['PM25_mean']>50: return 'Klaster C — Polusi Rendah-SDiagram tambahanng'
            else: return 'Klaster D — Polusi Rendah'
        prf['Klaster'] = prf.apply(ag2,axis=1)
        ps2 = prf.sort_values('PM25_mean',ascending=False)
        kc = {'Klaster A — Polusi Tinggi':'#e74c3c','Klaster B — Polusi SDiagram tambahanng':'#e67e22',
              'Klaster C — Polusi Rendah-SDiagram tambahanng':'#f1c40f','Klaster D — Polusi Rendah':'#27ae60'}
        col1,col2 = st.columns(2)
        with col1:
            with plt.rc_context(DS):
                fig,ax = plt.subplots(figsize=(7,5))
                ax.barh(ps2.index,ps2['PM25_mean'],color=[kc[ps2.loc[s,'Klaster']] for s in ps2.index])
                ax.axvline(80,color='red',   linestyle='--',lw=1,label='Batas A')
                ax.axvline(60,color='orange',linestyle='--',lw=1,label='Batas B')
                ax.axvline(50,color='gold',  linestyle='--',lw=1,label='Batas C')
                ax.set_xlabel('PM2.5 µg/m³'); ax.invert_yaxis()
                ax.legend(fontsize=8); ax.grid(alpha=0.2)
                fig.tight_layout(); st.pyplot(fig); plt.close()
        with col2:
            with plt.rc_context(DS):
                fig,ax = plt.subplots(figsize=(7,5))
                for stn,row in prf.iterrows():
                    ax.scatter(row['PM25_mean'],row['NO2_mean'],color=kc[row['Klaster']],s=120,zorder=3)
                    ax.annotate(stn,(row['PM25_mean'],row['NO2_mean']),fontsize=7,xytext=(3,3),textcoords='offset points')
                ax.set_xlabel('PM2.5'); ax.set_ylabel('NO2')
                hnd2 = [mpatches.Patch(color=c,label=l) for l,c in kc.items()]
                ax.legend(handles=hnd2,fontsize=7); ax.grid(alpha=0.2)
                fig.tight_layout(); st.pyplot(fig); plt.close()
        st.dataframe(ps2.head(n_rows),use_container_width=True)

    with tab3:
        st.markdown('<div class="section-title">Peta Distribusi Polusi per Stasiun</div>', unsafe_allow_html=True)
        sa = df.groupby('station').agg(
            PM25=('PM2.5','mean'),PM10=('PM10','mean'),
            NO2=('NO2','mean'),  SO2=('SO2','mean'),
            CO=('CO','mean'),    O3=('O3','mean'),
        ).round(2)
        def mkc(v): return 'red' if v>80 else 'orange' if v>60 else 'beige' if v>50 else 'green'
        m = folium.Map(location=[39.95,116.39],zoom_start=10,tiles='CartoDB positron')
        hd = []
        for stn,row in sa.iterrows():
            if stn not in STATION_COORDS: continue
            lat,lon = STATION_COORDS[stn]; clr = mkc(row['PM25'])
            folium.CircleMarker([lat,lon],radius=row['PM25']*0.35,color=clr,fill=True,
                                fill_color=clr,fill_opacity=0.45,weight=1.5).add_to(m)
            ph = f"""<div style="font-family:Arial;font-size:12px;width:190px">
                <b>{stn}</b><hr>PM2.5:<b>{row['PM25']} µg/m³</b><br>
                PM10:{row['PM10']} | NO2:{row['NO2']}<br>SO2:{row['SO2']} | CO:{row['CO']} | O3:{row['O3']}
            </div>"""
            folium.Marker([lat,lon],popup=folium.Popup(ph,max_width=210),
                          tooltip=f"{stn}|PM2.5:{row['PM25']}",
                          icon=folium.Icon(color=clr,icon='cloud',prefix='fa')).add_to(m)
            hd.append([lat,lon,row['PM25']])
        HeatMap(hd,radius=40,blur=25,min_opacity=0.3,
                gradient={0.4:'blue',0.65:'lime',0.85:'orange',1.0:'red'}).add_to(m)
        st_folium(m,width=None,height=500)
        st.markdown("""<div class="insight-box">
        Klik marker untuk detail polutan. Lingkaran lebih besar = PM2.5 lebih tinggi.
        </div>""", unsafe_allow_html=True)

    with tab4:
        st.markdown('<div class="section-title">Clustering Binning — Kategori AQI PM2.5</div>', unsafe_allow_html=True)
        db = df.copy()
        db['AQI_Category'] = pd.cut(db['PM2.5'],bins=AQI_BINS,labels=AQI_LABELS,right=True)
        gd = db['AQI_Category'].value_counts().reindex(AQI_LABELS).fillna(0)
        gp = (gd/gd.sum()*100).round(2)
        col1,col2 = st.columns(2)
        with col1:
            with plt.rc_context(DS):
                fig,ax = plt.subplots(figsize=(7,5))
                ax.barh(AQI_LABELS,gp.values,color=[AQI_COLORS[l] for l in AQI_LABELS],edgecolor='#0f172a')
                for i,pct in enumerate(gp.values):
                    ax.text(pct+0.3,i,f'{pct:.1f}%',va='center',fontsize=9)
                ax.set_xlabel('%'); ax.set_title('Distribusi AQI Global'); ax.grid(axis='x',alpha=0.2)
                fig.tight_layout(); st.pyplot(fig); plt.close()
        with col2:
            sd = (db.groupby(['station','AQI_Category'],observed=True)
                    .size().unstack(fill_value=0).reindex(columns=AQI_LABELS,fill_value=0))
            sp4 = sd.div(sd.sum(axis=1),axis=0)*100
            with plt.rc_context(DS):
                fig,ax = plt.subplots(figsize=(7,5))
                bt = np.zeros(len(sp4))
                for cat in AQI_LABELS:
                    vals = sp4[cat].values if cat in sp4.columns else np.zeros(len(sp4))
                    ax.bar(sp4.index,vals,bottom=bt,color=AQI_COLORS[cat],label=cat,edgecolor='#0f172a',lw=0.3)
                    bt += vals
                ax.set_xticklabels(sp4.index,rotation=35,ha='right',fontsize=8)
                ax.set_ylabel('%'); ax.legend(fontsize=7,loc='upper right'); ax.grid(axis='y',alpha=0.2)
                fig.tight_layout(); st.pyplot(fig); plt.close()
        smry = pd.DataFrame({'Kategori':AQI_LABELS,'Jumlah Jam':gd.values.astype(int),'%':gp.values})
        st.dataframe(smry.head(n_rows),use_container_width=True,hide_index=True)