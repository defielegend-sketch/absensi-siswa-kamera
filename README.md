# Absensi Siswa Online - Kamera

Aplikasi absensi siswa sederhana menggunakan Python Flask, Kamera (WebRTC), dan database CSV.

## Fitur
- Absen dengan Foto (Kamera)
- Tanggal dan Waktu Otomatis
- Panel Guru untuk melihat riwayat absen
- Penyimpanan database di CSV (Bisa dibuka di Excel)

## Cara Jalankan di Lokal
1. Install Python
2. Install dependensi: `pip install flask gunicorn`
3. Jalankan aplikasi: `python app.py`
4. Buka `http://localhost:5000`

## Cara Online (Deploy ke Render)
1. Buat akun di [GitHub](https://github.com) dan [Render](https://render.com).
2. Upload folder ini ke repository GitHub baru.
3. Di Render, pilih **New Web Service**.
4. Hubungkan dengan repo GitHub Anda.
5. Gunakan setting berikut:
   - **Runtime**: `Python`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app`
6. Klik Deploy. Selesai!

## Struktur Folder
- `app.py`: Backend Flask
- `templates/`: Halaman HTML (index, view)
- `static/photos/`: Lokasi penyimpanan foto
- `absensi_siswa.csv`: Database absen
