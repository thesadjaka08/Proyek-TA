import streamlit as st
from homepage import homepage
from pinjaman import pinjaman
from info import info

def mainapp():
    # st.sidebar.title("Menu")
    # page = st.sidebar.selectbox("Select a page", ["Homepage", "Prediksi Kelayakan Pinjaman", "Info"])

    # if page == "Homepage":
    #     homepage()
    # elif page == "Prediksi Kelayakan Pinjaman":
    #     pinjaman()
    # elif page == "Info":
    #     info()

    st.title("")
    st.markdown("<style> ul {display: none;} </style>", unsafe_allow_html=True)  

    st.sidebar.image('images/logo.png')

    st.markdown('<div style="text-align:center; font-size:46px; font-weight:bold; margin-bottom:25px;">Selamat Datang di Sistem Prediksi Pinjaman Pribadi Kami!</div>', unsafe_allow_html=True)

    st.sidebar.header("Menu")
    st.sidebar.write("[Chatbot](https://chatloanbot.000webhostapp.com/)")
    
    # Remove st.switch_page and use session state for navigation
    if st.sidebar.button("Prediksi Kelayakan Pinjaman"):
        st.session_state.page = "Prediksi Kelayakan Pinjaman"
    if st.sidebar.button("Info"):
        st.session_state.page = "Info"
    
    st.sidebar.markdown("""
    <a href="Login.py" target="_self">
        <button style="background-color:#f63366;color:white;border:none;padding:10px 20px;border-radius:5px; margin-top:50px;">
            Logout
        </button>
    </a>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    mainapp()
