# Bike Sharing Dashboard

## Setup Enviroment - Anaconda
```
conda create --name main-ds python=3.9
conda activate main-ds
pip install -r requirements.txt
```

## Setup  Environment - Shell/Terminal
```
mkdir proyek_analisis_data
cd proyek_analisis_data
pipenv install
pipenv shell
pip install -r requirements.txt
```

## Run Steamlit app
```
streamlit run dashboard.py
```

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

## Penulis
- **Nama:** Primo Putra Ramadhan
- **Dataset:** Bike Sharing Dataset (Kaggle)
