import streamlit as st

class Member:
    def __init__(self, nama, email):
        self.nama = nama
        self.email = email
        self.poin_loyalty = 0

    def tambah_poin(self, pembelian):
        poin_ditambah = pembelian // 100 * 10
        self.poin_loyalty += poin_ditambah

    def tukar_poin(self, jumlah_poin):
        if self.poin_loyalty >= jumlah_poin:
            self.poin_loyalty -= jumlah_poin
        else:
            return False
        return True

    def info_member(self):
        return f"Nama: {self.nama}\nEmail: {self.email}\nPoin Loyalty: {self.poin_loyalty}"


class SistemPendaftaran:
    def __init__(self):
        self.members = {}

    def daftar_member(self, nama, email):
        if email in self.members:
            return "Email sudah terdaftar."
        else:
            member_baru = Member(nama, email)
            self.members[email] = member_baru
            return f"{nama} berhasil terdaftar sebagai member."

    def tampilkan_member(self, email):
        if email in self.members:
            return self.members[email].info_member()
        else:
            return "Member tidak ditemukan."


# Inisialisasi sistem pendaftaran
sistem = SistemPendaftaran()

# Streamlit Interface
st.title("Sistem Pendaftaran Membership dan Loyalty")

# Menu utama untuk memilih tindakan
menu = st.sidebar.selectbox("Pilih Tindakan", ["Daftar Member", "Lihat Info Member", "Pembelian & Loyalty", "Tukar Poin"])

# Daftar Member
if menu == "Daftar Member":
    st.subheader("Daftar Member Baru")
    nama = st.text_input("Nama Lengkap")
    email = st.text_input("Email")
    
    if st.button("Daftar"):
        if nama and email:
            result = sistem.daftar_member(nama, email)
            st.success(result)
        else:
            st.warning("Nama dan email wajib diisi!")

# Lihat Info Member
elif menu == "Lihat Info Member":
    st.subheader("Lihat Info Member")
    email = st.text_input("Masukkan Email")
    
    if st.button("Tampilkan Info"):
        if email:
            info = sistem.tampilkan_member(email)
            st.text(info)
        else:
            st.warning("Email wajib diisi!")

# Pembelian & Loyalty
elif menu == "Pembelian & Loyalty":
    st.subheader("Proses Pembelian dan Poin Loyalty")
    email = st.text_input("Email Member")
    pembelian = st.number_input("Jumlah Pembelian (Rp)", min_value=0)

    if st.button("Proses Pembelian"):
        if email in sistem.members:
            member = sistem.members[email]
            member.tambah_poin(pembelian)
            st.success(f"{member.nama} mendapatkan {pembelian // 100 * 10} poin loyalty.")
        else:
            st.warning("Email tidak terdaftar sebagai member.")

# Tukar Poin
elif menu == "Tukar Poin":
    st.subheader("Tukar Poin Loyalty")
    email = st.text_input("Email Member")
    jumlah_poin = st.number_input("Jumlah Poin untuk Ditukar", min_value=0)

    if st.button("Tukar Poin"):
        if email in sistem.members:
            member = sistem.members[email]
            if member.tukar_poin(jumlah_poin):
                st.success(f"{member.nama} berhasil menukar {jumlah_poin} poin loyalty.")
            else:
                st.warning("Poin tidak cukup untuk ditukarkan.")
        else:
            st.warning("Email tidak terdaftar sebagai member.")
