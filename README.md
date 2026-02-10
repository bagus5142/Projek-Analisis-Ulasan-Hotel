# Projek Analisis Ulasan Hotel

## 📊 Overview
A comprehensive **Hotel Review Sentiment Analysis & Comparison Dashboard** that analyzes customer reviews to compare hotel performance, specifically focusing on BUMN (State-Owned Enterprises) vs Non-BUMN hotels. The project uses NLP-based sentiment analysis and aspect-based opinion mining to provide strategic insights.

## ✨ Features

### Interactive Dashboard (8 Tabs)
1. **Overview** - Sentiment distribution and aspect analysis overview
2. **BUMN vs Non-BUMN Comparison** - Strategic comparison with reasoning
3. **Detailed Hotel Analysis** - Per-hotel aspect breakdown
4. **Sentiment Heatmaps** - Distribution by aspect
5. **Multi-dimensional Comparisons** - Bubble charts and parallel coordinates
6. **Word Cloud Analysis** - Keyword analysis with sentiment filtering
7. **Strategic Insights** - Heatmaps with temporal trend analysis
8. **Raw Data Explorer** - Search, filter, and export (CSV/Excel/JSON)

### Key Capabilities
- 🎯 AI-powered sentiment classification (positive/negative/neutral)
- 🏷️ Aspect-based opinion mining (cleanliness, service, food, etc.)
- 📈 Temporal trend analysis
- 🔍 Advanced filtering by star category and hotel type
- 📊 10+ interactive visualization types
- 💾 Multi-format data export

## 🏗️ Architecture

```
Raw Data (DatasetHotel/)
    ↓
Preprocessing.ipynb → Text cleaning & normalization
    ↓
Model.ipynb → Sentiment & aspect classification
    ↓
Analisis_Master_Lengkap.csv (Processed Dataset)
    ↓
visual.py (Streamlit Dashboard) → Interactive visualizations
```

## 📁 Project Structure

```
Projek-Analisis-Ulasan-Hotel/
├── src/
│   ├── visual.py              # Main Streamlit dashboard
│   ├── Preprocessing.ipynb    # Data cleaning pipeline
│   ├── Model.ipynb            # ML models for sentiment analysis
│   ├── Visualisasi.ipynb      # Exploratory analysis
│   ├── Dashboard.ipynb        # Dashboard documentation
│   └── Analisis_Master_Lengkap.csv  # Processed dataset
├── DatasetHotel/              # Raw hotel review data
│   ├── BUMNB3/, BUMNB4/, BUMNB5/
│   └── KOMPETITORB3/, KOMPETITORB4/, KOMPETITORB5/
├── DatasetHotelCLEAN/         # Cleaned datasets
├── DataSampel/                # Sample data
│   ├── Raw/
│   └── Clean/
├── Results/                   # Output files and visualizations
├── requirements.txt           # Python dependencies
└── README.md                  # This file
```

## 🚀 Installation

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Setup Instructions

1. **Clone the repository**
   ```bash
   git clone https://github.com/bagus5142/Projek-Analisis-Ulasan-Hotel.git
   cd Projek-Analisis-Ulasan-Hotel
   ```

2. **Create virtual environment (recommended)**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Verify data files**
   Ensure `src/Analisis_Master_Lengkap.csv` exists. If not, run preprocessing notebooks first:
   ```bash
   cd src
   jupyter notebook  # Run Preprocessing.ipynb then Model.ipynb
   ```

## 💻 Usage

### Running the Dashboard

```bash
cd src
streamlit run visual.py
```

The dashboard will open in your default browser at `http://localhost:8501`

### Using Jupyter Notebooks

For data preprocessing and model training:
```bash
cd src
jupyter notebook
```

Open and run in sequence:
1. `Preprocessing.ipynb` - Clean and prepare data
2. `Model.ipynb` - Train sentiment analysis models
3. `Visualisasi.ipynb` - Exploratory data analysis

## 📊 Data Schema

### Key Columns in Processed Dataset

| Column | Description |
|--------|-------------|
| `Nama_Hotel` | Hotel name |
| `Kelas` | Star rating (3, 4, or 5 stars) |
| `Rating` | Review rating (1-5) |
| `AI_Sentiment` | Sentiment (positive/negative/neutral) |
| `AI_Aspek` | Aspect category (cleanliness, service, food, etc.) |
| `clean_text` | Preprocessed review text |
| `Review_Time` | Review timestamp |
| `Kategori_Hotel` | BUMN or Non-BUMN classification |

## 🛠️ Configuration

### Customizing the Dashboard

Edit color schemes in `visual.py`:
```python
SENTIMENT_PALETTE = {
    "positive": "#00D9C0",
    "negative": "#FF6B6B",
    "neutral": "#FFE66D"
}
```

### Changing Data Source

Update the file path in `visual.py` (line 455):
```python
file_path = "path/to/your/Analisis_Master_Lengkap.csv"
```

## 🧪 Testing

Run the dashboard with sample data:
```bash
# Test with reduced dataset
cd src
python -c "
import pandas as pd
df = pd.read_csv('Analisis_Master_Lengkap.csv')
df.sample(1000).to_csv('sample_data.csv', index=False)
"
# Then modify visual.py to use sample_data.csv
```

## 📈 Performance Notes

- **Recommended dataset size**: < 100,000 reviews for optimal performance
- **Memory usage**: ~500MB for typical datasets
- **Load time**: 2-5 seconds for initial data loading (cached)

For larger datasets:
- Use pagination in Tab 8 (Raw Data)
- Consider database backend instead of CSV
- Implement lazy loading for visualizations

## 🐛 Known Issues & Limitations

1. **BUMN categorization** uses keyword matching (line 563-571) - may misclassify hotels
2. **No pagination** in raw data view - performance issues with >50k rows
3. **Aspect scoring** uses simplified formula - doesn't account for review recency
4. **Hardcoded file paths** - requires manual configuration for different environments
5. **Limited error handling** - may crash on malformed data

## 🔧 Troubleshooting

### "File not found" error
- Ensure you're in the `src/` directory when running
- Verify `Analisis_Master_Lengkap.csv` exists

### Dashboard not loading
- Check if port 8501 is available
- Try: `streamlit run visual.py --server.port 8502`

### Import errors
- Reinstall dependencies: `pip install -r requirements.txt --force-reinstall`
- Check Python version: `python --version` (must be 3.8+)

### Slow performance
- Reduce dataset size for testing
- Clear Streamlit cache: Delete `.streamlit/cache/`
- Increase memory: `streamlit run visual.py --server.maxUploadSize 1000`

## 🤝 Contributing

Contributions are welcome! Areas for improvement:
- Modularize `visual.py` (currently 2,349 lines)
- Add unit tests for analytics functions
- Implement database backend (PostgreSQL/MongoDB)
- Add Indonesian stopword filtering
- Create REST API for programmatic access

## 📝 License

[Specify your license here]

## 👥 Authors

- bagus5142 - Initial work

## 🙏 Acknowledgments

- Streamlit for the dashboard framework
- Plotly for interactive visualizations
- Indonesian NLP community for text processing resources

## 📧 Contact

For questions or support, please open an issue on GitHub.

---

**Last Updated**: February 2026  
**Version**: 1.0.0