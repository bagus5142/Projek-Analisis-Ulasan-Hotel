# ============================================================
# KAGGLE NOTEBOOK 1: PREPROCESSING
# Cara pakai:
#   1. Buka Kaggle → New Notebook → pilih Code (bukan R)
#   2. Aktifkan GPU T4 + Internet ON
#   3. Tambahkan dataset: meongmesir/datasethotel
#   4. Copy-paste tiap CELL ke cell Kaggle baru
# ============================================================


# ───────────────────────────────────────────────
# CELL 1 — Install library tambahan
# ───────────────────────────────────────────────
"""
!pip install -q langdetect
"""


# ───────────────────────────────────────────────
# CELL 2 — Import & cek GPU
# ───────────────────────────────────────────────
"""
import os, re, gc, glob
import torch
import pandas as pd
from tqdm.auto import tqdm
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
from langdetect import detect, DetectorFactory

DetectorFactory.seed = 42

device = 'cuda' if torch.cuda.is_available() else 'cpu'
print(f'Device : {device.upper()}')
if device == 'cuda':
    print(f'GPU    : {torch.cuda.get_device_name(0)}')
    print(f'VRAM   : {torch.cuda.get_device_properties(0).total_memory / 1e9:.1f} GB')
"""


# ───────────────────────────────────────────────
# CELL 3 — Temukan path dataset otomatis ← JALANKAN INI DULU!
# ───────────────────────────────────────────────
"""
import os, glob

print('=== MENELUSURI SEMUA FILE DI /kaggle/input/ ===')
all_input = glob.glob('/kaggle/input/**/*.csv', recursive=True)

if not all_input:
    print('[ERROR] Tidak ada CSV ditemukan di /kaggle/input/')
    print('Pastikan dataset sudah ditambahkan ke notebook ini.')
else:
    print(f'Total CSV ditemukan: {len(all_input)}')
    print()
    print('10 contoh path:')
    for f in all_input[:10]:
        print(' ', f)

    # Tampilkan struktur folder
    print()
    print('=== STRUKTUR FOLDER /kaggle/input/ ===')
    for root, dirs, files in os.walk('/kaggle/input/'):
        depth = root.replace('/kaggle/input/', '').count(os.sep)
        if depth > 3:
            continue
        indent = '  ' * depth
        print(f'{indent}{os.path.basename(root)}/')
        subindent = '  ' * (depth + 1)
        for f in files[:2]:
            print(f'{subindent}{f}')
"""


# ───────────────────────────────────────────────
# CELL 4 — Set path & verifikasi (sesuaikan INPUT_ROOT jika perlu)
# ───────────────────────────────────────────────
"""
import os, glob

# ⚠️ Sesuaikan INPUT_ROOT berdasarkan output Cell 3
# Ambil salah satu path CSV dari Cell 3, lalu naik 2 folder ke belakang.
# Contoh jika path CSV: /kaggle/input/datasethotel/DatasetHotel/BUMNB3/xxx.csv
#   → INPUT_ROOT = '/kaggle/input/datasethotel/DatasetHotel'

INPUT_ROOT  = '/kaggle/input/datasets/meongmesir/datasethotel/DatasetHotel'
OUTPUT_ROOT = '/kaggle/working/DatasetHotelCLEAN'

FOLDERS = ['BUMNB3', 'BUMNB4', 'BUMNB5',
           'KOMPETITORB3', 'KOMPETITORB4', 'KOMPETITORB5']

for folder in FOLDERS:
    os.makedirs(os.path.join(OUTPUT_ROOT, folder), exist_ok=True)

all_files = glob.glob(os.path.join(INPUT_ROOT, '**', '*.csv'), recursive=True)
print(f'Total CSV ditemukan: {len(all_files)}')
for f in all_files[:5]:
    print(' ', f)
"""


# ───────────────────────────────────────────────
# CELL 4 — Load model translate (NLLB-200)
# ───────────────────────────────────────────────
"""
MODEL_NAME = 'facebook/nllb-200-distilled-600M'
print(f'Loading {MODEL_NAME}...')

tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
translate_model = AutoModelForSeq2SeqLM.from_pretrained(
    MODEL_NAME,
    torch_dtype=torch.float16 if device == 'cuda' else torch.float32
).to(device)

print('Model translate siap!')
"""


# ───────────────────────────────────────────────
# CELL 5 — Kamus slang & fungsi-fungsi
# ───────────────────────────────────────────────
"""
SLANG_DICT = {
    'yg': 'yang', 'ga': 'tidak', 'gak': 'tidak', 'nggak': 'tidak',
    'tp': 'tapi', 'krn': 'karena', 'utk': 'untuk', 'sdh': 'sudah',
    'udh': 'sudah', 'udah': 'sudah', 'blm': 'belum', 'dgn': 'dengan',
    'dlm': 'dalam', 'bgt': 'banget', 'tdk': 'tidak', 'jgn': 'jangan',
    'krg': 'kurang', 'sy': 'saya', 'ak': 'aku', 'kalo': 'kalau',
    'kl': 'kalau', 'dr': 'dari', 'bs': 'bisa', 'tmn': 'teman',
    'bgs': 'bagus', 'dtg': 'datang', 'br': 'baru', 'ok': 'oke',
    'thx': 'terima kasih', 'makasih': 'terima kasih',
    'tks': 'terima kasih', 'chekout': 'check out', 'chekin': 'check in',
    'pd': 'pada', 'pake': 'pakai', 'sm': 'sama', 'lbh': 'lebih',
    'bkn': 'bukan', 'spt': 'seperti', 'jd': 'jadi', 'aja': 'saja',
    'aj': 'saja', 'kmr': 'kamar', 'kmar': 'kamar', 'dl': 'dulu',
    'skrg': 'sekarang', 'dg': 'dengan', 'emg': 'memang', 'emang': 'memang',
    'hrs': 'harus', 'mgkn': 'mungkin', 'knp': 'kenapa', 'gmn': 'gimana',
    'gitu': 'begitu', 'ngga': 'tidak', 'bener': 'benar',
    'nih': '', 'sih': '', 'deh': '', 'dong': '',
}

SKIP_LANGS = {'id', 'ms'}


def detect_lang(text):
    try:
        return detect(str(text))
    except Exception:
        return 'id'


def clean_text(text):
    if not isinstance(text, str):
        return ''
    text = text.lower()
    text = re.sub(r'(.)\1{2,}', r'\1', text)
    text = re.sub(r'[^\w\s]', ' ', text)
    words = [SLANG_DICT.get(w, w) for w in text.split()]
    text = ' '.join(words)
    text = re.sub(r'\s+', ' ', text).strip()
    return text


def translate_batch(text_list, batch_size=128):
    results = []
    tokenizer.src_lang = 'eng_Latn'
    bos_id = tokenizer.convert_tokens_to_ids('ind_Latn')
    for i in range(0, len(text_list), batch_size):
        batch = text_list[i:i + batch_size]
        inputs = tokenizer(batch, return_tensors='pt', padding=True,
                           truncation=True, max_length=128).to(device)
        with torch.no_grad():
            tokens = translate_model.generate(
                **inputs, forced_bos_token_id=bos_id,
                max_new_tokens=128, num_beams=1, do_sample=False
            )
        decoded = tokenizer.batch_decode(tokens, skip_special_tokens=True)
        results.extend(decoded)
        del inputs, tokens
    return results


def smart_preprocess(texts, batch_size=128):
    results = [''] * len(texts)
    to_tr_idx, to_tr_txt = [], []
    for i, text in enumerate(texts):
        if detect_lang(text) in SKIP_LANGS:
            results[i] = text
        else:
            to_tr_idx.append(i)
            to_tr_txt.append(text)
    n_id = len(texts) - len(to_tr_idx)
    pct = n_id / len(texts) * 100 if texts else 0
    print(f'    Indonesia: {n_id} ({pct:.0f}%) | Translate: {len(to_tr_idx)}')
    if to_tr_txt:
        translated = translate_batch(to_tr_txt, batch_size=batch_size)
        for idx, val in zip(to_tr_idx, translated):
            results[idx] = val
    return results


print('Semua fungsi siap.')
"""


# ───────────────────────────────────────────────
# CELL 6 — Eksekusi: proses semua folder
# ───────────────────────────────────────────────
"""
BATCH = 128
total = 0

for folder in FOLDERS:
    raw_dir   = os.path.join(INPUT_ROOT, folder)
    clean_dir = os.path.join(OUTPUT_ROOT, folder)

    if not os.path.exists(raw_dir):
        print(f'[SKIP] {raw_dir}')
        continue

    files = [f for f in os.listdir(raw_dir) if f.endswith('.csv')]
    print(f'\n=== {folder} ({len(files)} file) ===')

    for i, fname in enumerate(files):
        print(f'  [{i+1}/{len(files)}] {fname}...', end=' ')
        try:
            df = pd.read_csv(os.path.join(raw_dir, fname))
            df = df.dropna(subset=['Review Text'])
            bl = {'N/A', 'n/a', 'na', 'nan', '-', '', ' ', 'null'}
            df = df[~df['Review Text'].astype(str).str.lower().str.strip().isin(bl)]
            df = df.drop(columns=[c for c in ['No', 'Review Count'] if c in df.columns], errors='ignore')

            df['Review Text Cleaned'] = df['Review Text'].apply(clean_text)
            df = df[df['Review Text Cleaned'].str.len() > 2].copy()

            if len(df) == 0:
                print('kosong.')
                continue

            texts = df['Review Text Cleaned'].tolist()
            processed = smart_preprocess(texts, batch_size=BATCH)
            df['Review Text Cleaned'] = processed

            out = fname.replace('.csv', '_Clean.csv')
            out_path = os.path.join(clean_dir, out)
            df = df.drop(columns=['Review Text'], errors='ignore')
            df = df.rename(columns={'Review Text Cleaned': 'Review Text'})
            df.to_csv(out_path, index=False, encoding='utf-8-sig')
            total += len(df)
            print(f'OK ({len(df)} baris)')

        except Exception as e:
            print(f'ERROR: {e}')

        try:
            del df, texts, processed
            gc.collect()
            torch.cuda.empty_cache()
        except Exception:
            pass

print(f'\nSELESAI! Total: {total:,} review')
print(f'Output: {OUTPUT_ROOT}')
"""


# ───────────────────────────────────────────────
# CELL 7 — Verifikasi hasil
# ───────────────────────────────────────────────
"""
clean_files = glob.glob(os.path.join(OUTPUT_ROOT, '**', '*.csv'), recursive=True)
print(f'Total file clean: {len(clean_files)}')
for folder in FOLDERS:
    ff = [f for f in clean_files if folder in f]
    rows = sum(len(pd.read_csv(f)) for f in ff)
    print(f'  {folder}: {len(ff)} file, {rows:,} baris')

print()
print('Langkah selanjutnya:')
print('1. Pergi ke tab Output di kanan atas')
print('2. Download folder DatasetHotelCLEAN')
print('3. Upload sebagai Kaggle Dataset baru (misal: datasethotel-clean)')
print('4. Jalankan Notebook 2')
"""
