import streamlit as st

st.markdown("<style> ul {display: none;} </style>", unsafe_allow_html=True)

# sidebars
st.sidebar.header("Menu")
st.sidebar.page_link("pages/Homepage.py", label="Beranda")
st.sidebar.page_link("pages/pinjaman.py", label="Prediksi Kelayakan Pinjaman")
st.sidebar.page_link("https://chatloanbot.000webhostapp.com/", label="Chatbot")
st.sidebar.markdown("""
<a href="Login.py" target="_self">
    <button style="background-color:#f63366;color:white;border:none;padding:10px 20px;border-radius:5px; margin-top:50px;">
        Logout
    </button>
</a>
""", unsafe_allow_html=True)



def show_loan_attributes_description():
    description = """
    ### Deskripsi Pertanyaan Terkait Pinjaman Pribadi

    1. **Usia**: Usia pelanggan dalam tahun.
    2. **Pengalaman**: Jumlah tahun pengalaman kerja pelanggan.
    3. **Pendapatan**: Pendapatan tahunan pelanggan dalam bentuk mata uang.
    4. **Kode Pos**: Kode pos lokasi tempat tinggal pelanggan.
    5. **Keluarga**: Jumlah orang dalam keluarga pelanggan (termasuk pelanggan itu sendiri).
    6. **CCAvg**: Rata-rata pengeluaran kartu kredit bulanan pelanggan dalam bentuk mata uang.
    7. **Pendidikan**: Tingkat pendidikan pelanggan, yang dapat berupa :red[**1**]: Sarjana (Bachelor's degree) :red[**2**]: Magister (Master's degree) :red[**3**]: Profesional (Professional degree)
    8. **Hipotek**: Nilai hipotek yang dimiliki nasabah dalam bentuk mata uang.
    9. **Rekening Surat Berharga**: Status apakah nasabah memiliki rekening surat berharga atau tidak (rekening investasi).
    10. **Rekening CD**: Status apakah nasabah memiliki rekening CD atau tidak.
    11. **Online**: Status apakah nasabah menggunakan layanan online bank atau tidak.
    12. **Kartu Kredit**: Status apakah nasabah menggunakan kartu kredit bank atau tidak.
    13. **Pinjaman Pribadi**: Status apakah nasabah diberikan pinjaman pribadi atau tidak.

    :tulip: :red[**Note Kode :**] 

    :zero:: Tidak Ada       :one:: Ada
    """

    st.markdown(description, unsafe_allow_html=True)


if __name__ == "__main__":
    show_loan_attributes_description()
