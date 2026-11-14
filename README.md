# Proyek Analisis Data: Bike Sharing Dataset

## Deskripsi Proyek
Proyek ini menganalisis dataset penyewaan sepeda (Bike Sharing) yang mencatat aktivitas penyewaan sepeda selama tahun 2011–2012. Analisis dilakukan untuk menjawab dua pertanyaan bisnis utama:
1. Bagaimana pengaruh kondisi cuaca dan musim terhadap jumlah total penyewaan sepeda harian?
2. Pada jam berapa saja terjadi puncak penggunaan sepeda oleh pengguna casual vs registered pada hari kerja dibandingkan hari libur?

## Dataset
Dataset yang digunakan adalah **Bike Sharing Dataset** yang terdiri dari:
- `day.csv` — data penyewaan sepeda harian (731 baris)
- `hour.csv` — data penyewaan sepeda per jam (17.379 baris)

## Tahapan Analisis
1. **Gathering Data** — memuat dataset day.csv dan hour.csv
2. **Assessing Data** — mengecek tipe data, missing value, dan duplikasi
3. **Cleaning Data** — konversi tipe data datetime dan mapping nilai kategorikal
4. **Exploratory Data Analysis (EDA)** — agregasi dan pivot table untuk menjawab pertanyaan bisnis
5. **Analisis Lanjutan** — binning suhu dan clustering hari berdasarkan pola penggunaan
6. **Visualization** — bar chart, heatmap, dan line chart
7. **Conclusion** — kesimpulan dari kedua pertanyaan bisnis

## Struktur Folder
proyek_analisis_data/
├── dashboard/
│ ├── dashboard.py # Script Streamlit dashboard
│ └── main_data.csv # Data bersih untuk dashboard
├── data/
│ ├── day.csv # Dataset harian
│ ├── hour.csv # Dataset per jam
│ └── Readme.txt # Keterangan dataset
├── notebook.ipynb # Notebook analisis lengkap
├── requirements.txt # Daftar dependency
├── README.md # Dokumentasi proyek
└── url.txt # Link dashboard


## Cara Menjalankan
1. Clone repository ini
2. Install dependency: `pip install -r requirements.txt`
3. Jalankan notebook: `jupyter notebook notebook.ipynb`
4. Jalankan dashboard: `cd dashboard && streamlit run dashboard.py`

## Teknologi
- Python 3.x
- Pandas
- Matplotlib & Seaborn
- Streamlit

## Penulis
- **Nama:** Primo Putra Ramadhan
- **Dataset:** Bike Sharing Dataset (Kaggle)
d