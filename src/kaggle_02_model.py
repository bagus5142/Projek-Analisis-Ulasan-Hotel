# ============================================================
# KAGGLE NOTEBOOK 2: MODEL (SENTIMEN + ASPEK EMBEDDING)
# Cara pakai:
#   1. Buka Kaggle → New Notebook → pilih Code
#   2. Aktifkan GPU T4 + Internet ON
#   3. Tambahkan dataset hasil preprocessing (datasethotel-clean)
#   4. Copy-paste tiap CELL ke cell Kaggle baru
# ============================================================


# ───────────────────────────────────────────────
# CELL 1 — Install library tambahan
# ───────────────────────────────────────────────
"""
!pip install -q sentence-transformers
"""


# ───────────────────────────────────────────────
# CELL 2 — Import & cek GPU
# ───────────────────────────────────────────────
"""
import os, glob
import numpy as np
import pandas as pd
import torch
from transformers import pipeline
from sentence_transformers import SentenceTransformer
from tqdm.auto import tqdm

device    = 'cuda' if torch.cuda.is_available() else 'cpu'
device_id = 0 if device == 'cuda' else -1

print(f'Device : {device.upper()}')
if device == 'cuda':
    print(f'GPU    : {torch.cuda.get_device_name(0)}')
    print(f'VRAM   : {torch.cuda.get_device_properties(0).total_memory / 1e9:.1f} GB')
"""


# ───────────────────────────────────────────────
# CELL 3 — Konfigurasi path
# ───────────────────────────────────────────────
"""
INPUT_CLEAN = '/kaggle/input/datasets/meongmesir/datasethotel-clean/DatasetHotelCLEAN'

OUTPUT_BASE = '/kaggle/working/Results'
OUTPUT_CSV  = os.path.join(OUTPUT_BASE, 'CSV')

FOLDERS = ['BUMNB3', 'BUMNB4', 'BUMNB5',
           'KOMPETITORB3', 'KOMPETITORB4', 'KOMPETITORB5']

for folder in FOLDERS:
    os.makedirs(os.path.join(OUTPUT_CSV, folder), exist_ok=True)

all_files = glob.glob(os.path.join(INPUT_CLEAN, '**', '*.csv'), recursive=True)
print(f'Total file cleaned CSV: {len(all_files)}')
"""


# ───────────────────────────────────────────────
# CELL 4 — Definisi label aspek
# ─────────────────────────────────────────────────────────
# Untuk MENAMBAH label baru:
#   Tambahkan entri baru di ASPEK_LABELS, lalu
#   jalankan ulang CELL 4 dan CELL 6.
#
# Format:
#   "Nama Label": {
#       "deskripsi": "Penjelasan lengkap aspek ini."
#   }
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

    # ── TAMBAHKAN LABEL BARU DI SINI ──────────────────────────
    # Contoh:
    # "WiFi & Teknologi": {
    #     "deskripsi": (
    #         "Kualitas koneksi WiFi dan layanan teknologi di hotel. Mencakup kecepatan internet, "
    #         "jangkauan sinyal WiFi di seluruh area hotel, kondisi TV, sistem pembayaran digital."
    #     ),
    # },
    # ──────────────────────────────────────────────────────────

}

print(f'Total label aspek: {len(ASPEK_LABELS)}')
for i, nama in enumerate(ASPEK_LABELS, 1):
    print(f'  {i:2}. {nama}')
"""


# ───────────────────────────────────────────────
# CELL 5 — Load kedua model
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
model_embed = SentenceTransformer(
    'paraphrase-multilingual-mpnet-base-v2',
    device=device
)

print('Kedua model siap!')
"""


# ───────────────────────────────────────────────
# CELL 6 — Pre-hitung embedding label (jalankan ulang jika label diubah)
# ───────────────────────────────────────────────
"""
LABEL_NAMES = list(ASPEK_LABELS.keys())
label_texts = [
    f"{name}: {defn['deskripsi']}"
    for name, defn in ASPEK_LABELS.items()
]

print(f'Menghitung embedding untuk {len(LABEL_NAMES)} label...')
LABEL_EMBEDDINGS = model_embed.encode(
    label_texts,
    normalize_embeddings=True,
    show_progress_bar=True,
    batch_size=32
)
print(f'Embedding selesai. Shape: {LABEL_EMBEDDINGS.shape}')
"""


# ───────────────────────────────────────────────
# CELL 7 — Fungsi inferensi
# ───────────────────────────────────────────────
"""
def run_inference(df, batch_size=64):
    if df.empty:
        return df

    texts = [str(t)[:512] for t in df['clean_text'].tolist()]

    # 1. SENTIMEN
    try:
        sent_out    = clf_sentimen(texts, batch_size=batch_size, truncation=True)
        sent_labels = [r['label'] for r in sent_out]
        sent_scores = [round(r['score'], 6) for r in sent_out]
    except Exception as e:
        print(f'  [Warning] Sentimen: {e}')
        sent_labels = ['neutral'] * len(texts)
        sent_scores = [0.0] * len(texts)

    # 2. ASPEK (embedding similarity)
    primary_list, all_list = [], []
    for i in tqdm(range(0, len(texts), batch_size), desc='  Aspek', leave=False):
        batch = texts[i:i + batch_size]
        text_embs = model_embed.encode(
            batch, normalize_embeddings=True,
            show_progress_bar=False, batch_size=batch_size
        )
        sims      = np.dot(text_embs, LABEL_EMBEDDINGS.T)
        top1_idx  = sims.argmax(axis=1)
        top3_idxs = sims.argsort(axis=1)[:, -3:][:, ::-1]

        for j in range(len(batch)):
            primary_list.append(LABEL_NAMES[top1_idx[j]])
            top3 = '; '.join(
                f"{LABEL_NAMES[k]} ({sims[j][k]:.2f})"
                for k in top3_idxs[j]
            )
            all_list.append(top3)

    # 3. Gabung ke DataFrame
    df = df.copy()
    df['AI_Sentiment']       = sent_labels
    df['AI_Sentiment_Score'] = sent_scores
    df['AI_Primary_Theme']   = primary_list
    df['AI_All_Themes']      = all_list

    if torch.cuda.is_available():
        torch.cuda.empty_cache()

    return df

print('Fungsi inferensi siap.')
"""


# ───────────────────────────────────────────────
# CELL 8 — Proses semua file
# ───────────────────────────────────────────────
"""
BATCH_SIZE    = 64
processed_dfs = []

for folder in FOLDERS:
    in_dir  = os.path.join(INPUT_CLEAN, folder)
    out_dir = os.path.join(OUTPUT_CSV, folder)

    if not os.path.exists(in_dir):
        print(f'[SKIP] {in_dir}')
        continue

    csv_files = [f for f in os.listdir(in_dir) if f.endswith('.csv')]
    tipe  = 'KOMPETITOR' if 'KOMPETITOR' in folder else 'BUMN'
    kelas = 'Bintang 3' if 'B3' in folder else 'Bintang 4' if 'B4' in folder else 'Bintang 5'

    print(f'\n=== {folder} ({len(csv_files)} file) ===')

    for idx, fname in enumerate(csv_files):
        print(f'  [{idx+1}/{len(csv_files)}] {fname}...')
        try:
            df = pd.read_csv(os.path.join(in_dir, fname))

            if 'Review Time' in df.columns:
                try:
                    df['Review Time'] = (
                        pd.to_datetime(df['Review Time'], errors='coerce')
                        .dt.year.astype('Int64')
                    )
                except Exception:
                    pass

            if 'Review Text' in df.columns:
                df = df.rename(columns={'Review Text': 'clean_text'})
            elif 'Review Text Cleaned' in df.columns:
                df = df.rename(columns={'Review Text Cleaned': 'clean_text'})

            if df.empty or 'clean_text' not in df.columns:
                print('    SKIP — kolom tidak ada.')
                continue

            df['Tipe']       = tipe
            df['Kelas']      = kelas
            df['Nama_Hotel'] = fname.replace('_Clean.csv', '').replace('.csv', '')

            df_result = run_inference(df, batch_size=BATCH_SIZE)

            out_path = os.path.join(out_dir, f'Analisis_{fname}')
            df_result.to_csv(out_path, index=False)
            processed_dfs.append(df_result)
            print(f'    OK — {len(df_result)} ulasan')

        except Exception as e:
            print(f'    ERROR: {e}')

print('\nSemua file selesai.')
"""


# ───────────────────────────────────────────────
# CELL 9 — Buat file master
# ───────────────────────────────────────────────
"""
print('Menggabungkan semua hasil...')

if processed_dfs:
    master_df = pd.concat(processed_dfs, ignore_index=True)
else:
    files = glob.glob(os.path.join(OUTPUT_CSV, '**', 'Analisis_*.csv'), recursive=True)
    master_df = pd.concat(
        [pd.read_csv(f) for f in tqdm(files, desc='Membaca')],
        ignore_index=True
    )

path_master = os.path.join(OUTPUT_CSV, 'Analisis_Master_Lengkap.csv')
master_df.to_csv(path_master, index=False)

df_bumn = master_df[master_df['Tipe'] == 'BUMN']
df_komp = master_df[master_df['Tipe'] == 'KOMPETITOR']

if not df_bumn.empty:
    df_bumn.to_csv(os.path.join(OUTPUT_CSV, 'Analisis_BUMN_All.csv'), index=False)
if not df_komp.empty:
    df_komp.to_csv(os.path.join(OUTPUT_CSV, 'Analisis_KOMPETITOR_All.csv'), index=False)

print(f'SELESAI!')
print(f'Total ulasan   : {len(master_df):,}')
print(f'Hotel unik     : {master_df["Nama_Hotel"].nunique()}')
print()
print('Distribusi sentimen:')
print(master_df['AI_Sentiment'].value_counts())
print()
print('Top 10 aspek:')
print(master_df['AI_Primary_Theme'].value_counts().head(10))
"""
