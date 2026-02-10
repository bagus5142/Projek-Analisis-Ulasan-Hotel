"""
Configuration module for Hotel Review Analysis Dashboard
Centralizes all configuration settings, color palettes, and constants
"""

import os
import json
from pathlib import Path

# ===== PATHS =====
BASE_DIR = Path(__file__).parent.parent
DATA_DIR = BASE_DIR / "src"
CONFIG_DIR = BASE_DIR / "config"
RESULTS_DIR = BASE_DIR / "Results"

# Default data file
DEFAULT_DATA_FILE = DATA_DIR / "Analisis_Master_Lengkap.csv"

# ===== COLOR PALETTES =====
SENTIMENT_PALETTE = {
    "positive": "#00D9C0",  # Turquoise bright
    "negative": "#FF6B6B",  # Coral red
    "neutral": "#FFE66D"    # Sunny yellow
}

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

# ===== APPLICATION SETTINGS =====
APP_CONFIG = {
    "title": "Dashboard Analisis Hotel - Advanced",
    "layout": "wide",
    "initial_sidebar_state": "expanded",
    "page_icon": "🏨"
}

# ===== DATA SETTINGS =====
DATA_CONFIG = {
    "required_columns": [
        "Nama_Hotel",
        "Kelas",
        "Rating",
        "AI_Sentiment",
        "AI_Aspek",
        "clean_text"
    ],
    "optional_columns": [
        "Review_Time",
        "Kategori_Hotel",
        "Reviewer_Name"
    ],
    "rating_range": (1, 5),
    "valid_sentiments": ["positive", "negative", "neutral"],
    "cache_ttl": 3600  # 1 hour
}

# ===== ANALYSIS SETTINGS =====
ANALYSIS_CONFIG = {
    "aspect_scoring": {
        "sentiment_weights": {
            "positive": 1.0,
            "neutral": 0.5,
            "negative": 0.0
        },
        "rating_weight_factor": 0.4,  # 40% weight for rating correlation
        "recency_half_life_days": 180,  # Exponential decay half-life
        "min_confidence_reviews": 50  # Reviews needed for 100% confidence
    },
    "wordcloud": {
        "min_word_length": 3,
        "max_words": 100,
        "background_color": "white",
        "width": 800,
        "height": 400
    },
    "pagination": {
        "default_page_size": 1000,
        "max_page_size": 5000
    }
}

# ===== VISUALIZATION SETTINGS =====
VIZ_CONFIG = {
    "chart_height": 500,
    "chart_width": None,  # Auto
    "font_family": "Arial, sans-serif",
    "animation_duration": 500,
    "template": "plotly_white"
}

# ===== HOTEL CATEGORIZATION =====
def load_hotel_categories():
    """Load hotel categorization rules from config file"""
    config_file = CONFIG_DIR / "hotel_categories.json"
    
    if config_file.exists():
        with open(config_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    else:
        # Fallback to default configuration
        return {
            "bumn_hotels": {
                "exact_matches": [],
                "partial_matches": ["patra", "garuda", "aerowisata"],
                "excluded_keywords": []
            },
            "non_bumn_competitors": [],
            "categorization_rules": {
                "priority": "exact_match",
                "case_sensitive": False,
                "fallback_to_partial": True,
                "confidence_threshold": 0.8
            }
        }

HOTEL_CATEGORIES = load_hotel_categories()

# ===== LOGGING SETTINGS =====
LOGGING_CONFIG = {
    "level": "INFO",
    "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    "log_dir": BASE_DIR / "logs",
    "max_bytes": 10 * 1024 * 1024,  # 10 MB
    "backup_count": 5
}

# ===== EXPORT SETTINGS =====
EXPORT_CONFIG = {
    "formats": ["csv", "excel", "json"],
    "max_export_rows": 100000,
    "excel_engine": "openpyxl"
}

# ===== INDONESIAN STOPWORDS =====
INDONESIAN_STOPWORDS = [
    "yang", "untuk", "pada", "ke", "para", "namun", "menurut", "antara", "dia",
    "dua", "ia", "seperti", "jika", "jika", "sehingga", "kembali", "dan", "tidak",
    "ini", "karena", "oleh", "pada", "dengan", "dari", "di", "adalah", "akan",
    "ada", "atau", "sudah", "saya", "telah", "dalam", "bisa", "bahwa", "mereka",
    "itu", "kita", "juga", "tersebut", "saat", "sebagai", "hanya", "kami", "sangat",
    "hotel", "kamar", "pelayanan", "staff", "tempat"
]

# ===== ASPECT CATEGORIES =====
ASPECT_CATEGORIES = {
    "cleanliness": {
        "label": "Kebersihan",
        "keywords": ["bersih", "rapi", "kotor", "higienis"],
        "icon": "🧹"
    },
    "service": {
        "label": "Pelayanan",
        "keywords": ["pelayanan", "staff", "ramah", "helpful"],
        "icon": "🤝"
    },
    "facilities": {
        "label": "Fasilitas",
        "keywords": ["fasilitas", "kolam", "gym", "wifi"],
        "icon": "🏊"
    },
    "food": {
        "label": "Makanan",
        "keywords": ["makanan", "breakfast", "restaurant", "masakan"],
        "icon": "🍽️"
    },
    "location": {
        "label": "Lokasi",
        "keywords": ["lokasi", "strategis", "dekat", "akses"],
        "icon": "📍"
    },
    "comfort": {
        "label": "Kenyamanan",
        "keywords": ["nyaman", "tenang", "sejuk", "cozy"],
        "icon": "😌"
    },
    "value": {
        "label": "Value for Money",
        "keywords": ["harga", "value", "worth", "mahal"],
        "icon": "💰"
    }
}

# ===== HELPER FUNCTIONS =====
def get_sentiment_color(sentiment: str) -> str:
    """Get color for a given sentiment"""
    return SENTIMENT_PALETTE.get(sentiment.lower(), EXTENDED_PALETTE["gray"])

def get_palette_color(key: str) -> str:
    """Get color from extended palette"""
    return EXTENDED_PALETTE.get(key, EXTENDED_PALETTE["gray"])

def validate_config():
    """Validate configuration settings"""
    errors = []
    
    # Check if data directory exists
    if not DATA_DIR.exists():
        errors.append(f"Data directory not found: {DATA_DIR}")
    
    # Check if default data file exists
    if not DEFAULT_DATA_FILE.exists():
        errors.append(f"Default data file not found: {DEFAULT_DATA_FILE}")
    
    # Validate rating range
    if DATA_CONFIG["rating_range"][0] >= DATA_CONFIG["rating_range"][1]:
        errors.append("Invalid rating range in DATA_CONFIG")
    
    # Create logs directory if it doesn't exist
    LOGGING_CONFIG["log_dir"].mkdir(parents=True, exist_ok=True)
    
    # Create results directory if it doesn't exist
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    
    return errors

# Run validation on import
_validation_errors = validate_config()
if _validation_errors:
    import warnings
    for error in _validation_errors:
        warnings.warn(f"Configuration warning: {error}")
