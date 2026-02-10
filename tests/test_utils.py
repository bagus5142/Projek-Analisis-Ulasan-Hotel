"""
Unit tests for utility functions in the Hotel Review Analysis Dashboard

Run with: pytest tests/test_utils.py -v
"""

import pytest
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from utils import (
    categorize_hotel,
    validate_dataframe,
    calculate_aspect_score_simple,
    calculate_aspect_score_advanced,
    clean_text_for_wordcloud,
    format_number,
    get_date_range
)


# ===== Test Data Fixtures =====

@pytest.fixture
def sample_dataframe():
    """Create a sample dataframe for testing"""
    return pd.DataFrame({
        'Nama_Hotel': ['Hotel A', 'Hotel B', 'Hotel C'],
        'Kelas': [5, 4, 3],
        'Rating': [4.5, 3.8, 4.2],
        'AI_Sentiment': ['positive', 'neutral', 'negative'],
        'AI_Aspek': ['cleanliness', 'service', 'cleanliness'],
        'clean_text': ['great hotel', 'okay stay', 'dirty room'],
        'Review_Time': [
            '2024-01-01',
            '2024-01-15',
            '2024-02-01'
        ]
    })


@pytest.fixture
def hotel_config():
    """Sample hotel categorization config"""
    return {
        "bumn_hotels": {
            "exact_matches": ["Hotel Patra Jasa"],
            "partial_matches": ["patra", "garuda"],
            "excluded_keywords": ["patra street"]
        },
        "non_bumn_competitors": ["Marriott", "Hilton"],
        "categorization_rules": {
            "priority": "exact_match",
            "case_sensitive": False,
            "fallback_to_partial": True
        }
    }


# ===== Hotel Categorization Tests =====

def test_categorize_hotel_exact_match(hotel_config):
    """Test exact match categorization"""
    category, confidence = categorize_hotel("Hotel Patra Jasa", hotel_config)
    assert category == "BUMN"
    assert confidence == 1.0


def test_categorize_hotel_partial_match(hotel_config):
    """Test partial match categorization"""
    category, confidence = categorize_hotel("Patra Comfort Hotel", hotel_config)
    assert category == "BUMN"
    assert 0.2 <= confidence < 1.0  # Confidence depends on keyword length ratio


def test_categorize_hotel_unknown(hotel_config):
    """Test unknown hotel categorization"""
    category, confidence = categorize_hotel("Random Hotel XYZ", hotel_config)
    assert category in ["BUMN", "Non-BUMN"]
    assert 0 <= confidence <= 1.0


# ===== DataFrame Validation Tests =====

def test_validate_dataframe_valid(sample_dataframe):
    """Test validation of valid dataframe"""
    is_valid, errors = validate_dataframe(sample_dataframe)
    assert is_valid
    assert len(errors) == 0


def test_validate_dataframe_missing_columns():
    """Test validation with missing columns"""
    df = pd.DataFrame({'Nama_Hotel': ['Hotel A']})
    is_valid, errors = validate_dataframe(df)
    assert not is_valid
    assert len(errors) > 0


def test_validate_dataframe_empty():
    """Test validation with empty dataframe"""
    df = pd.DataFrame()
    is_valid, errors = validate_dataframe(df)
    assert not is_valid


# ===== Aspect Scoring Tests =====

def test_calculate_aspect_score_simple():
    """Test simple aspect score calculation"""
    df = pd.DataFrame({
        'AI_Aspek': ['cleanliness'] * 10,
        'AI_Sentiment': ['positive'] * 7 + ['neutral'] * 2 + ['negative'] * 1
    })
    
    score = calculate_aspect_score_simple(df, 'cleanliness')
    assert score == 80.0


def test_calculate_aspect_score_simple_no_data():
    """Test aspect score with no matching data"""
    df = pd.DataFrame({
        'AI_Aspek': ['service'],
        'AI_Sentiment': ['positive']
    })
    
    score = calculate_aspect_score_simple(df, 'cleanliness')
    assert score == 0


# ===== Text Cleaning Tests =====

def test_clean_text_for_wordcloud_basic():
    """Test basic text cleaning"""
    text = "This hotel is very clean and comfortable!"
    cleaned = clean_text_for_wordcloud(text, min_length=3)
    
    assert 'hotel' in cleaned
    assert 'clean' in cleaned
    assert cleaned == cleaned.lower()


def test_clean_text_for_wordcloud_empty():
    """Test empty text handling"""
    assert clean_text_for_wordcloud("") == ""
    assert clean_text_for_wordcloud(None) == ""


# ===== Number Formatting Tests =====

def test_format_number_basic():
    """Test basic number formatting"""
    assert format_number(123.456, 2) == "123.46"


def test_format_number_thousands():
    """Test thousands formatting"""
    result = format_number(12345.67, 2)
    assert 'K' in result


def test_format_number_nan():
    """Test NaN handling"""
    assert format_number(np.nan) == "N/A"


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
