import streamlit as st

st.markdown("<style> ul {display: none;} </style>", unsafe_allow_html=True)

# sidebars
st.sidebar.header("Menu")

st.sidebar.page_link("pages/Homepage.py", label="Beranda")
st.sidebar.page_link("pages/pinjaman.py", label="Prediksi Kelayakan Pinjaman")

st.sidebar.markdown("""
<a href="Login.py" target="_self">
    <button style="background-color:#f63366;color:white;border:none;padding:10px 20px;border-radius:5px; margin-top:50px;">
        Logout
    </button>
</a>
""", unsafe_allow_html=True)



def show_loan_attributes_description():
    description = """
    ### Deskripsi Pertanyaan pada Fitur Prediksi Kelayakan Pinjaman 

    1. **Usia**: Usia nasabah.
    2. **Pengalaman**: Jumlah tahun pengalaman kerja nasabah.
    3. **Pendapatan**: Rata-rata pendapatan bulanan nasabah dalam bentuk mata uang rupiah.
    4. **Keluarga**: Jumlah orang dalam keluarga yang menjadi tanggungan nasabah (termasuk nasabah itu sendiri).
    5. **CCAvg**: Rata-rata pengeluaran bulanan nasabah dalam bentuk mata uang rupiah.
    6. **Pendidikan**: Tingkat pendidikan terakhir nasabah, dapat berupa :red[**1**]: Sarjana (Bachelor's degree) :red[**2**]: Magister (Master's degree) :red[**3**]: Profesional (Professional degree)
    7. **Hipotek**: Nilai hipotek yang dimiliki nasabah dalam bentuk mata uang rupiah. Nilai Hipotek adalah jumlah pinjaman dari bank dengan jaminan properti.
    8. **Rekening Investasi**: Status apakah nasabah memiliki rekening investasi atau tidak. Rekening investasi adalah rekening yang menyimpan saham, obligasi, dana, dan surat berharga lainnya, serta uang tunai.
    9. **Rekening CD**: Status apakah nasabah memiliki rekening CD atau tidak. Sertifikat deposito (CD) adalah jenis rekening tabungan yang memberikan suku bunga tetap atas uang yang disimpan selama jangka waktu yang disepakati.
    10. **Layanan Mobile Banking**: Status apakah nasabah menggunakan layanan online bank atau tidak.
    11. **Kartu Kredit**: Status apakah nasabah menggunakan kartu kredit bank atau tidak.

    :tulip: :red[**Note Kode :**] 

    :zero:: Tidak Ada       :one:: Ada
    """

    st.markdown(description, unsafe_allow_html=True)


if __name__ == "__main__":
    show_loan_attributes_description()
