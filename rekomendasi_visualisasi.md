# 🎯 Rekomendasi Visualisasi untuk Presentasi ke Perusahaan

## Kondisi Saat Ini

Yang sudah ada:
- 📊 **PNG Statis** — Matplotlib/Seaborn (15 chart di folder Visualisasi)
- 🌐 **HTML Dashboard** — Sederhana, filter per hotel, embed PNG

**Masalah untuk presentasi perusahaan:**
- Chart statis tidak bisa di-drill-down saat audiens bertanya
- HTML Dashboard hanya embed gambar, tidak interaktif
- Tampilan kurang profesional untuk level eksekutif

---

## ✅ Perbandingan Tool untuk Presentasi Perusahaan

| Tool | Interaktif | Mudah Share | Offline | Tampilan | Cocok Untuk |
|------|-----------|-------------|---------|----------|-------------|
| **Power BI** | ✅✅ | ✅✅✅ | ✅ | ⭐⭐⭐⭐⭐ | Eksekutif, Presentasi Formal |
| **Tableau Public** | ✅✅ | ✅✅ | ❌ | ⭐⭐⭐⭐⭐ | Visualisasi Profesional |
| **Streamlit** | ✅✅ | ✅ (web) | ✅ | ⭐⭐⭐⭐ | Demo Teknis, Prototype |
| **Plotly Dash** | ✅✅✅ | ✅ (web) | ✅ | ⭐⭐⭐⭐ | Dashboard Custom |
| **Google Looker Studio** | ✅✅ | ✅✅✅ | ❌ | ⭐⭐⭐⭐ | Gratis, Cloud |

---

## 🏆 Rekomendasi Utama: **Streamlit** (Paling Praktis untuk Konteks Ini)

### Mengapa Streamlit?

1. **Gratis & Open Source** — tidak perlu lisensi Power BI Pro
2. **Python Native** — langsung pakai data dari CSV yang sudah ada
3. **Deploy gratis** di Streamlit Cloud → bisa dibagikan via link ke pihak perusahaan
4. **Bisa dijalankan offline** saat presentasi (hanya butuh Python)
5. **Interaktif** — filter, dropdown, slider semua bisa tanpa kode JavaScript
6. **Terlihat profesional** dengan sedikit kustomisasi CSS

### Quick Start

```bash
pip install streamlit plotly pandas
streamlit run dashboard_hotel.py
```

---

## 🥈 Alternatif Terbaik: **Power BI Desktop** (Paling Keren Secara Visual)

Jika tujuannya adalah **kesan pertama yang WOW** kepada eksekutif perusahaan:

### Cara Import CSV ke Power BI:
1. Buka Power BI Desktop (gratis, download di microsoft.com)
2. **Get Data → Text/CSV** → pilih `Analisis_Master_Lengkap.csv`
3. Drag & drop untuk buat visualisasi

### Keunggulan Power BI:
- Tampilan enterprise-grade, langsung terlihat profesional
- Dapat disimpan sebagai `.pbix` dan dibagikan
- Bisa diekspor ke PDF untuk lampiran laporan
- Filter lintas chart otomatis (click satu chart → semua berubah)

---

## 📊 Konten Visualisasi yang Disarankan untuk Presentasi

### Halaman 1: Executive Summary
```
┌─────────────────────────────────────────────┐
│  KPI Cards:                                  │
│  [Total Ulasan] [% Positif BUMN] [% Positif │
│   Kompetitor] [Gap Score]                    │
├──────────────┬──────────────────────────────┤
│  Donut Chart │  Bar Chart                   │
│  Sentimen    │  Top 5 Keluhan BUMN          │
│  BUMN vs     │  vs Kompetitor               │
│  Kompetitor  │                              │
└──────────────┴──────────────────────────────┘
```

### Halaman 2: Perbandingan per Bintang
- **Grouped Bar** — Sentimen positif BUMN vs Kompetitor (B3, B4, B5)
- **Heatmap** — Gap score per aspek x bintang

### Halaman 3: Peta Kelemahan (Yang Paling Penting untuk BUMN!)
- **Horizontal Bar Chart** — Top 10 aspek dengan keluhan terbanyak BUMN
- **Radar/Spider Chart** — Performa BUMN vs Kompetitor per aspek
- **Sample Ulasan Negatif** — Quote review nyata (3-5 contoh)

### Halaman 4: Rekomendasi Strategis
- Tabel prioritas perbaikan berdasarkan frekuensi keluhan
- Roadmap aksi yang bisa dilakukan perusahaan

---

## 💡 Kode Streamlit Siap Pakai (Starter)

```python
# dashboard_hotel.py
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# === KONFIGURASI ===
st.set_page_config(
    page_title="Analisis Ulasan Hotel BUMN",
    page_icon="🏨",
    layout="wide"
)

# === LOAD DATA ===
@st.cache_data
def load_data():
    df = pd.read_csv("../Results/CSV/Analisis_Master_Lengkap.csv")
    df['AI_Sentiment'] = df['AI_Sentiment'].str.lower().str.strip()
    return df

df = load_data()

# === HEADER ===
st.title("🏨 Dashboard Analisis Ulasan Hotel")
st.markdown("Perbandingan Sentimen & Aspek: **BUMN** vs **Kompetitor**")

# === SIDEBAR FILTER ===
st.sidebar.header("Filter")
tipe_filter = st.sidebar.multiselect(
    "Tipe Hotel", ["BUMN", "KOMPETITOR"], default=["BUMN", "KOMPETITOR"]
)
kelas_filter = st.sidebar.multiselect(
    "Kelas Bintang", ["Bintang3", "Bintang4", "Bintang5"],
    default=["Bintang3", "Bintang4", "Bintang5"]
)

df_filtered = df[df['Tipe'].isin(tipe_filter) & df['Kelas'].isin(kelas_filter)]

# === KPI CARDS ===
col1, col2, col3, col4 = st.columns(4)

total_ulasan = len(df_filtered)
pct_pos_bumn = len(df_filtered[(df_filtered['Tipe']=='BUMN') & 
                                (df_filtered['AI_Sentiment']=='positive')]) / \
               max(len(df_filtered[df_filtered['Tipe']=='BUMN']), 1) * 100
pct_pos_komp = len(df_filtered[(df_filtered['Tipe']=='KOMPETITOR') & 
                                (df_filtered['AI_Sentiment']=='positive')]) / \
               max(len(df_filtered[df_filtered['Tipe']=='KOMPETITOR']), 1) * 100
gap = pct_pos_bumn - pct_pos_komp

col1.metric("Total Ulasan", f"{total_ulasan:,}")
col2.metric("Sentimen Positif BUMN", f"{pct_pos_bumn:.1f}%")
col3.metric("Sentimen Positif Kompetitor", f"{pct_pos_komp:.1f}%")
col4.metric("Gap (BUMN - Kompetitor)", f"{gap:+.1f}%",
            delta_color="normal" if gap >= 0 else "inverse")

st.divider()

# === CHART 1: Distribusi Sentimen ===
col_a, col_b = st.columns(2)

with col_a:
    st.subheader("Distribusi Sentimen")
    sent_data = df_filtered.groupby(['Tipe', 'AI_Sentiment']).size().reset_index(name='count')
    fig_sent = px.bar(sent_data, x='Tipe', y='count', color='AI_Sentiment',
                      barmode='group',
                      color_discrete_map={
                          'positive': '#069494',
                          'negative': '#B7410E',
                          'neutral': '#FFCE1B'
                      })
    st.plotly_chart(fig_sent, use_container_width=True)

with col_b:
    st.subheader("Top 8 Aspek Keluhan Negatif BUMN")
    df_neg_bumn = df_filtered[(df_filtered['Tipe']=='BUMN') & 
                               (df_filtered['AI_Sentiment']=='negative')]
    top_neg = df_neg_bumn['AI_Primary_Theme'].value_counts().head(8).reset_index()
    top_neg.columns = ['Aspek', 'Jumlah']
    fig_neg = px.bar(top_neg, x='Jumlah', y='Aspek', orientation='h',
                     color_discrete_sequence=['#B7410E'])
    fig_neg.update_layout(yaxis={'categoryorder': 'total ascending'})
    st.plotly_chart(fig_neg, use_container_width=True)

# === TABEL SAMPLE ULASAN ===
st.subheader("📝 Sample Ulasan Negatif Terbaru")
df_sample = df_filtered[df_filtered['AI_Sentiment']=='negative'][
    ['Nama_Hotel', 'Tipe', 'Kelas', 'AI_Primary_Theme', 'clean_text']
].head(10)
st.dataframe(df_sample, use_container_width=True)
```

---

## 🎨 Tips Tampilan untuk Presentasi ke Perusahaan

1. **Gunakan warna brand BUMN** (biasanya merah/biru) sebagai aksen utama
2. **Ukuran font minimal 14px** — ruang presentasi biasanya besar
3. **Hindari terlalu banyak data** di satu halaman — max 2-3 insight per slide
4. **Sertakan rekomendasi aksi nyata** di setiap temuan (eksekutif ingin tahu "lalu apa yang harus dilakukan?")
5. **Buat narasi "story"** — bukan hanya chart, tapi kesimpulan berbentuk kalimat
6. **Demo live** lebih berkesan daripada screenshot — jalankan Streamlit saat presentasi

> [!TIP]
> Jika tidak ada koneksi internet saat presentasi, jalankan Streamlit secara lokal:
> `streamlit run dashboard_hotel.py` → buka `http://localhost:8501` di browser

> [!IMPORTANT]
> Untuk presentasi ke level **Direksi/C-Level**, **Power BI** memberikan kesan lebih
> profesional. Untuk presentasi ke tim IT/Analitik, **Streamlit** lebih cocok karena
> menunjukkan kemampuan teknis.
