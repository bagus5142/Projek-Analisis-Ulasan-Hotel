# ============================================================
# MODEL V2 — Embedding Similarity untuk Klasifikasi Aspek
# ============================================================
# Perubahan dari V1:
#   - Aspek: mDeBERTa zero-shot → paraphrase-multilingual-mpnet-base-v2
#     (embedding similarity, lebih akurat & lebih efisien)
#   - Label aspek: 12 label konsolidasi Bahasa Indonesia
#     (mudah ditambah — cukup tambah entri di ASPEK_LABELS)
#   - Sentimen: tetap IndoBERT (w11wo/indonesian-roberta-base-sentiment-classifier)
# ============================================================


# ------ CELL 1: INSTALASI ------
# !pip install pandas transformers sentence-transformers seaborn matplotlib tqdm openpyxl scikit-learn
# !pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118


# ------ CELL 2: IMPORT & PATH ------
import os
import glob
import re
import numpy as np
import pandas as pd
import torch
import seaborn as sns
import matplotlib.pyplot as plt
from transformers import pipeline
from sentence_transformers import SentenceTransformer
from tqdm.auto import tqdm

sns.set_style("whitegrid")

INPUT_DATA_PATH = '../DatasetHotelCLEAN'
OUTPUT_BASE_PATH = '../Results'
OUTPUT_CSV_PATH = os.path.join(OUTPUT_BASE_PATH, 'CSV')
OUTPUT_IMG_PATH = os.path.join(OUTPUT_BASE_PATH, 'Visualisasi')

os.makedirs(OUTPUT_CSV_PATH, exist_ok=True)
os.makedirs(OUTPUT_IMG_PATH, exist_ok=True)

print("Konfigurasi path selesai.")


# ------ CELL 3: DEFINISI LABEL ASPEK (MUDAH DITAMBAH) ------
# ================================================================
# Untuk MENAMBAH label baru, cukup tambahkan entri baru di bawah
# dengan format:
#   "Nama Label": {
#       "deskripsi": "Penjelasan lengkap tentang aspek ini.",
#       "kata_kunci": ["kata1", "kata2", ...]   # opsional, tidak wajib
#   }
# ================================================================

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

    # ── TAMBAHKAN LABEL BARU DI SINI ─────────────────────────────────────
    # Contoh:
    # "WiFi & Teknologi": {
    #     "deskripsi": (
    #         "Kualitas koneksi WiFi dan layanan teknologi di hotel. Mencakup kecepatan internet, "
    #         "jangkauan sinyal WiFi di seluruh area hotel, kondisi TV, sistem pembayaran digital, "
    #         "dan penggunaan teknologi dalam layanan hotel."
    #     ),
    # },
    # ─────────────────────────────────────────────────────────────────────

}

print(f"Total label aspek: {len(ASPEK_LABELS)}")
for nama in ASPEK_LABELS:
    print(f"  - {nama}")


# ------ CELL 4: LOAD MODEL ------
def setup_models():
    print("Memuat Model AI...")

    device_id = 0 if torch.cuda.is_available() else -1
    if device_id == 0:
        print(f"GPU: {torch.cuda.get_device_name(0)} (FP16)")
    else:
        print("CPU mode.")

    # --- Model 1: Sentimen (tetap IndoBERT) ---
    model_sentimen = "w11wo/indonesian-roberta-base-sentiment-classifier"
    clf_sentimen = pipeline(
        "sentiment-analysis",
        model=model_sentimen,
        tokenizer=model_sentimen,
        device=device_id,
        torch_dtype=torch.float16 if device_id == 0 else torch.float32
    )

    # --- Model 2: Aspek (BARU — embedding similarity) ---
    # Model ini mendukung 50+ bahasa termasuk Indonesia & Inggris
    clf_aspek = SentenceTransformer(
        "paraphrase-multilingual-mpnet-base-v2",
        device="cuda" if device_id == 0 else "cpu"
    )

    print("Kedua model siap!")
    return clf_sentimen, clf_aspek

clf_sentimen, clf_aspek = setup_models()


# ------ CELL 5: PRA-HITUNG EMBEDDING LABEL (dilakukan SEKALI) ------
def build_label_embeddings(model_embed, aspek_dict: dict):
    """
    Encode semua deskripsi label menjadi vektor embedding.
    Ini hanya dilakukan SEKALI — jauh lebih efisien dari NLI per-label.
    """
    label_names = list(aspek_dict.keys())
    label_texts  = [
        f"{name}: {defn['deskripsi']}"
        for name, defn in aspek_dict.items()
    ]

    print(f"Menghitung embedding untuk {len(label_names)} label...")
    label_embeddings = model_embed.encode(
        label_texts,
        normalize_embeddings=True,  # penting untuk cosine similarity
        show_progress_bar=True,
        batch_size=32
    )
    print("Embedding label selesai.")
    return label_names, label_embeddings

LABEL_NAMES, LABEL_EMBEDDINGS = build_label_embeddings(clf_aspek, ASPEK_LABELS)


# ------ CELL 6: FUNGSI INFERENSI ------
def process_inference(df: pd.DataFrame, clf_sent, model_embed, batch_size: int = 32) -> pd.DataFrame:
    """
    Jalankan sentiment analysis + aspect classification.
    Aspect menggunakan embedding similarity (bukan zero-shot NLI).
    """
    if df.empty:
        return df

    # Ambil teks & truncate
    raw_texts = df['clean_text'].astype(str).tolist()
    texts     = [t[:512] for t in raw_texts]

    # ── 1. SENTIMEN ───────────────────────────────────────────
    print(f"  > Analisis sentimen ({len(texts)} data)...")
    try:
        sent_results    = clf_sent(texts, batch_size=batch_size, truncation=True)
        sentimen_labels = [r['label'] for r in sent_results]
        sentimen_scores = [r['score'] for r in sent_results]
    except Exception as e:
        print(f"  [Warning] Error sentimen: {e}")
        sentimen_labels = ["neutral"] * len(texts)
        sentimen_scores = [0.0] * len(texts)

    # ── 2. ASPEK (embedding similarity) ──────────────────────
    print(f"  > Klasifikasi aspek ({len(texts)} data) via embedding similarity...")

    primary_themes = []
    all_themes     = []

    for i in tqdm(range(0, len(texts), batch_size), desc="  Aspek Batch", leave=False):
        batch = texts[i:i + batch_size]

        # Encode teks batch
        text_embeddings = model_embed.encode(
            batch,
            normalize_embeddings=True,
            show_progress_bar=False
        )  # shape: (batch_size, embedding_dim)

        # Cosine similarity: (batch_size, n_labels)
        similarities = np.dot(text_embeddings, LABEL_EMBEDDINGS.T)

        # Ambil top-1 dan top-3 per teks
        top1_idx  = similarities.argmax(axis=1)
        top3_idxs = similarities.argsort(axis=1)[:, -3:][:, ::-1]

        for j in range(len(batch)):
            primary = LABEL_NAMES[top1_idx[j]]
            primary_themes.append(primary)

            top3_formatted = "; ".join([
                f"{LABEL_NAMES[k]} ({similarities[j][k]:.2f})"
                for k in top3_idxs[j]
            ])
            all_themes.append(top3_formatted)

    # ── 3. SIMPAN KE DATAFRAME ──────────────────────────────
    df = df.copy()
    df['AI_Sentiment']       = sentimen_labels
    df['AI_Sentiment_Score'] = sentimen_scores
    df['AI_Primary_Theme']   = primary_themes
    df['AI_All_Themes']      = all_themes

    # Bersihkan GPU cache
    if torch.cuda.is_available():
        torch.cuda.empty_cache()

    return df


# ------ CELL 7: PROSES SEMUA FILE ------
def run_model_per_file():
    print("\n=== MULAI PROSES AI V2: EMBEDDING SIMILARITY ===")

    all_files    = glob.glob(os.path.join(INPUT_DATA_PATH, "**", "*.csv"), recursive=True)
    processed_dfs = []
    BATCH_SIZE   = 32

    print(f"Total file: {len(all_files)} | Batch size: {BATCH_SIZE}")

    for i, file_path in enumerate(all_files):
        try:
            filename       = os.path.basename(file_path)
            kategori_folder = os.path.relpath(os.path.dirname(file_path), INPUT_DATA_PATH)
            target_folder  = os.path.join(OUTPUT_CSV_PATH, kategori_folder)
            os.makedirs(target_folder, exist_ok=True)

            print(f"\n[{i+1}/{len(all_files)}] {kategori_folder}/{filename}")

            df = pd.read_csv(file_path)

            # Fix kolom tanggal
            if 'Review Time' in df.columns:
                try:
                    df['Review Time'] = pd.to_datetime(df['Review Time'], errors='coerce').dt.year.astype('Int64')
                except Exception:
                    pass

            # Standarisasi kolom teks
            if 'Review Text' in df.columns:
                df = df.rename(columns={'Review Text': 'clean_text'})
            elif 'Review Text Cleaned' in df.columns:
                df = df.rename(columns={'Review Text Cleaned': 'clean_text'})

            if df.empty or 'clean_text' not in df.columns:
                print("   SKIP (kosong/kolom tidak ada).")
                continue

            # Metadata
            folder_upper = kategori_folder.upper()
            tipe  = "KOMPETITOR" if "KOMPETITOR" in folder_upper else "BUMN"
            kelas = ("Bintang 3" if "B3" in folder_upper else
                     "Bintang 4" if "B4" in folder_upper else
                     "Bintang 5" if "B5" in folder_upper else "Lainnya")

            df['Tipe']       = tipe
            df['Kelas']      = kelas
            df['Nama_Hotel'] = filename.replace('_Clean.csv', '').replace('.csv', '')

            # Jalankan AI
            df_result = process_inference(df, clf_sentimen, clf_aspek, batch_size=BATCH_SIZE)

            # Simpan
            target_file = os.path.join(target_folder, f"Analisis_{filename}")
            df_result.to_csv(target_file, index=False)
            processed_dfs.append(df_result)

            print(f"   OK — {len(df)} ulasan. Disimpan ke: {target_file}")

        except Exception as e:
            print(f"   ERROR: {e}")

    print("\n=== SELESAI ===")
    return processed_dfs

list_of_dfs = run_model_per_file()


# ------ CELL 8: GABUNG SEMUA HASIL JADI MASTER ------
def run_model_master(data_list=None):
    print("\n=== MEMBUAT DATA MASTER ===")

    if not data_list:
        print("Membaca ulang file Analisis_*.csv...")
        found_files = glob.glob(os.path.join(OUTPUT_CSV_PATH, "**", "Analisis_*.csv"), recursive=True)
        if not found_files:
            print("Tidak ada file hasil.")
            return pd.DataFrame()
        data_list = []
        for f in tqdm(found_files, desc="Membaca"):
            try:
                data_list.append(pd.read_csv(f))
            except Exception:
                pass

    if not data_list:
        return pd.DataFrame()

    master_df = pd.concat(data_list, ignore_index=True)

    path_master = os.path.join(OUTPUT_CSV_PATH, "Analisis_Master_Lengkap.csv")
    master_df.to_csv(path_master, index=False)
    print(f"Master disimpan: {path_master}")

    df_bumn = master_df[master_df['Tipe'] == 'BUMN']
    if not df_bumn.empty:
        df_bumn.to_csv(os.path.join(OUTPUT_CSV_PATH, "Analisis_BUMN_All.csv"), index=False)

    df_komp = master_df[master_df['Tipe'] == 'KOMPETITOR']
    if not df_komp.empty:
        df_komp.to_csv(os.path.join(OUTPUT_CSV_PATH, "Analisis_KOMPETITOR_All.csv"), index=False)

    print(f"Total data: {len(master_df):,} baris | Hotel unik: {master_df['Nama_Hotel'].nunique()}")
    return master_df

try:
    df_result = run_model_master(list_of_dfs)
except NameError:
    df_result = run_model_master()
