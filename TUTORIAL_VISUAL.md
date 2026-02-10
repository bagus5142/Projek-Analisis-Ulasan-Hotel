# 🎬 Tutorial Visual: Cara Download Kode dari GitHub

**Panduan Langkah-demi-Langkah dengan Gambar untuk Pemula** 📸

---

## 🌟 Metode 1: Download Langsung (PALING MUDAH)

### Langkah 1: Buka Repository
```
🔗 Link: https://github.com/bagus5142/Projek-Analisis-Ulasan-Hotel
```

**Yang Harus Kamu Lakukan:**
- Buka link di atas di browser kamu
- Kamu akan melihat halaman repository GitHub

---

### Langkah 2: Pilih Branch yang Benar

**Cari bagian ini di halaman:**
```
┌─────────────────────────────────────┐
│  bagus5142 / Projek-Analisis-Ulasan-Hotel  │
├─────────────────────────────────────┤
│  [main ▼]  <-- KLIK INI             │
└─────────────────────────────────────┘
```

**Langkah-langkahnya:**
1. ✅ Klik dropdown yang bertuliskan "main" atau "master"
2. ✅ Akan muncul daftar branch
3. ✅ Cari dan klik: **`copilot/analyze-code-structure`**

**Setelah diklik, halaman akan refresh dan menampilkan kode yang sudah diperbaiki!**

---

### Langkah 3: Download Kode

**Cari tombol hijau "Code":**
```
┌──────────────────────────────┐
│  < > Code  ▼     [hijau]    │  <-- KLIK INI
└──────────────────────────────┘
```

**Akan muncul menu dropdown:**
```
┌────────────────────────────────┐
│  Clone                         │
│  ┌──────────────────────────┐ │
│  │ HTTPS │ SSH │ GitHub CLI  │ │
│  └──────────────────────────┘ │
│  https://github.com/...       │
│  📋 [Copy]                    │
│                                │
│  ─────────────────────────    │
│  📦 Download ZIP  <-- KLIK!   │
└────────────────────────────────┘
```

**Klik "Download ZIP"** dan file akan terdownload!

---

### Langkah 4: Extract dan Gunakan

**Di Windows:**
1. Klik kanan file ZIP yang terdownload
2. Pilih "Extract All..."
3. Pilih lokasi folder
4. Klik "Extract"

**Di Mac:**
1. Double-click file ZIP
2. Otomatis akan extract

**Di Linux:**
```bash
unzip Projek-Analisis-Ulasan-Hotel-copilot-analyze-code-structure.zip
```

---

### Langkah 5: Buka Folder dan Lihat File

Setelah extract, buka folder. Kamu akan melihat:

```
📁 Projek-Analisis-Ulasan-Hotel-copilot-analyze-code-structure/
   ├── 📄 CARA_AKSES_KODE.md         ⭐ (file ini)
   ├── 📄 RINGKASAN_INDONESIA.md     ⭐ (BACA INI!)
   ├── 📄 README.md
   ├── 📄 CODE_ANALYSIS.md
   ├── 📄 requirements.txt
   ├── 📁 config/
   ├── 📁 src/
   ├── 📁 tests/
   └── ... (file lainnya)
```

**✅ SELESAI! Kode sudah kamu download!**

---

## 💻 Metode 2: Pakai Git Clone (Lebih Professional)

### Prasyarat: Install Git Dulu

**Cek apakah Git sudah terinstall:**
```bash
git --version
```

**Kalau muncul error "command not found":**

#### Windows:
1. Download dari: https://git-scm.com/download/win
2. Jalankan installer
3. Klik Next-Next-Next hingga selesai
4. Restart Command Prompt/PowerShell

#### Mac:
```bash
# Akan otomatis install Git
xcode-select --install
```

#### Linux (Ubuntu/Debian):
```bash
sudo apt-get update
sudo apt-get install git
```

---

### Langkah-langkah Clone dengan Git

**1. Buka Terminal/Command Prompt/PowerShell**

**Di Windows:**
- Tekan `Win + R`
- Ketik `cmd` atau `powershell`
- Enter

**Di Mac:**
- Tekan `Cmd + Space`
- Ketik `terminal`
- Enter

**Di Linux:**
- Tekan `Ctrl + Alt + T`

---

**2. Masuk ke Folder yang Kamu Inginkan**

```bash
# Contoh: Masuk ke folder Documents
cd Documents

# Atau masuk ke Desktop
cd Desktop

# Atau buat folder baru
mkdir MyProjects
cd MyProjects
```

---

**3. Clone Repository**

Copy dan paste command ini:
```bash
git clone https://github.com/bagus5142/Projek-Analisis-Ulasan-Hotel.git
```

**Kamu akan melihat output seperti ini:**
```
Cloning into 'Projek-Analisis-Ulasan-Hotel'...
remote: Enumerating objects: 150, done.
remote: Counting objects: 100% (150/150), done.
remote: Compressing objects: 100% (100/100), done.
remote: Total 150 (delta 50), reused 150 (delta 50)
Receiving objects: 100% (150/150), 5.25 MiB | 2.50 MiB/s, done.
Resolving deltas: 100% (50/50), done.
```

---

**4. Masuk ke Folder Repository**

```bash
cd Projek-Analisis-Ulasan-Hotel
```

---

**5. Pindah ke Branch dengan Perbaikan**

```bash
git checkout copilot/analyze-code-structure
```

**Output:**
```
Switched to branch 'copilot/analyze-code-structure'
Your branch is up to date with 'origin/copilot/analyze-code-structure'.
```

---

**6. Lihat File-file yang Ada**

```bash
# Windows
dir

# Mac/Linux
ls -la
```

**✅ SELESAI! Kode sudah siap digunakan!**

---

## 🚀 Cara Menjalankan Dashboard

### Langkah 1: Pastikan Python Terinstall

```bash
python --version
# atau
python3 --version
```

**Harus Python 3.8 atau lebih baru.**

**Kalau belum ada, download dari:**
- https://www.python.org/downloads/
- **PENTING:** Saat install, centang "Add Python to PATH"

---

### Langkah 2: Install Dependencies

Dari folder root project:

```bash
pip install -r requirements.txt
```

**Akan muncul:**
```
Collecting pandas>=1.5.0
Downloading pandas-1.5.3-cp39-cp39-win_amd64.whl (11.0 MB)
...
Successfully installed pandas-1.5.3 numpy-1.24.0 streamlit-1.28.0 ...
```

**Tunggu sampai selesai (mungkin 1-3 menit)**

---

### Langkah 3: Jalankan Dashboard

```bash
cd src
streamlit run visual.py
```

**Akan muncul:**
```
  You can now view your Streamlit app in your browser.

  Local URL: http://localhost:8501
  Network URL: http://192.168.1.100:8501
```

**Dashboard akan otomatis terbuka di browser!** 🎉

---

### Langkah 4: Gunakan Dashboard

**Browser akan terbuka dan kamu akan melihat:**
```
┌─────────────────────────────────────────────┐
│  Dashboard Analisis Hotel - Advanced        │
├─────────────────────────────────────────────┤
│  Sidebar:                    │  Main:       │
│  - Filter Kelas Hotel        │  - Overview  │
│  - Filter Kategori           │  - Charts    │
│  - Filter Sentimen           │  - Data      │
│                              │              │
│  Tab 1: Overview             │  [Grafik]    │
│  Tab 2: BUMN vs Non-BUMN     │  [Analisis]  │
│  Tab 3: Analisis Detail      │  [Insight]   │
│  ...                         │              │
└─────────────────────────────────────────────┘
```

**✅ Dashboard sudah berjalan!**

---

## 📖 Cara Membaca File Dokumentasi

### Buka File Markdown (.md)

**Di Windows:**
```bash
# Buka dengan Notepad
notepad RINGKASAN_INDONESIA.md

# Atau dengan VS Code (kalau ada)
code RINGKASAN_INDONESIA.md
```

**Di Mac:**
```bash
# Buka dengan TextEdit
open -a TextEdit RINGKASAN_INDONESIA.md

# Atau dengan VS Code
code RINGKASAN_INDONESIA.md
```

**Di Linux:**
```bash
# Buka dengan editor default
xdg-open RINGKASAN_INDONESIA.md

# Atau dengan gedit
gedit RINGKASAN_INDONESIA.md
```

**Atau lihat di GitHub:**
- Buka: https://github.com/bagus5142/Projek-Analisis-Ulasan-Hotel
- Pilih branch: `copilot/analyze-code-structure`
- Klik file yang ingin dibaca
- GitHub akan render file Markdown dengan bagus!

---

## 🧪 (Opsional) Jalankan Tests

Untuk memastikan semua berjalan dengan baik:

```bash
# Dari folder root project (bukan di folder src)
cd ..  # Kalau masih di folder src
pytest tests/ -v
```

**Output yang diharapkan:**
```
========================= test session starts =========================
platform linux -- Python 3.9.0, pytest-7.4.0, pluggy-1.0.0
collected 13 items

tests/test_utils.py::test_categorize_hotel_exact_match PASSED    [  7%]
tests/test_utils.py::test_categorize_hotel_partial_match PASSED  [ 15%]
tests/test_utils.py::test_categorize_hotel_unknown PASSED        [ 23%]
tests/test_utils.py::test_validate_dataframe_valid PASSED        [ 30%]
tests/test_utils.py::test_validate_dataframe_missing_columns PASSED [ 38%]
tests/test_utils.py::test_validate_dataframe_empty PASSED        [ 46%]
tests/test_utils.py::test_calculate_aspect_score_simple PASSED   [ 53%]
tests/test_utils.py::test_calculate_aspect_score_simple_no_data PASSED [ 61%]
tests/test_utils.py::test_clean_text_for_wordcloud_basic PASSED  [ 69%]
tests/test_utils.py::test_clean_text_for_wordcloud_empty PASSED  [ 76%]
tests/test_utils.py::test_format_number_basic PASSED             [ 84%]
tests/test_utils.py::test_format_number_thousands PASSED         [ 92%]
tests/test_utils.py::test_format_number_nan PASSED               [100%]

========================== 13 passed in 0.34s =========================
```

**✅ Semua test PASSED! Kode berjalan dengan baik!**

---

## 🎯 Ringkasan Cepat (Cheat Sheet)

### Download Kode (Metode Termudah):
```
1. Buka: github.com/bagus5142/Projek-Analisis-Ulasan-Hotel
2. Pilih branch: copilot/analyze-code-structure
3. Klik: Code → Download ZIP
4. Extract ZIP
5. Selesai!
```

### Download dengan Git:
```bash
git clone https://github.com/bagus5142/Projek-Analisis-Ulasan-Hotel.git
cd Projek-Analisis-Ulasan-Hotel
git checkout copilot/analyze-code-structure
```

### Install & Jalankan:
```bash
pip install -r requirements.txt
cd src
streamlit run visual.py
```

### Jalankan Tests:
```bash
pytest tests/ -v
```

---

## ❓ FAQ (Pertanyaan yang Sering Ditanya)

### Q: Apakah perlu install Git?
**A:** Tidak wajib. Kamu bisa download ZIP langsung dari GitHub (Metode 1).

### Q: File asli saya akan berubah?
**A:** Tidak! File `visual.py` tidak diubah. Saya hanya menambahkan file-file baru.

### Q: Bisa langsung pakai dashboard seperti biasa?
**A:** Ya! Dashboard bisa langsung dijalankan seperti biasa dengan `streamlit run visual.py`

### Q: Untuk apa file-file baru seperti utils.py dan config.py?
**A:** Itu adalah perbaikan dan utility tambahan. Opsional untuk digunakan. Baca RINGKASAN_INDONESIA.md untuk detail.

### Q: Gimana cara update kalau ada perubahan baru?
**A:** Kalau pakai Git, tinggal `git pull`. Kalau download ZIP, download ulang.

### Q: Dashboard error waktu dijalankan?
**A:** 
1. Pastikan file data (Analisis_Master_Lengkap.csv) ada di folder src/
2. Pastikan sudah install dependencies: `pip install -r requirements.txt`
3. Cek apakah Python versi 3.8 atau lebih baru

---

## 📚 File Dokumentasi yang Harus Dibaca

**Urutan prioritas:**
1. 🌟 **CARA_AKSES_KODE.md** (file ini) - Cara download & setup
2. ⭐ **RINGKASAN_INDONESIA.md** - Penjelasan lengkap apa yang diperbaiki
3. 📄 **README.md** - Panduan lengkap proyek
4. 📄 **CODE_ANALYSIS.md** - Analisis teknis mendalam

---

## ✅ Checklist: Apakah Saya Sudah Siap?

Centang setiap item:

**Setup:**
- [ ] Sudah download/clone kode
- [ ] Sudah di branch yang benar (`copilot/analyze-code-structure`)
- [ ] Python sudah terinstall (3.8+)
- [ ] Dependencies sudah terinstall (`pip install -r requirements.txt`)

**Pemahaman:**
- [ ] Sudah baca CARA_AKSES_KODE.md (file ini)
- [ ] Sudah baca RINGKASAN_INDONESIA.md
- [ ] Paham struktur folder proyek

**Testing:**
- [ ] Dashboard bisa dijalankan (`streamlit run visual.py`)
- [ ] (Opsional) Tests berjalan dengan baik (`pytest tests/ -v`)

**Jika semua tercentang, kamu sudah siap menggunakan kode yang diperbaiki!** 🎉

---

## 🎓 Tips untuk Pemula GitHub

1. **Branch = Versi Alternatif**
   - `main` = versi original
   - `copilot/analyze-code-structure` = versi dengan perbaikan

2. **Pull Request = Usulan Perubahan**
   - Tempat untuk review kode sebelum di-merge

3. **Clone vs Download ZIP**
   - Clone: Bisa update dengan `git pull`
   - ZIP: Harus download ulang untuk update

4. **Git itu Optional**
   - Kalau cuma mau pakai, ZIP sudah cukup
   - Kalau mau develop, lebih baik pakai Git

---

**Selamat Mencoba!** 🚀

Jika masih ada yang bingung, baca file **RINGKASAN_INDONESIA.md** untuk penjelasan lebih detail tentang apa yang sudah diperbaiki.
