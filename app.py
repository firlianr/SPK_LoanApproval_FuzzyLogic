import streamlit as st
from fuzzy_model import predict_fuzzy

st.title("Sistem Penunjang Keputusan Kelayakan Pinjaman Menggunakan Fuzzy Logic")

# --- Input Pengguna ---
pendapatan = st.number_input("Pendapatan Pemohon", min_value=0, max_value=25000, value=9000, step=500)
pinjaman = st.number_input("Jumlah Pinjaman", min_value=0, max_value=700, value=300, step=50)
riwayat = st.selectbox("Riwayat Kredit", options=["Buruk", "Baik"])

# --- Tombol Cek ---
if st.button("🔍 Cek Kelayakan"):
    try:
        score = predict_fuzzy(pendapatan, pinjaman, riwayat)
    except Exception as e:
        st.error(f"❌ Terjadi kesalahan dalam perhitungan: {e}")
        st.stop()

    # --- Analisis Alasan ---
    alasan = []

    if pendapatan < 5000:
        alasan.append("Pendapatan tergolong rendah sehingga kemampuan membayar cicilan dinilai berisiko.")
    elif 5000 <= pendapatan < 12000:
        alasan.append("Pendapatan berada pada kategori menengah, cukup stabil namun perlu keseimbangan dengan jumlah pinjaman.")
    else:
        alasan.append("Pendapatan tergolong tinggi dan menunjukkan kemampuan finansial yang baik untuk menanggung pinjaman.")

    if pinjaman > 500:
        alasan.append("Jumlah pinjaman yang diajukan cukup besar sehingga perlu evaluasi terhadap kemampuan pembayaran.")
    elif 250 <= pinjaman <= 500:
        alasan.append("Jumlah pinjaman berada di tingkat sedang, masih dalam batas wajar namun perlu penilaian lebih lanjut.")
    else:
        alasan.append("Jumlah pinjaman relatif kecil dibanding kemampuan pendapatan, sehingga risiko gagal bayar rendah.")

    if riwayat == "Baik":
        alasan.append("Riwayat kredit tergolong baik dan menjadi nilai positif dalam penilaian kelayakan.")
    else:
        alasan.append("Riwayat kredit kurang baik, hal ini menurunkan tingkat kepercayaan dalam penilaian pinjaman.")

    if score >= 70:
        decision = "DISETUJUI ✅"
        alasan.append("Kondisi pendapatan, pinjaman, dan riwayat kredit menunjukkan tingkat kelayakan tinggi.")
    elif 40 <= score < 70:
        decision = "PERLU PERTIMBANGAN ⚖️"
        alasan.append("Perlu analisis lanjutan terhadap keseimbangan antara pendapatan, jumlah pinjaman, dan riwayat kredit sebelum keputusan akhir ditetapkan.")
    else:
        decision = "DITOLAK ❌"
        alasan.append("Kombinasi pendapatan, jumlah pinjaman, dan riwayat kredit belum mencerminkan kelayakan pinjaman.")

    st.subheader("📋 Hasil Penilaian")
    st.write(f"**Persentase Kelayakan Pinjaman:** {round(score, 2)}%")
    st.write(f"**Keputusan:** {decision}")
    st.write(f"**Alasan:** {' '.join(alasan)}")
