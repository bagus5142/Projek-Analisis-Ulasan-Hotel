# 💡 Ide Data Mining Tambahan — Dataset Ulasan Hotel

## Yang Sudah Dilakukan

Berdasarkan pipeline yang ada, project ini sudah melakukan:
- ✅ **Preprocessing** — Cleaning teks, normalisasi slang, translasi EN→ID (NLLB-200)
- ✅ **Sentiment Analysis** — Klasifikasi Positif/Negatif/Netral (IndoBERT-RoBERTa)
- ✅ **Aspect-Based Classification** — Zero-shot ke 23 topik (mDeBERTa)
- ✅ **Segmentasi** — BUMN vs Kompetitor, Bintang 3/4/5
- ✅ **Visualisasi & Dashboard** — Grafik distribusi topik, sentimen, dll.

---

## 🚀 Ide Mining Tambahan yang Bisa Dilakukan

### 1. 📊 Analisis Tren Waktu (Temporal Mining)
> Kolom `Review Time` sudah ada dan dikonversi ke Tahun!

**Apa yang bisa digali:**
- Tren sentimen per tahun (apakah kualitas hotel membaik/memburuk?)
- Topik apa yang paling banyak dikeluhkan sebelum vs sesudah pandemi (2020-2021)
- Perbandingan rating BUMN vs Kompetitor dari waktu ke waktu
- Peak complaint period — bulan/tahun berapa ulasan negatif paling banyak muncul

```python
# Contoh sederhana
df.groupby(['Review Time', 'Tipe', 'AI_Sentiment']).size().unstack().plot()
```

---

### 2. 🔤 Topic Modeling — LDA / BERTopic
> Berbeda dari zero-shot yang pakai label tetap, ini **menemukan topik secara otomatis**

**Apa yang bisa digali:**
- Topik tersembunyi yang tidak ter-cover oleh 23 label yang sudah ada
- Cluster kata kunci yang sering muncul bersamaan di ulasan negatif
- Perbandingan topik dominan BUMN vs Kompetitor secara unsupervised

**Tools:** `gensim` (LDA) atau `bertopic` (lebih modern, berbasis embedding)

```python
from bertopic import BERTopic
topic_model = BERTopic(language="multilingual")
topics, probs = topic_model.fit_transform(df['clean_text'].tolist())
```

---

### 3. 🧩 Association Rule Mining (Market Basket Analysis)
> **Apakah ada pola kombinasi aspek yang sering muncul bersamaan?**

**Contoh insight yang bisa ditemukan:**
- Ulasan yang menyebut "Kamar Kotor" juga sering menyebut "Pelayanan Buruk" → artinya 2 masalah ini saling berkaitan
- Ulasan positif tentang "Lokasi" + "Value for Money" → driver kepuasan utama
- Rekomendasi perbaikan: kalau hotel bisa fix satu masalah, masalah apa yang paling sering co-occur?

**Tools:** `mlxtend` dengan Apriori/FP-Growth

```python
from mlxtend.frequent_patterns import apriori, association_rules
# Ubah kolom AI_All_Themes jadi one-hot encoding lalu jalankan Apriori
```

---

### 4. 👤 Segmentasi Reviewer (Clustering)
> **Siapa tipe tamu yang memberikan ulasan?**

Kolom yang bisa dipakai: `Rating`, `Review Time`, tema dominan, sentimen, panjang teks

**Cluster yang mungkin ditemukan:**
- 🏢 Business Traveler — ulasan singkat, fokus di WiFi, Check-in, Lokasi
- 👨‍👩‍👧 Family — ulasan panjang, fokus di Kolam Renang, Sarapan, Parkir
- 💑 Couple — fokus di Ambience, Romantis, Special Service
- 🎒 Budget Traveler — banyak menyebut Value for Money, Price

**Tools:** `KMeans` atau `HDBSCAN` di atas TF-IDF/Sentence Embedding

---

### 5. 📈 Competitive Gap Analysis
> **Di aspek mana BUMN paling tertinggal dari Kompetitor?**

**Yang bisa dihitung:**
- Sentiment Score rata-rata per aspek: BUMN vs Kompetitor (per bintang)
- Gap score = `SkorKompetitor - SkorBUMN` per topik → identifikasi priority improvement area
- Heatmap weakness BUMN: aspek mana yang paling merah?

```python
# Contoh output: tabel gap score per aspek
gap_table = df.groupby(['Tipe', 'AI_Primary_Theme'])['AI_Sentiment_Score'].mean().unstack('Tipe')
gap_table['GAP'] = gap_table['KOMPETITOR'] - gap_table['BUMN']
```

---

### 6. 💬 Keyword Extraction & Word Cloud per Sentimen
> **Kata apa yang paling sering disebut di ulasan positif vs negatif?**

**Lebih dari sekadar word cloud biasa:**
- TF-IDF per sentimen untuk menemukan kata yang *benar-benar* membedakan positif dari negatif
- Bigram/Trigram: "kamar tidak bersih", "sarapan lezat", "staff ramah sekali"
- Perbandingan vocabulary BUMN vs Kompetitor

**Tools:** `sklearn TfidfVectorizer`, `wordcloud`, `YAKE` (keyword extractor)

---

### 7. 📉 Anomaly Detection — Hotel Outlier
> **Hotel mana yang performanya jauh di bawah atau di atas rata-rata grupnya?**

**Use case:**
- Identifikasi hotel BUMN yang performanya setara Kompetitor (best practice)
- Identifikasi hotel yang mendapat banyak ulasan negatif ekstrem (perlu intervensi segera)
- Deteksi hotel yang memiliki pola sentimen aneh (naik-turun drastis)

**Tools:** `IsolationForest`, Z-score analysis, atau heatmap anomali

---

### 8. 🌍 Geospatial Analysis
> **Apakah lokasi kota/wilayah mempengaruhi pola ulasan?**

**Yang bisa digali:**
- Hotel di Bali vs Jakarta vs Surabaya — apakah aspek keluhannya berbeda?
- Peta sebaran rating hotel BUMN di seluruh Indonesia
- Apakah hotel di kota wisata lebih banyak keluhan tentang "Overpriced"?

**Tools:** `folium` atau `plotly` untuk peta interaktif

---

### 9. 🤖 Aspect Sentiment (ABSA) yang Lebih Granular
> Yang sekarang: satu sentimen per ulasan. Yang diusulkan: **sentimen per aspek dalam satu ulasan**

**Contoh:**
> _"Kamar sangat bersih ✅ tapi pelayanan resepsionis sangat lambat ❌"_
- Kamar → **Positif**
- Pelayanan → **Negatif**

**Model yang bisa dipakai:**
- `InstructABSA` (fine-tuned untuk ABSA)
- Prompt-based dengan LLM kecil (mis. Qwen2.5 atau Llama 3.2)

---

### 10. 📝 Automatic Review Summarization
> **Buat ringkasan otomatis dari ratusan ulasan per hotel**

**Output yang berguna:**
- "3 kelebihan utama hotel X menurut 500 tamu adalah..."
- "Keluhan terbanyak di hotel Y adalah..."
- Bisa dipakai untuk laporan manajemen otomatis

**Tools:** `facebook/bart-large-cnn`, `Falconsai/text_summarization`, atau API Gemini/GPT

---

## 🏆 Prioritas Rekomendasi

| # | Ide | Kesulitan | Nilai Insight | Cocok untuk Skripsi/Paper? |
|---|-----|-----------|--------------|---------------------------|
| 5 | Competitive Gap Analysis | ⭐ Mudah | ⭐⭐⭐⭐⭐ | ✅ Sangat Cocok |
| 1 | Analisis Tren Waktu | ⭐ Mudah | ⭐⭐⭐⭐ | ✅ Sangat Cocok |
| 6 | Keyword/TF-IDF per Sentimen | ⭐⭐ Sedang | ⭐⭐⭐⭐ | ✅ Cocok |
| 3 | Association Rule Mining | ⭐⭐ Sedang | ⭐⭐⭐⭐ | ✅ Cocok |
| 4 | Segmentasi Reviewer | ⭐⭐ Sedang | ⭐⭐⭐ | ✅ Cocok |
| 2 | Topic Modeling (BERTopic) | ⭐⭐⭐ Menengah | ⭐⭐⭐⭐ | ✅ Cocok |
| 9 | ABSA Granular | ⭐⭐⭐⭐ Sulit | ⭐⭐⭐⭐⭐ | ✅ Nilai tinggi |
| 7 | Anomaly Detection | ⭐⭐ Sedang | ⭐⭐⭐ | ✅ Cocok |
| 8 | Geospatial | ⭐⭐ Sedang | ⭐⭐⭐ | 🔄 Opsional |
| 10 | Summarization | ⭐⭐⭐ Menengah | ⭐⭐⭐ | 🔄 Opsional |
