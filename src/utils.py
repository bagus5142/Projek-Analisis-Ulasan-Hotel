"""
Utility functions for Hotel Review Analysis Dashboard
Contains helper functions for hotel categorization, data validation, and common operations
"""

import json
import logging
from pathlib import Path
from typing import Dict, List, Optional, Tuple

import pandas as pd
import numpy as np

# Setup logger
logger = logging.getLogger(__name__)


def categorize_hotel(hotel_name: str, config: Dict = None) -> Tuple[str, float]:
    """
    Categorize hotel as BUMN or Non-BUMN with confidence score
    
    Args:
        hotel_name: Name of the hotel
        config: Configuration dict with categorization rules
    
    Returns:
        Tuple of (category, confidence) where:
        - category is 'BUMN', 'Non-BUMN', or 'Unknown'
        - confidence is a float between 0 and 1
    """
    if config is None:
        # Load default config
        try:
            config_file = Path(__file__).parent.parent / "config" / "hotel_categories.json"
            with open(config_file, 'r', encoding='utf-8') as f:
                config = json.load(f)
        except Exception as e:
            logger.warning(f"Could not load hotel categories config: {e}")
            # Fallback to basic categorization
            bumn_keywords = ['patra', 'garuda', 'aerowisata', 'indonesia tourism', 'mandarin oriental']
            hotel_lower = hotel_name.lower()
            for keyword in bumn_keywords:
                if keyword in hotel_lower:
                    return "BUMN", 0.7
            return "Non-BUMN", 0.5
    
    hotel_lower = hotel_name.lower() if not config.get('categorization_rules', {}).get('case_sensitive', False) else hotel_name
    
    # Check excluded keywords first
    excluded = config.get('bumn_hotels', {}).get('excluded_keywords', [])
    for keyword in excluded:
        if keyword.lower() in hotel_lower:
            return "Non-BUMN", 0.9
    
    # Priority 1: Exact match
    exact_matches = config.get('bumn_hotels', {}).get('exact_matches', [])
    for match in exact_matches:
        match_lower = match.lower() if not config.get('categorization_rules', {}).get('case_sensitive', False) else match
        if match_lower == hotel_lower:
            return "BUMN", 1.0
    
    # Priority 2: Partial match
    if config.get('categorization_rules', {}).get('fallback_to_partial', True):
        partial_matches = config.get('bumn_hotels', {}).get('partial_matches', [])
        for keyword in partial_matches:
            keyword_lower = keyword.lower()
            if keyword_lower in hotel_lower:
                # Calculate confidence based on match ratio
                confidence = min(len(keyword_lower) / len(hotel_lower), 0.9)
                return "BUMN", confidence
    
    # Check if it's a known competitor
    competitors = config.get('non_bumn_competitors', [])
    for competitor in competitors:
        competitor_lower = competitor.lower()
        if competitor_lower in hotel_lower:
            return "Non-BUMN", 0.9
    
    # Default: Non-BUMN with low confidence
    return "Non-BUMN", 0.3


def validate_dataframe(df: pd.DataFrame, required_cols: List[str] = None) -> Tuple[bool, List[str]]:
    """
    Validate dataframe has required columns and valid data
    
    Args:
        df: DataFrame to validate
        required_cols: List of required column names
    
    Returns:
        Tuple of (is_valid, error_messages)
    """
    errors = []
    
    if df is None or df.empty:
        errors.append("DataFrame is None or empty")
        return False, errors
    
    # Default required columns
    if required_cols is None:
        required_cols = ["Nama_Hotel", "Kelas", "Rating", "AI_Sentiment", "AI_Aspek", "clean_text"]
    
    # Check required columns exist
    missing_cols = set(required_cols) - set(df.columns)
    if missing_cols:
        errors.append(f"Missing required columns: {missing_cols}")
    
    # Validate data types and ranges
    if 'Rating' in df.columns:
        invalid_ratings = ~df['Rating'].between(1, 5)
        if invalid_ratings.any():
            count = invalid_ratings.sum()
            errors.append(f"{count} rows have invalid ratings (not between 1-5)")
    
    if 'AI_Sentiment' in df.columns:
        valid_sentiments = {'positive', 'negative', 'neutral'}
        invalid_sentiments = ~df['AI_Sentiment'].isin(valid_sentiments)
        if invalid_sentiments.any():
            count = invalid_sentiments.sum()
            unique_invalid = df.loc[invalid_sentiments, 'AI_Sentiment'].unique()
            errors.append(f"{count} rows have invalid sentiments: {unique_invalid}")
    
    if 'Kelas' in df.columns:
        valid_classes = {3, 4, 5, '3', '4', '5'}
        invalid_classes = ~df['Kelas'].isin(valid_classes)
        if invalid_classes.any():
            count = invalid_classes.sum()
            errors.append(f"{count} rows have invalid hotel class (not 3, 4, or 5)")
    
    is_valid = len(errors) == 0
    return is_valid, errors


def calculate_aspect_score_simple(df: pd.DataFrame, aspek: str) -> float:
    """
    Calculate simple aspect score (original algorithm)
    
    Args:
        df: DataFrame with sentiment data
        aspek: Aspect to calculate score for
    
    Returns:
        Score between 0-100
    """
    filtered = df[df['AI_Aspek'] == aspek]
    
    if len(filtered) == 0:
        return 0
    
    sentiment_counts = filtered['AI_Sentiment'].value_counts()
    positive = sentiment_counts.get('positive', 0)
    neutral = sentiment_counts.get('neutral', 0)
    total = len(filtered)
    
    score = ((positive * 1.0 + neutral * 0.5) / total) * 100
    return round(score, 2)


def calculate_aspect_score_advanced(
    df: pd.DataFrame, 
    aspek: str, 
    recency_weight: bool = True,
    rating_weight: bool = True,
    recency_half_life_days: int = 180
) -> Dict:
    """
    Calculate aspect score with context-aware weighting
    
    Args:
        df: DataFrame with review data
        aspek: Aspect to score
        recency_weight: Apply time decay (recent reviews weighted higher)
        rating_weight: Weight by star rating correlation
        recency_half_life_days: Half-life for exponential decay
    
    Returns:
        Dict with score, confidence, total_reviews, and breakdown
    """
    filtered = df[df['AI_Aspek'] == aspek].copy()
    
    if len(filtered) == 0:
        return {
            'score': None,
            'confidence': 0,
            'total_reviews': 0,
            'breakdown': {'positive': 0, 'neutral': 0, 'negative': 0},
            'message': 'No reviews for this aspect'
        }
    
    # Base sentiment scoring
    sentiment_map = {'positive': 1.0, 'neutral': 0.5, 'negative': 0.0}
    filtered['sentiment_score'] = filtered['AI_Sentiment'].map(sentiment_map).fillna(0.5)
    
    # Apply rating weight (correlation with star rating)
    if rating_weight and 'Rating' in filtered.columns:
        # Normalize rating to 0-1 scale
        filtered['rating_norm'] = (filtered['Rating'] - 1) / 4
        # Weighted average: 60% sentiment, 40% rating
        filtered['weighted_score'] = (
            filtered['sentiment_score'] * 0.6 +
            filtered['rating_norm'] * 0.4
        )
    else:
        filtered['weighted_score'] = filtered['sentiment_score']
    
    # Apply recency weight (exponential decay)
    if recency_weight and 'Review_Time' in filtered.columns:
        try:
            filtered['Review_Time'] = pd.to_datetime(filtered['Review_Time'], errors='coerce')
            max_date = filtered['Review_Time'].max()
            
            if pd.notna(max_date):
                filtered['days_old'] = (max_date - filtered['Review_Time']).dt.days
                filtered['days_old'] = filtered['days_old'].fillna(0)
                # Exponential decay with specified half-life
                filtered['time_weight'] = np.exp(-filtered['days_old'] / recency_half_life_days)
            else:
                filtered['time_weight'] = 1.0
        except Exception as e:
            logger.warning(f"Could not apply recency weight: {e}")
            filtered['time_weight'] = 1.0
    else:
        filtered['time_weight'] = 1.0
    
    # Calculate weighted score
    filtered['final_score'] = filtered['weighted_score'] * filtered['time_weight']
    
    total_weight = filtered['time_weight'].sum()
    if total_weight > 0:
        score = (filtered['final_score'].sum() / total_weight) * 100
    else:
        score = 0
    
    # Calculate confidence (higher sample size = higher confidence)
    confidence = min(len(filtered) / 50, 1.0) * 100
    
    # Get sentiment breakdown
    breakdown = {
        'positive': int((filtered['AI_Sentiment'] == 'positive').sum()),
        'neutral': int((filtered['AI_Sentiment'] == 'neutral').sum()),
        'negative': int((filtered['AI_Sentiment'] == 'negative').sum()),
    }
    
    return {
        'score': round(score, 2),
        'confidence': round(confidence, 2),
        'total_reviews': len(filtered),
        'breakdown': breakdown
    }


def clean_text_for_wordcloud(text: str, stopwords: List[str] = None, min_length: int = 3) -> str:
    """
    Clean text for wordcloud generation
    
    Args:
        text: Input text
        stopwords: List of stopwords to remove
        min_length: Minimum word length to include
    
    Returns:
        Cleaned text string
    """
    if not text or pd.isna(text):
        return ""
    
    # Convert to lowercase
    text = str(text).lower()
    
    # Remove punctuation and split
    import re
    words = re.findall(r'\b[a-zA-Z]+\b', text)
    
    # Filter by length
    words = [w for w in words if len(w) >= min_length]
    
    # Remove stopwords
    if stopwords:
        stopwords_set = set(w.lower() for w in stopwords)
        words = [w for w in words if w not in stopwords_set]
    
    return ' '.join(words)


def format_number(num: float, decimal_places: int = 2) -> str:
    """
    Format number for display
    
    Args:
        num: Number to format
        decimal_places: Number of decimal places
    
    Returns:
        Formatted string
    """
    if pd.isna(num):
        return "N/A"
    
    if num >= 1_000_000:
        return f"{num/1_000_000:.{decimal_places}f}M"
    elif num >= 1_000:
        return f"{num/1_000:.{decimal_places}f}K"
    else:
        return f"{num:.{decimal_places}f}"


def export_dataframe(df: pd.DataFrame, filename: str, format: str = 'csv') -> bool:
    """
    Export dataframe to file
    
    Args:
        df: DataFrame to export
        filename: Output filename
        format: Export format ('csv', 'excel', 'json')
    
    Returns:
        True if successful, False otherwise
    """
    try:
        if format == 'csv':
            df.to_csv(filename, index=False, encoding='utf-8')
        elif format == 'excel':
            df.to_excel(filename, index=False, engine='openpyxl')
        elif format == 'json':
            df.to_json(filename, orient='records', force_ascii=False, indent=2)
        else:
            logger.error(f"Unsupported export format: {format}")
            return False
        
        logger.info(f"Successfully exported {len(df)} rows to {filename}")
        return True
        
    except Exception as e:
        logger.error(f"Error exporting dataframe: {e}")
        return False


def get_date_range(df: pd.DataFrame, date_column: str = 'Review_Time') -> Tuple[Optional[str], Optional[str]]:
    """
    Get date range from dataframe
    
    Args:
        df: DataFrame with date column
        date_column: Name of date column
    
    Returns:
        Tuple of (min_date, max_date) as strings
    """
    if date_column not in df.columns:
        return None, None
    
    try:
        dates = pd.to_datetime(df[date_column], errors='coerce')
        dates = dates.dropna()
        
        if len(dates) == 0:
            return None, None
        
        min_date = dates.min().strftime('%Y-%m-%d')
        max_date = dates.max().strftime('%Y-%m-%d')
        
        return min_date, max_date
        
    except Exception as e:
        logger.error(f"Error getting date range: {e}")
        return None, None
