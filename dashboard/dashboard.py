# Import library yang dibutuhkan
import streamlit as st                    # Framework untuk dashboard web interaktif
import pandas as pd                       # Manipulasi dan analisis data tabular
import matplotlib.pyplot as plt           # Membuat grafik visualisasi
import seaborn as sns                     # Grafik statistik yang lebih menarik

# ==================== KONFIGURASI HALAMAN ====================
# Atur judul tab browser, icon, dan layout dashboard menjadi full width
st.set_page_config(page_title="Bike Sharing Dashboard", page_icon="🚲", layout="wide")

# ==================== LOAD DATA ====================
# Decorator @st.cache_data agar data hanya dibaca sekali (tidak reload saat ganti filter)
@st.cache_data
def load_data():
     # Baca file main_data.csv hasil export dari notebook
    data = pd.read_csv("main_data.csv")
    return data

# Simpan data ke variabel day_df
day_df = load_data()

# ==================== SIDEBAR FILTER ====================
# Judul sidebar
st.sidebar.title("🚲 Bike Sharing Dashboard")
st.sidebar.markdown("---")

# Filter berdasarkan musim (user bisa pilih lebih dari satu)
season_filter = st.sidebar.multiselect(
    "Pilih Musim",
    options=day_df["season"].unique(),              # Opsi: Springer, Summer, Fall, Winter
    default=day_df["season"].unique()               # Default: semua terpilih
)

# Filter berdasarkan kondisi cuaca
weather_filter = st.sidebar.multiselect(
    "Pilih Kondisi Cuaca",
    options=day_df["weathersit"].unique(),
    default=day_df["weathersit"].unique()
)

# Filter berdasarkan tahun
year_filter = st.sidebar.multiselect(
    "Pilih Tahun",
    options=day_df["yr"].unique(),
    default=day_df["yr"].unique()
)

# Terapkan filter ke dataframe: ambil baris yang sesuai pilihan user
filtered_df = day_df[
    (day_df["season"].isin(season_filter)) &
    (day_df["weathersit"].isin(weather_filter)) &
    (day_df["yr"].isin(year_filter))
]

# Tampilkan jumlah data setelah difilter di sidebar
st.sidebar.markdown("---")
st.sidebar.markdown(f"**Total Data:** {len(filtered_df)} hari")

# ==================== HEADER DASHBOARD ====================
st.title("🚲 Bike Sharing Dashboard")
st.markdown("Analisis penyewaan sepeda berdasarkan musim, cuaca, dan pola penggunaan harian (2011–2012)")
st.markdown("---")

# ==================== METRICS CARD ====================
# 4 kartu metrik yang menampilkan ringkasan angka secara cepat
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Total Penyewaan", f"{filtered_df['cnt'].sum():,}")              # Jumlah total sewa
with col2:
    st.metric("Rata-Rata Harian", f"{filtered_df['cnt'].mean():,.0f}")         # Rata-rata per hari
with col3:
    st.metric("Penyewa Registered", f"{filtered_df['registered'].sum():,}")    # Total pengguna terdaftar
with col4:
    st.metric("Penyewa Casual", f"{filtered_df['casual'].sum():,}")            # Total pengguna biasa

st.markdown("---")

# ==================== PERTANYAAN 1: PENGARUH MUSIM & CUACA ====================
st.subheader("📊 Pertanyaan 1: Pengaruh Cuaca dan Musim terhadap Penyewaan Sepeda")

# Bagi layar menjadi 2 kolom untuk grafik musim dan cuaca
col_left, col_right = st.columns(2)

# Grafik kiri: Bar chart rata-rata penyewaan per musim
with col_left:
    st.markdown("**Rata-Rata Penyewaan Berdasarkan Musim**")
    # Hitung rata-rata cnt per musim, urutkan dari tertinggi
    season_avg = filtered_df.groupby("season")["cnt"].mean().sort_values(ascending=False).reset_index()
    
    fig1, ax1 = plt.subplots(figsize=(8, 5))
    sns.barplot(data=season_avg, x="season", y="cnt", ax=ax1, palette="Set2", hue="season", legend=False)
    ax1.set_xlabel("Musim")
    ax1.set_ylabel("Rata-Rata Penyewaan per Hari")
    ax1.set_title("Penyewaan Sepeda per Musim")
    # Tambahkan label angka di atas tiap batang
    for i, v in enumerate(season_avg["cnt"]):
        ax1.text(i, v + 50, f"{v:.0f}", ha="center", fontsize=10)
    st.pyplot(fig1)

# Grafik kanan: Bar chart rata-rata penyewaan per kondisi cuaca
with col_right:
    st.markdown("**Rata-Rata Penyewaan Berdasarkan Cuaca**")
    weather_avg = filtered_df.groupby("weathersit")["cnt"].mean().sort_values(ascending=False).reset_index()
    
    fig2, ax2 = plt.subplots(figsize=(8, 5))
    sns.barplot(data=weather_avg, x="weathersit", y="cnt", ax=ax2, palette="coolwarm", hue="weathersit", legend=False)
    ax2.set_xlabel("Kondisi Cuaca")
    ax2.set_ylabel("Rata-Rata Penyewaan per Hari")
    ax2.set_title("Penyewaan Sepeda per Kondisi Cuaca")
    ax2.tick_params(axis="x", rotation=15)  # Miringkan label sumbu X agar tidak bertumpuk
    for i, v in enumerate(weather_avg["cnt"]):
        ax2.text(i, v + 50, f"{v:.0f}", ha="center", fontsize=10)
    st.pyplot(fig2)

# Heatmap: silang musim (baris) vs cuaca (kolom), isi = rata-rata sewa
st.markdown("**Heatmap: Rata-Rata Penyewaan (Musim vs Cuaca)**")
pivot_data = filtered_df.pivot_table(index="season", columns="weathersit", values="cnt", aggfunc="mean")

fig3, ax3 = plt.subplots(figsize=(10, 5))
sns.heatmap(pivot_data, annot=True, fmt=".0f", cmap="YlGnBu", linewidths=0.5, ax=ax3)
ax3.set_xlabel("Kondisi Cuaca")
ax3.set_ylabel("Musim")
st.pyplot(fig3)

st.markdown("---")

# ==================== PERTANYAAN 2: POLA JAM PENGGUNAAN ====================
st.subheader("🕐 Pertanyaan 2: Pola Jam Penggunaan (Casual vs Registered)")

# Baca data per jam dari hour.csv untuk analisis peak hours
@st.cache_data
def load_hour_data():
    hour_data = pd.read_csv("../data/hour.csv")
    # Mapping kode workingday menjadi label deskriptif
    workingday_map = {0: "Holiday/Weekend", 1: "Working Day"}
    hour_data["workingday"] = hour_data["workingday"].map(workingday_map)
    return hour_data

try:
    hour_df = load_hour_data()
    # Hitung rata-rata sewa per jam, dipisah berdasarkan jenis hari
    hourly_usage = hour_df.groupby(["workingday", "hr"])[["casual", "registered", "cnt"]].mean().reset_index()

    # Bagi layar menjadi 2 kolom: hari kerja vs hari libur
    col_wd, col_hol = st.columns(2)

    # Grafik kiri: Pola penyewaan per jam di hari kerja
    with col_wd:
        st.markdown("**Hari Kerja (Working Day)**")
        wd_data = hourly_usage[hourly_usage["workingday"] == "Working Day"]
        
        fig4, ax4 = plt.subplots(figsize=(8, 5))
        ax4.plot(wd_data["hr"], wd_data["registered"], color="#2E86C1", label="Registered", linewidth=2)
        ax4.plot(wd_data["hr"], wd_data["casual"], color="#E67E22", label="Casual", linewidth=2)
        ax4.set_xlabel("Jam")
        ax4.set_ylabel("Rata-Rata Penyewaan")
        ax4.set_title("Pola Penyewaan per Jam (Hari Kerja)")
        ax4.set_xticks(range(0, 24))  # Sumbu X: jam 0-23
        ax4.legend()
        st.pyplot(fig4)

    # Grafik kanan: Pola penyewaan per jam di hari libur
    with col_hol:
        st.markdown("**Hari Libur (Holiday/Weekend)**")
        hol_data = hourly_usage[hourly_usage["workingday"] == "Holiday/Weekend"]
        
        fig5, ax5 = plt.subplots(figsize=(8, 5))
        ax5.plot(hol_data["hr"], hol_data["registered"], color="#2E86C1", label="Registered", linewidth=2)
        ax5.plot(hol_data["hr"], hol_data["casual"], color="#E67E22", label="Casual", linewidth=2)
        ax5.set_xlabel("Jam")
        ax5.set_ylabel("Rata-Rata Penyewaan")
        ax5.set_title("Pola Penyewaan per Jam (Hari Libur)")
        ax5.set_xticks(range(0, 24))
        ax5.legend()
        st.pyplot(fig5)

except FileNotFoundError:
    # Tampilkan pesan jika file hour.csv tidak ditemukan
    st.warning("File data/hour.csv tidak ditemukan. Pastikan struktur folder benar.")

st.markdown("---")

# ==================== ANALISIS LANJUTAN ====================
st.subheader("🔬 Analisis Lanjutan: Binning Suhu & Clustering")

col_bin, col_clust = st.columns(2)

# Grafik kiri: Hasil binning suhu
with col_bin:
    st.markdown("**Penyewaan Berdasarkan Kategori Suhu**")
    if "temp_category" in filtered_df.columns:
        # Agregasi rata-rata sewa per kategori suhu
temp_data = filtered_df.groupby("temp_category", observed=True)["cnt"].agg(["mean", "count"]).reset_index()
        
        fig6, ax6 = plt.subplots(figsize=(8, 5))
        sns.barplot(data=temp_data, x="temp_category", y="mean", ax=ax6, palette="RdYlBu_r", hue="temp_category", legend=False)
        ax6.set_xlabel("Kategori Suhu")
        ax6.set_ylabel("Rata-Rata Penyewaan")
        ax6.set_title("Penyewaan Sepeda per Kategori Suhu")
        ax6.tick_params(axis="x", rotation=15)
        st.pyplot(fig6)
    else:
        st.info("Kolom temp_category tidak tersedia.")

# Grafik kanan: Hasil clustering hari
with col_clust:
    st.markdown("**Clustering Hari Berdasarkan Pola Penggunaan**")
    if "day_cluster" in filtered_df.columns:
        # Agregasi rata-rata sewa per klaster hari
        cluster_data = filtered_df.groupby("day_cluster")["cnt"].mean().sort_values(ascending=False).reset_index()
        
        fig7, ax7 = plt.subplots(figsize=(8, 5))
        sns.barplot(data=cluster_data, y="day_cluster", x="cnt", ax=ax7, palette="viridis", hue="day_cluster", legend=False)
        ax7.set_xlabel("Rata-Rata Penyewaan")
        ax7.set_ylabel("Klaster Hari")
        ax7.set_title("Rata-Rata Penyewaan per Klaster")
        st.pyplot(fig7)
    else:
        st.info("Kolom day_cluster tidak tersedia.")

st.markdown("---")

# Footer dashboard
st.caption("Dashboard by Primo Putra Ramadhan | Bike Sharing Dataset Analysis (2011–2012)")
temp_data = filtered_df.groupby("temp_category", observed=True)["cnt"].agg(["mean", "count"]).reset_index()
        
        fig6, ax6 = plt.subplots(figsize=(8, 5))
        sns.barplot(data=temp_data, x="temp_category", y="mean", ax=ax6, palette="RdYlBu_r", hue="temp_category", legend=False)
        ax6.set_xlabel("Kategori Suhu")
        ax6.set_ylabel("Rata-Rata Penyewaan")
        ax6.set_title("Penyewaan Sepeda per Kategori Suhu")
        ax6.tick_params(axis="x", rotation=15)
        st.pyplot(fig6)
    else:
        st.info("Kolom temp_category tidak tersedia.")

# Grafik kanan: Hasil clustering hari
with col_clust:
    st.markdown("**Clustering Hari Berdasarkan Pola Penggunaan**")
    if "day_cluster" in filtered_df.columns:
        # Agregasi rata-rata sewa per klaster hari
        cluster_data = filtered_df.groupby("day_cluster")["cnt"].mean().sort_values(ascending=False).reset_index()
        
        fig7, ax7 = plt.subplots(figsize=(8, 5))
        sns.barplot(data=cluster_data, y="day_cluster", x="cnt", ax=ax7, palette="viridis", hue="day_cluster", legend=False)
        ax7.set_xlabel("Rata-Rata Penyewaan")
        ax7.set_ylabel("Klaster Hari")
        ax7.set_title("Rata-Rata Penyewaan per Klaster")
        st.pyplot(fig7)
    else:
        st.info("Kolom day_cluster tidak tersedia.")

st.markdown("---")

# Footer dashboard
st.caption("Dashboard by Primo Putra Ramadhan | Bike Sharing Dataset Analysis (2011–2012)")
