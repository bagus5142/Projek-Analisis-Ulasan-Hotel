import streamlit as st
import pandas as pd
import io
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import os
from collections import Counter

# --- KONFIGURASI HALAMAN ---
st.set_page_config(
    page_title="Dashboard Analisis Hotel - Advanced",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ===== COLOR PALETTE MODERN & VIBRANT =====
SENTIMENT_PALETTE = {
    "positive": "#00D9C0",  # Turquoise bright
    "negative": "#FF6B6B",  # Coral red
    "neutral":  "#FFE66D"   # Sunny yellow
}

# Extended palette - Modern & Bold
EXTENDED_PALETTE = {
    "primary": "#6C5CE7",        # Purple modern
    "primary_dark": "#5B4BD4",   # Darker purple
    "secondary": "#00D9C0",      # Turquoise
    "secondary_dark": "#00B8A3", # Dark turquoise
    "accent": "#FF6B6B",         # Coral
    "accent_dark": "#EE5A5A",    # Dark coral
    "warning": "#FFE66D",        # Yellow
    "success": "#00D9C0",        # Success turquoise
    "danger": "#FF6B6B",         # Danger coral
    "info": "#74B9FF",           # Light blue
    "dark": "#2D3436",           # Dark charcoal
    "gray": "#636E72",           # Gray
    "light": "#F8F9FA",          # Light background
    "gradient_start": "#6C5CE7", # Gradient purple
    "gradient_end": "#A29BFE",   # Gradient light purple
    "bumn_primary": "#6C5CE7",   # BUMN purple
    "non_bumn_primary": "#FF6B6B", # Non-BUMN coral
    "bg_card": "#FFFFFF",        # Card background
    "bg_page": "#F0F2F5",        # Page background
    "text_primary": "#2D3436",   # Primary text
    "text_secondary": "#636E72"  # Secondary text
}

# Custom CSS dengan tema modern
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    
    * {{
        font-family: 'Inter', sans-serif;
    }}
    
    @keyframes fadeIn {{
        from {{ opacity: 0; transform: translateY(20px); }}
        to {{ opacity: 1; transform: translateY(0); }}
    }}
    
    @keyframes slideInLeft {{
        from {{ transform: translateX(-50px); opacity: 0; }}
        to {{ transform: translateX(0); opacity: 1; }}
    }}
    
    @keyframes slideInRight {{
        from {{ transform: translateX(50px); opacity: 0; }}
        to {{ transform: translateX(0); opacity: 1; }}
    }}
    
    @keyframes float {{
        0%, 100% {{ transform: translateY(0px); }}
        50% {{ transform: translateY(-10px); }}
    }}
    
    @keyframes shimmer {{
        0% {{ background-position: -1000px 0; }}
        100% {{ background-position: 1000px 0; }}
    }}
    
    .main-header {{
        background: linear-gradient(135deg, {EXTENDED_PALETTE['gradient_start']} 0%, {EXTENDED_PALETTE['gradient_end']} 100%);
        padding: 40px;
        border-radius: 20px;
        margin-bottom: 30px;
        box-shadow: 0 20px 60px rgba(108, 92, 231, 0.3);
        animation: fadeIn 0.8s ease-out;
        position: relative;
        overflow: hidden;
    }}
    
    .main-header::before {{
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: linear-gradient(45deg, transparent, rgba(255,255,255,0.1), transparent);
        transform: rotate(45deg);
        animation: shimmer 3s infinite;
    }}
    
    .main-header h1 {{
        color: white;
        font-size: 2.8rem;
        font-weight: 800;
        text-align: center;
        margin: 0;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
        position: relative;
        z-index: 1;
    }}
    
    .main-header p {{
        color: rgba(255,255,255,0.9);
        text-align: center;
        font-size: 1.1rem;
        margin-top: 10px;
        position: relative;
        z-index: 1;
    }}
    
    .author-section {{
        background: linear-gradient(135deg, {EXTENDED_PALETTE['secondary']} 0%, {EXTENDED_PALETTE['secondary_dark']} 100%);
        padding: 25px;
        border-radius: 15px;
        margin-bottom: 30px;
        box-shadow: 0 10px 40px rgba(0, 217, 192, 0.3);
        animation: fadeIn 1s ease-out;
        border: 2px solid rgba(255,255,255,0.2);
    }}
    
    .author-section h3 {{
        color: white;
        margin: 0 0 15px 0;
        font-size: 1.3rem;
        font-weight: 700;
    }}
    
    .author-grid {{
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 15px;
    }}
    
    .author-card {{
        background: rgba(255,255,255,0.2);
        padding: 15px;
        border-radius: 10px;
        text-align: center;
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255,255,255,0.3);
        transition: all 0.3s ease;
    }}
    
    .author-card:hover {{
        transform: translateY(-5px);
        background: rgba(255,255,255,0.3);
    }}
    
    .author-card p {{
        color: white;
        margin: 0;
        font-weight: 600;
        font-size: 0.95rem;
    }}
    
    .metric-card {{
        background: {EXTENDED_PALETTE['bg_card']};
        padding: 25px;
        border-radius: 15px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.08);
        border-left: 5px solid {EXTENDED_PALETTE['primary']};
        transition: all 0.3s ease;
        animation: slideInLeft 0.6s ease-out;
    }}
    
    .metric-card:hover {{
        transform: translateY(-5px);
        box-shadow: 0 8px 30px rgba(108, 92, 231, 0.2);
    }}
    
    .metric-card.bumn {{
        border-left-color: {EXTENDED_PALETTE['bumn_primary']};
    }}
    
    .metric-card.non-bumn {{
        border-left-color: {EXTENDED_PALETTE['non_bumn_primary']};
    }}
    
    .insight-box {{
        background: linear-gradient(135deg, #FFF9E6 0%, #FFF3CD 100%);
        padding: 20px;
        border-radius: 12px;
        border-left: 5px solid {EXTENDED_PALETTE['warning']};
        margin: 15px 0;
        box-shadow: 0 4px 15px rgba(255, 230, 109, 0.2);
        animation: fadeIn 0.8s ease-out;
    }}
    
    .success-box {{
        background: linear-gradient(135deg, #E8F8F5 0%, #D1F2EB 100%);
        padding: 20px;
        border-radius: 12px;
        border-left: 5px solid {EXTENDED_PALETTE['success']};
        margin: 15px 0;
        box-shadow: 0 4px 15px rgba(0, 217, 192, 0.2);
    }}
    
    .danger-box {{
        background: linear-gradient(135deg, #FDEDEC 0%, #FADBD8 100%);
        padding: 20px;
        border-radius: 12px;
        border-left: 5px solid {EXTENDED_PALETTE['danger']};
        margin: 15px 0;
        box-shadow: 0 4px 15px rgba(255, 107, 107, 0.2);
    }}
    
    .info-box {{
        background: linear-gradient(135deg, #EBF5FB 0%, #D6EAF8 100%);
        padding: 20px;
        border-radius: 12px;
        border-left: 5px solid {EXTENDED_PALETTE['info']};
        margin: 15px 0;
        box-shadow: 0 4px 15px rgba(116, 185, 255, 0.2);
    }}
    
    .bumn-box {{
        background: linear-gradient(135deg, {EXTENDED_PALETTE['bumn_primary']} 0%, {EXTENDED_PALETTE['gradient_end']} 100%);
        padding: 25px;
        border-radius: 15px;
        color: white;
        box-shadow: 0 10px 40px rgba(108, 92, 231, 0.3);
        animation: slideInLeft 0.8s ease-out;
        border: 2px solid rgba(255,255,255,0.2);
    }}
    
    .non-bumn-box {{
        background: linear-gradient(135deg, {EXTENDED_PALETTE['non_bumn_primary']} 0%, #FF8E8E 100%);
        padding: 25px;
        border-radius: 15px;
        color: white;
        box-shadow: 0 10px 40px rgba(255, 107, 107, 0.3);
        animation: slideInRight 0.8s ease-out;
        border: 2px solid rgba(255,255,255,0.2);
    }}
    
    .comparison-header {{
        background: linear-gradient(135deg, {EXTENDED_PALETTE['primary']} 0%, {EXTENDED_PALETTE['secondary']} 100%);
        padding: 25px;
        border-radius: 15px;
        text-align: center;
        color: white;
        font-size: 1.8rem;
        font-weight: 700;
        margin: 20px 0;
        box-shadow: 0 10px 40px rgba(108, 92, 231, 0.3);
        animation: float 3s ease-in-out infinite;
    }}
    
    .stTabs [data-baseweb="tab-list"] {{
        gap: 15px;
        background: {EXTENDED_PALETTE['bg_card']};
        padding: 15px;
        border-radius: 15px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.05);
    }}
    
    .stTabs [data-baseweb="tab"] {{
        background: transparent;
        border-radius: 10px;
        padding: 12px 24px;
        font-weight: 600;
        transition: all 0.3s ease;
        border: 2px solid transparent;
        color: {EXTENDED_PALETTE['gray']};
    }}
    
    .stTabs [data-baseweb="tab"]:hover {{
        background: rgba(108, 92, 231, 0.1);
        color: {EXTENDED_PALETTE['primary']};
        transform: translateY(-2px);
    }}
    
    .stTabs [aria-selected="true"] {{
        background: linear-gradient(135deg, {EXTENDED_PALETTE['primary']} 0%, {EXTENDED_PALETTE['secondary']} 100%);
        color: white !important;
        box-shadow: 0 4px 15px rgba(108, 92, 231, 0.3);
    }}
    
    div[data-testid="stMetricValue"] {{
        font-size: 2.2rem;
        font-weight: 800;
        background: linear-gradient(135deg, {EXTENDED_PALETTE['primary']} 0%, {EXTENDED_PALETTE['secondary']} 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }}
    
    div[data-testid="stMetricLabel"] {{
        font-size: 0.95rem;
        color: {EXTENDED_PALETTE['gray']};
        font-weight: 500;
    }}
    
    .footer {{
        background: linear-gradient(135deg, {EXTENDED_PALETTE['dark']} 0%, {EXTENDED_PALETTE['gray']} 100%);
        padding: 40px;
        border-radius: 20px;
        margin-top: 40px;
        color: white;
        text-align: center;
        box-shadow: 0 -10px 40px rgba(0,0,0,0.1);
    }}
    
    .footer h4 {{
        color: white;
        font-size: 1.5rem;
        margin-bottom: 15px;
    }}
    
    .footer p {{
        color: rgba(255,255,255,0.8);
        margin: 5px 0;
    }}
    
    .animated-card {{
        animation: fadeIn 0.8s ease-out;
        transition: all 0.3s ease;
    }}
    
    .animated-card:hover {{
        transform: scale(1.02);
        box-shadow: 0 12px 40px rgba(108, 92, 231, 0.15);
    }}
    
    /* Custom scrollbar */
    ::-webkit-scrollbar {{
        width: 12px;
        height: 12px;
    }}
    
    ::-webkit-scrollbar-track {{
        background: {EXTENDED_PALETTE['bg_page']};
        border-radius: 10px;
    }}
    
    ::-webkit-scrollbar-thumb {{
        background: linear-gradient(135deg, {EXTENDED_PALETTE['primary']} 0%, {EXTENDED_PALETTE['secondary']} 100%);
        border-radius: 10px;
        border: 3px solid {EXTENDED_PALETTE['bg_page']};
    }}
    
    ::-webkit-scrollbar-thumb:hover {{
        background: linear-gradient(135deg, {EXTENDED_PALETTE['primary_dark']} 0%, {EXTENDED_PALETTE['secondary_dark']} 100%);
    }}
    
    /* Table styling */
    .stDataFrame {{
        background-color: {EXTENDED_PALETTE['bg_card']};
        border-radius: 15px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.08);
        overflow: hidden;
    }}
    
    /* Button styling */
    .stButton > button {{
        background: linear-gradient(135deg, {EXTENDED_PALETTE['primary']} 0%, {EXTENDED_PALETTE['secondary']} 100%);
        color: white;
        border: none;
        border-radius: 10px;
        padding: 12px 28px;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(108, 92, 231, 0.3);
    }}
    
    .stButton > button:hover {{
        transform: translateY(-3px);
        box-shadow: 0 8px 25px rgba(108, 92, 231, 0.4);
    }}
    
    /* Section headers */
    .section-header {{
        background: linear-gradient(90deg, {EXTENDED_PALETTE['primary']} 0%, transparent 100%);
        padding: 15px 25px;
        border-radius: 10px;
        color: white;
        font-size: 1.4rem;
        font-weight: 700;
        margin: 30px 0 20px 0;
        box-shadow: 0 4px 15px rgba(108, 92, 231, 0.2);
    }}
    
    /* Card grid */
    .card-grid {{
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
        gap: 20px;
        margin: 20px 0;
    }}
    
    /* Progress bar styling */
    .stProgress > div > div {{
        background: linear-gradient(90deg, {EXTENDED_PALETTE['primary']} 0%, {EXTENDED_PALETTE['secondary']} 100%);
        border-radius: 10px;
    }}
    
    /* Selectbox styling */
    .stSelectbox > div > div {{
        background: {EXTENDED_PALETTE['bg_card']};
        border-radius: 10px;
        border: 2px solid {EXTENDED_PALETTE['primary']};
    }}
    
    /* Multiselect styling */
    .stMultiSelect > div > div > div {{
        background: {EXTENDED_PALETTE['bg_card']};
        border-radius: 8px;
    }}
    
    /* Sidebar styling */
    .css-1d391kg {{
        background: linear-gradient(180deg, {EXTENDED_PALETTE['bg_card']} 0%, {EXTENDED_PALETTE['bg_page']} 100%);
    }}
    
    /* Expander styling */
    .streamlit-expanderHeader {{
        background: linear-gradient(90deg, rgba(108, 92, 231, 0.1) 0%, transparent 100%);
        border-radius: 10px;
        border-left: 4px solid {EXTENDED_PALETTE['primary']};
        font-weight: 600;
    }}
    
    /* Tooltip styling */
    .stTooltip {{
        background: {EXTENDED_PALETTE['dark']};
        color: white;
        border-radius: 8px;
        padding: 8px 12px;
    }}
    </style>
""", unsafe_allow_html=True)

# --- FUNGSI LOAD DATA ---
@st.cache_data
def load_data():
    """Load dan preprocessing data"""
    file_path = os.path.join(os.path.dirname(__file__), "Analisis_Master_Lengkap.csv")
    if not os.path.exists(file_path):
        return None
    
    df = pd.read_csv(file_path)
    df['Rating'] = pd.to_numeric(df['Rating'], errors='coerce')
    df['Review Time'] = pd.to_numeric(df['Review Time'], errors='coerce')
    
    required_columns = ['Nama_Hotel', 'Kelas', 'Rating', 'AI_Sentiment', 'AI_Aspek', 'clean_text']
    for col in required_columns:
        if col not in df.columns:
            st.error(f"Kolom '{col}' tidak ditemukan dalam dataset!")
            return None
    
    return df.dropna(subset=['Rating'])

# --- FUNGSI ANALISIS ---
def analyze_aspect_sentiment(df, hotel_name=None):
    """Analisis sentimen per aspek untuk hotel tertentu atau semua hotel"""
    if hotel_name:
        df_temp = df[df['Nama_Hotel'] == hotel_name]
    else:
        df_temp = df
    
    aspect_sentiment = df_temp.groupby(['AI_Aspek', 'AI_Sentiment']).size().unstack(fill_value=0)
    return aspect_sentiment

def get_aspect_scores(df, hotel_name):
    """Menghitung skor untuk setiap aspek berdasarkan sentimen (0-100)"""
    df_hotel = df[df['Nama_Hotel'] == hotel_name]
    
    scores = {}
    for aspek in df_hotel['AI_Aspek'].unique():
        df_aspek = df_hotel[df_hotel['AI_Aspek'] == aspek]
        
        positive = len(df_aspek[df_aspek['AI_Sentiment'] == 'positive'])
        negative = len(df_aspek[df_aspek['AI_Sentiment'] == 'negative'])
        neutral = len(df_aspek[df_aspek['AI_Sentiment'] == 'neutral'])
        total = positive + negative + neutral
        
        if total > 0:
            score = ((positive * 1.0 + neutral * 0.5) / total) * 100
            scores[aspek] = {
                'score': score,
                'positive': positive,
                'negative': negative,
                'neutral': neutral,
                'total': total
            }
    
    return scores

def get_category_aspect_scores(df, category):
    """Menghitung skor aspek untuk kategori hotel (BUMN/Non-BUMN)"""
    df_category = df[df['Kategori_Hotel'] == category]
    
    scores = {}
    for aspek in df_category['AI_Aspek'].unique():
        df_aspek = df_category[df_category['AI_Aspek'] == aspek]
        
        positive = len(df_aspek[df_aspek['AI_Sentiment'] == 'positive'])
        negative = len(df_aspek[df_aspek['AI_Sentiment'] == 'negative'])
        neutral = len(df_aspek[df_aspek['AI_Sentiment'] == 'neutral'])
        total = positive + negative + neutral
        
        if total > 0:
            score = ((positive * 1.0 + neutral * 0.5) / total) * 100
            scores[aspek] = {
                'score': score,
                'positive': positive,
                'negative': negative,
                'neutral': neutral,
                'total': total
            }
    
    return scores

def get_top_keywords(df, hotel_name, sentiment=None, top_n=20):
    """Ekstrak kata-kata yang paling sering muncul"""
    df_hotel = df[df['Nama_Hotel'] == hotel_name]
    
    if sentiment:
        df_hotel = df_hotel[df_hotel['AI_Sentiment'] == sentiment]
    
    text = " ".join(df_hotel['clean_text'].astype(str).tolist())
    words = text.split()
    
    words = [w for w in words if len(w) > 3]
    
    word_counts = Counter(words)
    return word_counts.most_common(top_n)

def get_sentiment_percentage(df, hotel_name):
    """Hitung persentase sentimen untuk hotel"""
    df_hotel = df[df['Nama_Hotel'] == hotel_name]
    total = len(df_hotel)
    
    if total == 0:
        return {'positive': 0, 'negative': 0, 'neutral': 0}
    
    positive = len(df_hotel[df_hotel['AI_Sentiment'] == 'positive']) / total * 100
    negative = len(df_hotel[df_hotel['AI_Sentiment'] == 'negative']) / total * 100
    neutral = len(df_hotel[df_hotel['AI_Sentiment'] == 'neutral']) / total * 100
    
    return {'positive': positive, 'negative': negative, 'neutral': neutral}

def categorize_hotel_type(hotel_name):
    """Kategorikan hotel sebagai BUMN atau Non-BUMN"""
    bumn_keywords = ['patra', 'garuda', 'aerowisata', 'indonesia tourism', 'mandarin oriental']
    
    hotel_lower = hotel_name.lower()
    
    for keyword in bumn_keywords:
        if keyword in hotel_lower:
            return 'BUMN'
    
    return 'Non-BUMN'

# --- LOAD DATA ---
df = load_data()

if df is None:
    st.error("File CSV tidak ditemukan! Pastikan file 'Analisis_Master_Lengkap.csv' ada di direktori yang sama.")
    st.stop()

# Tambahkan kolom kategori hotel
df['Kategori_Hotel'] = df['Nama_Hotel'].apply(categorize_hotel_type)

# --- HEADER DASHBOARD ---
st.markdown(f"""
<div class="main-header">
    <h1>🏨 Dashboard Analisis Ulasan Hotel</h1>
    <p>Analisis Sentimen & Perbandingan Kinerja Hotel BUMN vs Non-BUMN</p>
</div>
""", unsafe_allow_html=True)

# --- AUTHOR SECTION ---
st.markdown(f"""
<div class="author-section">
    <h3>👥 Tim Pengembang</h3>
    <div class="author-grid">
        <div class="author-card">
            <p>Bagus Muhammad Razzan Wahyudi</p>
        </div>
        <div class="author-card">
            <p>Raihan Ade Alfattah</p>
        </div>
        <div class="author-card">
            <p>Maulana Naufal Habibie</p>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# --- SIDEBAR FILTER REVISI ---
st.sidebar.title("🎛️ Panel Kontrol")
st.sidebar.markdown("---")

# ========== FILTER 1: KELAS (BINTANG) ==========
st.sidebar.subheader("⭐ Filter 1: Kategori Bintang Hotel")
list_bintang = sorted(df['Kelas'].unique())
selected_bintang = st.sidebar.multiselect(
    "Pilih Kategori Bintang:",
    list_bintang,
    default=list_bintang,
    help="Pilih kategori bintang hotel yang ingin dianalisis"
)

# Filter berdasarkan bintang
df_filter1 = df[df['Kelas'].isin(selected_bintang)]

st.sidebar.markdown("---")

# ========== FILTER 2: HOTEL BUMN (TERPISAH) ==========
st.sidebar.subheader("🏛️ Filter 2: Hotel BUMN")
df_bumn_only = df_filter1[df_filter1['Kategori_Hotel'] == 'BUMN']
list_hotel_bumn = sorted(df_bumn_only['Nama_Hotel'].unique())

selected_bumn_hotels = st.sidebar.multiselect(
    "Pilih Hotel BUMN:",
    list_hotel_bumn,
    default=list_hotel_bumn[:min(2, len(list_hotel_bumn))] if len(list_hotel_bumn) > 0 else [],
    help="Pilih hotel milik BUMN untuk dibandingkan"
)

st.sidebar.markdown("---")

# ========== FILTER 3: HOTEL NON-BUMN (TERPISAH) ==========
st.sidebar.subheader("🏢 Filter 3: Hotel Non-BUMN")
df_non_bumn_only = df_filter1[df_filter1['Kategori_Hotel'] == 'Non-BUMN']
list_hotel_non_bumn = sorted(df_non_bumn_only['Nama_Hotel'].unique())

selected_non_bumn_hotels = st.sidebar.multiselect(
    "Pilih Hotel Non-BUMN:",
    list_hotel_non_bumn,
    default=list_hotel_non_bumn[:min(2, len(list_hotel_non_bumn))] if len(list_hotel_non_bumn) > 0 else [],
    help="Pilih hotel non-BUMN untuk dibandingkan"
)

# Gabungkan pilihan hotel
selected_hotels = selected_bumn_hotels + selected_non_bumn_hotels

# Final Filter
df_final = df_filter1[df_filter1['Nama_Hotel'].isin(selected_hotels)]

st.sidebar.markdown("---")
st.sidebar.info(f"""
📊 **Statistik Data:**
• Total Ulasan: {len(df_final):,}
• Hotel BUMN: {len(selected_bumn_hotels)}
• Hotel Non-BUMN: {len(selected_non_bumn_hotels)}
• Total Hotel: {len(selected_hotels)}
""")

if len(selected_hotels) == 0:
    st.warning("⚠️ Silakan pilih minimal 1 hotel dari kategori BUMN atau Non-BUMN untuk memulai analisis.")
    st.stop()

# Info Filter Aktif dengan desain modern
st.markdown(f"""
<div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 20px; margin-bottom: 30px;">
    <div class="info-box animated-card" style="margin: 0;">
        <h4 style="color: {EXTENDED_PALETTE['primary']}; margin: 0 0 10px 0;">⭐ Kategori Bintang</h4>
        <p style="margin: 0; font-size: 1.1rem; font-weight: 600;">{', '.join(map(str, selected_bintang))}</p>
    </div>
    <div class="success-box animated-card" style="margin: 0;">
        <h4 style="color: {EXTENDED_PALETTE['secondary_dark']}; margin: 0 0 10px 0;">🏛️ Hotel BUMN</h4>
        <p style="margin: 0; font-size: 1.1rem; font-weight: 600;">{len(selected_bumn_hotels)} hotel dipilih</p>
    </div>
    <div class="danger-box animated-card" style="margin: 0;">
        <h4 style="color: {EXTENDED_PALETTE['accent_dark']}; margin: 0 0 10px 0;">🏢 Hotel Non-BUMN</h4>
        <p style="margin: 0; font-size: 1.1rem; font-weight: 600;">{len(selected_non_bumn_hotels)} hotel dipilih</p>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# --- METRICS OVERVIEW ---
st.markdown(f'<div class="section-header">📊 Ringkasan Statistik Hotel</div>', unsafe_allow_html=True)

# Buat grid metrics yang lebih modern
num_hotels = len(selected_hotels)
cols_per_row = min(4, num_hotels)
rows_needed = (num_hotels + cols_per_row - 1) // cols_per_row

for row in range(rows_needed):
    cols = st.columns(cols_per_row)
    start_idx = row * cols_per_row
    end_idx = min(start_idx + cols_per_row, num_hotels)
    
    for idx, hotel in enumerate(selected_hotels[start_idx:end_idx]):
        df_hotel = df_final[df_final['Nama_Hotel'] == hotel]
        
        with cols[idx]:
            avg_rating = df_hotel['Rating'].mean()
            total_reviews = len(df_hotel)
            sentiment_pct = get_sentiment_percentage(df_final, hotel)
            kategori = df_hotel['Kategori_Hotel'].iloc[0] if len(df_hotel) > 0 else 'N/A'
            
            card_class = "bumn" if kategori == "BUMN" else "non-bumn"
            
            st.markdown(f"""
            <div class="metric-card {card_class}">
                <h4 style="margin: 0 0 10px 0; color: {EXTENDED_PALETTE['text_primary']}; font-size: 1rem;">{hotel[:25]}{'...' if len(hotel) > 25 else ''}</h4>
                <div style="font-size: 2.2rem; font-weight: 800; background: linear-gradient(135deg, {EXTENDED_PALETTE['primary'] if kategori == 'BUMN' else EXTENDED_PALETTE['non_bumn_primary']} 0%, {EXTENDED_PALETTE['secondary'] if kategori == 'BUMN' else '#FF8E8E'} 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text;">
                    {avg_rating:.2f}
                </div>
                <div style="color: {EXTENDED_PALETTE['gray']}; font-size: 0.9rem; margin-bottom: 10px;">⭐ Rata-rata Rating</div>
                <div style="background: {'rgba(108, 92, 231, 0.1)' if kategori == 'BUMN' else 'rgba(255, 107, 107, 0.1)'}; padding: 8px; border-radius: 8px; text-align: center;">
                    <span style="color: {EXTENDED_PALETTE['success']}; font-weight: 700;">{sentiment_pct['positive']:.1f}%</span> <span style="color: {EXTENDED_PALETTE['gray']}; font-size: 0.85rem;">positif</span>
                </div>
                <div style="margin-top: 10px; font-size: 0.85rem; color: {EXTENDED_PALETTE['gray']};">
                    {total_reviews:,} ulasan | <span style="color: {EXTENDED_PALETTE['primary'] if kategori == 'BUMN' else EXTENDED_PALETTE['non_bumn_primary']}; font-weight: 600;">{kategori}</span>
                </div>
            </div>
            """, unsafe_allow_html=True)

st.markdown("---")

# --- TAB VISUALISASI ---
tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8 = st.tabs([
    "📊 Overview",
    "⚖️ BUMN vs Non-BUMN",
    "🔍 Analisis Aspek Detail",
    "💭 Sentimen per Aspek",
    "📈 Perbandingan Hotel",
    "☁️ Word Cloud",
    "🗺️ Heatmap & Insights",
    "📋 Data Mentah"
])

# ===== TAB 1: OVERVIEW =====
with tab1:
    st.markdown(f'<div class="section-header">📈 Ringkasan Umum Dashboard</div>', unsafe_allow_html=True)
    
    # Layout 2 kolom untuk visualisasi utama
    col1, col2 = st.columns([1, 1])
    
    with col1:
        # Distribusi Sentimen Keseluruhan dengan donut chart modern
        st.markdown(f"""
        <div style="background: {EXTENDED_PALETTE['bg_card']}; padding: 25px; border-radius: 15px; box-shadow: 0 4px 20px rgba(0,0,0,0.08);">
            <h4 style="color: {EXTENDED_PALETTE['text_primary']}; margin-bottom: 20px; text-align: center;">Distribusi Sentimen Keseluruhan</h4>
        """, unsafe_allow_html=True)
        
        sentimen_count = df_final.groupby('AI_Sentiment').size().reset_index(name='Jumlah')
        
        fig_donut = px.pie(
            sentimen_count,
            values='Jumlah',
            names='AI_Sentiment',
            hole=0.6,
            color='AI_Sentiment',
            color_discrete_map=SENTIMENT_PALETTE
        )
        fig_donut.update_traces(
            textposition='inside', 
            textinfo='percent+label',
            textfont=dict(size=14, color='white', family='Inter', weight='bold'),
            marker=dict(line=dict(color='white', width=3))
        )
        fig_donut.update_layout(
            showlegend=False, 
            height=400,
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color=EXTENDED_PALETTE['text_primary']),
            margin=dict(t=20, b=20, l=20, r=20)
        )
        # Tambahkan center text
        fig_donut.add_annotation(
            text=f"<b>{len(df_final):,}</b><br>Ulasan",
            showarrow=False,
            font=dict(size=16, color=EXTENDED_PALETTE['text_primary'], family='Inter')
        )
        st.plotly_chart(fig_donut, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)
    
    with col2:
        # Aspek yang Paling Sering Dibahas dengan bar chart horizontal
        st.markdown(f"""
        <div style="background: {EXTENDED_PALETTE['bg_card']}; padding: 25px; border-radius: 15px; box-shadow: 0 4px 20px rgba(0,0,0,0.08);">
            <h4 style="color: {EXTENDED_PALETTE['text_primary']}; margin-bottom: 20px; text-align: center;">Aspek yang Paling Sering Dibahas</h4>
        """, unsafe_allow_html=True)
        
        aspek_count = df_final.groupby('AI_Aspek').size().reset_index(name='Frekuensi').sort_values(by='Frekuensi', ascending=True)
        
        fig_aspek = px.bar(
            aspek_count,
            x='Frekuensi',
            y='AI_Aspek',
            orientation='h',
            color='Frekuensi',
            color_continuous_scale=['#E8F8F5', '#00D9C0', '#6C5CE7'],
            text='Frekuensi'
        )
        fig_aspek.update_traces(
            texttemplate='%{text}', 
            textposition='outside', 
            textfont=dict(size=12, color=EXTENDED_PALETTE['text_primary'], weight='bold'),
            marker=dict(line=dict(color='white', width=2))
        )
        fig_aspek.update_layout(
            showlegend=False, 
            height=400,
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color=EXTENDED_PALETTE['text_primary']),
            yaxis=dict(color=EXTENDED_PALETTE['text_primary'], tickfont=dict(size=11)),
            xaxis=dict(color=EXTENDED_PALETTE['text_primary']),
            margin=dict(t=20, b=20, l=20, r=20),
            coloraxis_showscale=False
        )
        st.plotly_chart(fig_aspek, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Rating per Hotel dengan visualisasi yang lebih menarik
    st.markdown(f'<div class="section-header">⭐ Perbandingan Rating Rata-rata</div>', unsafe_allow_html=True)
    
    avg_rating = df_final.groupby('Nama_Hotel')['Rating'].mean().reset_index().sort_values(by='Rating', ascending=False)
    avg_rating['Kategori'] = avg_rating['Nama_Hotel'].apply(lambda x: df_final[df_final['Nama_Hotel'] == x]['Kategori_Hotel'].iloc[0])
    
    fig_rating = px.bar(
        avg_rating,
        x='Nama_Hotel',
        y='Rating',
        color='Kategori',
        text_auto='.2f',
        color_discrete_map={'BUMN': EXTENDED_PALETTE['bumn_primary'], 'Non-BUMN': EXTENDED_PALETTE['non_bumn_primary']}
    )
    # FIX: borderRadius -> cornerradius
    fig_rating.update_traces(
        textposition='outside', 
        textfont=dict(size=13, color=EXTENDED_PALETTE['text_primary'], weight='bold'),
        marker=dict(line=dict(color='white', width=2), cornerradius=8) 
    )
    fig_rating.update_layout(
        showlegend=True, 
        yaxis_range=[0, 5.2], 
        height=450,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color=EXTENDED_PALETTE['text_primary']),
        xaxis=dict(tickangle=-30, tickfont=dict(size=11)),
        yaxis=dict(tickfont=dict(size=11)),
        legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='right', x=1),
        margin=dict(t=80, b=100)
    )
    st.plotly_chart(fig_rating, use_container_width=True)
    
    # Distribusi Sentimen per Hotel dengan grouped bar
    st.markdown(f'<div class="section-header">📊 Distribusi Sentimen per Hotel</div>', unsafe_allow_html=True)
    
    sentiment_hotel = df_final.groupby(['Nama_Hotel', 'AI_Sentiment']).size().reset_index(name='Jumlah')
    
    fig_sentiment_hotel = px.bar(
        sentiment_hotel,
        x='Nama_Hotel',
        y='Jumlah',
        color='AI_Sentiment',
        barmode='group',
        color_discrete_map=SENTIMENT_PALETTE,
        text='Jumlah'
    )
    # FIX: borderRadius -> cornerradius
    fig_sentiment_hotel.update_traces(
        textposition='outside', 
        textfont=dict(size=11, color=EXTENDED_PALETTE['text_primary']),
        marker=dict(line=dict(color='white', width=1), cornerradius=4)
    )
    fig_sentiment_hotel.update_layout(
        height=450, 
        xaxis_tickangle=-30,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color=EXTENDED_PALETTE['text_primary']),
        xaxis=dict(tickfont=dict(size=11)),
        yaxis=dict(tickfont=dict(size=11)),
        legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='right', x=1),
        margin=dict(t=80, b=100)
    )
    st.plotly_chart(fig_sentiment_hotel, use_container_width=True)
    
    # Distribusi Rating dengan histogram modern
    st.markdown(f'<div class="section-header">📉 Distribusi Rating</div>', unsafe_allow_html=True)
    
    fig_rating_dist = px.histogram(
        df_final,
        x='Rating',
        color='Kategori_Hotel',
        barmode='overlay',
        nbins=10,
        opacity=0.8,
        color_discrete_map={'BUMN': EXTENDED_PALETTE['bumn_primary'], 'Non-BUMN': EXTENDED_PALETTE['non_bumn_primary']}
    )
    # FIX: borderRadius -> cornerradius
    fig_rating_dist.update_traces(marker=dict(line=dict(color='white', width=1), cornerradius=4))
    fig_rating_dist.update_layout(
        height=400,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color=EXTENDED_PALETTE['text_primary']),
        xaxis=dict(tickfont=dict(size=11), title='Rating'),
        yaxis=dict(tickfont=dict(size=11), title='Frekuensi'),
        legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='right', x=1),
        bargap=0.1
    )
    st.plotly_chart(fig_rating_dist, use_container_width=True)

# ===== TAB 2: PERBANDINGAN BUMN VS NON-BUMN =====
with tab2:
    st.markdown(f'<div class="comparison-header">⚖️ Analisis Komprehensif: BUMN vs Non-BUMN</div>', unsafe_allow_html=True)
    
    df_bumn = df_final[df_final['Kategori_Hotel'] == 'BUMN']
    df_non_bumn = df_final[df_final['Kategori_Hotel'] == 'Non-BUMN']
    
    if len(df_bumn) == 0 or len(df_non_bumn) == 0:
        st.warning("⚠️ Tidak ada cukup data untuk membandingkan BUMN dan Non-BUMN. Silakan pilih hotel dari kedua kategori.")
    else:
        # SECTION 1: STATISTIK UMUM dengan cards yang lebih menarik
        st.markdown(f'<div class="section-header">📋 Statistik Umum Perbandingan</div>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown('<div class="bumn-box">', unsafe_allow_html=True)
            st.markdown("### 🏛️ Hotel BUMN")
            st.markdown("---")
            
            bumn_avg_rating = df_bumn['Rating'].mean()
            bumn_total_reviews = len(df_bumn)
            bumn_pos = len(df_bumn[df_bumn['AI_Sentiment'] == 'positive']) / len(df_bumn) * 100
            bumn_neg = len(df_bumn[df_bumn['AI_Sentiment'] == 'negative']) / len(df_bumn) * 100
            bumn_hotels = df_bumn['Nama_Hotel'].nunique()
            
            metrics_col1, metrics_col2 = st.columns(2)
            with metrics_col1:
                st.metric("⭐ Rating Rata-rata", f"{bumn_avg_rating:.2f}")
                st.metric("💬 Total Ulasan", f"{bumn_total_reviews:,}")
            with metrics_col2:
                st.metric("😊 Sentimen Positif", f"{bumn_pos:.1f}%")
                st.metric("😞 Sentimen Negatif", f"{bumn_neg:.1f}%")
            
            st.metric("🏨 Jumlah Hotel", f"{bumn_hotels}")
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col2:
            st.markdown('<div class="non-bumn-box">', unsafe_allow_html=True)
            st.markdown("### 🏢 Hotel Non-BUMN")
            st.markdown("---")
            
            non_bumn_avg_rating = df_non_bumn['Rating'].mean()
            non_bumn_total_reviews = len(df_non_bumn)
            non_bumn_pos = len(df_non_bumn[df_non_bumn['AI_Sentiment'] == 'positive']) / len(df_non_bumn) * 100
            non_bumn_neg = len(df_non_bumn[df_non_bumn['AI_Sentiment'] == 'negative']) / len(df_non_bumn) * 100
            non_bumn_hotels = df_non_bumn['Nama_Hotel'].nunique()
            
            metrics_col1, metrics_col2 = st.columns(2)
            with metrics_col1:
                st.metric("⭐ Rating Rata-rata", f"{non_bumn_avg_rating:.2f}")
                st.metric("💬 Total Ulasan", f"{non_bumn_total_reviews:,}")
            with metrics_col2:
                st.metric("😊 Sentimen Positif", f"{non_bumn_pos:.1f}%")
                st.metric("😞 Sentimen Negatif", f"{non_bumn_neg:.1f}%")
            
            st.metric("🏨 Jumlah Hotel", f"{non_bumn_hotels}")
            st.markdown('</div>', unsafe_allow_html=True)
        
        # REASONING SECTION
        st.markdown(f'<div class="section-header">🤔 Analisis & Reasoning Perbandingan</div>', unsafe_allow_html=True)
        
        reasoning_col1, reasoning_col2 = st.columns(2)
        
        with reasoning_col1:
            st.markdown("""
            <div class="success-box" style="height: 100%;">
                <h4 style="color: #00B8A3; margin-top: 0;">✅ Kelebihan BUMN</h4>
                <ul style="margin: 0; padding-left: 20px;">
            """, unsafe_allow_html=True)
            
            # Analisis otomatis kelebihan BUMN
            advantages = []
            if bumn_avg_rating > non_bumn_avg_rating:
                advantages.append(f"Rating rata-rata lebih tinggi ({bumn_avg_rating:.2f} vs {non_bumn_avg_rating:.2f})")
            if bumn_pos > non_bumn_pos:
                advantages.append(f"Persentase sentimen positif lebih tinggi ({bumn_pos:.1f}% vs {non_bumn_pos:.1f}%)")
            if bumn_neg < non_bumn_neg:
                advantages.append(f"Persentase sentimen negatif lebih rendah ({bumn_neg:.1f}% vs {non_bumn_neg:.1f}%)")
            
            if advantages:
                for adv in advantages:
                    st.markdown(f"<li>{adv}</li>", unsafe_allow_html=True)
            else:
                st.markdown("<li>Perlu analisis lebih lanjut untuk identifikasi kelebihan spesifik</li>", unsafe_allow_html=True)
            
            st.markdown("""
                </ul>
                <p style="margin-top: 15px; font-size: 0.9rem; color: #636E72;">
                    <b>Insight:</b> Hotel BUMN menunjukkan performa yang kompetitif dalam hal kepuasan pelanggan berdasarkan metrik rating dan sentimen.
                </p>
            </div>
            """, unsafe_allow_html=True)
        
        with reasoning_col2:
            st.markdown("""
            <div class="danger-box" style="height: 100%;">
                <h4 style="color: #EE5A5A; margin-top: 0;">⚠️ Area Pengembangan BUMN</h4>
                <ul style="margin: 0; padding-left: 20px;">
            """, unsafe_allow_html=True)
            
            # Analisis otomatis kekurangan BUMN
            disadvantages = []
            if bumn_avg_rating < non_bumn_avg_rating:
                disadvantages.append(f"Rating rata-rata lebih rendah ({bumn_avg_rating:.2f} vs {non_bumn_avg_rating:.2f})")
            if bumn_pos < non_bumn_pos:
                disadvantages.append(f"Persentase sentimen positif lebih rendah ({bumn_pos:.1f}% vs {non_bumn_pos:.1f}%)")
            if bumn_neg > non_bumn_neg:
                disadvantages.append(f"Persentase sentimen negatif lebih tinggi ({bumn_neg:.1f}% vs {non_bumn_neg:.1f}%)")
            
            if disadvantages:
                for dis in disadvantages:
                    st.markdown(f"<li>{dis}</li>", unsafe_allow_html=True)
            else:
                st.markdown("<li>BUMN kompetitif di semua metrik utama</li>", unsafe_allow_html=True)
            
            st.markdown("""
                </ul>
                <p style="margin-top: 15px; font-size: 0.9rem; color: #636E72;">
                    <b>Rekomendasi:</b> Fokus pada peningkatan aspek-aspek kritis yang tertinggal dari kompetitor untuk meningkatkan daya saing.
                </p>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # SECTION 2: PERBANDINGAN SENTIMEN
        st.markdown(f'<div class="section-header">😊😞😊 Perbandingan Distribusi Sentimen</div>', unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns([1, 1, 1.2])
        
        with col1:
            sentiment_bumn = df_bumn.groupby('AI_Sentiment').size().reset_index(name='Jumlah')
            fig_pie_bumn = px.pie(
                sentiment_bumn,
                values='Jumlah',
                names='AI_Sentiment',
                title='BUMN',
                color='AI_Sentiment',
                color_discrete_map=SENTIMENT_PALETTE,
                hole=0.5
            )
            fig_pie_bumn.update_traces(
                textposition='inside',
                textinfo='percent+label',
                textfont=dict(size=12, color='white', weight='bold')
            )
            fig_pie_bumn.update_layout(
                height=350,
                title_font=dict(size=14, color=EXTENDED_PALETTE['text_primary']),
                paper_bgcolor='rgba(0,0,0,0)',
                showlegend=False,
                margin=dict(t=50, b=20)
            )
            st.plotly_chart(fig_pie_bumn, use_container_width=True)
        
        with col2:
            sentiment_non_bumn = df_non_bumn.groupby('AI_Sentiment').size().reset_index(name='Jumlah')
            fig_pie_non_bumn = px.pie(
                sentiment_non_bumn,
                values='Jumlah',
                names='AI_Sentiment',
                title='Non-BUMN',
                color='AI_Sentiment',
                color_discrete_map=SENTIMENT_PALETTE,
                hole=0.5
            )
            fig_pie_non_bumn.update_traces(
                textposition='inside',
                textinfo='percent+label',
                textfont=dict(size=12, color='white', weight='bold')
            )
            fig_pie_non_bumn.update_layout(
                height=350,
                title_font=dict(size=14, color=EXTENDED_PALETTE['text_primary']),
                paper_bgcolor='rgba(0,0,0,0)',
                showlegend=False,
                margin=dict(t=50, b=20)
            )
            st.plotly_chart(fig_pie_non_bumn, use_container_width=True)
        
        with col3:
            comparison_sentiment = pd.DataFrame({
                'Kategori': ['BUMN', 'BUMN', 'BUMN', 'Non-BUMN', 'Non-BUMN', 'Non-BUMN'],
                'Sentimen': ['Positif', 'Negatif', 'Netral', 'Positif', 'Negatif', 'Netral'],
                'Persentase': [
                    bumn_pos, bumn_neg, 100-bumn_pos-bumn_neg,
                    non_bumn_pos, non_bumn_neg, 100-non_bumn_pos-non_bumn_neg
                ]
            })
            
            color_map_comparison = {
                'Positif': SENTIMENT_PALETTE['positive'],
                'Negatif': SENTIMENT_PALETTE['negative'],
                'Netral': SENTIMENT_PALETTE['neutral']
            }
            
            fig_comp_sent = px.bar(
                comparison_sentiment,
                x='Kategori',
                y='Persentase',
                color='Sentimen',
                barmode='group',
                title='Perbandingan Langsung (%)',
                color_discrete_map=color_map_comparison,
                text_auto='.1f'
            )
            # FIX: borderRadius -> cornerradius
            fig_comp_sent.update_traces(
                textposition='outside', 
                textfont=dict(size=11, weight='bold'),
                marker=dict(line=dict(color='white', width=2), cornerradius=4)
            )
            fig_comp_sent.update_layout(
                height=350,
                title_font=dict(size=14),
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                legend=dict(orientation='h', yanchor='bottom', y=1.02),
                margin=dict(t=80, b=20)
            )
            st.plotly_chart(fig_comp_sent, use_container_width=True)
        
        st.markdown("---")
        
        # SECTION 3: PERBANDINGAN RATING
        st.markdown(f'<div class="section-header">⭐ Analisis Rating Mendalam</div>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            rating_comparison = pd.concat([
                df_bumn[['Rating', 'Kategori_Hotel']],
                df_non_bumn[['Rating', 'Kategori_Hotel']]
            ])
            
            fig_box = px.box(
                rating_comparison,
                x='Kategori_Hotel',
                y='Rating',
                color='Kategori_Hotel',
                title='Distribusi Rating',
                color_discrete_map={
                    'BUMN': EXTENDED_PALETTE['bumn_primary'],
                    'Non-BUMN': EXTENDED_PALETTE['non_bumn_primary']
                },
                points='all'
            )
            fig_box.update_layout(
                showlegend=False,
                height=400,
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                margin=dict(t=50, b=20)
            )
            st.plotly_chart(fig_box, use_container_width=True)
        
        with col2:
            fig_violin = px.violin(
                rating_comparison,
                x='Kategori_Hotel',
                y='Rating',
                color='Kategori_Hotel',
                title='Distribusi Density Rating',
                box=True,
                color_discrete_map={
                    'BUMN': EXTENDED_PALETTE['bumn_primary'],
                    'Non-BUMN': EXTENDED_PALETTE['non_bumn_primary']
                }
            )
            fig_violin.update_layout(
                showlegend=False,
                height=400,
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                margin=dict(t=50, b=20)
            )
            st.plotly_chart(fig_violin, use_container_width=True)
        
        # Histogram Perbandingan
        fig_hist_comp = go.Figure()
        
        fig_hist_comp.add_trace(go.Histogram(
            x=df_bumn['Rating'],
            name='BUMN',
            marker_color=EXTENDED_PALETTE['bumn_primary'],
            opacity=0.7,
            nbinsx=15
        ))
        
        fig_hist_comp.add_trace(go.Histogram(
            x=df_non_bumn['Rating'],
            name='Non-BUMN',
            marker_color=EXTENDED_PALETTE['non_bumn_primary'],
            opacity=0.7,
            nbinsx=15
        ))
        
        fig_hist_comp.update_layout(
            barmode='overlay',
            title='Distribusi Frekuensi Rating',
            xaxis_title='Rating',
            yaxis_title='Frekuensi',
            height=400,
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            legend=dict(orientation='h', yanchor='bottom', y=1.02),
            margin=dict(t=80, b=20)
        )
        st.plotly_chart(fig_hist_comp, use_container_width=True)
        
        st.markdown("---")
        
        # SECTION 4: PERBANDINGAN ASPEK
        st.markdown(f'<div class="section-header">🎯 Perbandingan Skor Aspek</div>', unsafe_allow_html=True)
        
        bumn_aspect_scores = get_category_aspect_scores(df_final, 'BUMN')
        non_bumn_aspect_scores = get_category_aspect_scores(df_final, 'Non-BUMN')
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            fig_radar_comp = go.Figure()
            
            if bumn_aspect_scores and non_bumn_aspect_scores:
                aspects = list(bumn_aspect_scores.keys())
                bumn_values = [bumn_aspect_scores[asp]['score'] for asp in aspects]
                non_bumn_values = [non_bumn_aspect_scores.get(asp, {'score': 0})['score'] for asp in aspects]
                
                aspects_closed = aspects + [aspects[0]]
                bumn_values_closed = bumn_values + [bumn_values[0]]
                non_bumn_values_closed = non_bumn_values + [non_bumn_values[0]]
                
                fig_radar_comp.add_trace(go.Scatterpolar(
                    r=bumn_values_closed,
                    theta=aspects_closed,
                    fill='toself',
                    name='BUMN',
                    line=dict(color=EXTENDED_PALETTE['bumn_primary'], width=3),
                    fillcolor='rgba(108, 92, 231, 0.3)'
                ))
                
                fig_radar_comp.add_trace(go.Scatterpolar(
                    r=non_bumn_values_closed,
                    theta=aspects_closed,
                    fill='toself',
                    name='Non-BUMN',
                    line=dict(color=EXTENDED_PALETTE['non_bumn_primary'], width=3),
                    fillcolor='rgba(255, 107, 107, 0.3)'
                ))
            
            fig_radar_comp.update_layout(
                polar=dict(
                    radialaxis=dict(visible=True, range=[0, 100]),
                    bgcolor='rgba(0,0,0,0)'
                ),
                showlegend=True,
                height=500,
                title="Radar Chart Perbandingan Aspek",
                paper_bgcolor='rgba(0,0,0,0)',
                legend=dict(orientation='h', yanchor='bottom', y=-0.2),
                margin=dict(t=60, b=80)
            )
            st.plotly_chart(fig_radar_comp, use_container_width=True)
        
        with col2:
            st.markdown(f"<h4 style='color: {EXTENDED_PALETTE['text_primary']};'>Tabel Skor Aspek</h4>", unsafe_allow_html=True)
            
            comparison_table = []
            for aspect in bumn_aspect_scores.keys():
                bumn_score = bumn_aspect_scores[aspect]['score']
                non_bumn_score = non_bumn_aspect_scores.get(aspect, {'score': 0})['score']
                diff = bumn_score - non_bumn_score
                
                comparison_table.append({
                    'Aspek': aspect,
                    'BUMN': round(bumn_score, 1),
                    'Non-BUMN': round(non_bumn_score, 1),
                    'Selisih': round(diff, 1)
                })
            
            df_comp_table = pd.DataFrame(comparison_table).sort_values('Selisih', ascending=False)
            
            st.dataframe(
                df_comp_table.style.background_gradient(
                    subset=['BUMN', 'Non-BUMN'],
                    cmap='YlGn',
                    vmin=0,
                    vmax=100
                ).background_gradient(
                    subset=['Selisih'],
                    cmap='RdYlGn',
                    vmin=-20,
                    vmax=20
                ).format({'Selisih': '{:+.1f}'}),
                use_container_width=True,
                height=450
            )
        
        # Bar chart perbandingan aspek
        df_bar_comp = []
        for aspect in bumn_aspect_scores.keys():
            df_bar_comp.append({
                'Aspek': aspect,
                'Kategori': 'BUMN',
                'Skor': bumn_aspect_scores[aspect]['score']
            })
            if aspect in non_bumn_aspect_scores:
                df_bar_comp.append({
                    'Aspek': aspect,
                    'Kategori': 'Non-BUMN',
                    'Skor': non_bumn_aspect_scores[aspect]['score']
                })
        
        df_bar_comp = pd.DataFrame(df_bar_comp)
        
        fig_bar_comp = px.bar(
            df_bar_comp,
            x='Aspek',
            y='Skor',
            color='Kategori',
            barmode='group',
            color_discrete_map={
                'BUMN': EXTENDED_PALETTE['bumn_primary'],
                'Non-BUMN': EXTENDED_PALETTE['non_bumn_primary']
            },
            text_auto='.1f'
        )
        # FIX: borderRadius -> cornerradius
        fig_bar_comp.update_traces(
            textposition='outside',
            marker=dict(line=dict(color='white', width=1), cornerradius=4)
        )
        fig_bar_comp.update_layout(
            height=450,
            xaxis_tickangle=-30,
            title="Perbandingan Skor per Aspek",
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            legend=dict(orientation='h', yanchor='bottom', y=1.02),
            margin=dict(t=80, b=100),
            yaxis=dict(range=[0, 105])
        )
        st.plotly_chart(fig_bar_comp, use_container_width=True)
        
        st.markdown("---")
        
        # SECTION 5: ANALISIS GAP
        st.markdown(f'<div class="section-header">📊 Analisis Gap & Rekomendasi Strategis</div>', unsafe_allow_html=True)
        
        gap_analysis = []
        for aspect in bumn_aspect_scores.keys():
            if aspect in non_bumn_aspect_scores:
                bumn_score = bumn_aspect_scores[aspect]['score']
                non_bumn_score = non_bumn_aspect_scores[aspect]['score']
                gap = non_bumn_score - bumn_score
                
                status = 'Unggul' if gap < -5 else ('Perlu Perbaikan' if gap > 5 else 'Kompetitif')
                
                gap_analysis.append({
                    'Aspek': aspect,
                    'Skor BUMN': round(bumn_score, 1),
                    'Skor Non-BUMN': round(non_bumn_score, 1),
                    'Gap': round(gap, 1),
                    'Status': status
                })
        
        df_gap = pd.DataFrame(gap_analysis).sort_values('Gap', ascending=False)
        
        # Visualisasi Gap
        fig_gap = go.Figure()
        
        colors = []
        for gap in df_gap['Gap']:
            if gap > 5:
                colors.append(EXTENDED_PALETTE['danger'])
            elif gap < -5:
                colors.append(EXTENDED_PALETTE['success'])
            else:
                colors.append(EXTENDED_PALETTE['warning'])
        
        fig_gap.add_trace(go.Bar(
            y=df_gap['Aspek'],
            x=df_gap['Gap'],
            orientation='h',
            marker_color=colors,
            text=[f"{x:+.1f}" for x in df_gap['Gap']],
            textposition='outside',
            textfont=dict(size=11, weight='bold')
        ))
        
        fig_gap.add_vline(x=0, line_dash="dash", line_color="gray")
        
        fig_gap.update_layout(
            title='Gap Analysis: Non-BUMN - BUMN (Positif = Non-BUMN Lebih Baik)',
            xaxis_title='Selisih Skor',
            yaxis_title='Aspek',
            height=450,
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            margin=dict(t=60, b=40),
            showlegend=False
        )
        st.plotly_chart(fig_gap, use_container_width=True)
        
        # Tabel Gap dengan styling
        st.dataframe(
            df_gap.style.applymap(
                lambda x: f'background-color: {EXTENDED_PALETTE["danger"]}; color: white; font-weight: bold' if x == 'Perlu Perbaikan' else 
                          (f'background-color: {EXTENDED_PALETTE["success"]}; color: white; font-weight: bold' if x == 'Unggul' else 
                           f'background-color: {EXTENDED_PALETTE["warning"]}; color: {EXTENDED_PALETTE["dark"]}; font-weight: bold'),
                subset=['Status']
            ).background_gradient(
                subset=['Gap'],
                cmap='RdYlGn_r',
                vmin=-20,
                vmax=20
            ).format({'Gap': '{:+.1f}'}),
            use_container_width=True,
            height=400
        )
        
        # Kesimpulan dan Rekomendasi
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            <div class="success-box">
                <h4 style="color: #00B8A3; margin-top: 0;">🏆 Kekuatan BUMN</h4>
            """, unsafe_allow_html=True)
            
            unggul_aspects = df_gap[df_gap['Status'] == 'Unggul']['Aspek'].tolist()
            if unggul_aspects:
                for asp in unggul_aspects[:5]:
                    score_diff = df_gap[df_gap['Aspek'] == asp]['Gap'].iloc[0]
                    st.markdown(f"<p style='margin: 5px 0;'>✅ <b>{asp}</b>: Unggul {abs(score_diff):.1f} poin</p>", unsafe_allow_html=True)
            else:
                st.markdown("<p>Tidak ada aspek yang unggul signifikan</p>", unsafe_allow_html=True)
            
            st.markdown("</div>", unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div class="danger-box">
                <h4 style="color: #EE5A5A; margin-top: 0;">⚠️ Prioritas Perbaikan</h4>
            """, unsafe_allow_html=True)
            
            perbaikan_aspects = df_gap[df_gap['Status'] == 'Perlu Perbaikan'].sort_values('Gap', ascending=False)
            if not perbaikan_aspects.empty:
                for _, row in perbaikan_aspects.head(5).iterrows():
                    st.markdown(f"<p style='margin: 5px 0;'>🔴 <b>{row['Aspek']}</b>: Gap {row['Gap']:.1f} poin</p>", unsafe_allow_html=True)
            else:
                st.markdown("<p>Tidak ada gap kritis yang memerlukan perbaikan</p>", unsafe_allow_html=True)
            
            st.markdown("</div>", unsafe_allow_html=True)

# ===== TAB 3: ANALISIS ASPEK DETAIL =====
with tab3:
    st.markdown(f'<div class="section-header">🔍 Analisis Detail Aspek per Hotel</div>', unsafe_allow_html=True)
    
    # Radar Chart untuk semua hotel
    fig_radar = go.Figure()
    
    colors_radar = [EXTENDED_PALETTE['bumn_primary'], EXTENDED_PALETTE['non_bumn_primary'], 
                    EXTENDED_PALETTE['secondary'], EXTENDED_PALETTE['accent'], 
                    EXTENDED_PALETTE['info'], EXTENDED_PALETTE['warning']]
    
    for i, hotel in enumerate(selected_hotels):
        scores = get_aspect_scores(df_final, hotel)
        
        if scores:
            aspects = list(scores.keys())
            values = [scores[asp]['score'] for asp in aspects]
            
            aspects_closed = aspects + [aspects[0]]
            values_closed = values + [values[0]]
            
            kategori = df_final[df_final['Nama_Hotel'] == hotel]['Kategori_Hotel'].iloc[0]
            
            fig_radar.add_trace(go.Scatterpolar(
                r=values_closed,
                theta=aspects_closed,
                fill='toself',
                name=f"{hotel} ({kategori})",
                line=dict(color=colors_radar[i % len(colors_radar)], width=2.5),
                fillcolor=f'rgba{tuple(int(colors_radar[i % len(colors_radar)].lstrip("#")[j:j+2], 16) for j in (0, 2, 4)) + (0.25,)}'
            ))
    
    fig_radar.update_layout(
        polar=dict(
            radialaxis=dict(visible=True, range=[0, 100], tickfont=dict(size=10)),
            angularaxis=dict(tickfont=dict(size=11)),
            bgcolor='rgba(0,0,0,0)'
        ),
        showlegend=True,
        height=600,
        title="Perbandingan Skor Aspek Semua Hotel (0-100)",
        paper_bgcolor='rgba(0,0,0,0)',
        legend=dict(orientation='h', yanchor='bottom', y=-0.2, xanchor='center', x=0.5),
        margin=dict(t=60, b=100)
    )
    st.plotly_chart(fig_radar, use_container_width=True)
    
    st.markdown("---")
    
    # Detail per hotel dalam expander
    st.markdown(f'<div class="section-header">📋 Detail Analisis per Hotel</div>', unsafe_allow_html=True)
    
    for hotel in selected_hotels:
        kategori = df_final[df_final['Nama_Hotel'] == hotel]['Kategori_Hotel'].iloc[0]
        border_color = EXTENDED_PALETTE['bumn_primary'] if kategori == 'BUMN' else EXTENDED_PALETTE['non_bumn_primary']
        
        with st.expander(f"🏨 {hotel} ({kategori})", expanded=True):
            scores = get_aspect_scores(df_final, hotel)
            
            if not scores:
                st.warning("Tidak ada data untuk hotel ini.")
                continue
            
            sorted_aspects = sorted(scores.items(), key=lambda x: x[1]['score'], reverse=True)
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown(f"<h4 style='color: {EXTENDED_PALETTE['success']};'>✨ Top 5 Aspek Terbaik</h4>", unsafe_allow_html=True)
                
                for i, (aspek, data) in enumerate(sorted_aspects[:5], 1):
                    score = data['score']
                    color = EXTENDED_PALETTE['success'] if score >= 75 else (EXTENDED_PALETTE['warning'] if score >= 50 else EXTENDED_PALETTE['danger'])
                    
                    st.markdown(f"""
                    <div style="background: linear-gradient(90deg, rgba(0, 217, 192, 0.1) 0%, transparent 100%); 
                                padding: 15px; border-radius: 10px; margin: 10px 0; 
                                border-left: 4px solid {color};">
                        <div style="display: flex; justify-content: space-between; align-items: center;">
                            <span style="font-weight: 600; color: {EXTENDED_PALETTE['text_primary']};">{i}. {aspek}</span>
                            <span style="font-size: 1.3rem; font-weight: 800; color: {color};">{score:.1f}</span>
                        </div>
                        <div style="margin-top: 8px;">
                            <div style="background: #E0E0E0; border-radius: 10px; height: 8px;">
                                <div style="background: linear-gradient(90deg, {color} 0%, {color}80 100%); 
                                            width: {score}%; height: 100%; border-radius: 10px; transition: width 0.5s ease;">
                                </div>
                            </div>
                        </div>
                        <div style="margin-top: 8px; font-size: 0.85rem; color: {EXTENDED_PALETTE['gray']};">
                            👍 {data['positive']} | 😐 {data['neutral']} | 👎 {data['negative']} | Total: {data['total']}
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
            
            with col2:
                st.markdown(f"<h4 style='color: {EXTENDED_PALETTE['danger']};'>⚠️ Top 5 Aspek Perlu Perbaikan</h4>", unsafe_allow_html=True)
                
                for i, (aspek, data) in enumerate(sorted_aspects[-5:][::-1], 1):
                    score = data['score']
                    color = EXTENDED_PALETTE['danger'] if score < 50 else (EXTENDED_PALETTE['warning'] if score < 75 else EXTENDED_PALETTE['success'])
                    
                    st.markdown(f"""
                    <div style="background: linear-gradient(90deg, rgba(255, 107, 107, 0.1) 0%, transparent 100%); 
                                padding: 15px; border-radius: 10px; margin: 10px 0; 
                                border-left: 4px solid {color};">
                        <div style="display: flex; justify-content: space-between; align-items: center;">
                            <span style="font-weight: 600; color: {EXTENDED_PALETTE['text_primary']};">{i}. {aspek}</span>
                            <span style="font-size: 1.3rem; font-weight: 800; color: {color};">{score:.1f}</span>
                        </div>
                        <div style="margin-top: 8px;">
                            <div style="background: #E0E0E0; border-radius: 10px; height: 8px;">
                                <div style="background: linear-gradient(90deg, {color} 0%, {color}80 100%); 
                                            width: {score}%; height: 100%; border-radius: 10px; transition: width 0.5s ease;">
                                </div>
                            </div>
                        </div>
                        <div style="margin-top: 8px; font-size: 0.85rem; color: {EXTENDED_PALETTE['gray']};">
                            👍 {data['positive']} | 😐 {data['neutral']} | 👎 {data['negative']} | Total: {data['total']}
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
            
            # Bar chart untuk semua aspek
            st.markdown(f"<h4 style='color: {EXTENDED_PALETTE['text_primary']}; margin-top: 25px;'>📊 Grafik Skor Semua Aspek</h4>", unsafe_allow_html=True)
            df_scores = pd.DataFrame([
                {'Aspek': aspek, 'Skor': data['score']}
                for aspek, data in scores.items()
            ]).sort_values('Skor', ascending=True)
            
            fig_hotel_scores = px.bar(
                df_scores,
                x='Skor',
                y='Aspek',
                orientation='h',
                color='Skor',
                color_continuous_scale=['#FF6B6B', '#FFE66D', '#00D9C0'],
                range_color=[0, 100],
                text='Skor'
            )
            # FIX: borderRadius -> cornerradius
            fig_hotel_scores.update_traces(
                texttemplate='%{text:.1f}', 
                textposition='outside',
                textfont=dict(size=11, weight='bold'),
                marker=dict(line=dict(color='white', width=1), cornerradius=4)
            )
            fig_hotel_scores.update_layout(
                showlegend=False, 
                height=400,
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                yaxis=dict(tickfont=dict(size=11)),
                coloraxis_showscale=False,
                margin=dict(t=20, b=20, l=20, r=80)
            )
            st.plotly_chart(fig_hotel_scores, use_container_width=True)

# ===== TAB 4: SENTIMEN PER ASPEK =====
with tab4:
    st.markdown(f'<div class="section-header">💭 Analisis Sentimen Berdasarkan Aspek</div>', unsafe_allow_html=True)
    
    # Pilih hotel
    selected_hotel_analysis = st.selectbox(
        "🏨 Pilih hotel untuk analisis detail:",
        selected_hotels,
        key="sentiment_analysis"
    )
    
    df_hotel_analysis = df_final[df_final['Nama_Hotel'] == selected_hotel_analysis]
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(f"<h4 style='text-align: center; color: {EXTENDED_PALETTE['text_primary']};'>Stacked Bar Chart</h4>", unsafe_allow_html=True)
        sentiment_aspect = df_hotel_analysis.groupby(['AI_Aspek', 'AI_Sentiment']).size().reset_index(name='Jumlah')
        
        fig_stacked = px.bar(
            sentiment_aspect,
            x='AI_Aspek',
            y='Jumlah',
            color='AI_Sentiment',
            color_discrete_map=SENTIMENT_PALETTE,
            barmode='stack'
        )
        fig_stacked.update_layout(
            xaxis_tickangle=-30, 
            height=450,
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            legend=dict(orientation='h', yanchor='bottom', y=1.02),
            margin=dict(t=80, b=100)
        )
        st.plotly_chart(fig_stacked, use_container_width=True)
    
    with col2:
        st.markdown(f"<h4 style='text-align: center; color: {EXTENDED_PALETTE['text_primary']};'>Grouped Bar Chart</h4>", unsafe_allow_html=True)
        fig_grouped = px.bar(
            sentiment_aspect,
            x='AI_Aspek',
            y='Jumlah',
            color='AI_Sentiment',
            color_discrete_map=SENTIMENT_PALETTE,
            barmode='group'
        )
        fig_grouped.update_layout(
            xaxis_tickangle=-30, 
            height=450,
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            legend=dict(orientation='h', yanchor='bottom', y=1.02),
            margin=dict(t=80, b=100)
        )
        st.plotly_chart(fig_grouped, use_container_width=True)
    
    st.markdown("---")
    
    # Heatmap
    st.markdown(f'<div class="section-header">🌡️ Heatmap Intensitas Sentimen</div>', unsafe_allow_html=True)
    
    pivot_data = df_hotel_analysis.groupby(['AI_Aspek', 'AI_Sentiment']).size().unstack(fill_value=0)
    
    fig_heatmap = go.Figure(data=go.Heatmap(
        z=pivot_data.values.T,
        x=pivot_data.index,
        y=pivot_data.columns,
        colorscale=[[0, '#FFFFFF'], [0.33, '#FFE66D'], [0.66, '#00D9C0'], [1, '#6C5CE7']],
        text=pivot_data.values.T,
        texttemplate='%{text}',
        textfont={"size": 12}
    ))
    
    fig_heatmap.update_layout(
        height=500,
        paper_bgcolor='rgba(0,0,0,0)',
        xaxis_tickangle=-30,
        margin=dict(t=40, b=100)
    )
    st.plotly_chart(fig_heatmap, use_container_width=True)
    
    # Diverging bar chart
    st.markdown(f'<div class="section-header">⚖️ Diverging Chart: Positif vs Negatif</div>', unsafe_allow_html=True)
    
    comparison_data = []
    for aspek in df_hotel_analysis['AI_Aspek'].unique():
        df_aspek = df_hotel_analysis[df_hotel_analysis['AI_Aspek'] == aspek]
        pos = len(df_aspek[df_aspek['AI_Sentiment'] == 'positive'])
        neg = len(df_aspek[df_aspek['AI_Sentiment'] == 'negative'])
        
        comparison_data.append({
            'Aspek': aspek,
            'Positif': pos,
            'Negatif': -neg,
            'Net': pos - neg
        })
    
    df_comparison = pd.DataFrame(comparison_data).sort_values('Positif', ascending=True)
    
    fig_diverging = go.Figure()
    
    fig_diverging.add_trace(go.Bar(
        y=df_comparison['Aspek'],
        x=df_comparison['Positif'],
        name='Positif',
        orientation='h',
        marker=dict(color=SENTIMENT_PALETTE['positive'], line=dict(color='white', width=1)),
        text=df_comparison['Positif'],
        textposition='outside',
        textfont=dict(size=10)
    ))
    
    fig_diverging.add_trace(go.Bar(
        y=df_comparison['Aspek'],
        x=df_comparison['Negatif'],
        name='Negatif',
        orientation='h',
        marker=dict(color=SENTIMENT_PALETTE['negative'], line=dict(color='white', width=1)),
        text=df_comparison['Negatif'].abs(),
        textposition='outside',
        textfont=dict(size=10)
    ))
    
    fig_diverging.update_layout(
        barmode='relative',
        title=f"Diverging Analysis: {selected_hotel_analysis}",
        xaxis_title="Jumlah Ulasan",
        yaxis_title="Aspek",
        height=500,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        legend=dict(orientation='h', yanchor='bottom', y=1.02),
        margin=dict(t=80, b=40)
    )
    st.plotly_chart(fig_diverging, use_container_width=True)

# ===== TAB 5: PERBANDINGAN HOTEL =====
with tab5:
    st.markdown(f'<div class="section-header">📈 Perbandingan Komprehensif Antar Hotel</div>', unsafe_allow_html=True)
    
    # Tabel perbandingan
    comparison_table = []
    for hotel in selected_hotels:
        df_hotel = df_final[df_final['Nama_Hotel'] == hotel]
        
        avg_rating = df_hotel['Rating'].mean()
        total_reviews = len(df_hotel)
        sentiment_pct = get_sentiment_percentage(df_final, hotel)
        
        scores = get_aspect_scores(df_final, hotel)
        sorted_scores = sorted(scores.items(), key=lambda x: x[1]['score'], reverse=True)
        
        best_aspect = sorted_scores[0][0] if sorted_scores else 'N/A'
        worst_aspect = sorted_scores[-1][0] if sorted_scores else 'N/A'
        avg_aspect_score = np.mean([s[1]['score'] for s in sorted_scores]) if sorted_scores else 0
        
        kelas = df_hotel['Kelas'].iloc[0] if len(df_hotel) > 0 else 'N/A'
        kategori = df_hotel['Kategori_Hotel'].iloc[0] if len(df_hotel) > 0 else 'N/A'
        
        comparison_table.append({
            'Hotel': hotel,
            'Kategori': kategori,
            'Bintang': kelas,
            'Rata-rata Rating': round(avg_rating, 2),
            'Total Ulasan': total_reviews,
            'Sentimen Positif (%)': round(sentiment_pct['positive'], 1),
            'Sentimen Negatif (%)': round(sentiment_pct['negative'], 1),
            'Skor Aspek Rata-rata': round(avg_aspect_score, 1),
            'Aspek Terbaik': best_aspect,
            'Aspek Terburuk': worst_aspect
        })
    
    df_comparison_table = pd.DataFrame(comparison_table)
    
    st.dataframe(
        df_comparison_table.style.background_gradient(
            subset=['Rata-rata Rating', 'Sentimen Positif (%)', 'Skor Aspek Rata-rata'],
            cmap='YlGn'
        ).background_gradient(
            subset=['Sentimen Negatif (%)'],
            cmap='OrRd'
        ).applymap(
            lambda x: f'color: {EXTENDED_PALETTE["bumn_primary"]}; font-weight: bold' if x == 'BUMN' else 
                      f'color: {EXTENDED_PALETTE["non_bumn_primary"]}; font-weight: bold',
            subset=['Kategori']
        ),
        use_container_width=True,
        height=400
    )
    
    st.markdown("---")
    
    # Bubble chart
    st.markdown(f'<div class="section-header">🫧 Bubble Chart: Multi-dimensi Analysis</div>', unsafe_allow_html=True)
    
    fig_bubble = px.scatter(
        df_comparison_table,
        x='Rata-rata Rating',
        y='Sentimen Positif (%)',
        size='Total Ulasan',
        color='Kategori',
        hover_name='Hotel',
        hover_data=['Bintang', 'Total Ulasan', 'Skor Aspek Rata-rata'],
        size_max=70,
        color_discrete_map={
            'BUMN': EXTENDED_PALETTE['bumn_primary'],
            'Non-BUMN': EXTENDED_PALETTE['non_bumn_primary']
        }
    )
    fig_bubble.update_traces(marker=dict(line=dict(color='white', width=2)))
    fig_bubble.update_layout(
        height=500,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        legend=dict(orientation='h', yanchor='bottom', y=1.02),
        margin=dict(t=80, b=40)
    )
    st.plotly_chart(fig_bubble, use_container_width=True)
    
    # Parallel coordinates
    st.markdown(f'<div class="section-header">📊 Parallel Coordinates Analysis</div>', unsafe_allow_html=True)
    
    df_parallel = df_comparison_table.copy()
    df_parallel['Rating_Norm'] = (df_parallel['Rata-rata Rating'] / 5) * 100
    df_parallel['Review_Norm'] = (df_parallel['Total Ulasan'] / df_parallel['Total Ulasan'].max()) * 100
    
    fig_parallel = go.Figure(data=
        go.Parcoords(
            line=dict(
                color=df_parallel['Kategori'].map({'BUMN': 0, 'Non-BUMN': 1}),
                colorscale=[[0, EXTENDED_PALETTE['bumn_primary']], [1, EXTENDED_PALETTE['non_bumn_primary']]],
                showscale=True,
                cmin=0,
                cmax=1
            ),
            dimensions=[
                dict(label='Rating (Norm)', values=df_parallel['Rating_Norm']),
                dict(label='Sentimen Positif %', values=df_parallel['Sentimen Positif (%)']),
                dict(label='Skor Aspek', values=df_parallel['Skor Aspek Rata-rata']),
                dict(label='Ulasan (Norm)', values=df_parallel['Review_Norm'])
            ],
            labelfont=dict(size=12),
            tickfont=dict(size=10)
        )
    )
    fig_parallel.update_layout(
        height=450,
        paper_bgcolor='rgba(0,0,0,0)',
        margin=dict(t=60, b=40)
    )
    st.plotly_chart(fig_parallel, use_container_width=True)

# ===== TAB 6: WORD CLOUD =====
with tab6:
    st.markdown(f'<div class="section-header">☁️ Word Cloud - Analisis Kata Kunci</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 3])
    
    with col1:
        target_hotel = st.selectbox(
            "🏨 Pilih Hotel:",
            selected_hotels,
            key="wordcloud_hotel"
        )
        
        sentiment_filter = st.radio(
            "😊 Filter Sentimen:",
            ["Semua", "Positive", "Negative", "Neutral"],
            key="wordcloud_sentiment"
        )
        
        st.markdown("---")
        
        st.markdown(f"<h4 style='color: {EXTENDED_PALETTE['text_primary']};'>⚙️ Pengaturan</h4>", unsafe_allow_html=True)
        max_words = st.slider("Jumlah Kata", 50, 200, 100)
        colormap = st.selectbox(
            "🎨 Skema Warna",
            ["viridis", "plasma", "inferno", "magma", "cividis", "twilight", "rainbow", "turbo"]
        )
    
    with col2:
        df_wc = df_final[df_final['Nama_Hotel'] == target_hotel]
        
        if sentiment_filter != "Semua":
            df_wc = df_wc[df_wc['AI_Sentiment'] == sentiment_filter.lower()]
        
        text_data = " ".join(review for review in df_wc['clean_text'].astype(str))
        
        if text_data.strip():
            wordcloud = WordCloud(
                width=1400,
                height=700,
                background_color='white',
                colormap=colormap,
                max_words=max_words,
                relative_scaling=0.5,
                min_font_size=10,
                collocation_threshold=3,
                contour_width=1,
                contour_color='steelblue'
            ).generate(text_data)
            
            fig_wc, ax = plt.subplots(figsize=(18, 9))
            ax.imshow(wordcloud, interpolation='bilinear')
            ax.axis('off')
            ax.set_title(
                f"Word Cloud: {target_hotel} ({sentiment_filter})",
                fontsize=20,
                fontweight='bold',
                pad=20,
                color=EXTENDED_PALETTE['text_primary']
            )
            st.pyplot(fig_wc)
            plt.close()
        else:
            st.warning("Tidak ada data teks untuk kombinasi filter ini.")
    
    st.markdown("---")
    
    # Top Keywords
    st.markdown(f'<div class="section-header">🔝 Top Keywords Analysis</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(f"<h4 style='color: {EXTENDED_PALETTE['primary']}; text-align: center;'>Bar Chart Top 20</h4>", unsafe_allow_html=True)
        keywords = get_top_keywords(
            df_final,
            target_hotel,
            sentiment_filter.lower() if sentiment_filter != "Semua" else None,
            top_n=20
        )
        
        if keywords:
            df_keywords = pd.DataFrame(keywords, columns=['Kata', 'Frekuensi'])
            
            fig_keywords = px.bar(
                df_keywords,
                x='Frekuensi',
                y='Kata',
                orientation='h',
                color='Frekuensi',
                color_continuous_scale=['#E8F8F5', '#00D9C0', '#6C5CE7'],
                text='Frekuensi'
            )
            fig_keywords.update_traces(
                textposition='outside',
                textfont=dict(size=11, weight='bold')
            )
            fig_keywords.update_layout(
                height=550,
                showlegend=False,
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                yaxis=dict(categoryorder='total ascending'),
                margin=dict(t=20, b=20, l=20, r=80)
            )
            st.plotly_chart(fig_keywords, use_container_width=True)
        else:
            st.info("Tidak ada data kata kunci.")
    
    with col2:
        st.markdown(f"<h4 style='color: {EXTENDED_PALETTE['secondary']}; text-align: center;'>Treemap Visualization</h4>", unsafe_allow_html=True)
        if keywords:
            df_treemap = pd.DataFrame(keywords, columns=['Kata', 'Frekuensi'])
            
            fig_treemap = px.treemap(
                df_treemap,
                path=['Kata'],
                values='Frekuensi',
                color='Frekuensi',
                color_continuous_scale=['#FCE8E0', '#FFE66D', '#6C5CE7']
            )
            fig_treemap.update_layout(
                height=550,
                paper_bgcolor='rgba(0,0,0,0)',
                margin=dict(t=20, b=20, l=20, r=20)
            )
            fig_treemap.update_traces(textfont=dict(size=14))
            st.plotly_chart(fig_treemap, use_container_width=True)

# ===== TAB 7: HEATMAP & INSIGHTS =====
with tab7:
    st.markdown(f'<div class="section-header">🗺️ Heatmap & Strategic Insights</div>', unsafe_allow_html=True)
    
    # Heatmap skor aspek
    heatmap_data = []
    for hotel in selected_hotels:
        scores = get_aspect_scores(df_final, hotel)
        row = {'Hotel': hotel}
        for aspect, data in scores.items():
            row[aspect] = data['score']
        heatmap_data.append(row)
    
    df_heatmap = pd.DataFrame(heatmap_data)
    
    if len(df_heatmap.columns) > 1:
        fig_heatmap = px.imshow(
            df_heatmap.set_index('Hotel'),
            aspect='auto',
            color_continuous_scale=['#FF6B6B', '#FFE66D', '#00D9C0', '#6C5CE7'],
            text_auto='.1f'
        )
        fig_heatmap.update_layout(
            height=500,
            paper_bgcolor='rgba(0,0,0,0)',
            margin=dict(t=40, b=100)
        )
        st.plotly_chart(fig_heatmap, use_container_width=True)
    else:
        st.warning("Tidak ada data untuk skor aspek.")
    
    st.markdown("---")
    
    # Strategic Insights
    st.markdown(f'<div class="section-header">💡 Strategic Insights & Rekomendasi</div>', unsafe_allow_html=True)
    
    bumn_hotels = df_final[df_final['Kategori_Hotel'] == 'BUMN']
    non_bumn_hotels = df_final[df_final['Kategori_Hotel'] == 'Non-BUMN']
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(f"""
        <div class="success-box" style="height: 100%;">
            <h4 style="color: {EXTENDED_PALETTE['success']}; margin-top: 0;">🏆 Kekuatan Utama</h4>
        """, unsafe_allow_html=True)
        
        if len(bumn_hotels) > 0 and len(non_bumn_hotels) > 0:
            bumn_rating = bumn_hotels['Rating'].mean()
            non_bumn_rating = non_bumn_hotels['Rating'].mean()
            
            if bumn_rating > non_bumn_rating:
                st.markdown(f"<p>✅ <b>Rating BUMN</b> lebih tinggi ({bumn_rating:.2f} vs {non_bumn_rating:.2f})</p>", unsafe_allow_html=True)
            else:
                st.markdown(f"<p>✅ <b>Rating Non-BUMN</b> lebih tinggi ({non_bumn_rating:.2f} vs {bumn_rating:.2f})</p>", unsafe_allow_html=True)
            
            all_scores = {}
            for hotel in selected_hotels:
                scores = get_aspect_scores(df_final, hotel)
                for aspect, data in scores.items():
                    if aspect not in all_scores:
                        all_scores[aspect] = []
                    all_scores[aspect].append(data['score'])
            
            if all_scores:
                avg_scores = {k: np.mean(v) for k, v in all_scores.items()}
                best_aspect = max(avg_scores, key=avg_scores.get)
                st.markdown(f"<p>✅ <b>Aspek terkuat</b>: {best_aspect} ({avg_scores[best_aspect]:.1f}/100)</p>", unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="danger-box" style="height: 100%;">
            <h4 style="color: {EXTENDED_PALETTE['danger']}; margin-top: 0;">⚠️ Area Perbaikan</h4>
        """, unsafe_allow_html=True)
        
        if len(bumn_hotels) > 0:
            bumn_neg = len(bumn_hotels[bumn_hotels['AI_Sentiment'] == 'negative']) / len(bumn_hotels) * 100
            st.markdown(f"<p>🔴 <b>Sentimen negatif BUMN</b>: {bumn_neg:.1f}%</p>", unsafe_allow_html=True)
            
            bumn_scores = get_category_aspect_scores(df_final, 'BUMN')
            if bumn_scores:
                weakest = min(bumn_scores.items(), key=lambda x: x[1]['score'])
                st.markdown(f"<p>🔴 <b>Perlu perbaikan</b>: {weakest[0]} ({weakest[1]['score']:.1f}/100)</p>", unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="info-box" style="height: 100%;">
            <h4 style="color: {EXTENDED_PALETTE['info']}; margin-top: 0;">💡 Rekomendasi Strategis</h4>
        """, unsafe_allow_html=True)
        
        if len(bumn_hotels) > 0 and len(non_bumn_hotels) > 0:
            bumn_pos = len(bumn_hotels[bumn_hotels['AI_Sentiment'] == 'positive']) / len(bumn_hotels) * 100
            non_bumn_pos = len(non_bumn_hotels[non_bumn_hotels['AI_Sentiment'] == 'positive']) / len(non_bumn_hotels) * 100
            
            if bumn_pos < non_bumn_pos:
                st.markdown(f"<p>💡 Tingkatkan sentimen positif (gap: {non_bumn_pos - bumn_pos:.1f}%)</p>", unsafe_allow_html=True)
            
            st.markdown("<p>💡 Fokus pada aspek dengan skor < 60</p>", unsafe_allow_html=True)
            st.markdown("<p>💡 Benchmark terhadap kompetitor unggul</p>", unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Trend Analysis
    st.markdown(f'<div class="section-header">📈 Analisis Tren Temporal</div>', unsafe_allow_html=True)
    
    if 'Review Time' in df_final.columns and df_final['Review Time'].notna().sum() > 0:
        df_time = df_final.copy()
        df_time['Review Time'] = pd.to_datetime(df_time['Review Time'], unit='s', errors='coerce')
        df_time = df_time.dropna(subset=['Review Time'])
        
        if len(df_time) > 0:
            df_time['Year-Month'] = df_time['Review Time'].dt.to_period('M').astype(str)
            
            trend_data = df_time.groupby(['Year-Month', 'Nama_Hotel']).agg({
                'Rating': 'mean',
                'AI_Sentiment': lambda x: (x == 'positive').mean() * 100
            }).reset_index()
            
            fig_trend = px.line(
                trend_data,
                x='Year-Month',
                y='Rating',
                color='Nama_Hotel',
                markers=True,
                title='Tren Rating per Waktu',
                color_discrete_sequence=[EXTENDED_PALETTE['bumn_primary'], EXTENDED_PALETTE['non_bumn_primary'], 
                                        EXTENDED_PALETTE['secondary'], EXTENDED_PALETTE['accent'], 
                                        EXTENDED_PALETTE['info'], EXTENDED_PALETTE['warning']]
            )
            fig_trend.update_layout(
                height=400,
                xaxis_tickangle=-45,
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                legend=dict(orientation='h', yanchor='bottom', y=1.02),
                margin=dict(t=80, b=100)
            )
            st.plotly_chart(fig_trend, use_container_width=True)
            
            fig_trend_sent = px.line(
                trend_data,
                x='Year-Month',
                y='AI_Sentiment',
                color='Nama_Hotel',
                markers=True,
                title='Tren Sentimen Positif (%) per Waktu',
                color_discrete_sequence=[EXTENDED_PALETTE['bumn_primary'], EXTENDED_PALETTE['non_bumn_primary'], 
                                        EXTENDED_PALETTE['secondary'], EXTENDED_PALETTE['accent'], 
                                        EXTENDED_PALETTE['info'], EXTENDED_PALETTE['warning']]
            )
            fig_trend_sent.update_layout(
                height=400,
                xaxis_tickangle=-45,
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                legend=dict(orientation='h', yanchor='bottom', y=1.02),
                margin=dict(t=80, b=100)
            )
            st.plotly_chart(fig_trend_sent, use_container_width=True)
        else:
            st.info("Data temporal tidak tersedia untuk analisis tren.")
    else:
        st.info("Kolom waktu tidak tersedia dalam dataset.")

# ===== TAB 8: DATA MENTAH =====
with tab8:
    st.markdown(f'<div class="section-header">📋 Data Mentah & Export</div>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        search_term = st.text_input("🔍 Cari dalam ulasan:", "")
    
    with col2:
        if 'AI_Sentiment' in df_final.columns:
            sentiment_filter_data = st.multiselect(
                "😊 Filter Sentimen:",
                options=df_final['AI_Sentiment'].unique(),
                default=df_final['AI_Sentiment'].unique()
            )
        else:
            sentiment_filter_data = []
    
    with col3:
        rows_per_page = st.selectbox("Baris per halaman:", [10, 25, 50, 100], index=1)
    
    df_display = df_final.copy()
    
    if search_term:
        mask = df_display.astype(str).apply(lambda x: x.str.contains(search_term, case=False, na=False))
        df_display = df_display[mask.any(axis=1)]
    
    if sentiment_filter_data:
        df_display = df_display[df_display['AI_Sentiment'].isin(sentiment_filter_data)]
    
    st.markdown(f"<p style='color: {EXTENDED_PALETTE['text_primary']}; font-size: 1.1rem;'><b>Menampilkan {len(df_display):,} dari {len(df_final):,} baris data</b></p>", unsafe_allow_html=True)
    
    st.dataframe(
        df_display,
        use_container_width=True,
        height=600,
        column_config={
            "Rating": st.column_config.NumberColumn(
                "⭐ Rating",
                help="Rating 1-5",
                format="%.1f"
            ),
            "AI_Sentiment": st.column_config.SelectboxColumn(
                "😊 Sentimen",
                help="Klasifikasi sentimen AI",
                options=["positive", "negative", "neutral"]
            ),
            "Kategori_Hotel": st.column_config.SelectboxColumn(
                "🏨 Kategori",
                options=["BUMN", "Non-BUMN"]
            ),
            "clean_text": st.column_config.TextColumn(
                "📝 Ulasan",
                help="Teks ulasan yang telah dibersihkan",
                width="large"
            )
        }
    )
    
    st.markdown("---")
    
    # Export options
    st.markdown(f'<div class="section-header">💾 Export Data</div>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        csv = df_display.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Download CSV",
            data=csv,
            file_name=f"hotel_analysis_{pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv",
            use_container_width=True
        )
    
    with col2:
        buffer = io.BytesIO()
        with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
            df_display.to_excel(writer, sheet_name='Data Ulasan', index=False)
            
            summary_data = []
            for hotel in selected_hotels:
                df_h = df_display[df_display['Nama_Hotel'] == hotel]
                if len(df_h) > 0:
                    summary_data.append({
                        'Hotel': hotel,
                        'Kategori': df_h['Kategori_Hotel'].iloc[0],
                        'Total Ulasan': len(df_h),
                        'Avg Rating': df_h['Rating'].mean(),
                        'Positive %': (df_h['AI_Sentiment'] == 'positive').mean() * 100,
                        'Negative %': (df_h['AI_Sentiment'] == 'negative').mean() * 100
                    })
            
            if summary_data:
                pd.DataFrame(summary_data).to_excel(writer, sheet_name='Ringkasan', index=False)
        
        st.download_button(
            label="📥 Download Excel",
            data=buffer.getvalue(),
            file_name=f"hotel_analysis_{pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            use_container_width=True
        )
    
    with col3:
        json_str = df_display.to_json(orient='records', indent=2)
        st.download_button(
            label="📥 Download JSON",
            data=json_str,
            file_name=f"hotel_analysis_{pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')}.json",
            mime="application/json",
            use_container_width=True
        )
    
    st.markdown("---")
    
    # Statistik deskriptif
    st.markdown(f'<div class="section-header">📊 Statistik Deskriptif</div>', unsafe_allow_html=True)
    
    numeric_cols = df_display.select_dtypes(include=[np.number]).columns
    if len(numeric_cols) > 0:
        st.dataframe(
            df_display[numeric_cols].describe(),
            use_container_width=True
        )

# --- FOOTER ---
st.markdown(f"""
<div class="footer">
    <h4>🏨 Dashboard Analisis Ulasan Hotel - Advanced Analytics</h4>
    <p><b>Tim Pengembang:</b> Bagus Muhammad Razzan Wahyudi, Raihan Ade Alfattah, Maulana Naufal Habibie</p>
    <p>© 2024 - Powered by Streamlit & Plotly | Modern Analytics Dashboard</p>
    <p style="font-size: 0.9rem; margin-top: 15px; opacity: 0.8;">
        Data diolah menggunakan NLP dan Sentiment Analysis untuk memberikan insight mendalam 
        mengenai performa layanan hotel BUMN vs Non-BUMN
    </p>
</div>
""", unsafe_allow_html=True)

# Sidebar info tambahan
st.sidebar.markdown("---")
st.sidebar.markdown("### ℹ️ Tentang Dashboard")
st.sidebar.info("""
Dashboard ini menganalisis ulasan hotel menggunakan:
- **🧠 Sentiment Analysis**: Klasifikasi positif, negatif, netral
- **🎯 Aspect-Based Analysis**: Analisis per aspek layanan
- **⚖️ Comparative Analysis**: Perbandingan BUMN vs Non-BUMN

**Versi:** 3.0 Modern UI
""")

st.sidebar.markdown("---")
st.sidebar.markdown("### 🚀 Navigasi Cepat")
if st.sidebar.button("⬆️ Kembali ke Atas", use_container_width=True):
    st.rerun()