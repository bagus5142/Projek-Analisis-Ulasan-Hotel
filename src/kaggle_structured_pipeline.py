# ============================================================
# KAGGLE NOTEBOOK — STRUCTURED S.O.T.A PIPELINE (LEXICON-CENTROID)
# ============================================================
# Pipeline ini menggunakan arsitektur industri yang cepat & akurat:
# 1. Sentimen  : mdhugol/indonesia-bert-sentiment-classification (Universal)
# 2. Aspek     : Lexicon-Centroid menggunakan SentenceTransformer (Sangat Cepat)
# 3. Kata Kunci: Ekstraksi Frasa N-Gram berdasarkan Prediksi Sentimen AI.
# ============================================================

# ───────────────────────────────────────────────
# CELL 1 — Install library AI
# ───────────────────────────────────────────────
"""
!pip install -q transformers sentence-transformers scikit-learn
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
import concurrent.futures
from tqdm.auto import tqdm
from transformers import pipeline
from sentence_transformers import SentenceTransformer

n_gpu = torch.cuda.device_count()
device_0 = 'cuda:0' if n_gpu > 0 else 'cpu'
device_1 = 'cuda:1' if n_gpu > 1 else device_0

print(f'Mendeteksi {n_gpu} GPU.')
if n_gpu > 0:
    for i in range(n_gpu):
        print(f'GPU {i}: {torch.cuda.get_device_name(i)}')
"""

# ───────────────────────────────────────────────
# CELL 3 — Cari Path Data Kaggle
# ───────────────────────────────────────────────
"""
all_csv = glob.glob('/kaggle/input/**/*.csv', recursive=True)
print(f'CSV ditemukan: {len(all_csv)}')
for f in all_csv:
    print('👉', f)
"""

# ───────────────────────────────────────────────
# CELL 4 — Load Dataset Bersih
# ───────────────────────────────────────────────
"""
# ⚠️ PASTE path CSV Anda ke sini:
INPUT_CSV   = '/kaggle/input/nama-dataset-anda/MasterDataset_Hotel_Clean.csv'

OUTPUT_MASTER = '/kaggle/working/AI_Structured_Final.csv'
OUTPUT_KW     = '/kaggle/working/AI_Structured_Keywords.csv'

df = pd.read_csv(INPUT_CSV)
df = df.dropna(subset=['Review Text']).reset_index(drop=True)
df['clean_text'] = df['Review Text'].astype(str)

print(f'Shape siap proses: {df.shape}')
df.head(2)
"""

# ───────────────────────────────────────────────
# CELL 5 — Setup Model & Hitung Centroid Aspek (MULTI-GPU)
# ───────────────────────────────────────────────
"""
# Kamus Jangkar (Lexicon) untuk membentuk Pusat Gravitasi (Centroid) tiap Aspek
ASPEK_LEXICON = {
    "Kebersihan": ["kotor", "debu", "bau", "kecoak", "pesing", "jorok", "bersih", "wangi", "noda"],
    "Kualitas Kamar": ["kasur", "ac", "tv", "sempit", "luas", "nyaman", "bocor", "berisik", "sprei", "bantal"],
    "Fasilitas Hotel": ["kolam renang", "gym", "wifi", "lift", "parkir", "rusak", "kolam", "lobi"],
    "Makanan & Minuman": ["sarapan", "menu", "rasa", "hambar", "basi", "enak", "restoran", "kopi", "buffet"],
    "Pelayanan Staf": ["ramah", "judes", "senyum", "bantu", "kasar", "lambat", "resepsionis", "staf", "layanan"],
    "Kecepatan Layanan": ["lama", "antre", "cepat", "lambat", "nunggu", "sigap", "respons", "lelet"],
    "Proses Check-in/out": ["check-in", "check-out", "ktp", "deposit", "administrasi", "lancar", "ribet"],
    "Lokasi": ["strategis", "dekat", "jauh", "akses", "macet", "pusat kota", "bandara", "jalan"],
    "Harga": ["mahal", "murah", "diskon", "promo", "worth it", "terjangkau", "overprice", "harga"],
    "Keamanan": ["aman", "maling", "hilang", "satpam", "cctv", "kunci", "seram", "gembok"],
    "Penanganan Keluhan": ["komplain", "solusi", "diam", "tanggung jawab", "ganti rugi", "cuek", "maaf"],
    "Fasilitas Khusus": ["anak", "keluarga", "halal", "mushola", "disabilitas", "playground", "stroller"]
}

print(f'Membagi beban: Sentimen ke {device_0}, Aspek Lexicon ke {device_1}...')

print('Memuat Model Sentimen (mdhugol)...')
clf_sentimen = pipeline(
    'sentiment-analysis',
    model='mdhugol/indonesia-bert-sentiment-classification',
    tokenizer='mdhugol/indonesia-bert-sentiment-classification',
    device=0 if n_gpu > 0 else -1,
    truncation=True,
    max_length=512
)

print('Memuat Model Aspek (Multilingual MPNet)...')
model_embed = SentenceTransformer('paraphrase-multilingual-mpnet-base-v2', device=device_1)

# Pre-computing Centroid Embeddings
print('Menghitung Pusat Gravitasi (Centroid) untuk 12 Aspek...')
LABEL_NAMES = list(ASPEK_LEXICON.keys())
LABEL_CENTROIDS = []

for label in LABEL_NAMES:
    anchor_words = ASPEK_LEXICON[label]
    word_embs = model_embed.encode(anchor_words, normalize_embeddings=True, show_progress_bar=False)
    # Rata-rata dari semua kata jangkar menjadi 1 vektor Centroid
    centroid = np.mean(word_embs, axis=0)
    # Normalisasi agar cosine similarity akurat
    centroid = centroid / np.linalg.norm(centroid)
    LABEL_CENTROIDS.append(centroid)

LABEL_CENTROIDS = np.array(LABEL_CENTROIDS)
print('✅ Seluruh Model SOTA & Centroid Siap!')
"""

# ───────────────────────────────────────────────
# CELL 6 — EKSEKUSI PARALEL (SENTIMEN & ASPEK)
# ───────────────────────────────────────────────
"""
BATCH_SIZE = 128 if n_gpu > 0 else 32
texts = [str(t)[:1500] for t in df['clean_text'].tolist()] # Batasi karakter aman
n = len(texts)

print(f'🚀 Memulai Inferensi Paralel pada {n:,} Ulasan...')

def run_sentimen(texts_input):
    sent_labels = []
    try:
        for i in tqdm(range(0, n, BATCH_SIZE), desc='1. Sentimen (GPU 0)', position=0, leave=True):
            batch = texts_input[i:i + BATCH_SIZE]
            res = clf_sentimen(batch, batch_size=BATCH_SIZE, truncation=True, max_length=512)
            # mdhugol output: LABEL_0 (Pos), LABEL_1 (Neu), LABEL_2 (Neg)
            label_map = {'LABEL_0': 'positive', 'LABEL_1': 'neutral', 'LABEL_2': 'negative'}
            sent_labels.extend([label_map.get(r['label'], 'neutral') for r in res])
    except Exception as e:
        print(f'Error Sentimen: {e}')
        sent_labels = ['neutral'] * n
    return sent_labels

def run_aspek(texts_input):
    primary_list, all_list = [], []
    for i in tqdm(range(0, n, BATCH_SIZE), desc='2. Aspek    (GPU 1)', position=1, leave=True):
        batch = texts_input[i:i + BATCH_SIZE]
        text_embs = model_embed.encode(batch, normalize_embeddings=True, show_progress_bar=False, batch_size=BATCH_SIZE)
        
        # Perkalian titik dengan Centroid (Cosine Similarity)
        sims = np.dot(text_embs, LABEL_CENTROIDS.T)
        
        top1_idx = sims.argmax(axis=1)
        top3_idxs = sims.argsort(axis=1)[:, -3:][:, ::-1]

        for j in range(len(batch)):
            primary_list.append(LABEL_NAMES[top1_idx[j]])
            top3 = '; '.join(f"{LABEL_NAMES[k]} ({sims[j][k]:.2f})" for k in top3_idxs[j])
            all_list.append(top3)
    return primary_list, all_list

with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
    future_sentimen = executor.submit(run_sentimen, texts)
    future_aspek = executor.submit(run_aspek, texts)

    df['AI_Sentiment'] = future_sentimen.result()
    df['AI_Primary_Theme'], df['AI_All_Themes'] = future_aspek.result()

if torch.cuda.is_available(): torch.cuda.empty_cache()
print('\\n✅ Inferensi Sentimen & Aspek Selesai (Sangat Cepat)!')
"""

    # ───────────────────────────────────────────────
    # CELL 7 — Ekstraksi N-Gram (Frasa) Berkorelasi AI
    # ───────────────────────────────────────────────
    """
    from sklearn.feature_extraction.text import CountVectorizer
    from sklearn.linear_model import LogisticRegression

    print('=== EKSTRAKSI FRASA PENGHANCUR & PENDONGKRAK (N-GRAM) ===')
    # Menggunakan prediksi Sentimen AI (Menangani 'LABEL_0' atau 'positive')
    valid_labels = ['label_0', 'label_2', 'positive', 'negative']
    df_kw = df[df['AI_Sentiment'].str.lower().isin(valid_labels)].copy()

    def map_target(x):
        val = str(x).lower()
        return 1 if val in ['label_0', 'positive'] else 0

    df_kw['Target'] = df_kw['AI_Sentiment'].apply(map_target)

    def extract_phrases(data, nama_hotel, top_n=10):
        # Turunkan batas minimum agar hotel dengan ulasan sedikit tetap diproses
        if len(data) < 20: return None
        
        # 1. STOPWORDS KHUSUS HOTEL
        custom_stopwords = [
            'saya', 'aku', 'kami', 'kita', 'hotel', 'kamar', 'ini', 'itu', 'di', 'ke', 'dari', 
            'pada', 'dalam', 'untuk', 'dengan', 'dan', 'atau', 'tapi', 'karena', 'sehingga', 
            'yang', 'yg', 'sangat', 'sekali', 'banget', 'agak', 'lumayan', 'cukup', 'paling', 
            'lebih', 'bisa', 'ada', 'adalah', 'akan', 'sudah', 'telah', 'belum', 'juga', 'nya',
            'kecewa', 'mengecewakan', 'mengerikan', 'parah', 'payah', 'biasa', 'saja'
        ]
        
        # 2. Extract Frasa dengan min_df=2 agar frasa langka di hotel kecil tetap terbaca
        try:
            vec = CountVectorizer(max_features=1000, ngram_range=(2, 3), min_df=2, stop_words=custom_stopwords)
            X = vec.fit_transform(data['clean_text'])
        except ValueError:
            return None # Mengatasi error jika vocabulary kosong
            
        y = data['Target']
        
        # Cek jika target hanya 1 kelas (semua positif atau semua negatif)
        if len(y.unique()) < 2: return None
        
        lr = LogisticRegression(max_iter=1000, random_state=42)
        lr.fit(X, y)
        
        frasa = np.array(vec.get_feature_names_out())
        bobot = lr.coef_[0]
        
        # Jika top_n lebih besar dari jumlah frasa yang ditemukan
        n_frasa = len(frasa)
        ambil = min(top_n, n_frasa)
        
        idx_pos = bobot.argsort()[-ambil:][::-1]
        idx_neg = bobot.argsort()[:ambil]
        
        return pd.DataFrame({
            'Nama_Hotel': nama_hotel,
            'Top_Positif_Phrase': frasa[idx_pos],
            'Bobot_Pos': np.round(bobot[idx_pos], 4),
            'Top_Negatif_Phrase': frasa[idx_neg],
            'Bobot_Neg': np.round(bobot[idx_neg], 4)
        })

    if 'Nama Hotel' in df.columns:
        semua_hasil = []
        hotel_unik = df_kw['Nama Hotel'].unique()
        
        print(f'Mengekstrak Frasa secara spesifik untuk {len(hotel_unik)} Hotel...')
        for hotel in tqdm(hotel_unik, desc='Ekstraksi per Hotel'):
            df_temp = df_kw[df_kw['Nama Hotel'] == hotel]
            hasil_hotel = extract_phrases(df_temp, hotel, top_n=10)
            if hasil_hotel is not None:
                semua_hasil.append(hasil_hotel)

        if semua_hasil:
            df_keywords = pd.concat(semua_hasil, ignore_index=True)
            df_keywords.to_csv(OUTPUT_KW, index=False)
            
            contoh_hotel = df_keywords['Nama_Hotel'].unique()[:2]
            for h in contoh_hotel:
                print(f'\\nTop 5 Frasa Penghancur Rating untuk: {h}')
                print(df_keywords[df_keywords['Nama_Hotel'] == h][['Top_Negatif_Phrase', 'Bobot_Neg']].head(5))
                
            print(f'\\n✅ Insight Frasa PER HOTEL disimpan ke: {OUTPUT_KW}')
    else:
        print('Kolom "Nama Hotel" tidak ditemukan.')
"""

# ───────────────────────────────────────────────
# CELL 8 — Export CSV Akhir
# ───────────────────────────────────────────────
"""
df_final = df.drop(columns=['clean_text', 'Target'], errors='ignore')
df_final.to_csv(OUTPUT_MASTER, index=False)

print(f'✅ File Master AI Terstruktur disimpan: {OUTPUT_MASTER}')
print('\\n🎉 SELURUH PIPELINE SOTA SELESAI!')
"""
