# Memuat Library yang dibutuhkan
import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os
import nbformat

# Memuat Dataset
@st.cache_data
def load_data():
    # Use relative path instead of absolute path
    df = pd.read_csv("hour_df.csv")
    df["dteday"] = pd.to_datetime(df["dteday"])
    return df

try:
    df = load_data()

    # Sidebar
    st.sidebar.title("Dashboard Bike Sharing")
    menu = st.sidebar.radio("Pilih Halaman", ["Dashboard Analisis", "Lihat Notebook (.ipynb)"])

    if menu == "Dashboard Analisis":
        st.title("📊 Dashboard Analisis Peminjaman Sepeda")
        
        # Filter rentang waktu
        min_date = df["dteday"].min().date()
        max_date = df["dteday"].max().date()
        date_range = st.sidebar.date_input("Pilih Rentang Waktu", [min_date, max_date], min_value=min_date, max_value=max_date)
        df_filtered = df[(df["dteday"] >= pd.to_datetime(date_range[0])) & (df["dteday"] <= pd.to_datetime(date_range[1]))]
        
        st.divider()

        # Pengaruh Cuaca terhadap Peminjaman
        with st.container():
            st.subheader("Pengaruh Cuaca terhadap Jumlah Peminjaman Sepeda")
            weather_usage = df_filtered.groupby("weathersit")["cnt"].mean()
            
            fig, ax = plt.subplots(figsize=(8, 5))
            sns.barplot(x=weather_usage.index, y=weather_usage.values, palette="coolwarm", ax=ax)
            ax.set_title("Rata-rata Peminjaman Berdasarkan Kondisi Cuaca")
            ax.set_xlabel("Kondisi Cuaca")
            ax.set_ylabel("Jumlah Peminjaman")
            ax.set_xticklabels(["Cerah", "Mendung", "Hujan Ringan", "Hujan Lebat"])
            
            st.pyplot(fig)
            st.write("📌 **Insight:** Cuaca cerah meningkatkan peminjaman, sedangkan hujan dan badai menurunkannya.")

        st.divider()

        # Perbandingan Hari Kerja, Akhir Pekan, dan Hari Libur
        with st.container():
            st.subheader("Perbandingan Peminjaman: Hari Kerja vs Akhir Pekan vs Hari Libur")
            df_workingday = df_filtered[(df_filtered["workingday"] == 1) & (df_filtered["holiday"] == 0)]
            df_weekend = df_filtered[(df_filtered["workingday"] == 0) & (df_filtered["holiday"] == 0)]
            df_holiday = df_filtered[df_filtered["holiday"] == 1]
            
            hourly_workingday = df_workingday.groupby("hr")["cnt"].mean()
            hourly_weekend = df_weekend.groupby("hr")["cnt"].mean()
            hourly_holiday = df_holiday.groupby("hr")["cnt"].mean()
            
            fig, ax = plt.subplots(figsize=(10, 5))
            sns.lineplot(x=hourly_workingday.index, y=hourly_workingday.values, label="Hari Kerja", color="blue", marker="o", ax=ax)
            sns.lineplot(x=hourly_weekend.index, y=hourly_weekend.values, label="Akhir Pekan", color="green", marker="o", ax=ax)
            sns.lineplot(x=hourly_holiday.index, y=hourly_holiday.values, label="Hari Libur", color="red", marker="o", ax=ax)
            
            ax.set_title("Pola Peminjaman Sepeda Berdasarkan Waktu")
            ax.set_xlabel("Jam")
            ax.set_ylabel("Jumlah Peminjaman")
            ax.legend()
            
            st.pyplot(fig)
            st.write("📌 **Insight:** Hari kerja memiliki dua puncak peminjaman (pagi & sore), sementara akhir pekan dan hari libur lebih merata sepanjang hari.")

        st.divider()

        # Tren Peminjaman Tahun 2011 vs 2012
        with st.container():
            st.subheader("Perbandingan Peminjaman Sepeda Tahun 2011 vs 2012")
            yearly_usage = df_filtered.groupby("yr")["cnt"].sum()
            
            fig, ax = plt.subplots(figsize=(6, 5))
            sns.barplot(x=yearly_usage.index, y=yearly_usage.values, palette="Blues", ax=ax)
            ax.set_title("Total Peminjaman Sepeda per Tahun")
            ax.set_xlabel("Tahun")
            ax.set_ylabel("Total Peminjaman")
            ax.set_xticklabels(["2011", "2012"])
            
            st.pyplot(fig)
            st.write("📌 **Insight:** Peminjaman sepeda meningkat signifikan di tahun 2012 dibanding 2011.")

    elif menu == "Lihat Notebook (.ipynb)":
        st.title("📘 Lihat Notebook Analisis Data")
        file_path = "../notebook.ipynb" 
        
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                nb_content = nbformat.read(f, as_version=4)
                for cell in nb_content.cells:
                    if cell.cell_type == "markdown":
                        st.markdown(cell.source)
                    elif cell.cell_type == "code":
                        st.code(cell.source)
        except FileNotFoundError:
            st.error("File .ipynb tidak ditemukan. Pastikan file tersedia atau sesuaikan path.")

    st.sidebar.markdown("---")
    st.sidebar.text("Sumber: Dataset Bike Sharing")

except FileNotFoundError:
    st.error("Dataset tidak ditemukan. Pastikan file 'hour_df.csv' ada dalam direktori yang sama dengan aplikasi.")
    st.info("Struktur file saat ini:")
    st.code(f"Files in current directory: {os.listdir('.')}")
