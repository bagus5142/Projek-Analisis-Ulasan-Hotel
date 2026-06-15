# 🔍 Evaluasi Kritis Pipeline yang Sudah Ada

## Overview: Apa yang Sudah Dibuat?

```
Raw CSV (EN/ID) → Preprocessing (NLLB-200 Translate) → DatasetHotelCLEAN
                                                              ↓
                                           Model.ipynb (IndoBERT + mDeBERTa)
                                                              ↓
                                              Results (Sentimen + 23 Aspek)
```

---

## 🚨 Masalah 1: Preprocessing — Translasi yang Bermasalah

### Apa yang Dilakukan Sekarang
```python
# Di Preprocessing.ipynb
MODEL_NAME = "facebook/nllb-200-distilled-600M"
tokenizer.src_lang = "eng_Latn"  # <-- SELALU dianggap Bahasa INGGRIS
forced_bos_token_id = tokenizer.convert_tokens_to_ids("ind_Latn")  # → Ditranslate ke Indonesia
```

### ⚠️ Masalahnya
Kode ini mengasumsikan **semua ulasan berbahasa Inggris** dan menerjemahkannya ke Bahasa Indonesia. Padahal, dari output yang terlihat di Visualisasi.ipynb:

```
"dulu beberapa tahun yang lalu pernah kesini mu..."  ← Sudah Bahasa Indonesia!
"saya kesini di akhr bulan mei sprtinya masih l..."  ← Sudah Bahasa Indonesia!
```

**Artinya:** Ulasan yang sudah Bahasa Indonesia ikut di-translate ulang → hasilnya noise/distorsi teks!

### ✅ Solusi yang Lebih Baik: Deteksi Bahasa Dulu

```python
from langdetect import detect  # pip install langdetect

def smart_translate(text, model, tokenizer):
    try:
        lang = detect(text)
    except:
        lang = "id"  # default ke Indonesia
    
    if lang == "id":
        return text  # Sudah Indonesia, tidak perlu translate
    elif lang == "en":
        return translate_to_id(text, model, tokenizer)  # Baru translate
    else:
        return text  # Bahasa lain, biarkan apa adanya
```

**Dampak:** Mengurangi distorsi pada ulasan yang sudah Bahasa Indonesia (kemungkinan mayoritas data).

---

## 🚨 Masalah 2: Preprocessing — Normalisasi Teks yang Kurang Lengkap

### Apa yang Dilakukan Sekarang
```python
slang_dict = {
    'yg': 'yang', 'ga': 'tidak', 'gak': 'tidak',  # hanya ~50 kata
    ...
}
# Tidak ada: stopword removal, stemming, emoji handling
```

### ⚠️ Masalahnya
1. **Kamus slang terbatas** — hanya ~50 kata, padahal kosakata informal Indonesia ribuan kata
2. **Tidak ada stemming** — "berlari", "lari", "berlarian" dianggap kata berbeda
3. **Tidak ada stopword removal** — kata "yang", "di", "dan" ikut dianalisis
4. **Emoji tidak ditangani** — ⭐🙏😊 tidak dikonversi ke teks atau dihapus

### ✅ Solusi yang Lebih Baik

```python
# 1. Gunakan kamus slang yang lebih lengkap (komunitas Indonesia)
# Referensi: https://github.com/insomniachi/IndonesianSlangDictionary

# 2. Tambahkan Sastrawi untuk stemming Bahasa Indonesia
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
factory = StemmerFactory()
stemmer = factory.create_stemmer()
text = stemmer.stem("berlarian")  # → "lari"

# 3. Stopword removal
from nltk.corpus import stopwords
stop_words = set(stopwords.words('indonesian'))

# 4. Emoji handling
import emoji
text = emoji.demojize("Kamar bagus 😊")  # → "Kamar bagus :smiling_face:"
# atau hapus emoji sama sekali:
text = emoji.replace_emoji(text, replace='')
```

---

## 🚨 Masalah 3: Model Sentimen — Kurang Optimal untuk Data Campuran

### Apa yang Digunakan Sekarang
```python
model_sentiment = "w11wo/indonesian-roberta-base-sentiment-classifier"
```

### ⚠️ Masalahnya
- Model ini dilatih untuk teks **Indonesia bersih**, bukan teks campur-kode (Indonesia + Inggris)
- Rating bintang (1-5) tidak dimanfaatkan sebagai **ground truth** untuk validasi
- Hasilnya hanya **3 kelas** (positif/negatif/netral) — tidak ada granularitas

### ✅ Alternatif Model yang Lebih Baik

| Model | Keunggulan | Link |
|-------|-----------|------|
| `mdhugol/indonesia-bert-sentiment-classifier` | IndoBERT fine-tuned, lebih stabil | HuggingFace |
| `cahya/bert-base-indonesian-522M` | Corpus Indonesia lebih besar | HuggingFace |
| `papluca/xlm-roberta-base-language-detection` | Multilingual, cocok data campur | HuggingFace |
| `cardiffnlp/twitter-xlm-roberta-base-sentiment` | Multilingual, fine-tuned sentimen | HuggingFace |

### 💡 Ide yang Lebih Cerdas: Gunakan Rating sebagai Label

```python
# Rating 1-2 → Negatif, Rating 3 → Netral, Rating 4-5 → Positif
# Ini adalah "free ground truth" yang sudah ada di dataset!
df['Rating_Sentiment'] = df['Rating'].map({
    '1': 'negative', '2': 'negative',
    '3': 'neutral',
    '4': 'positive', '5': 'positive'
})

# Hitung akurasi model AI vs Rating asli
from sklearn.metrics import classification_report
print(classification_report(df['Rating_Sentiment'], df['AI_Sentiment']))
```

> [!TIP]
> Dengan cara ini kamu bisa **mengukur akurasi model** tanpa perlu labeling manual!

---

## 🚨 Masalah 4: Aspect Classification — Zero-shot dengan 23 Label

### Apa yang Digunakan Sekarang
```python
model_zeroshot = "MoritzLaurer/mDeBERTa-v3-base-mnli-xnli"
CANDIDATE_LABELS = [...]  # 23 topik
clf_aspect(texts, candidate_labels=CANDIDATE_LABELS, multi_label=True)
```

### ⚠️ Masalahnya

**1. Zero-shot = Tidak Dilatih Spesifik untuk Hotel**  
Model ini dilatih untuk Natural Language Inference umum, bukan untuk domain hotel. Artinya ia "menebak" berdasarkan kemiripan semantik label, bukan pemahaman konteks hotel.

**2. Label Tumpang Tindih Menyebabkan Dominasi Satu Topik**  
Dari hasil visualisasi:
```
BUMN:        Facilities & Amenities → 35% (sangat dominan!)
KOMPETITOR:  Facilities & Amenities → 29%
```
Topik "Facilities & Amenities" terlalu luas sehingga "menyerap" ulasan yang sebenarnya tentang Kamar, Restoran, dll.

**3. Top-1 saja yang diambil sebagai Primary Theme**  
Informasi dari multi-label (Top-3) tidak dieksploitasi maksimal.

### ✅ Solusi yang Lebih Baik

**Opsi A: Perbaiki Label — Buat Lebih Spesifik & Tidak Tumpang Tindih**
```python
# Sebelum (terlalu luas):
"Facilities & Amenities"  # Menyerap segalanya

# Sesudah (lebih spesifik):
"Swimming Pool & Recreation Facilities"
"Room Amenities & In-room Facilities"
"Hotel Lobby & Common Areas"
"Parking & Transportation"
```

**Opsi B: Fine-tune Model Khusus Domain Hotel**
```python
# Kumpulkan ~200-500 ulasan, label manual aspeknya
# Fine-tune IndoBERT atau XLM-RoBERTa untuk klasifikasi aspek hotel
# Hasilnya JAUH lebih akurat daripada zero-shot

from transformers import Trainer, TrainingArguments
# ... fine-tuning code
```

**Opsi C: Gunakan LLM dengan Prompt Engineering (Paling Mudah)**
```python
# Gunakan Gemini API (gratis tier) atau GPT-3.5 untuk labeling
import google.generativeai as genai

prompt = f"""
Ulasan hotel berikut membahas aspek apa? Pilih dari:
[Kebersihan Kamar, Kualitas Pelayanan, Makanan & Minuman, Fasilitas Kolam Renang, 
 Lokasi, Harga, Check-in/Check-out, WiFi & Teknologi]

Ulasan: "{review_text}"
Jawab dengan 1-3 aspek yang paling relevan.
"""
```

---

## 📊 Masalah 5: Tidak Ada Evaluasi / Validasi Model

### ⚠️ Masalahnya
Tidak ada kode yang mengukur **seberapa akurat** model yang digunakan. Ini membuat sulit untuk:
- Membandingkan antara model A vs model B
- Klaim dalam paper bahwa "model ini akurat X%"

### ✅ Solusi: Buat Evaluasi Cepat

```python
# Gunakan Rating sebagai proxy ground truth
df['Rating_num'] = pd.to_numeric(df['Rating'], errors='coerce')
df['Ground_Truth'] = df['Rating_num'].apply(lambda x: 
    'negative' if x <= 2 else ('neutral' if x == 3 else 'positive'))

from sklearn.metrics import classification_report, confusion_matrix

# Evaluasi Sentimen
report = classification_report(df['Ground_Truth'], df['AI_Sentiment'])
print(report)

# Confusion Matrix
cm = confusion_matrix(df['Ground_Truth'], df['AI_Sentiment'], 
                      labels=['positive', 'neutral', 'negative'])
```

---

## 🏆 Prioritas Perbaikan

| # | Masalah | Dampak | Effort | Prioritas |
|---|---------|--------|--------|-----------|
| 1 | **Deteksi Bahasa sebelum Translate** | 🔴 Tinggi (distorsi data) | ⭐ Mudah | 🥇 SEGERA |
| 2 | **Evaluasi model dengan Rating** | 🔴 Tinggi (validasi ilmiah) | ⭐ Mudah | 🥇 SEGERA |
| 3 | **Perbaiki label Aspect** | 🟠 Sedang (akurasi topik) | ⭐⭐ Sedang | 🥈 Penting |
| 4 | **Tambah Stemming + Stopword** | 🟠 Sedang (kualitas teks) | ⭐⭐ Sedang | 🥈 Penting |
| 5 | **Ganti model Sentimen** | 🟡 Sedang | ⭐⭐ Sedang | 🥉 Opsional |
| 6 | **Fine-tune Aspect model** | 🔴 Tinggi (akurasi max) | ⭐⭐⭐⭐ Sulit | 🔄 Jangka Panjang |

> [!IMPORTANT]
> **Paling kritis untuk paper/skripsi:** Masalah #2 (evaluasi) karena tanpa metric akurasi,
> klaim ilmiah tentang model tidak bisa dipertahankan.

> [!WARNING]
> **Masalah #1 (translasi)** bisa menyebabkan data sudah "rusak" sebelum masuk ke model.
> Jika dataset perlu diproses ulang, ini yang harus diperbaiki terlebih dahulu.
