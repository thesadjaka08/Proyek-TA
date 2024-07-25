import streamlit as st
import pandas as pd
import joblib
from xgboost import XGBClassifier

# st.markdown("<style> ul {display: none;} </style>", unsafe_allow_html=True)
no_sidebar_style = """
    <style>
        div[data-testid="stSidebarNav"] {display: none;}
    </style>
"""
st.markdown(no_sidebar_style, unsafe_allow_html=True)

# sidebars
st.sidebar.header("Menu")
st.sidebar.page_link("pages/Homepage.py", label="Beranda")
st.sidebar.page_link("https://chatloanbot.000webhostapp.com/", label="Chatbot")
st.sidebar.page_link("pages/info.py", label="Info")
st.sidebar.markdown("""
<a href="Login.py" target="_self">
    <button style="background-color:#f63366;color:white;border:none;padding:10px 20px;border-radius:5px; margin-top:50px;">
        Logout
    </button>
</a>
""", unsafe_allow_html=True)

# Load the trained model
model = joblib.load('model_xgb.sav')

# Title of the app
st.title("Prediksi Kelayakan Pinjaman")

# Collect user input
if st.button("Info"):
    st.switch_page("pages/info.py")

Age = st.number_input("Usia", min_value=18, max_value=100)
Family = st.number_input("Jumlah Keluarga", min_value=1, max_value=50)
Education = st.selectbox("Pendidikan Terakhir", options=["1", "2", "3"])
st.caption(":red[**1**]: Sarjana (Bachelor's degree) :red[**2**]: Magister (Master's degree) :red[**3**]: Profesional (Professional degree)")
Experience = st.number_input("Jumlah Tahun Pengalaman Kerja", min_value=1, max_value=100)
Income = st.number_input("Jumlah Pendapatan Bulanan (dalam Rupiah)", min_value=0, max_value=500000000)
CCAvg = st.number_input("Jumlah Pengeluaran Bulanan (dalam Rupiah)", min_value=0, max_value=100000000)
Mortgage = st.number_input("Jumlah Hipotek (dalam Rupiah)", min_value=0, max_value=100000000)
st.caption("Nilai barang yang dijadikan jaminan nasabah kepada bank")
Securities_Account = st.selectbox("Apakah memiliki Rekening Investasi?", options=[0, 1])
st.caption(":red[**0**] :  Tidak Ada;  :red[**1**] :  Ada")
CD_Account = st.selectbox("Apakah memiliki Rekening CD (Sertifikat Deposito)?", options=[0, 1])
st.caption(":red[**0**] :  Tidak Ada;  :red[**1**] :  Ada")
Online = st.selectbox("Apakah menggunakan layanan Mobile Banking?", options=[0, 1])
st.caption(":red[**0**] :  Tidak Ada;  :red[**1**] :  Ada")
CreditCard = st.selectbox("Apakah memiliki kartu kredit?", options=[0, 1])
st.caption(":red[**0**] :  Tidak Ada;  :red[**1**] :  Ada")

# Create a DataFrame from user input
input_data = pd.DataFrame({
    'Age': [Age],
    'Family': [Family],
    'Education': [int(Education)],
    'Experience': [Experience],
    'Income': [Income],
    'CCAvg': [CCAvg],
    'Mortgage': [Mortgage],
    'Securities Account': [Securities_Account],
    'CD Account': [CD_Account],
    'Online': [Online],
    'CreditCard': [CreditCard]
})

# Ensure all data types are numeric and there are no missing values
input_data = input_data.astype(float).fillna(0)

# Make prediction
if st.button("Prediksi"):
    try:
        prediction = model.predict(input_data)
        prediction_proba = model.predict_proba(input_data)

        if prediction[0] == 1:
            st.error(f"Nasabah di berikan pinjaman dengan prediksi {prediction_proba[0][1] * 100:.2f}%")
        else:
            st.success(f"Nasabah tidak di berikan pinjaman dengan prediksi {prediction_proba[0][0] * 100:.2f}%")
    except ValueError as e:
        st.error(f"Terjadi kesalahan pada input data: {e}")
