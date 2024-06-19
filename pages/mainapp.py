import streamlit as st
from homepage import homepage
from pinjaman import pinjaman
from info import info

def mainapp():
    st.sidebar.title("Menu")
    page = st.sidebar.selectbox("Select a page", ["Homepage", "Prediksi Kelayakan Pinjaman", "Info"])

    if page == "Homepage":
        homepage()
    elif page == "Prediksi Kelayakan Pinjaman":
        pinjaman()
    elif page == "Info":
        info()

if __name__ == "__main__":
    mainapp()
