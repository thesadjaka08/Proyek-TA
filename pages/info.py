import streamlit as st

def show_loan_attributes_description():
    st.markdown("### Deskripsi Pertanyaan Terkait Pinjaman Pribadi")
    
    st.markdown("1. **Usia**: Usia pelanggan dalam tahun.")
    st.markdown("2. **Pengalaman**: Jumlah tahun pengalaman kerja pelanggan.")
    st.markdown("3. **Pendapatan**: Pendapatan tahunan pelanggan dalam bentuk mata uang.")
    st.markdown("4. **Kode Pos**: Kode pos lokasi tempat tinggal pelanggan.")
    st.markdown("5. **Keluarga**: Jumlah orang dalam keluarga pelanggan (termasuk pelanggan itu sendiri).")
    st.markdown("6. **CCAvg**: Rata-rata pengeluaran kartu kredit bulanan pelanggan dalam bentuk mata uang.")
    st.markdown("7. **Pendidikan**: Tingkat pendidikan pelanggan, yang dapat berupa:")
    st.markdown("   - 1: Sarjana (Bachelor's degree)")
    st.markdown("   - 2: Sarjana (Master's degree)")
    st.markdown("   - 3: Profesional (Professional degree)")
    st.markdown("8. **Hipotek**: Nilai hipotek yang dimiliki nasabah dalam bentuk mata uang.")
    st.markdown("9. **Rekening Surat Berharga**: Status apakah nasabah mempunyai rekening surat berharga atau tidak (rekening investasi).")
    st.markdown("10. **Rekening CD**: Status apakah nasabah mempunyai rekening CD atau tidak.")
    st.markdown("11. **Online**: Status apakah nasabah menggunakan layanan online bank atau tidak.")
    st.markdown("12. **CreditCard**: Status apakah nasabah menggunakan kartu kredit bank atau tidak.")
    st.markdown("13. **Pinjaman Pribadi**: Status apakah nasabah diberikan pinjaman pribadi atau tidak.")

if __name__ == "__main__":
    show_loan_attributes_description()
