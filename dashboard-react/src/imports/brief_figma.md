# Brief untuk AI Figma: Dashboard Analisis Ulasan Hotel

## Latar Belakang Proyek

Ini adalah proyek riset bisnis yang menganalisis **165.962 ulasan tamu hotel** dari Google Maps. Tujuannya adalah membandingkan kinerja pelayanan **hotel-hotel milik BUMN** (Badan Usaha Milik Negara / pemerintah) dengan **hotel-hotel Kompetitor** (swasta) di Indonesia.

Ulasan tamu telah diproses oleh model AI (NLP) untuk menghasilkan:
1. **Sentimen** — apakah tamu merasa Positif, Negatif, atau Netral.
2. **Aspek/Topik** — aspek pelayanan apa yang dibahas (contoh: Kebersihan, Makanan, Pelayanan Staf, dll). Ada 12 aspek.
3. **Frasa kunci** — frasa 2-3 kata yang menjadi akar masalah kelemahan atau kekuatan hotel (contoh: "ac rusak", "staf ramah", "sarapan enak").

Hasil analisis ini akan dipresentasikan ke **jajaran Direksi** perusahaan BUMN perhotelan. Dashboard harus terlihat **profesional, bersih, dan corporate** — bukan seperti tool data scientist, tapi seperti **product dashboard** yang siap pakai oleh eksekutif.

---

## Data yang Tersedia

### Tabel 1: Data Utama (165.962 baris)
| Kolom | Tipe | Contoh Nilai |
|-------|------|-------------|
| Review Time | Tanggal | 2026-01-03 |
| Rating | Angka 1-5 | 5 |
| Review Text | Teks panjang | "sarapan enak, staf ramah, kamar bersih..." |
| Nama Hotel | Teks | Banaran 9 Resort, Hotel Indonesia Kempinski, dll |
| Kategori | Teks | BUMN atau KOMPETITOR |
| Bintang | Teks | bintang3, bintang4, bintang5 |
| AI_Sentiment | Teks | Positive, Negative, atau Neutral |
| AI_Primary_Theme | Teks | Kebersihan, Makanan & Minuman, Pelayanan Staf, dll |
| AI_All_Themes | Teks | "Makanan & Minuman (0.47); Pelayanan Staf (0.39); Harga (0.35)" |

**Distribusi Sentimen:**
- Positive: 125.395 (75.6%)
- Negative: 35.307 (21.3%)
- Neutral: 5.260 (3.2%)

**Distribusi Kategori:**
- KOMPETITOR: 110.265 ulasan
- BUMN: 55.697 ulasan

**12 Aspek yang tersedia:**
Kebersihan, Kualitas Kamar, Fasilitas Hotel, Makanan & Minuman, Pelayanan Staf, Kecepatan Layanan, Proses Check-in/out, Lokasi, Harga, Keamanan, Penanganan Keluhan, Fasilitas Khusus.

### Tabel 2: Frasa Kunci per Hotel (2.259 baris)
| Kolom | Contoh |
|-------|--------|
| Nama_Hotel | Banaran 9 Resort |
| Top_Positif_Phrase | kebun kopi |
| Bobot_Pos | 0.8139 |
| Top_Negatif_Phrase | tidak terawat |
| Bobot_Neg | -1.7513 |

---

## Halaman/Fitur yang Dibutuhkan

### Halaman 1: Ringkasan (Overview)
**Filter global** di sidebar atau di atas:
- Kategori: Semua / BUMN / KOMPETITOR (tombol radio atau toggle)
- Hotel: dropdown daftar hotel (berubah sesuai kategori yang dipilih)
- Periode: rentang waktu (slider atau date range picker)

**Konten halaman:**
- **4 kartu metrik** di baris atas:
  - Total Ulasan (contoh: 165.962)
  - Sentimen Positif (contoh: 75.6%)
  - Sentimen Negatif (contoh: 21.3%)
  - Rating Rata-rata (contoh: 4.2 / 5)
- **Grafik batang horizontal (diverging bar)**: menunjukkan persentase positif vs negatif per aspek pelayanan. Batang ke kanan = positif (hijau), batang ke kiri = negatif (merah). Ini grafik utama.
- **Donut chart**: distribusi topik apa yang paling sering dibahas tamu.
- **Radar chart** (muncul jika satu hotel dipilih): jaring laba-laba yang menunjukkan skor positif di setiap aspek. Bisa ditumpuk dengan rata-rata kategori sebagai perbandingan.
- **Kartu frasa kunci** (muncul jika satu hotel dipilih): dua kolom — kiri menampilkan 5 frasa kelemahan (merah muda), kanan menampilkan 5 frasa kekuatan (hijau muda). Setiap frasa punya skor bobot di sebelah kanan.

### Halaman 2: Perbandingan (BUMN vs Kompetitor)
- **Grouped bar chart**: batang berdampingan per aspek, warna biru untuk BUMN dan warna kuning/amber untuk Kompetitor. Sumbu Y = % sentimen positif.
- **Adu hotel spesifik**: 2 dropdown sejajar (pilih 1 BUMN, pilih 1 Kompetitor), di tengahnya label "vs".
  - Radar chart bertumpuk membandingkan kedua hotel.
  - Kartu frasa kelemahan kedua hotel berdampingan.

### Halaman 3: Peringkat Hotel (Ranking)
- **Tabel peringkat**: kolom = Rank, Nama Hotel, Kategori, Total Ulasan, % Positif, % Negatif, Rating, Aspek Terlemah. Baris diurutkan dari % Positif tertinggi. Sel % Positif diwarnai conditional (hijau jika tinggi, merah jika rendah).
- **Bubble scatter chart**: sumbu X = % Positif, sumbu Y = Rating, ukuran bubble = jumlah ulasan, warna = kategori (biru BUMN, amber Kompetitor). Garis rata-rata vertikal dan horizontal membagi menjadi 4 kuadran.

### Halaman 4: Tren Waktu
- **Line chart**: sumbu X = bulan, sumbu Y = % sentimen positif. Garis dengan area fill transparan. Garis putus-putus horizontal menunjukkan rata-rata.
- **Stacked bar chart**: volume ulasan per bulan, ditumpuk positif (hijau) dan negatif (merah).

---

## Panduan Desain

### Tone
- **Corporate, bersih, profesional.** Seperti dashboard produk SaaS (Stripe, Linear, Notion).
- **BUKAN** dashboard data scientist yang penuh jargon teknis.
- Tidak ada emoji berlebihan. Tidak ada bahasa "AI-Powered" atau "Machine Learning".
- Bahasa interface dalam **Bahasa Indonesia**.

### Warna
- Background utama: putih (#ffffff)
- Background sekunder (sidebar, kartu): abu sangat muda (#f8fafc atau #f9fafb)
- Teks utama: abu gelap (#1e293b atau #111827)
- Teks sekunder: abu medium (#6b7280)
- Border/garis: abu muda (#e5e7eb)
- Aksen positif/hijau: #22c55e
- Aksen negatif/merah: #ef4444
- Aksen BUMN/biru: #3b82f6
- Aksen Kompetitor/amber: #f59e0b
- Aksen ungu (opsional): #8b5cf6

### Tipografi
- Font: Inter (Google Fonts) atau sistem sans-serif.
- Judul halaman: 20-24px, font-weight 700.
- Label metrik: 11-12px, uppercase, letter-spacing 0.5px, warna abu.
- Nilai metrik: 28-32px, font-weight 700.
- Body text: 13-14px.

### Layout
- Lebar konten maksimal: 1100-1200px, center-aligned.
- Spacing antar section: 24-32px.
- Border-radius kartu: 8-12px.
- Navigasi antar halaman: tab bar horizontal di atas konten (bukan sidebar).
- Sidebar hanya untuk filter.

### Yang Harus Dihindari
- Dark mode / tema gelap.
- Warna neon atau gradien mencolok.
- Emoji di judul section.
- Istilah teknis AI/ML.
- Tampilan yang terlalu "dashboard template" generik.
- Elemen dekoratif tanpa fungsi.

---

## Contoh Teks untuk Mockup

- Judul sidebar: "Filter Data"
- Label filter: "Kategori", "Hotel", "Periode"
- Tab: "Ringkasan", "Perbandingan", "Peringkat", "Tren"
- Kartu metrik: "Total Ulasan: 55.697", "Sentimen Positif: 72.3%", "Sentimen Negatif: 24.1%", "Rating Rata-rata: 3.8 / 5"
- Judul grafik: "Sentimen per Aspek", "Distribusi Topik", "Profil Aspek", "Frasa Kunci"
- Contoh aspek: Kebersihan, Makanan & Minuman, Pelayanan Staf, Lokasi, Harga, Fasilitas Hotel
- Contoh frasa negatif: "tidak terawat", "ac rusak", "pelayanan lambat"
- Contoh frasa positif: "kebun kopi", "staf ramah", "sarapan enak"
- Nama hotel contoh: "Banaran 9 Resort" (BUMN), "Hotel Indonesia Kempinski" (Kompetitor)
