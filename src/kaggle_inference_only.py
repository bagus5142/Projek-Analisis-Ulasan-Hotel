# ============================================================
# KAGGLE NOTEBOOK — INFERENCE & DATA MINING ONLY
# ============================================================
# Notebook ini HANYA bertugas menjalankan model AI tingkat tinggi
# menggunakan GPU Kaggle karena data sudah dibersihkan sebelumnya.
#
# CARA PAKAI:
# 1. Upload file MasterDataset_Hotel_Clean.csv ke Kaggle.
# 2. Aktifkan GPU T4x2 atau P100.
# 3. Copy-paste tiap Cell di bawah ini ke Kaggle dan jalankan.
# ============================================================


# ───────────────────────────────────────────────
# CELL 1 — Install library AI
# ───────────────────────────────────────────────
"""
!pip install -q sentence-transformers scikit-learn
print('✅ Instalasi pustaka selesai.')
"""


# ───────────────────────────────────────────────
# CELL 2 — Setup GPU & Import Modul
# ───────────────────────────────────────────────
"""
import os, gc, glob
import numpy as np
import pandas as pd
import torch
from tqdm.auto import tqdm
from transformers import pipeline
from sentence_transformers import SentenceTransformer

# Konfigurasi GPU
device    = 'cuda' if torch.cuda.is_available() else 'cpu'
device_id = 0 if device == 'cuda' else -1

print(f'Device : {device.upper()}')
if device == 'cuda':
    print(f'GPU    : {torch.cuda.get_device_name(0)}')
    print(f'VRAM   : {torch.cuda.get_device_properties(0).total_memory / 1e9:.1f} GB')
"""


# ───────────────────────────────────────────────
# CELL 3 — Cari Path Data Kaggle
# ───────────────────────────────────────────────
"""
# Menampilkan path file CSV yang baru diupload
import glob
all_csv = glob.glob('/kaggle/input/**/*.csv', recursive=True)
print(f'CSV ditemukan: {len(all_csv)}')
for f in all_csv:
    print('👉', f)
"""


# ───────────────────────────────────────────────
# CELL 4 — Load Dataset Bersih
# ───────────────────────────────────────────────
"""
# ⚠️ PASTE path dari output Cell 3 ke sini:
INPUT_CSV   = '/kaggle/input/nama-dataset-anda/MasterDataset_Hotel_Clean.csv'

OUTPUT_MASTER = '/kaggle/working/AI_Analisis_Master_Final.csv'
OUTPUT_BUMN   = '/kaggle/working/AI_Analisis_BUMN.csv'
OUTPUT_KOMP   = '/kaggle/working/AI_Analisis_KOMPETITOR.csv'
OUTPUT_KW     = '/kaggle/working/AI_Analisis_Keywords.csv'

df = pd.read_csv(INPUT_CSV)
print(f'Shape awal: {df.shape}')

# Pastikan data tidak kosong
df = df.dropna(subset=['Review Text']).reset_index(drop=True)
df['clean_text'] = df['Review Text'].astype(str)

print(f'Shape siap proses: {df.shape}')
print(f'Kolom tersedia   : {list(df.columns)}')
df.head(3)
"""


# ───────────────────────────────────────────────
# CELL 5 — Setup 12 Label Aspek Utama
# ───────────────────────────────────────────────
"""
ASPEK_LABELS = {
    "Kebersihan & Higienitas": "Standar kebersihan kamar, area publik, debu, masalah hama, linen, dan kolam renang.",
    "Kualitas Kamar & Kenyamanan": "Kondisi fisik kamar, kasur, insulasi suara, AC, TV, pencahayaan, dan perlengkapan.",
    "Fasilitas Hotel": "Kelengkapan fasilitas seperti gym, spa, lift, ruang pertemuan, lobby, dan parkir.",
    "Makanan & Minuman": "Kualitas sarapan, restoran hotel, layanan kamar, rasa, dan variasi menu.",
    "Kualitas & Sikap Pelayanan Staf": "Profesionalisme, keramahan, dan inisiatif staf resepsionis, housekeeping, dll.",
    "Efisiensi & Kecepatan Layanan": "Waktu tunggu check-in, kecepatan room service, dan efisiensi operasional.",
    "Check-in & Check-out": "Prosedur, waktu tunggu, dan kelancaran proses administrasi resepsionis.",
    "Lokasi & Aksesibilitas": "Lokasi strategis, kemudahan akses ke pusat kota, transportasi, dan jalan masuk.",
    "Harga & Nilai": "Kesesuaian harga hotel dengan kualitas (Value for Money), promo, dan transparansi tarif.",
    "Keamanan & Keselamatan": "Keamanan barang bawaan, CCTV, satpam, dan kunci kamar yang aman.",
    "Penanganan Keluhan": "Respons staf terhadap komplain, kecepatan penyelesaian masalah, dan kompensasi.",
    "Fitur Khusus (Halal / Keluarga)": "Mushola, makanan halal, fasilitas ramah anak (playground), dan kebutuhan khusus."
}

print(f'Total {len(ASPEK_LABELS)} Label Aspek siap.')
"""


# ───────────────────────────────────────────────
# CELL 6 — Inisialisasi Model AI (MULTI-GPU)
# ───────────────────────────────────────────────
"""
n_gpu = torch.cuda.device_count()
device_0 = 'cuda:0' if n_gpu > 0 else 'cpu'
device_1 = 'cuda:1' if n_gpu > 1 else device_0

print(f'Mendeteksi {n_gpu} GPU. Membagi beban kerja...')

print(f'Memuat Model Sentimen ke {device_0}...')
clf_sentimen = pipeline(
    'sentiment-analysis',
    model='w11wo/indonesian-roberta-base-sentiment-classifier',
    tokenizer='w11wo/indonesian-roberta-base-sentiment-classifier',
    device=0 if n_gpu > 0 else -1,
    torch_dtype=torch.float16 if n_gpu > 0 else torch.float32
)

print(f'Memuat Model Aspek ke {device_1}...')
model_embed = SentenceTransformer('paraphrase-multilingual-mpnet-base-v2', device=device_1)

LABEL_NAMES = list(ASPEK_LABELS.keys())
label_texts = [f"{n}: {d}" for n, d in ASPEK_LABELS.items()]

print('Pre-computing Embedding Label Aspek...')
LABEL_EMBEDDINGS = model_embed.encode(
    label_texts, normalize_embeddings=True, show_progress_bar=False, batch_size=32
)

print('✅ Seluruh Model AI Siap Memproses Data di 2 GPU!')
"""


# ───────────────────────────────────────────────
# CELL 7 — EKSEKUSI: Analisis Pararel (Multi-GPU)
# ───────────────────────────────────────────────
"""
import concurrent.futures

BATCH_SIZE = 128 if n_gpu > 0 else 16

# Batasi 2000 karakter per review untuk mencegah memori penuh
texts = [str(t)[:2000] for t in df['clean_text'].tolist()]
n = len(texts)

print(f'🚀 Memulai Inferensi Pararel pada {n:,} Ulasan...')

def run_sentimen(texts_input):
    sent_labels, sent_scores = [], []
    try:
        for i in tqdm(range(0, n, BATCH_SIZE), desc='1. Sentimen (GPU 0)', position=0, leave=True):
            batch = texts_input[i:i + BATCH_SIZE]
            res = clf_sentimen(batch, batch_size=BATCH_SIZE, truncation=True, max_length=512)
            sent_labels.extend([r['label'] for r in res])
            sent_scores.extend([round(r['score'], 6) for r in res])
    except Exception as e:
        print(f'Error Sentimen: {e}')
        sent_labels = ['neutral'] * n
        sent_scores = [0.0] * n
    return sent_labels, sent_scores

def run_aspek(texts_input):
    primary_list, all_list = [], []
    for i in tqdm(range(0, n, BATCH_SIZE), desc='2. Aspek    (GPU 1)', position=1, leave=True):
        batch = texts_input[i:i + BATCH_SIZE]
        text_embs = model_embed.encode(batch, normalize_embeddings=True, show_progress_bar=False, batch_size=BATCH_SIZE)
        sims = np.dot(text_embs, LABEL_EMBEDDINGS.T)
        
        top1_idx = sims.argmax(axis=1)
        top3_idxs = sims.argsort(axis=1)[:, -3:][:, ::-1]

        for j in range(len(batch)):
            primary_list.append(LABEL_NAMES[top1_idx[j]])
            top3 = '; '.join(f"{LABEL_NAMES[k]} ({sims[j][k]:.2f})" for k in top3_idxs[j])
            all_list.append(top3)
    return primary_list, all_list

# Menjalankan kedua fungsi secara BERSAMAAN di GPU 0 dan GPU 1
with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
    future_sentimen = executor.submit(run_sentimen, texts)
    future_aspek = executor.submit(run_aspek, texts)

    # Tunggu sampai keduanya selesai
    sent_labels, sent_scores = future_sentimen.result()
    primary_list, all_list = future_aspek.result()

df['AI_Sentiment'] = sent_labels
df['AI_Sentiment_Score'] = sent_scores
df['AI_Primary_Theme'] = primary_list
df['AI_All_Themes'] = all_list

if torch.cuda.is_available(): torch.cuda.empty_cache()
print('\\n✅ Inferensi Selesai! Waktu berhasil dipangkas setengahnya.')
"""


# ───────────────────────────────────────────────
# CELL 8 — Validasi Model (AI vs Rating Pelanggan)
# ───────────────────────────────────────────────
"""
from sklearn.metrics import classification_report

print('=== VALIDASI AKURASI MODEL SENTIMEN AI ===')
if 'Rating' in df.columns:
    df['Rating_Num'] = pd.to_numeric(df['Rating'], errors='coerce')

    def rating_to_sentiment(r):
        if pd.isna(r): return 'unknown'
        if r <= 2: return 'negative'
        elif r == 3: return 'neutral'
        else: return 'positive'

    df['Ground_Truth'] = df['Rating_Num'].apply(rating_to_sentiment)
    
    df_eval = df[df['Ground_Truth'] != 'unknown'].copy()
    df_eval['AI_Sentiment_Clean'] = df_eval['AI_Sentiment'].str.lower()

    if not df_eval.empty:
        report = classification_report(df_eval['Ground_Truth'], df_eval['AI_Sentiment_Clean'])
        print(report)
    else:
        print('Tidak ada data rating yang valid untuk evaluasi.')
else:
    print('Kolom "Rating" tidak ditemukan. Lewati validasi.')
"""


# ───────────────────────────────────────────────
# CELL 9 — Ekstraksi Kata Kunci Penting (TF-IDF + AI)
# ───────────────────────────────────────────────
"""
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

print('=== EKSTRAKSI KATA PENGHANCUR & PENDONGKRAK RATING ===')
if 'Ground_Truth' in df.columns and 'Kategori' in df.columns:
    
    df_kw = df[df['Ground_Truth'].isin(['positive', 'negative'])].copy()
    df_kw['Target'] = df_kw['Ground_Truth'].apply(lambda x: 1 if x == 'positive' else 0)

    def get_top_keywords(data, nama_kategori, top_n=20):
        if len(data) < 50: return None
        
        tfidf = TfidfVectorizer(max_features=3000, ngram_range=(1, 2), min_df=5)
        X = tfidf.fit_transform(data['clean_text'])
        y = data['Target']
        
        lr = LogisticRegression(max_iter=1000, random_state=42)
        lr.fit(X, y)
        
        kata = np.array(tfidf.get_feature_names_out())
        bobot = lr.coef_[0]
        
        idx_pos = bobot.argsort()[-top_n:][::-1]
        idx_neg = bobot.argsort()[:top_n]
        
        return pd.DataFrame({
            'Tipe_Hotel': nama_kategori,
            'Top_Positif_Word': kata[idx_pos],
            'Bobot_Positif': np.round(bobot[idx_pos], 4),
            'Top_Negatif_Word': kata[idx_neg],
            'Bobot_Negatif': np.round(bobot[idx_neg], 4)
        })

    # Analisis per Kategori (BUMN vs Kompetitor)
    df_bumn = df_kw[df_kw['Kategori'].str.upper() == 'BUMN']
    df_komp = df_kw[df_kw['Kategori'].str.upper() == 'KOMPETITOR']

    hasil_bumn = get_top_keywords(df_bumn, 'BUMN')
    hasil_komp = get_top_keywords(df_komp, 'KOMPETITOR')

    if hasil_bumn is not None and hasil_komp is not None:
        df_keywords = pd.concat([hasil_bumn, hasil_komp], ignore_index=True)
        df_keywords.to_csv(OUTPUT_KW, index=False)
        
        print('\\nTop 5 Kata Bikin Rating Hancur (BUMN):')
        print(hasil_bumn[['Top_Negatif_Word', 'Bobot_Negatif']].head(5))
        
        print('\\nTop 5 Kata Bikin Rating Hancur (KOMPETITOR):')
        print(hasil_komp[['Top_Negatif_Word', 'Bobot_Negatif']].head(5))
        print(f'\\n✅ Kata Kunci disimpan ke: {OUTPUT_KW}')
    else:
        print('Jumlah data kurang untuk mengekstrak keyword.')
else:
    print('Pastikan kolom "Rating" dan "Kategori" ada untuk analisis ini.')
"""


# ───────────────────────────────────────────────
# CELL 10 — Export CSV Akhir
# ───────────────────────────────────────────────
"""
# Hapus kolom bantuan yang tidak perlu sebelum disimpan
df_final = df.drop(columns=['clean_text', 'Rating_Num', 'Ground_Truth'], errors='ignore')

df_final.to_csv(OUTPUT_MASTER, index=False)
print(f'✅ File Master AI disimpan: {OUTPUT_MASTER}')

if 'Kategori' in df_final.columns:
    bumn_only = df_final[df_final['Kategori'].str.upper() == 'BUMN']
    komp_only = df_final[df_final['Kategori'].str.upper() == 'KOMPETITOR']

    if not bumn_only.empty:
        bumn_only.to_csv(OUTPUT_BUMN, index=False)
        print(f'✅ File BUMN disimpan  : {OUTPUT_BUMN} ({len(bumn_only):,} baris)')
    if not komp_only.empty:
        komp_only.to_csv(OUTPUT_KOMP, index=False)
        print(f'✅ File KOMP disimpan  : {OUTPUT_KOMP} ({len(komp_only):,} baris)')

print('\\n🎉 SELURUH PROSES AI SELESAI!')
"""
