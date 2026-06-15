# Rencana: Dashboard Analisis Ulasan Hotel (BUMN vs Kompetitor)

## Context

Proyek nyata untuk **pengelola hotel BUMN**. Tujuan: memvisualisasikan hasil analisis NLP atas **165.962 ulasan tamu hotel** (Google Maps) untuk presentasi ke Direksi, membandingkan kinerja pelayanan **hotel BUMN vs Kompetitor (swasta)** di Indonesia. Sumber kebenaran: `src/imports/brief_figma.md`.

Keputusan yang sudah dikonfirmasi user:
1. **Desain corporate bersih** (gaya Stripe/Linear/Notion). Tanpa dark mode, neon, monospace, emoji, atau jargon AI/ML. Bahasa Indonesia.
2. **Data asli dari model** harus bisa divisualisasikan → bangun **fitur upload CSV** untuk dua tabel di brief. **Mock data realistis** dipakai sebagai demo default agar dashboard langsung penuh sebelum upload.
3. **Visualisasi super detail**: perbandingan per-hotel, BUMN vs Kompetitor, **per-bintang (bintang3/4/5)**, drill-down detail hotel, dan banyak informasi turunan.

Proyek punya komponen shadcn/ui lengkap (`src/app/components/ui`), `recharts@2.15.2`, dan `ui/chart.tsx`. Tidak ada `@make-kits`. Perlu install **`papaparse`** (+ types) untuk parsing CSV.

## Skema Data (sesuai brief)

- **Tabel utama (per ulasan):** Review Time, Rating(1-5), Review Text, Nama Hotel, Kategori(BUMN/KOMPETITOR), Bintang(bintang3/4/5), AI_Sentiment(Positive/Negative/Neutral), AI_Primary_Theme(12 aspek), AI_All_Themes("Tema (skor); ...").
- **Tabel frasa (per hotel):** Nama_Hotel, Top_Positif_Phrase, Bobot_Pos, Top_Negatif_Phrase, Bobot_Neg.
- 12 aspek: Kebersihan, Kualitas Kamar, Fasilitas Hotel, Makanan & Minuman, Pelayanan Staf, Kecepatan Layanan, Proses Check-in/out, Lokasi, Harga, Keamanan, Penanganan Keluhan, Fasilitas Khusus.

## Theme (`src/styles/theme.css`, light-only)

Update `:root`: `--background #ffffff`, surface `#f9fafb`, `--card #ffffff`, `--foreground #111827`, muted-foreground `#6b7280`, border `#e5e7eb`. Tambah token semantik sekali & ekspor via `@theme inline`: `--c-pos #22c55e`, `--c-neg #ef4444`, `--c-neu #94a3b8`, `--c-bumn #3b82f6`, `--c-komp #f59e0b`, `--c-accent #8b5cf6`. Biarkan blok `.dark`. Tambah font Inter di `src/styles/fonts.css` (import paling atas).

## Arsitektur File

**Data & tipe**
- `src/app/data/types.ts` — `Review`, `PhraseRow`, `HotelAgg` (`{ id, nama, kategori, bintang, totalUlasan, rating, pctPos/Neg/Neu, aspek: Record<aspek,{pos,neg,total}>, frasaPos[], frasaNeg[], trenBulanan[] }`).
- `src/app/data/constants.ts` — 12 aspek, daftar bintang, warna semantik, label.
- `src/app/data/mockData.ts` — ~18–24 hotel (campuran BUMN & Kompetitor lintas bintang3/4/5) konsisten dengan agregat brief (Pos 75.6%, Neg 21.3%, Neu 3.2%; total 165.962; BUMN 55.697 / Kompetitor 110.265), tiap hotel punya skor per-aspek, frasa kunci, dan tren 12 bulan.

**Parsing & state**
- `src/app/lib/parseCsv.ts` — pakai `papaparse` (worker, header:true). Dua fungsi: `parseReviews(file)` → agregasi streaming ke `HotelAgg[]` (hitung pctSentimen, rating rata2, aspek dari AI_Primary_Theme + opsional AI_All_Themes, tren per bulan dari Review Time); `parsePhrases(file)` → gabungkan top frasa ke hotel by Nama_Hotel. Validasi kolom, tampilkan error ramah.
- `src/app/context/DataContext.tsx` — menyimpan `hotels: HotelAgg[]`, `source: 'mock'|'uploaded'`, `setHotelsFromUpload()`, `resetToMock()`.
- `src/app/context/FilterContext.tsx` — `{ kategori: 'SEMUA'|'BUMN'|'KOMPETITOR', bintang: 'SEMUA'|'bintang3'|'bintang4'|'bintang5', hotelId: string|null, periode:[startIdx,endIdx] }` + setter.
- `src/app/lib/aggregate.ts` — helper murni atas hasil filter: `applyFilter`, `metrics`, `aspectSentiment`, `topicDistribution`, `radarProfile`, `categoryByStar`, `gapAnalysis`, `rankHotels`, `ratingDistribution`, `monthlyTrend`, `bubbleData`.

**Layout**
- `src/app/App.tsx` (default export) — `DataProvider`→`FilterProvider`→ Header (judul + tombol "Muat Data CSV" buka `UploadDialog`, badge sumber data) + `FilterSidebar` (sticky kiri) + area kanan `TabBar` + halaman. Konten max-w ~1240px.
- `src/app/components/FilterSidebar.tsx` — "Filter Data": ToggleGroup Kategori; ToggleGroup/Select **Bintang**; Select Hotel (difilter kategori+bintang); Slider range Periode (label bulan). Menampilkan ringkas jumlah ulasan terfilter.
- `src/app/components/TabBar.tsx` — Tabs: Ringkasan · Perbandingan · Per Bintang · Peringkat · Detail Hotel · Tren.
- `src/app/components/UploadDialog.tsx` — Dialog: dua dropzone/input file (Data Ulasan, Frasa Kunci), tombol parse, progress, tombol "Kembali ke data demo".

**Charts** (`src/app/components/charts/`, recharts): `MetricCard`, `DivergingAspectBar`, `TopicDonut`, `AspectRadar` (multi-series overlay), `KeyPhrasesCard`, `GroupedAspectBar`, `BubbleScatter` (ReferenceLine 4 kuadran), `TrendLine` (area+ReferenceLine rata2), `VolumeStackedBar`, **`StarGroupedBar`** (BUMN vs Kompetitor per bintang), **`GapDivergingBar`** (selisih %pos BUMN−Kompetitor per aspek), **`AspectHeatmap`** (aspek×kategori atau aspek×bintang), **`RatingHistogram`** (distribusi rating 1-5 per kategori).

**Halaman** (`src/app/components/pages/`):
- `OverviewPage` — 4 MetricCard (Total, %Pos, %Neg, Rating); DivergingAspectBar (utama); TopicDonut; bila satu hotel dipilih → AspectRadar (hotel vs rata2 kategori) + KeyPhrasesCard.
- `ComparisonPage` — GroupedAspectBar BUMN vs Kompetitor; GapDivergingBar (aspek unggul/tertinggal); AspectHeatmap; "Adu Hotel": 2 Select (BUMN | vs | Kompetitor) → AspectRadar bertumpuk + 2 KeyPhrasesCard.
- `PerBintangPage` — StarGroupedBar %pos per bintang per kategori; RatingHistogram per kategori; small-multiples metrik ringkas per tier bintang.
- `RankingPage` — Table peringkat (Rank, Hotel, Kategori, Bintang, Total, %Pos, %Neg, Rating, Aspek Terlemah) urut %Pos desc, sel %Pos diwarnai kondisional, filter sortir kolom; BubbleScatter (%Pos×Rating, size=volume, warna=kategori, 4 kuadran).
- `HotelDetailPage` — pilih satu hotel → header profil (kategori, bintang, total, rating); AspectRadar hotel vs rata2 kategori & rata2 bintang; KeyPhrasesCard; RatingHistogram hotel; TrendLine hotel; tabel aspek terkuat/terlemah.
- `TrendsPage` — TrendLine %pos bulanan (+rata2); VolumeStackedBar volume pos/neg per bulan; opsi overlay BUMN vs Kompetitor.

## Catatan implementasi
- Gunakan komponen `ui/*` (`card`, `select`, `tabs`, `table`, `slider`, `toggle-group`, `radio-group`, `dialog`, `badge`, `separator`, `scroll-area`, `progress`). Grafik via recharts langsung / `ui/chart`.
- Angka diformat `toLocaleString('id-ID')` (pemisah titik). Warna konsisten dari token semantik.
- Hindari class Tailwind font-size/weight/line-height kecuali gaya khusus brief (label metrik uppercase kecil, nilai metrik besar) — di sana memang diminta.
- Visualisasi kondisional (radar, detail, frasa) hanya tampil saat relevan; semua halaman responsif.

## Verifikasi
1. App render tanpa error (dev server jalan; cek preview, bukan localhost). Demo mock langsung terisi.
2. Navigasi 6 tab berfungsi; semua grafik tampil dengan data mock.
3. Filter Kategori/Bintang/Hotel/Periode meng-update seluruh metrik & grafik; pilih hotel → Radar+Frasa muncul.
4. Upload dua CSV contoh → dashboard beralih ke data asli (badge "Data diunggah"); "Kembali ke data demo" memulihkan mock.
5. Per Bintang, Gap, Heatmap, Bubble (4 kuadran), Ranking (terurut+pewarnaan) tampil benar.
6. Tidak ada dark mode/neon; palet sesuai brief.

## Next steps (opsional)
- Ekspor halaman/laporan ke PDF untuk Direksi.
- Penyimpanan data terunggah (Supabase) agar persist antar sesi.
