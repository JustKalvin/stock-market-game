import streamlit as st
import pandas as pd
import yfinance as yf
import plotly.graph_objects as go
import random
from datetime import datetime
import matplotlib.pyplot as plt
import base64

def get_base64(image_path):
  with open(image_path, "rb") as img_file:
    return base64.b64encode(img_file.read()).decode()

# Ganti path ke gambar kamu
image_base64 = get_base64("assets/stonk_wp_for_game.jpg")

# Masukin ke CSS
page_bg_color = f"""
<style>
[data-testid="stAppViewContainer"] {{
    background-image: url("data:image/jpeg;base64,{image_base64}");
    background-size: cover;
    background-position: center;
    background-repeat: no-repeat;
}}
</style>
"""

st.markdown(page_bg_color, unsafe_allow_html=True)


sidebar_base64 = get_base64('assets/peakpx.jpg')

sidebar_bg_image = f"""
<style>
[data-testid="stSidebar"] {{
    background-image: url("data:image/jpeg;base64,{sidebar_base64}");
    background-size: cover;
    background-position: center;
}}
</style>
"""

st.markdown(sidebar_bg_image, unsafe_allow_html=True)




st.title('Stock Market Prediction')


text_input_style = """
<style>
[data-testid="stSidebar"] [data-testid="stTextInput"] input {
    background-color: #1E1E1E; /* Warna background */
    color: white; /* Warna teks */
    border-radius: 8px; /* Radius border */
    padding: 8px; /* Padding */
    border: 1px solid #555; /* Warna border */
}
</style>
"""

st.markdown(text_input_style, unsafe_allow_html=True)

# Input dari sidebar
ticker = st.sidebar.text_input('Code Saham', 'BBCA.JK')

# Inisialisasi session state untuk menyimpan tanggal dan status tebakan
if "date1" not in st.session_state:
    st.session_state["date1"] = None
if "date2" not in st.session_state:
    st.session_state["date2"] = None
if "prediction_correct" not in st.session_state:  # ✅ Tambahkan ini
    st.session_state["prediction_correct"] = False


# Fungsi untuk menghasilkan tanggal acak
def generate_dates():
  while True:
    # Pilih tahun
    year1, year2 = sorted([random.randint(2015, 2024) for _ in range(2)])
    # Pilih bulan
    month1, month2 = sorted([random.randint(1, 12) for _ in range(2)])
    # Pilih hari
    day1, day2 = sorted([random.randint(1, 28) for _ in range(2)])

    # Buat objek datetime setelah dipilih
    temp_date1 = datetime(year1, month1, day1)
    temp_date2 = datetime(year2, month2, day2)

    # Pastikan rentang minimal 40 hari
    if abs((temp_date2 - temp_date1).days) >= 40:
        break  

    # Simpan ke session state setelah valid
  st.session_state["date1"] = temp_date1
  st.session_state["date2"] = temp_date2


# Tombol untuk generate tanggal
if st.sidebar.button("Generate"):
  generate_dates()

# Ambil tanggal dari session_state
date1 = st.session_state["date1"]
date2 = st.session_state["date2"]
   

# Plot hanya jika date1 dan date2 sudah ada
if date1 and date2:
  st.write(f"Menampilkan data dari {date1.strftime('%Y-%m-%d')} hingga {date2.strftime('%Y-%m-%d')}")
  theData = yf.download(ticker, start = date1, end = date2)
  # Reset index (just in case)
  theData = theData.reset_index()
  theData.columns = theData.columns.droplevel(1)
  theData = theData.reset_index(drop = True)
  theData1 = theData[-30 : -1].reset_index(drop = True)
  theData2 = theData[-30 : ].reset_index(drop = True)
  st.write(theData1)

  st.subheader('Closing Price vs Time Chart with 100MA')
  ma100 = theData1['Close']
  fig = plt.figure(figsize=(12, 6))
  plt.plot(theData1['Date'], theData1['Close'], label='Close Price', color='blue')
  plt.legend(loc='best')
  st.pyplot(fig)
  today_price = theData['Close'].iloc[-1]
  previous_price = theData['Close'].iloc[-2]
  
  col1, col2 = st.columns(2)
  with col1:
    if st.button('📈'):
      if today_price > previous_price:
        st.success('BENAR ✔️')
        st.write(f"Harga sebelumnya : {previous_price:.2f}, Harga saat ini: {today_price:.2f}")  # ✅ Tambahkan harga sebagai bukti
        st.session_state["prediction_correct"] = True
      else:
        st.error('SALAH ❌')
        st.session_state["prediction_correct"] = False
  with col2:
      if st.button('📉'):
        if today_price < previous_price:
          st.success('BENAR ✔️')
          st.write(f"Harga sebelumnya : {previous_price:.2f}, Harga saat ini: {today_price:.2f}")  # ✅ Tambahkan harga sebagai bukti
          st.session_state["prediction_correct"] = True
        else:
          st.error('SALAH ❌')
          st.session_state["prediction_correct"] = False
else:
  st.info("Klik tombol 'Generate' untuk mendapatkan rentang tanggal secara acak dan menampilkan data saham.")
