# 📚 Panduan Lengkap: Cara Mengakses Kode yang Sudah Diperbaiki

**Untuk Pemula GitHub** 🌟

Panduan ini akan membantu kamu mengakses dan menggunakan kode yang sudah diperbaiki, meskipun kamu masih awam dengan GitHub.

---

## 🎯 Pilihan 1: Lihat di GitHub (Paling Mudah - Tidak Perlu Install Apa-apa)

### Langkah 1: Buka GitHub
1. Buka browser kamu (Chrome, Firefox, dll)
2. Pergi ke: **https://github.com/bagus5142/Projek-Analisis-Ulasan-Hotel**

### Langkah 2: Pilih Branch dengan Perbaikan
1. Di halaman repository, lihat di bagian atas kiri ada tombol yang tulisannya **"main"** atau **"master"**
2. Klik tombol tersebut
3. Pilih branch: **`copilot/analyze-code-structure`**
4. Sekarang kamu melihat kode yang sudah diperbaiki! 🎉

### Langkah 3: Lihat File-file Baru
File-file baru yang sudah saya buat:
- 📄 **RINGKASAN_INDONESIA.md** - Baca ini dulu! Penjelasan lengkap dalam bahasa Indonesia
- 📄 **README.md** - Panduan lengkap proyek
- 📄 **CODE_ANALYSIS.md** - Analisis teknis
- 📄 **requirements.txt** - Daftar library yang dibutuhkan
- 📁 **config/** folder - File konfigurasi
- 📁 **tests/** folder - File testing
- 📄 **src/utils.py** - Fungsi-fungsi utility baru
- 📄 **src/config.py** - Konfigurasi terpusat

### Langkah 4: Lihat Apa yang Berubah
1. Klik tab **"Pull requests"** di bagian atas
2. Atau langsung ke: https://github.com/bagus5142/Projek-Analisis-Ulasan-Hotel/pulls
3. Cari Pull Request dengan judul yang mengandung "analyze-code-structure"
4. Di sana kamu bisa lihat semua perubahan secara detail

---

## 💻 Pilihan 2: Download Kode (Tanpa Git)

### Cara Termudah - Download ZIP:

1. **Pergi ke branch yang benar:**
   - Buka: https://github.com/bagus5142/Projek-Analisis-Ulasan-Hotel
   - Klik dropdown **"main"** → Pilih **"copilot/analyze-code-structure"**

2. **Download sebagai ZIP:**
   - Klik tombol hijau **"Code"** 
   - Pilih **"Download ZIP"**
   - File ZIP akan terdownload

3. **Extract dan Gunakan:**
   - Extract file ZIP ke folder kamu
   - Buka folder hasil extract
   - Semua file sudah ada di sana!

4. **Jalankan Dashboard:**
   ```bash
   # Install dependencies dulu
   pip install -r requirements.txt
   
   # Jalankan dashboard
   cd src
   streamlit run visual.py
   ```

---

## 🔧 Pilihan 3: Pakai Git (Lebih Proper - Butuh Install Git)

### A. Kalau Belum Punya Git

#### Untuk Windows:
1. Download Git dari: https://git-scm.com/download/win
2. Install dengan klik Next-Next-Next
3. Setelah install, buka **Git Bash** atau **Command Prompt**

#### Untuk Mac:
1. Buka Terminal
2. Ketik: `git --version`
3. Kalau belum ada, ikuti instruksi untuk install

#### Untuk Linux:
```bash
sudo apt-get install git  # Ubuntu/Debian
sudo yum install git      # CentOS/Fedora
```

### B. Clone Repository (Download dengan Git)

1. **Buka Terminal/Command Prompt/Git Bash**

2. **Masuk ke folder yang kamu inginkan:**
   ```bash
   cd Documents
   # Atau folder lain yang kamu mau
   ```

3. **Clone repository:**
   ```bash
   git clone https://github.com/bagus5142/Projek-Analisis-Ulasan-Hotel.git
   ```

4. **Masuk ke folder:**
   ```bash
   cd Projek-Analisis-Ulasan-Hotel
   ```

5. **Pindah ke branch dengan perbaikan:**
   ```bash
   git checkout copilot/analyze-code-structure
   ```

6. **Sekarang kamu sudah punya kode yang diperbaiki!** 🎉

### C. Update Kode (Kalau Sudah Clone Sebelumnya)

Kalau kamu sudah pernah clone tapi mau update:

```bash
# Masuk ke folder repository
cd Projek-Analisis-Ulasan-Hotel

# Download update terbaru
git fetch origin

# Pindah ke branch dengan perbaikan
git checkout copilot/analyze-code-structure

# Pull update terbaru
git pull origin copilot/analyze-code-structure
```

---

## 🚀 Cara Menjalankan Dashboard Setelah Download

### Langkah 1: Install Python (Kalau Belum Ada)
- Download Python dari: https://www.python.org/downloads/
- Install dengan centang "Add Python to PATH"
- Versi Python 3.8 atau lebih baru

### Langkah 2: Install Dependencies
Buka Terminal/Command Prompt di folder project, lalu:

```bash
# Install semua library yang dibutuhkan
pip install -r requirements.txt
```

### Langkah 3: Jalankan Dashboard
```bash
# Masuk ke folder src
cd src

# Jalankan dashboard
streamlit run visual.py
```

### Langkah 4: Buka di Browser
- Dashboard akan otomatis terbuka di browser
- Atau buka manual: http://localhost:8501

---

## 🧪 Cara Menjalankan Tests (Opsional)

Untuk memastikan semua berjalan dengan baik:

```bash
# Dari folder root project
pytest tests/ -v
```

Harusnya muncul:
```
13 passed in 0.34s ✅
```

---

## 📁 Struktur File yang Sudah Diperbaiki

```
Projek-Analisis-Ulasan-Hotel/
│
├── 📄 RINGKASAN_INDONESIA.md    ⭐ BACA INI DULU!
├── 📄 README.md                  - Panduan lengkap
├── 📄 CODE_ANALYSIS.md           - Analisis teknis
├── 📄 CONTRIBUTING.md            - Panduan kontribusi
├── 📄 DEPLOYMENT.md              - Panduan deployment
├── 📄 SUMMARY.md                 - Ringkasan eksekutif
├── 📄 requirements.txt           - Daftar library
├── 📄 .gitignore                 - File yang diabaikan Git
│
├── 📁 config/
│   └── hotel_categories.json    - Konfigurasi hotel
│
├── 📁 src/
│   ├── visual.py                - Dashboard utama
│   ├── config.py                - Konfigurasi terpusat
│   ├── utils.py                 - Fungsi utility
│   └── *.ipynb                  - Notebook analisis
│
├── 📁 tests/
│   ├── __init__.py
│   └── test_utils.py            - 13 unit tests
│
├── 📁 DatasetHotel/             - Data mentah
├── 📁 DatasetHotelCLEAN/        - Data bersih
└── 📁 Results/                  - Hasil analisis
```

---

## 💡 Tips Penting

### 1. Lihat File RINGKASAN_INDONESIA.md Dulu
File ini berisi penjelasan lengkap tentang apa yang sudah diperbaiki:
```bash
# Di Windows
notepad RINGKASAN_INDONESIA.md

# Di Mac/Linux
cat RINGKASAN_INDONESIA.md
# atau
open RINGKASAN_INDONESIA.md
```

### 2. File Asli Tidak Berubah
File `src/visual.py` (dashboard utama) **TIDAK DIUBAH**.
Saya hanya menambahkan file-file baru untuk perbaikan.

### 3. Bisa Langsung Pakai
Kamu bisa langsung pakai dashboard seperti biasa:
```bash
cd src
streamlit run visual.py
```

### 4. File Baru Opsional
File-file baru (utils.py, config.py, tests/) adalah opsional.
Kamu bisa pakai kalau mau perbaiki dashboard lebih lanjut.

---

## 🤔 Kalau Ada Masalah

### "Git command not found"
- Install Git dulu (lihat Pilihan 3A)

### "pip command not found"
- Install Python dulu
- Atau coba: `python -m pip install -r requirements.txt`

### "Module not found"
- Pastikan sudah install dependencies:
  ```bash
  pip install -r requirements.txt
  ```

### "Can't find file Analisis_Master_Lengkap.csv"
- Pastikan file data ada di folder `src/`
- Atau jalankan notebook preprocessing dulu

### Masih Bingung?
1. Buka file **RINGKASAN_INDONESIA.md**
2. Baca bagian yang relevan
3. Atau gunakan **Pilihan 1** (lihat di GitHub) - paling mudah!

---

## 📞 Ringkasan Singkat (TL;DR)

**Cara Paling Mudah (Tidak Perlu Install):**
1. Buka: https://github.com/bagus5142/Projek-Analisis-Ulasan-Hotel
2. Klik dropdown "main" → Pilih "copilot/analyze-code-structure"
3. Klik "Code" → "Download ZIP"
4. Extract ZIP, install dependencies, jalankan!

**Atau dengan Git:**
```bash
git clone https://github.com/bagus5142/Projek-Analisis-Ulasan-Hotel.git
cd Projek-Analisis-Ulasan-Hotel
git checkout copilot/analyze-code-structure
pip install -r requirements.txt
cd src
streamlit run visual.py
```

**File Penting untuk Dibaca:**
1. ⭐ **RINGKASAN_INDONESIA.md** - Penjelasan lengkap dalam bahasa Indonesia
2. 📄 **README.md** - Panduan teknis
3. 📄 **CODE_ANALYSIS.md** - Analisis mendalam

---

## ✅ Checklist Langkah-langkah

Centang setiap langkah yang sudah kamu lakukan:

- [ ] Buka repository di GitHub
- [ ] Pilih branch `copilot/analyze-code-structure`
- [ ] Download/Clone kode
- [ ] Install Python (kalau belum)
- [ ] Install dependencies: `pip install -r requirements.txt`
- [ ] Baca file RINGKASAN_INDONESIA.md
- [ ] Jalankan dashboard: `streamlit run src/visual.py`
- [ ] (Opsional) Jalankan tests: `pytest tests/ -v`

---

**Selamat! Kamu sekarang bisa mengakses dan menggunakan kode yang sudah diperbaiki!** 🎉

Jika ada pertanyaan, lihat file **RINGKASAN_INDONESIA.md** untuk penjelasan lebih detail.
