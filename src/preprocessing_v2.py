# ============================================================
# PREPROCESSING V2 — Dengan Deteksi Bahasa Otomatis
# ============================================================
# Perubahan dari V1:
#   - Tambah langdetect: teks yang sudah Bahasa Indonesia
#     TIDAK akan ditranslate ulang (mencegah distorsi data)
#   - Teks non-Indonesia (Inggris, dll.) tetap ditranslate ke ID
#   - Semua fungsi lain tetap sama
# ============================================================

# ------ CELL 1: INSTALASI ------
# !pip install pandas transformers torch tqdm langdetect
# !pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118

# ------ CELL 2: IMPORT ------
import os
import re
import gc
import torch
import pandas as pd
from tqdm import tqdm
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

# [BARU] Import untuk deteksi bahasa
from langdetect import detect, DetectorFactory
DetectorFactory.seed = 42  # Supaya hasil deteksi konsisten/reproducible


# ------ CELL 3: SETUP MODEL TRANSLATE ------
device = "cuda" if torch.cuda.is_available() else "cpu"
print(f"Menyiapkan Engine di: {device.upper()}")

MODEL_NAME = "facebook/nllb-200-distilled-600M"
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)

model = AutoModelForSeq2SeqLM.from_pretrained(
    MODEL_NAME,
    torch_dtype=torch.float16 if device == "cuda" else torch.float32
).to(device)

print("Model Translate Siap!")


# ------ CELL 4: KONFIGURASI PATH ------
# Sesuaikan folder input & output yang ingin diproses
# Ganti bagian ini sesuai dataset yang sedang dikerjakan
RAW_PATH   = "../DatasetHotel/BUMNB3"       # ← ganti sesuai folder
CLEAN_PATH = "../DatasetHotelCLEAN/BUMNB3"  # ← ganti sesuai folder
os.makedirs(CLEAN_PATH, exist_ok=True)


# ------ CELL 5: KAMUS SLANG ------
slang_dict = {
    'yg': 'yang', 'ga': 'tidak', 'gak': 'tidak', 'nggak': 'tidak',
    'tp': 'tapi', 'krn': 'karena', 'utk': 'untuk', 'sdh': 'sudah',
    'udh': 'sudah', 'blm': 'belum', 'dgn': 'dengan', 'dlm': 'dalam',
    'bgt': 'banget', 'tdk': 'tidak', 'jgn': 'jangan', 'krg': 'kurang',
    'sy': 'saya', 'ak': 'aku', 'kalo': 'kalau', 'kl': 'kalau',
    'dr': 'dari', 'bs': 'bisa', 'kmn': 'kemana', 'tmn': 'teman',
    'bgs': 'bagus', 'dtg': 'datang', 'br': 'baru', 'ok': 'oke',
    'thx': 'terima kasih', 'makasih': 'terima kasih', 'tks': 'terima kasih',
    'min': 'minus', 'chek': 'check', 'chekout': 'check out',
    'chekin': 'check in', 'pas': 'saat', 'pd': 'pada', 'pake': 'pakai',
    'sm': 'sama', 'lbh': 'lebih', 'bkn': 'bukan', 'spt': 'seperti',
    'jd': 'jadi', 'aja': 'saja', 'aj': 'saja', 'kmr': 'kamar',
    'kmar': 'kamar', 'mnt': 'minta', 'dl': 'dulu', 'skrg': 'sekarang',
    'dg': 'dengan', 'yk': 'yogyakarta', 'tp': 'tapi', 'emg': 'memang',
    'emang': 'memang', 'hrs': 'harus', 'mgkn': 'mungkin', 'knp': 'kenapa',
    'gmn': 'gimana', 'gitu': 'begitu', 'gt': 'begitu', 'udah': 'sudah',
    'ngga': 'tidak', 'ga bisa': 'tidak bisa', 'bener': 'benar',
    'banget': 'sekali', 'sih': '', 'deh': '', 'dong': '', 'nih': '',
}


# ------ CELL 6: FUNGSI DETEKSI BAHASA (BARU) ------
def detect_language(text: str) -> str:
    """
    Mendeteksi bahasa dari teks.
    Return: kode bahasa ISO (e.g. 'id', 'en', 'ms')
    Jika gagal deteksi, default ke 'id' (Indonesia).
    """
    try:
        lang = detect(str(text))
        return lang
    except Exception:
        return "id"  # default ke Indonesia jika gagal

# Bahasa yang dianggap "sudah Indonesia / tidak perlu translate"
SKIP_TRANSLATE_LANGS = {"id", "ms"}  # Indonesia & Melayu (sangat mirip)


# ------ CELL 7: FUNGSI CLEANING TEKS ------
def clean_text_advanced(text: str) -> str:
    if not isinstance(text, str):
        return ""
    text = text.lower()
    text = re.sub(r'(.)\1{2,}', r'\1', text)        # hapus pengulangan huruf
    text = re.sub(r'[^\w\s]', ' ', text)              # hapus tanda baca
    words = text.split()
    words = [slang_dict.get(word, word) for word in words]  # normalisasi slang
    text = ' '.join(words)
    text = re.sub(r'\s+', ' ', text).strip()
    return text


# ------ CELL 8: FUNGSI TRANSLATE (TIDAK BERUBAH) ------
def translate_fast(text_list: list, batch_size: int = 64) -> list:
    """Translate list teks dari EN ke ID menggunakan NLLB-200."""
    results = []
    tokenizer.src_lang = "eng_Latn"
    forced_bos_token_id = tokenizer.convert_tokens_to_ids("ind_Latn")

    for i in range(0, len(text_list), batch_size):
        batch = text_list[i:i + batch_size]
        inputs = tokenizer(
            batch, return_tensors="pt", padding=True,
            truncation=True, max_length=128
        ).to(device)

        with torch.no_grad():
            translated_tokens = model.generate(
                **inputs,
                forced_bos_token_id=forced_bos_token_id,
                max_new_tokens=128,
                num_beams=1,    # Greedy Search — cepat
                do_sample=False
            )

        decoded = tokenizer.batch_decode(translated_tokens, skip_special_tokens=True)
        results.extend(decoded)

        del inputs, translated_tokens

    return results


# ------ CELL 9: FUNGSI UTAMA — DETEKSI + TRANSLATE (BARU) ------
def smart_preprocess(texts: list, translate_batch_size: int = 64) -> list:
    """
    Proses cerdas:
    1. Deteksi bahasa setiap teks
    2. Teks Indonesia/Melayu → langsung dikembalikan (tanpa translate)
    3. Teks lain (Inggris, dll.) → diterjemahkan ke Indonesia

    Ini mencegah distorsi data akibat translate ulang teks yang sudah Indonesia.
    """
    results = [""] * len(texts)

    # Pisahkan mana yang perlu translate dan mana yang tidak
    to_translate_idx = []
    to_translate_txt = []

    print(f"  > Mendeteksi bahasa untuk {len(texts)} teks...")
    for i, text in enumerate(tqdm(texts, desc="  Deteksi bahasa", leave=False)):
        lang = detect_language(text)
        if lang in SKIP_TRANSLATE_LANGS:
            results[i] = text  # Sudah Indonesia, simpan langsung
        else:
            to_translate_idx.append(i)
            to_translate_txt.append(text)

    n_id   = len(texts) - len(to_translate_idx)
    n_en   = len(to_translate_idx)
    pct_id = n_id / len(texts) * 100 if texts else 0
    print(f"  > Bahasa terdeteksi: {n_id} Indonesia ({pct_id:.1f}%), {n_en} non-Indonesia")

    # Translate yang non-Indonesia (jika ada)
    if to_translate_txt:
        print(f"  > Mentranslate {n_en} teks ke Bahasa Indonesia...")
        translated = translate_fast(to_translate_txt, batch_size=translate_batch_size)
        for idx, translated_text in zip(to_translate_idx, translated):
            results[idx] = translated_text

    return results


# ------ CELL 10: EKSEKUSI UTAMA ------
BATCH_SIZE = 64

files = [f for f in os.listdir(RAW_PATH) if f.endswith(".csv")]
print(f"\nMulai Memproses {len(files)} File...\n")

for idx, filename in enumerate(files):
    print(f"[{idx+1}/{len(files)}] {filename}...", end=" ")

    try:
        input_path  = os.path.join(RAW_PATH, filename)
        df          = pd.read_csv(input_path)

        # --- Cleaning awal ---
        df = df.dropna(subset=['Review Text'])
        blacklist = ['N/A', 'n/a', 'na', 'nan', '-', '', ' ', 'null']
        df = df[~df['Review Text'].astype(str).str.lower().str.strip().isin(blacklist)]
        df = df.drop(columns=[c for c in ['No', 'Review Count'] if c in df.columns], errors='ignore')

        df['Review Text Cleaned'] = df['Review Text'].apply(clean_text_advanced)
        df = df[df['Review Text Cleaned'].str.len() > 2]

        texts = df['Review Text Cleaned'].tolist()
        if len(texts) == 0:
            print("Kosong.")
            continue

        # --- [BARU] Deteksi bahasa + translate hanya yang perlu ---
        processed = smart_preprocess(texts, translate_batch_size=BATCH_SIZE)
        df['Review Text Cleaned'] = processed

        # --- Simpan ---
        clean_filename = filename.replace(".csv", "_Clean.csv")
        output_path    = os.path.join(CLEAN_PATH, clean_filename)
        df = df.drop(columns=['Review Text'], errors='ignore')
        df = df.rename(columns={'Review Text Cleaned': 'Review Text'})
        df.to_csv(output_path, index=False, encoding='utf-8-sig')

        print(f"Selesai ({len(texts)} data).")

    except Exception as e:
        print(f"Error: {e}")

    # Cleanup GPU memory
    try:
        del df, texts, processed
        gc.collect()
        torch.cuda.empty_cache()
    except Exception:
        pass

print("\nSEMUA SELESAI!")
