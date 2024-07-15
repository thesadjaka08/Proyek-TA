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
model = joblib.load('Xgboost_model.sav', 'rb')

# Title of the app
st.title("Prediksi Kelayakan Pinjaman")

# Collect user input
if st.button("Info"):
    st.switch_page("pages/info.py")

Age = st.number_input("Masukkan Usia", min_value=17, max_value=100)

Experience = st.number_input("Jumlah Tahun Pengalaman Kerja", min_value=1, max_value=100)

Income = st.number_input("Jumlah Pendapatan", min_value=0, max_value=float('inf'))

Family = st.selectbox("Jumlah Keluarga", min_value=1, max_value=20)

CCAvg = st.number_input("Jumlah CCAvg", min_value=0, max_value=float('inf'))

Education = st.selectbox("Pendidikan", options=[1, 2, 3])
st.caption(":red[**1**]: Sarjana (Bachelor's degree) :red[**2**]: Magister (Master's degree) :red[**3**]: Profesional (Professional degree)")

Mortgage = st.number_input("Jumlah Mortgage/Hipotek", min_value=0, max_value=float('inf'))

Securitiesaccount = st.selectbox("Apakah memiliki Securities Account", options=[0, 1])
st.caption(":red[**0**] :  Tidak Ada;  :red[**1**] :  Ada")


CDaccount = st.selectbox("Apakah memiliki CD Account", options=[0, 1])
st.caption(":red[**0**] :  Tidak Ada;  :red[**1**] :  Ada")

Online = st.selectbox("Apakah Online", options=[0, 1])
st.caption(":red[**0**] :  Tidak Ada;  :red[**1**] :  Ada")

CreditCard = st.selectbox("Apakah memiliki CreditCard", options=[0, 1])
st.caption(":red[**0**] :  Tidak Ada;  :red[**1**] :  Ada")

# Create a DataFrame from user input
input_data = pd.DataFrame({
    'Age': [Age],
    'Experience': [Experience],
    'Income': [Income],
    'Family': [Family],
    'CCAvg': [CCAvg],
    'Education': [Education],
    'Mortgage': [Mortgage],
    'Securitiesaccount': [Securitiesaccount],
    'CDaccount': [CDaccount],
    'Online': [Online],
    'CreditCard': [CreditCard]
})

# Make prediction
if st.button("Prediksi"):
    prediction = model.predict(input_data)
    prediction_proba = model.predict_proba(input_data)

    if prediction[0] == 1:
        st.error(f"Nasabah di berikan pinjaman dengan prediksi {prediction_proba[0][1] * 100:.2f}%")
    else:
        st.success(f"Nasabah tidak di berikan pinjaman dengan prediksi {prediction_proba[0][0] * 100:.2f}%")
