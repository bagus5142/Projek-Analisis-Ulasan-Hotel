# ============================================================
# KAGGLE NOTEBOOK — FULL PIPELINE (SINGLE FILE)
# Menggunakan MasterDataset_Ulasan_Hotel.csv
#
# Cara pakai:
#   1. Upload MasterDataset_Ulasan_Hotel.csv ke Kaggle Dataset baru
#      (misal nama: masterdata-hotel)
#   2. Buat Notebook baru di Kaggle → pilih Code
#   3. Aktifkan GPU T4 + Internet ON
#   4. Tambahkan dataset masterdata-hotel sebagai input
#   5. Copy-paste tiap CELL ke cell Kaggle, lalu Run All
#
# Output: /kaggle/working/Analisis_Master_Final.csv
# ============================================================


# ───────────────────────────────────────────────
# CELL 1 — Install library tambahan
# ───────────────────────────────────────────────
"""
!pip install -q langdetect sentence-transformers Sastrawi
print('Instalasi selesai.')
"""


# ───────────────────────────────────────────────
# CELL 2 — Import & cek GPU
# ───────────────────────────────────────────────
"""
import os, re, gc, glob
import numpy as np
import pandas as pd
import torch
from tqdm.auto import tqdm
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, pipeline
from sentence_transformers import SentenceTransformer
from langdetect import detect, DetectorFactory

DetectorFactory.seed = 42

device    = 'cuda' if torch.cuda.is_available() else 'cpu'
device_id = 0 if device == 'cuda' else -1

print(f'Device : {device.upper()}')
if device == 'cuda':
    print(f'GPU    : {torch.cuda.get_device_name(0)}')
    print(f'VRAM   : {torch.cuda.get_device_properties(0).total_memory / 1e9:.1f} GB')
"""


# ───────────────────────────────────────────────
# CELL 3 — Temukan path file CSV
# ───────────────────────────────────────────────
"""
import glob

all_csv = glob.glob('/kaggle/input/**/*.csv', recursive=True)
print(f'CSV ditemukan: {len(all_csv)}')
for f in all_csv:
    print(' ', f)
"""


# ───────────────────────────────────────────────
# CELL 4 — Load & inspeksi data
# ───────────────────────────────────────────────
"""
# ⚠️ Sesuaikan path berdasarkan output Cell 3
INPUT_CSV   = '/kaggle/input/masterdata-hotel/MasterDataset_Ulasan_Hotel.csv'
OUTPUT_CSV  = '/kaggle/working/Analisis_Master_Final.csv'
OUTPUT_BUMN = '/kaggle/working/Analisis_BUMN_All.csv'
OUTPUT_KOMP = '/kaggle/working/Analisis_KOMPETITOR_All.csv'

df_raw = pd.read_csv(INPUT_CSV)
print(f'Shape raw   : {df_raw.shape}')
print(f'Kolom       : {list(df_raw.columns)}')
print(f'Kategori    : {df_raw["Kategori"].unique().tolist()}')
print(f'Bintang     : {df_raw["Bintang"].unique().tolist()}')
print(f'Null Review : {df_raw["Review Text"].isnull().sum()}')
print()
df_raw.head(3)
"""


# ───────────────────────────────────────────────
# CELL 5 — Bersihkan data & filter null
# ───────────────────────────────────────────────
"""
# Drop null & review tidak valid
blacklist = {'n/a', 'na', 'nan', '-', '', ' ', 'null'}

df = df_raw.copy()
df = df.dropna(subset=['Review Text'])
df = df[~df['Review Text'].astype(str).str.lower().str.strip().isin(blacklist)]
df = df.reset_index(drop=True)

# Standarisasi nama kolom agar seragam dengan pipeline sebelumnya
df = df.rename(columns={
    'Nama Hotel' : 'Nama_Hotel',
    'Kategori'   : 'Tipe',
    'Bintang'    : 'Kelas'
})

# Standarisasi format Kelas
kelas_map = {'bintang3': 'Bintang 3', 'bintang4': 'Bintang 4', 'bintang5': 'Bintang 5'}
df['Kelas'] = df['Kelas'].str.lower().map(kelas_map).fillna(df['Kelas'])

# Standarisasi Review Time ke tahun
if 'Review Time' in df.columns:
    df['Review Time'] = pd.to_datetime(df['Review Time'], errors='coerce').dt.year.astype('Int64')

print(f'Shape setelah filter: {df.shape}')
print(f'Hotel unik  : {df["Nama_Hotel"].nunique()}')
print(f'Tipe        : {df["Tipe"].value_counts().to_dict()}')
print(f'Kelas       : {df["Kelas"].value_counts().to_dict()}')
"""


# ───────────────────────────────────────────────
# CELL 6 — Kamus slang, Stopwords & fungsi cleaning
# ───────────────────────────────────────────────
"""
import urllib.request

print('Mendownload kamus slang & stopwords dari GitHub...')

# 1. Kamus Slang (15.000+ kata)
slang_url = 'https://raw.githubusercontent.com/nasalsabila/kamus-alay/master/colloquial-indonesian-lexicon.csv'
try:
    df_slang = pd.read_csv(slang_url)
    SLANG_DICT = dict(zip(df_slang['slang'], df_slang['formal']))
    print(f'Kamus slang siap: {len(SLANG_DICT):,} kata')
except Exception as e:
    print(f'Gagal download kamus slang: {e}')
    SLANG_DICT = {}

# 2. Stopwords (750+ kata)
stop_url = 'https://raw.githubusercontent.com/masdevid/ID-Stopwords/master/id.stopwords.02.01.2016.txt'
try:
    with urllib.request.urlopen(stop_url) as response:
        STOPWORDS = set(response.read().decode('utf-8').splitlines())
        
    # ⚠️ PENTING: Jangan hapus kata negasi agar arti sentimen tidak terbalik!
    negations = {'tidak', 'bukan', 'jangan', 'belum', 'kurang', 'enggak', 'ga', 'gak', 'nggak', 'tak'}
    STOPWORDS = STOPWORDS - negations
    
    print(f'Stopwords siap: {len(STOPWORDS):,} kata')
except Exception as e:
    print(f'Gagal download stopwords: {e}')
    STOPWORDS = set()

SKIP_LANGS = {'id', 'ms'}

def detect_lang(text):
    try:
        return detect(str(text))
    except Exception:
        return 'id'

def clean_text(text):
    if not isinstance(text, str):
        return ''
    
    # Lowercase & hapus karakter berulang berlebihan (misal: bgssss -> bgs)
    text = text.lower()
    text = re.sub(r'(.)\\1{2,}', r'\\1', text)
    
    # Hapus tanda baca
    text = re.sub(r'[^\\w\\s]', ' ', text)
    
    # Slang normalization
    words = [SLANG_DICT.get(w, w) for w in text.split()]
    
    # Stopword removal
    words = [w for w in words if w and w not in STOPWORDS]
    
    text = ' '.join(words)
    
    text = re.sub(r'\\s+', ' ', text).strip()
    return text

print('Fungsi cleaning siap.')
"""


# ───────────────────────────────────────────────
# CELL 7 — Load model translate & jalankan preprocessing
# ───────────────────────────────────────────────
"""
# Load NLLB-200
MODEL_NLLB = 'facebook/nllb-200-distilled-600M'
print(f'Loading translate model: {MODEL_NLLB}')
nllb_tokenizer = AutoTokenizer.from_pretrained(MODEL_NLLB)
nllb_model = AutoModelForSeq2SeqLM.from_pretrained(
    MODEL_NLLB,
    torch_dtype=torch.float16 if device == 'cuda' else torch.float32
).to(device)
print('Model translate siap!')


def translate_batch(text_list, batch_size=128):
    results = []
    nllb_tokenizer.src_lang = 'eng_Latn'
    bos_id = nllb_tokenizer.convert_tokens_to_ids('ind_Latn')
    for i in range(0, len(text_list), batch_size):
        batch = text_list[i:i + batch_size]
        inputs = nllb_tokenizer(batch, return_tensors='pt', padding=True,
                                truncation=True, max_length=128).to(device)
        with torch.no_grad():
            tokens = nllb_model.generate(
                **inputs, forced_bos_token_id=bos_id,
                max_new_tokens=128, num_beams=1, do_sample=False
            )
        decoded = nllb_tokenizer.batch_decode(tokens, skip_special_tokens=True)
        results.extend(decoded)
        del inputs, tokens
    return results


# Step 1: Clean teks
print('Step 1: Cleaning teks (membutuhkan waktu beberapa menit)...')
tqdm.pandas(desc='Cleaning Text')
df['clean_text'] = df['Review Text'].progress_apply(clean_text)
df = df[df['clean_text'].str.len() > 2].copy().reset_index(drop=True)
print(f'  Setelah filter teks kosong: {len(df):,} baris')

# Step 2: Deteksi bahasa
print('Step 2: Deteksi bahasa...')
langs = [detect_lang(t) for t in tqdm(df['clean_text'], desc='Deteksi bahasa')]
df['lang_detected'] = langs

id_count = sum(1 for l in langs if l in SKIP_LANGS)
en_count = len(langs) - id_count
print(f'  Indonesia: {id_count:,} ({id_count/len(langs)*100:.1f}%)')
print(f'  Non-Indonesia: {en_count:,} ({en_count/len(langs)*100:.1f}%)')

# Step 3: Translate yang non-Indonesia
print('Step 3: Translating non-Indonesian reviews...')
to_tr_idx = [i for i, l in enumerate(langs) if l not in SKIP_LANGS]
to_tr_txt = [df['clean_text'].iloc[i] for i in to_tr_idx]

if to_tr_txt:
    translated = translate_batch(to_tr_txt, batch_size=128)
    for idx, val in zip(to_tr_idx, translated):
        df.at[idx, 'clean_text'] = val

# Hapus kolom bantu (Tetap simpan Review Text asli untuk keperluan dashboard)
df = df.drop(columns=['lang_detected'], errors='ignore')

# Bersihkan memori translate model
del nllb_model, nllb_tokenizer
gc.collect()
torch.cuda.empty_cache()
print(f'Preprocessing selesai! Total: {len(df):,} baris')
"""


# ───────────────────────────────────────────────
# CELL 8 — Definisi label aspek
# ─────────────────────────────────────────────────────────
# Untuk MENAMBAH label baru:
#   Tambahkan entri di ASPEK_LABELS, lalu
#   jalankan ulang cell ini + cell berikutnya (pra-hitung embedding)
# ─────────────────────────────────────────────────────────
"""
ASPEK_LABELS = {

    "Kebersihan & Higienitas": {
        "deskripsi": (
            "Standar kebersihan kamar, kamar mandi, area publik, dan fasilitas hotel. "
            "Termasuk kondisi linen, handuk, karpet, debu, dan masalah hama seperti kecoa atau nyamuk. "
            "Juga mencakup kebersihan kolam renang dan area restoran."
        ),
    },

    "Kualitas Kamar & Kenyamanan": {
        "deskripsi": (
            "Kondisi fisik dan kenyamanan kamar hotel. Mencakup kualitas kasur dan tempat tidur, "
            "suasana dan dekorasi kamar, ketenangan (insulasi suara), kondisi AC, TV, pencahayaan, "
            "pemandangan dari kamar, dan perlengkapan dalam kamar."
        ),
    },

    "Fasilitas Hotel": {
        "deskripsi": (
            "Kelengkapan dan kondisi fasilitas hotel seperti kolam renang, gym, spa, lift, "
            "ruang pertemuan, ballroom, area parkir, lobby, dan fasilitas umum lainnya. "
            "Termasuk penilaian apakah fasilitas berfungsi dengan baik atau dalam kondisi rusak."
        ),
    },

    "Makanan & Minuman": {
        "deskripsi": (
            "Kualitas, variasi rasa, dan pengalaman makan di hotel. Mencakup kualitas sarapan, "
            "restoran hotel, layanan kamar (room service), variasi menu, kesegaran bahan makanan, "
            "rasa masakan, dan minuman yang tersedia."
        ),
    },

    "Kualitas & Sikap Pelayanan Staf": {
        "deskripsi": (
            "Profesionalisme, keramahan, kesopanan, dan kompetensi staf hotel dalam melayani tamu. "
            "Meliputi resepsionis, bellboy, housekeeping, staf restoran, dan semua karyawan hotel. "
            "Termasuk penilaian terhadap sikap, senyuman, dan inisiatif staf membantu tamu."
        ),
    },

    "Efisiensi & Kecepatan Layanan": {
        "deskripsi": (
            "Kecepatan dan responsivitas dalam memberikan layanan. Mencakup waktu tunggu saat "
            "check-in, antrian di resepsionis, kecepatan room service, respons terhadap permintaan "
            "tamu, dan efisiensi operasional hotel secara keseluruhan."
        ),
    },

    "Check-in & Check-out": {
        "deskripsi": (
            "Pengalaman proses check-in dan check-out hotel. Mencakup kemudahan prosedur, "
            "waktu tunggu, akurasi kamar yang dipesan versus yang diberikan, "
            "layanan early check-in atau late check-out, dan proses administrasi pemesanan."
        ),
    },

    "Lokasi & Aksesibilitas": {
        "deskripsi": (
            "Lokasi strategis hotel dan kemudahan akses ke berbagai destinasi. "
            "Meliputi kedekatan dengan bandara, pusat kota, mall, pantai, tempat wisata, "
            "kemudahan transportasi, kondisi jalan menuju hotel, dan aksesibilitas parkir."
        ),
    },

    "Harga & Nilai": {
        "deskripsi": (
            "Kesesuaian harga hotel dengan kualitas layanan dan fasilitas yang diterima. "
            "Mencakup penilaian apakah harga worth it, keterjangkauan tarif, "
            "transparansi biaya tambahan, promo, dan perbandingan harga dengan ekspektasi tamu."
        ),
    },

    "Keamanan & Keselamatan": {
        "deskripsi": (
            "Keamanan properti hotel dan keselamatan tamu selama menginap. "
            "Mencakup keamanan barang bawaan, prosedur keamanan pintu masuk, "
            "CCTV, satpam, kunci kamar, brankas, dan kondisi lingkungan sekitar yang aman."
        ),
    },

    "Penanganan Keluhan": {
        "deskripsi": (
            "Kemampuan dan kecepatan hotel dalam menangani keluhan dan masalah tamu. "
            "Mencakup respons terhadap laporan masalah, tindak lanjut penyelesaian, "
            "kompensasi yang diberikan, dan kemampuan pemulihan layanan setelah ada masalah."
        ),
    },

    "Fitur Khusus (Halal / Keluarga / Budaya)": {
        "deskripsi": (
            "Layanan dan fasilitas khusus yang melayani kebutuhan segmen tertentu. "
            "Meliputi fitur halal (mushola, makanan halal), ramah keluarga (kolam anak, playground), "
            "nilai budaya dan heritage hotel, serta layanan untuk tamu dengan kebutuhan khusus."
        ),
    },

    # ── TAMBAH LABEL BARU DI SINI ─────────────────────────────────────
    # "WiFi & Teknologi": {
    #     "deskripsi": (
    #         "Kualitas koneksi WiFi dan layanan teknologi di hotel. "
    #         "Mencakup kecepatan internet, jangkauan sinyal, kondisi TV, dll."
    #     ),
    # },
    # ──────────────────────────────────────────────────────────────────

}

print(f'Total label: {len(ASPEK_LABELS)}')
for i, nama in enumerate(ASPEK_LABELS, 1):
    print(f'  {i:2}. {nama}')
"""


# ───────────────────────────────────────────────
# CELL 9 — Load model sentimen & aspek, pre-hitung embedding label
# ───────────────────────────────────────────────
"""
print('Loading model sentimen (IndoBERT)...')
clf_sentimen = pipeline(
    'sentiment-analysis',
    model='w11wo/indonesian-roberta-base-sentiment-classifier',
    tokenizer='w11wo/indonesian-roberta-base-sentiment-classifier',
    device=device_id,
    torch_dtype=torch.float16 if device == 'cuda' else torch.float32
)

print('Loading model embedding aspek (multilingual-mpnet)...')
model_embed = SentenceTransformer('paraphrase-multilingual-mpnet-base-v2', device=device)

# Pre-hitung embedding label (dilakukan SEKALI)
LABEL_NAMES = list(ASPEK_LABELS.keys())
label_texts  = [f"{n}: {d['deskripsi']}" for n, d in ASPEK_LABELS.items()]

print(f'Pre-computing {len(LABEL_NAMES)} label embeddings...')
LABEL_EMBEDDINGS = model_embed.encode(
    label_texts, normalize_embeddings=True,
    show_progress_bar=True, batch_size=32
)

print('Semua model siap!')
"""


# ───────────────────────────────────────────────
# CELL 10 — Jalankan inferensi pada semua data
# ───────────────────────────────────────────────
"""
BATCH_SIZE = 64

# Batasi panjang teks hingga 2000 karakter agar tidak OOM tapi konteks tetap utuh
texts = [str(t)[:2000] for t in df['clean_text'].tolist()]
n     = len(texts)
print(f'Memproses {n:,} ulasan dengan batch size {BATCH_SIZE}...')

# 1. SENTIMEN
print('\n[1/2] Analisis sentimen...')
sent_labels, sent_scores = [], []
try:
    for i in tqdm(range(0, n, BATCH_SIZE), desc='Sentimen'):
        batch  = texts[i:i + BATCH_SIZE]
        res    = clf_sentimen(batch, batch_size=BATCH_SIZE, truncation=True)
        sent_labels.extend([r['label'] for r in res])
        sent_scores.extend([round(r['score'], 6) for r in res])
except Exception as e:
    print(f'Error sentimen: {e}')
    sent_labels = ['neutral'] * n
    sent_scores = [0.0] * n

# 2. ASPEK (embedding similarity)
print('\n[2/2] Klasifikasi aspek...')
primary_list, all_list = [], []

for i in tqdm(range(0, n, BATCH_SIZE), desc='Aspek'):
    batch     = texts[i:i + BATCH_SIZE]
    text_embs = model_embed.encode(batch, normalize_embeddings=True,
                                   show_progress_bar=False, batch_size=BATCH_SIZE)
    sims      = np.dot(text_embs, LABEL_EMBEDDINGS.T)
    top1_idx  = sims.argmax(axis=1)
    top3_idxs = sims.argsort(axis=1)[:, -3:][:, ::-1]

    for j in range(len(batch)):
        primary_list.append(LABEL_NAMES[top1_idx[j]])
        top3 = '; '.join(f"{LABEL_NAMES[k]} ({sims[j][k]:.2f})" for k in top3_idxs[j])
        all_list.append(top3)

# Simpan hasil ke DataFrame
df['AI_Sentiment']       = sent_labels
df['AI_Sentiment_Score'] = sent_scores
df['AI_Primary_Theme']   = primary_list
df['AI_All_Themes']      = all_list

if torch.cuda.is_available():
    torch.cuda.empty_cache()

print('\\nInferensi selesai!')
print('Distribusi sentimen:')
print(df['AI_Sentiment'].value_counts())
print('\\nTop 10 aspek:')
print(df['AI_Primary_Theme'].value_counts().head(10))
"""


# ───────────────────────────────────────────────
# CELL 10.5 — Evaluasi Model (AI Sentimen vs Rating Asli)
# ───────────────────────────────────────────────
"""
from sklearn.metrics import classification_report

print('=== EVALUASI MODEL SENTIMEN ===')
# Jadikan rating bintang sebagai Ground Truth (1-2 Negatif, 3 Netral, 4-5 Positif)
df['Rating_Num'] = pd.to_numeric(df['Rating'], errors='coerce')

def get_ground_truth(r):
    if pd.isna(r): return 'unknown'
    if r <= 2: return 'negative'
    elif r == 3: return 'neutral'
    else: return 'positive'

df['Ground_Truth'] = df['Rating_Num'].apply(get_ground_truth)

# Filter hanya yang ada rating valid
df_eval = df[df['Ground_Truth'] != 'unknown'].copy()

# Map hasil AI 'neutral' menjadi sesuai format
# (Tergantung output model, IndoBERT w11wo biasanya: positive, neutral, negative)
df_eval['AI_Sentiment_Clean'] = df_eval['AI_Sentiment'].str.lower()

if not df_eval.empty:
    report = classification_report(df_eval['Ground_Truth'], df_eval['AI_Sentiment_Clean'])
    print(report)
else:
    print('Tidak dapat mengevaluasi karena tidak ada data rating valid.')
"""


# ───────────────────────────────────────────────
# CELL 11 — Mining Tambahan: TF-IDF Keyword Importance
# ───────────────────────────────────────────────
"""
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

print('=== EXTRAKSI KATA KUNCI PENGHANCUR & PENDONGKRAK RATING ===')
# Ambil ulasan Positif dan Negatif saja
df_kw = df[df['Ground_Truth'].isin(['positive', 'negative'])].copy()
df_kw['Target'] = df_kw['Ground_Truth'].apply(lambda x: 1 if x == 'positive' else 0)

def extract_top_keywords(data, name, top_n=20):
    if len(data) < 100: return None
    
    # Ekstrak unigram dan bigram (kombinasi 1-2 kata)
    tfidf = TfidfVectorizer(max_features=5000, ngram_range=(1, 2), min_df=10)
    X = tfidf.fit_transform(data['clean_text'])
    y = data['Target']
    
    # Train Logistic Regression
    lr = LogisticRegression(max_iter=1000, random_state=42)
    lr.fit(X, y)
    
    # Ambil kata dan bobotnya (koefisien)
    features = np.array(tfidf.get_feature_names_out())
    coefs = lr.coef_[0]
    
    # Sort dari terpenting
    top_pos_idx = coefs.argsort()[-top_n:][::-1]
    top_neg_idx = coefs.argsort()[:top_n]
    
    res = pd.DataFrame({
        'Kategori': name,
        'Top_Positive_Words': features[top_pos_idx],
        'Pos_Weight': np.round(coefs[top_pos_idx], 4),
        'Top_Negative_Words': features[top_neg_idx],
        'Neg_Weight': np.round(coefs[top_neg_idx], 4)
    })
    return res

# Ekstrak pola untuk BUMN vs KOMPETITOR
df_bumn_kw = df_kw[df_kw['Tipe'] == 'BUMN']
df_komp_kw = df_kw[df_kw['Tipe'] == 'KOMPETITOR']

res_bumn = extract_top_keywords(df_bumn_kw, 'BUMN')
res_komp = extract_top_keywords(df_komp_kw, 'KOMPETITOR')

if res_bumn is not None and res_komp is not None:
    df_keywords = pd.concat([res_bumn, res_komp], ignore_index=True)
    out_kw_path = '/kaggle/working/Analisis_Keywords.csv'
    df_keywords.to_csv(out_kw_path, index=False)
    
    print('\\nTop 10 Kata Penghancur Rating (BUMN):')
    print(res_bumn[['Top_Negative_Words', 'Neg_Weight']].head(10))
    
    print('\\nTop 10 Kata Penghancur Rating (KOMPETITOR):')
    print(res_komp[['Top_Negative_Words', 'Neg_Weight']].head(10))
    
    print(f'\\n✅ Insight keywords disimpan ke: {out_kw_path}')
else:
    print('Data tidak cukup untuk ekstraksi keyword.')
"""


# ───────────────────────────────────────────────
# CELL 12 — Simpan hasil
# ───────────────────────────────────────────────
"""
# Simpan master
df.to_csv(OUTPUT_CSV, index=False)
print(f'Master disimpan: {OUTPUT_CSV}')

# Simpan per tipe
df_bumn = df[df['Tipe'] == 'BUMN']
df_komp = df[df['Tipe'] == 'KOMPETITOR']

if not df_bumn.empty:
    df_bumn.to_csv(OUTPUT_BUMN, index=False)
    print(f'BUMN disimpan  : {OUTPUT_BUMN} ({len(df_bumn):,} baris)')

if not df_komp.empty:
    df_komp.to_csv(OUTPUT_KOMP, index=False)
    print(f'KOMP disimpan  : {OUTPUT_KOMP} ({len(df_komp):,} baris)')

print()
print('=== RINGKASAN AKHIR ===')
print(f'Total ulasan  : {len(df):,}')
print(f'Hotel unik    : {df["Nama_Hotel"].nunique()}')
print(f'Kolom output  : {list(df.columns)}')
"""
