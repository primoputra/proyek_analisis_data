from pathlib import Path
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Atur judul tab browser, icon, dan layout full width
st.set_page_config(page_title="Bike Sharing Dashboard", page_icon="🚲", layout="wide")

# Load data menggunakan Path(__file__).parent agar aman dijalankan dari folder manapun
@st.cache_data
def load_data():
    data_path = Path(__file__).parent / "main_data.csv"
    data = pd.read_csv(data_path, parse_dates=["dteday"])
    return data

df = load_data()

# ==================== SIDEBAR FILTER ====================
st.sidebar.title("Bike Sharing Dashboard")
st.sidebar.markdown("Filter data di bawah ini untuk memperbarui seluruh metrik dan visualisasi:")
st.sidebar.markdown("---")

# Filter musim
season_filter = st.sidebar.multiselect(
    "Pilih Musim",
    options=df["season"].unique(),
    default=df["season"].unique()
)

# Filter kondisi cuaca
weather_filter = st.sidebar.multiselect(
    "Pilih Kondisi Cuaca",
    options=df["weathersit"].unique(),
    default=df["weathersit"].unique()
)

# Filter tahun
year_filter = st.sidebar.multiselect(
    "Pilih Tahun",
    options=sorted(df["yr"].unique()),
    default=sorted(df["yr"].unique())
)

# Terapkan filter ke seluruh dataset
filtered_df = df[
    (df["season"].isin(season_filter)) &
    (df["weathersit"].isin(weather_filter)) &
    (df["yr"].isin(year_filter))
]

if filtered_df.empty:
    st.warning("Tidak ada data yang sesuai dengan kombinasi filter yang dipilih. Silakan pilih minimal satu opsi pada setiap filter.")
    st.stop()

# Agregasi tingkat harian dari data yang sudah difilter (untuk metrik harian & Pertanyaan 1)
daily_filtered_df = filtered_df.groupby(
    ["dteday", "season", "weathersit", "yr", "temp_category", "day_cluster"],
    as_index=False
)[["casual", "registered", "cnt"]].sum()

st.sidebar.markdown("---")
st.sidebar.markdown(f"**Total Data Terfilter:** {len(daily_filtered_df)} hari ({len(filtered_df):,} jam)")

# ==================== HEADER DASHBOARD ====================
st.title("🚲 Bike Sharing Dashboard (2011–2012)")
st.markdown("Analisis perbedaan rata-rata penyewaan sepeda harian berdasarkan musim & cuaca, serta pola jam puncak pengguna *casual* vs *registered*.")
st.markdown("---")

# ==================== METRICS CARD ====================
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Total Penyewaan", f"{filtered_df['cnt'].sum():,}")
with col2:
    st.metric("Rata-Rata Penyewaan Harian", f"{daily_filtered_df['cnt'].mean():,.0f}")
with col3:
    st.metric("Total Penyewa Registered", f"{filtered_df['registered'].sum():,}")
with col4:
    st.metric("Total Penyewa Casual", f"{filtered_df['casual'].sum():,}")

st.markdown("---")

# ==================== PERTANYAAN 1: MUSIM & CUACA ====================
st.subheader("Pertanyaan 1: Rata-Rata Penyewaan Harian Berdasarkan Musim dan Cuaca")
col_left, col_right = st.columns(2)

# Grafik kiri: Bar chart rata-rata penyewaan per musim
with col_left:
    st.markdown("**Rata-Rata Penyewaan Harian per Musim**")
    season_avg = daily_filtered_df.groupby("season")["cnt"].mean().sort_values(ascending=False).reset_index()
    fig1, ax1 = plt.subplots(figsize=(8, 5))
    sns.barplot(data=season_avg, x="season", y="cnt", ax=ax1, palette="Set2", hue="season", legend=False)
    ax1.set_xlabel("Musim")
    ax1.set_ylabel("Rata-Rata Penyewaan (Sepeda/Hari)")
    ax1.set_title("Rata-Rata Penyewaan per Musim")
    for i, v in enumerate(season_avg["cnt"]):
        ax1.text(i, v + (season_avg["cnt"].max() * 0.02), f"{v:.0f}", ha="center", fontsize=10)
    st.pyplot(fig1)

# Grafik kanan: Bar chart rata-rata penyewaan per kondisi cuaca
with col_right:
    st.markdown("**Rata-Rata Penyewaan Harian per Kondisi Cuaca**")
    weather_avg = daily_filtered_df.groupby("weathersit")["cnt"].mean().sort_values(ascending=False).reset_index()
    fig2, ax2 = plt.subplots(figsize=(8, 5))
    sns.barplot(data=weather_avg, x="weathersit", y="cnt", ax=ax2, palette="coolwarm", hue="weathersit", legend=False)
    ax2.set_xlabel("Kondisi Cuaca")
    ax2.set_ylabel("Rata-Rata Penyewaan (Sepeda/Hari)")
    ax2.set_title("Rata-Rata Penyewaan per Kondisi Cuaca")
    ax2.tick_params(axis="x", rotation=15)
    for i, v in enumerate(weather_avg["cnt"]):
        ax2.text(i, v + (weather_avg["cnt"].max() * 0.02), f"{v:.0f}", ha="center", fontsize=10)
    st.pyplot(fig2)

# Heatmap: silang musim vs cuaca (menggunakan rata-rata harian)
st.markdown("**Heatmap: Rata-Rata Penyewaan Harian (Musim vs Cuaca)**")
pivot_data = daily_filtered_df.pivot_table(index="season", columns="weathersit", values="cnt", aggfunc="mean")
fig3, ax3 = plt.subplots(figsize=(10, 4.5))
sns.heatmap(pivot_data, annot=True, fmt=".0f", cmap="YlGnBu", linewidths=0.5, ax=ax3)
ax3.set_xlabel("Kondisi Cuaca")
ax3.set_ylabel("Musim")
st.pyplot(fig3)

st.markdown("---")

# ==================== PERTANYAAN 2: POLA JAM ====================
st.subheader("Pertanyaan 2: Pola Jam Puncak Penggunaan (Casual vs Registered)")

# Agregasi rata-rata per jam dari filtered_df (sehingga ikut ter-update oleh semua filter!)
hourly_usage = filtered_df.groupby(["workingday", "hr"])[["casual", "registered", "cnt"]].mean().reset_index()
col_wd, col_hol = st.columns(2)

# Grafik kiri: pola jam di hari kerja
with col_wd:
    st.markdown("**Hari Kerja (Working Day)**")
    wd_data = hourly_usage[hourly_usage["workingday"] == "Working Day"]
    fig4, ax4 = plt.subplots(figsize=(8, 5))
    if not wd_data.empty:
        ax4.plot(wd_data["hr"], wd_data["registered"], color="#2E86C1", label="Registered", linewidth=2)
        ax4.plot(wd_data["hr"], wd_data["casual"], color="#E67E22", label="Casual", linewidth=2)
    ax4.set_xlabel("Jam")
    ax4.set_ylabel("Rata-Rata Penyewaan (Sepeda/Jam)")
    ax4.set_title("Pola Penyewaan per Jam - Hari Kerja")
    ax4.set_xticks(range(0, 24))
    ax4.legend()
    st.pyplot(fig4)

# Grafik kanan: pola jam di hari libur / akhir pekan
with col_hol:
    st.markdown("**Hari Libur / Akhir Pekan (Holiday/Weekend)**")
    hol_data = hourly_usage[hourly_usage["workingday"] == "Holiday/Weekend"]
    fig5, ax5 = plt.subplots(figsize=(8, 5))
    if not hol_data.empty:
        ax5.plot(hol_data["hr"], hol_data["registered"], color="#2E86C1", label="Registered", linewidth=2)
        ax5.plot(hol_data["hr"], hol_data["casual"], color="#E67E22", label="Casual", linewidth=2)
    ax5.set_xlabel("Jam")
    ax5.set_ylabel("Rata-Rata Penyewaan (Sepeda/Jam)")
    ax5.set_title("Pola Penyewaan per Jam - Hari Libur / Akhir Pekan")
    ax5.set_xticks(range(0, 24))
    ax5.legend()
    st.pyplot(fig5)

st.markdown("---")

# ==================== ANALISIS LANJUTAN ====================
st.subheader("Analisis Lanjutan: Binning Suhu & Clustering Hari")
col_bin, col_clust = st.columns(2)

# Grafik kiri: hasil binning kategori suhu
with col_bin:
    st.markdown("**Rata-Rata Penyewaan Harian Berdasarkan Kategori Suhu**")
    temp_order = ['Dingin (< 10°C)', 'Sejuk (10-20°C)', 'Hangat (20-30°C)', 'Panas (> 30°C)']
    temp_data = daily_filtered_df.groupby("temp_category", observed=True)["cnt"].mean().reindex(temp_order).dropna().reset_index()
    fig6, ax6 = plt.subplots(figsize=(8, 5))
    sns.barplot(data=temp_data, x="temp_category", y="cnt", ax=ax6, palette="RdYlBu_r", hue="temp_category", legend=False)
    ax6.set_xlabel("Kategori Suhu")
    ax6.set_ylabel("Rata-Rata Penyewaan (Sepeda/Hari)")
    ax6.set_title("Rata-Rata Penyewaan per Kategori Suhu")
    ax6.tick_params(axis="x", rotation=15)
    for i, v in enumerate(temp_data["cnt"]):
        ax6.text(i, v + (temp_data["cnt"].max() * 0.02), f"{v:.0f}", ha="center", fontsize=10)
    st.pyplot(fig6)

# Grafik kanan: hasil clustering hari
with col_clust:
    st.markdown("**Clustering Hari Berdasarkan Pola Penggunaan**")
    cluster_data = daily_filtered_df.groupby("day_cluster")["cnt"].mean().sort_values(ascending=False).reset_index()
    fig7, ax7 = plt.subplots(figsize=(8, 5))
    sns.barplot(data=cluster_data, y="day_cluster", x="cnt", ax=ax7, palette="viridis", hue="day_cluster", legend=False)
    ax7.set_xlabel("Rata-Rata Penyewaan (Sepeda/Hari)")
    ax7.set_ylabel("Klaster Hari")
    ax7.set_title("Rata-Rata Penyewaan per Klaster Hari")
    for i, v in enumerate(cluster_data["cnt"]):
        ax7.text(v + (cluster_data["cnt"].max() * 0.02), i, f"{v:.0f}", va="center", fontsize=10)
    st.pyplot(fig7)

st.markdown("---")
st.caption("Dashboard by Primo Putra Ramadhan | Bike Sharing Dataset Analysis (2011–2012)")