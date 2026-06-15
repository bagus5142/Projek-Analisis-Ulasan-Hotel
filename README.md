# Hotel Review Sentiment Analysis Dashboard

Proyek ini berisi repositori lengkap untuk analisis sentimen ulasan hotel, mencakup data mentah, skrip pipeline, dan dua varian dashboard (Streamlit & React).

## Struktur Repositori

- `/data/`: Berisi dataset CSV mentah dan yang sudah terstruktur (`AI_Structured_Final.csv`, `AI_Structured_Keywords.csv`, dll).
- `/dashboard-react/`: Dashboard utama (SaaS-grade) yang dibangun menggunakan Vite, React, TailwindCSS, dan Shadcn UI.
- `/dashboard-streamlit/`: Versi alternatif/lama dari dashboard menggunakan Python Streamlit.
- `/src/` atau `/notebooks/`: Skrip Python untuk pipeline NLP (Kaggle).

## Menjalankan Dashboard React (Utama)

Dashboard React menggunakan pendekatan pre-processing offline untuk memastikan waktu load instan (< 0.1 detik).

1. Buka terminal dan masuk ke direktori `/dashboard-react/`:
   ```bash
   cd dashboard-react
   ```
2. Pastikan dependensi sudah terinstal:
   ```bash
   npm install
   ```
3. Jika data CSV di `/data/` diubah, jalankan skrip build untuk meng-generate ulang `hotels.json` dan memetakan `constants.ts`:
   ```bash
   node buildData.mjs
   ```
4. Jalankan *development server*:
   ```bash
   npm run dev
   ```
5. Buka `http://localhost:5173/` di browser Anda.

## Deployment (Untuk Tim IT / Github)
Karena aplikasi React ini sepenuhnya statis (memuat `hotels.json` lokal), aplikasi ini bisa langsung di-build dan di-deploy ke **Vercel, Netlify, atau GitHub Pages**.
- Jalankan `npm run build` di dalam `/dashboard-react/`.
- Deploy folder `dist/` ke platform pilihan Anda.

---
*Dibuat untuk keperluan evaluasi layanan BUMN vs Kompetitor.*