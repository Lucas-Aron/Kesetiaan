import streamlit as st

# Cek apakah session_state untuk members sudah ada, jika belum, inisialisasi
if 'members' not in st.session_state:
    st.session_state.members = {}

class Member:
    def __init__(self, nama, email):
        self.nama = nama
        self.email = email
        self.poin_loyalty = 0
        self.riwayat_penukaran = []

    def tambah_poin(self, pembelian):
        poin_ditambah = pembelian // 100 * 10
        self.poin_loyalty += poin_ditambah
        # Menambahkan riwayat penambahan poin
        self.riwayat_penukaran.append(f"Menambah {poin_ditambah} poin dari pembelian Rp{pembelian}")

    def tukar_poin(self, jumlah_poin):
        if self.poin_loyalty >= jumlah_poin:
            self.poin_loyalty -= jumlah_poin
            # Menambahkan riwayat penukaran poin
            self.riwayat_penukaran.append(f"Menukar {jumlah_poin} poin")
        else:
            return False
        return True

    def info_member(self):
        return f"Nama: {self.nama}\nEmail: {self.email}\nPoin Loyalty: {self.poin_loyalty}"

    def riwayat_penukaran_poin(self):
        return self.riwayat_penukaran if self.riwayat_penukaran else ["Tidak ada riwayat penukaran."]


class SistemPendaftaran:
    def __init__(self):
        self.members = st.session_state.members

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

    def list_member(self):
        if self.members:
            return [(member.nama, member.email, member.poin_loyalty) for member in self.members.values()]
        else:
            return "Tidak ada member terdaftar."


# Inisialisasi sistem pendaftaran
sistem = SistemPendaftaran()

# Streamlit Interface
st.title("Sistem Pendaftaran Membership dan Loyalty")

# Menu utama untuk memilih tindakan
menu = st.sidebar.selectbox("Pilih Tindakan", ["Daftar Member", "Lihat Info Member", "Pembelian & Loyalty", "Tukar Poin", "List Member", "Riwayat Penukaran Poin"])

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

# List Member
elif menu == "List Member":
    st.subheader("Daftar Member Terdaftar")
    members_list = sistem.list_member()
    if isinstance(members_list, list) and members_list:
        st.write("Daftar Member:")
        for member in members_list:
            st.write(f"- Nama: {member[0]}, Email: {member[1]}, Poin: {member[2]}")
    else:
        st.write("Tidak ada member terdaftar.")

# Riwayat Penukaran Poin
elif menu == "Riwayat Penukaran Poin":
    st.subheader("Riwayat Penukaran Poin")
    email = st.text_input("Email Member")
    
    if st.button("Tampilkan Riwayat Penukaran"):
        if email in sistem.members:
            member = sistem.members[email]
            riwayat = member.riwayat_penukaran_poin()
            st.write(f"Riwayat Penukaran Poin untuk {member.nama}:")
            if isinstance(riwayat, list) and riwayat:
                for transaksi in riwayat:
                    st.write(f"- {transaksi}")
            else:
                st.write(riwayat)
        else:
            st.warning("Email tidak terdaftar sebagai member.")
