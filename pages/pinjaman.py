import streamlit as st
import pandas as pd
import joblib
from xgboost import XGBClassifier

# Load the trained model
model = joblib.load('Xgboost_model.sav', 'rb')

# Title of the app
st.title("Prediksi Kelayakan Pinjaman")

# Collect user input
st.page_link("pages/info.py", label="Info")

Age = st.number_input("Masukkan Usia", min_value=10, max_value=100)
Experience = st.number_input("Jumlah Pengalaman", min_value=1, max_value=100)
Income = st.number_input("Jumlah Pendapatan", min_value=0.0, max_value=20.0)
Family = st.selectbox("Jumlah Keluarga", options=[1, 2, 3, 4])
CCAvg = st.number_input("Jumlah CCAvg", min_value=0.0, max_value=10.0)
Education = st.selectbox("Pendidikan", options=[1, 2, 3])
Mortgage = st.number_input("Jumlah Mortgage/Hipotek", min_value=0, max_value=650)
Securitiesaccount = st.selectbox("Apakah memiliki Securities Account", options=[0, 1])
CDaccount = st.selectbox("Apakah memiliki CD Account", options=[0, 1])
Online = st.selectbox("Apakah Online", options=[0, 1])
CreditCard = st.selectbox("Apakah memiliki CreditCard", options=[0, 1])

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
