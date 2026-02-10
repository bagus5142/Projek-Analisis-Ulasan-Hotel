# Deployment Guide - Hotel Review Analysis Dashboard

This guide provides instructions for deploying the dashboard in various environments.

## 📋 Prerequisites

- Python 3.8 or higher
- Git
- 2GB RAM minimum (4GB recommended)
- 1GB disk space

## 🚀 Deployment Options

### Option 1: Local Development

**Best for**: Testing, development, demos

```bash
# 1. Clone repository
git clone https://github.com/bagus5142/Projek-Analisis-Ulasan-Hotel.git
cd Projek-Analisis-Ulasan-Hotel

# 2. Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run dashboard
cd src
streamlit run visual.py
```

Access at: `http://localhost:8501`

---

### Option 2: Streamlit Cloud (FREE)

**Best for**: Public demos, sharing with team

1. **Fork the repository** on GitHub

2. **Go to** [streamlit.io/cloud](https://streamlit.io/cloud)

3. **Connect your GitHub account**

4. **Deploy new app**:
   - Repository: `yourusername/Projek-Analisis-Ulasan-Hotel`
   - Branch: `main`
   - Main file path: `src/visual.py`

5. **Configure settings** (optional):
   - Set Python version to 3.9+
   - Add secrets if needed

6. **Deploy!** - Your app will be live at `yourapp.streamlit.app`

**Note**: Ensure `Analisis_Master_Lengkap.csv` is in the repository or use alternative data source.

---

### Option 3: Docker Deployment

**Best for**: Containerized environments, consistent deployments

1. **Create Dockerfile**:

```dockerfile
# Dockerfile
FROM python:3.9-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY . .

# Expose Streamlit port
EXPOSE 8501

# Health check
HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health || exit 1

# Run the application
CMD ["streamlit", "run", "src/visual.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

2. **Build and run**:

```bash
# Build image
docker build -t hotel-analysis-dashboard .

# Run container
docker run -p 8501:8501 hotel-analysis-dashboard
```

3. **Using Docker Compose** (recommended for production):

```yaml
# docker-compose.yml
version: '3.8'

services:
  dashboard:
    build: .
    ports:
      - "8501:8501"
    environment:
      - STREAMLIT_SERVER_HEADLESS=true
      - STREAMLIT_SERVER_PORT=8501
    volumes:
      - ./src:/app/src:ro
      - ./config:/app/config:ro
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8501/_stcore/health"]
      interval: 30s
      timeout: 10s
      retries: 3
```

```bash
docker-compose up -d
```

---

### Option 4: AWS EC2 Deployment

**Best for**: Production deployments with full control

1. **Launch EC2 instance**:
   - AMI: Ubuntu 22.04 LTS
   - Instance type: t3.medium (or larger)
   - Security group: Allow port 8501

2. **Connect and setup**:

```bash
# SSH into instance
ssh -i your-key.pem ubuntu@your-ec2-ip

# Update system
sudo apt update && sudo apt upgrade -y

# Install Python and pip
sudo apt install python3.9 python3-pip python3-venv -y

# Clone repository
git clone https://github.com/bagus5142/Projek-Analisis-Ulasan-Hotel.git
cd Projek-Analisis-Ulasan-Hotel

# Setup virtual environment
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Install tmux for background running
sudo apt install tmux -y
```

3. **Run dashboard in background**:

```bash
# Start tmux session
tmux new -s dashboard

# Run dashboard
cd src
streamlit run visual.py --server.port 8501 --server.address 0.0.0.0

# Detach from tmux: Ctrl+B, then D
# Reattach: tmux attach -t dashboard
```

4. **Setup systemd service** (for automatic restart):

```bash
# Create service file
sudo nano /etc/systemd/system/hotel-dashboard.service
```

```ini
[Unit]
Description=Hotel Review Analysis Dashboard
After=network.target

[Service]
Type=simple
User=ubuntu
WorkingDirectory=/home/ubuntu/Projek-Analisis-Ulasan-Hotel/src
ExecStart=/home/ubuntu/Projek-Analisis-Ulasan-Hotel/venv/bin/streamlit run visual.py --server.port 8501 --server.address 0.0.0.0
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

```bash
# Enable and start service
sudo systemctl enable hotel-dashboard
sudo systemctl start hotel-dashboard

# Check status
sudo systemctl status hotel-dashboard
```

5. **Setup Nginx reverse proxy** (optional but recommended):

```bash
sudo apt install nginx -y
sudo nano /etc/nginx/sites-available/dashboard
```

```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://localhost:8501;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
    }
}
```

```bash
sudo ln -s /etc/nginx/sites-available/dashboard /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

---

### Option 5: Heroku Deployment

**Best for**: Quick cloud deployment, small to medium traffic

1. **Create Heroku account** at [heroku.com](https://heroku.com)

2. **Install Heroku CLI**:
```bash
curl https://cli-assets.heroku.com/install.sh | sh
heroku login
```

3. **Prepare files**:

Create `setup.sh`:
```bash
mkdir -p ~/.streamlit/
echo "\
[server]\n\
headless = true\n\
port = $PORT\n\
enableCORS = false\n\
\n\
" > ~/.streamlit/config.toml
```

Create `Procfile`:
```
web: sh setup.sh && streamlit run src/visual.py
```

4. **Deploy**:
```bash
git init
git add .
git commit -m "Initial commit"

heroku create your-app-name
git push heroku main

heroku open
```

---

## 🔧 Configuration

### Environment Variables

Create `.env` file for sensitive configurations:

```bash
# .env (DO NOT COMMIT)
DATA_FILE_PATH=/path/to/Analisis_Master_Lengkap.csv
LOG_LEVEL=INFO
CACHE_TTL=3600
```

Load in `visual.py`:
```python
from dotenv import load_dotenv
load_dotenv()

DATA_FILE = os.getenv('DATA_FILE_PATH', 'Analisis_Master_Lengkap.csv')
```

### Streamlit Configuration

Create `~/.streamlit/config.toml`:

```toml
[theme]
primaryColor = "#6C5CE7"
backgroundColor = "#FFFFFF"
secondaryBackgroundColor = "#F0F2F5"
textColor = "#2D3436"

[server]
port = 8501
enableCORS = false
maxUploadSize = 200

[browser]
gatherUsageStats = false
```

---

## 📊 Performance Optimization

### For Large Datasets (>100k rows)

1. **Use database backend**:
```python
# Instead of CSV
import psycopg2
import streamlit as st

@st.cache_resource
def get_db_connection():
    return psycopg2.connect(
        host="your-db-host",
        database="reviews",
        user="user",
        password="password"
    )

@st.cache_data(ttl=600)
def load_data():
    conn = get_db_connection()
    df = pd.read_sql_query("SELECT * FROM reviews", conn)
    return df
```

2. **Implement pagination**:
```python
page = st.number_input('Page', min_value=1, max_value=100)
page_size = 1000
df_page = df.iloc[(page-1)*page_size : page*page_size]
```

3. **Use Parquet instead of CSV**:
```python
# Save as parquet
df.to_parquet('data.parquet', compression='snappy')

# Load (much faster)
df = pd.read_parquet('data.parquet')
```

---

## 🔐 Security Checklist

- [ ] Change default passwords/keys
- [ ] Enable HTTPS (use Let's Encrypt)
- [ ] Set up firewall (UFW on Ubuntu)
- [ ] Regular security updates
- [ ] Implement rate limiting
- [ ] Add authentication if needed
- [ ] Backup data regularly
- [ ] Monitor logs for suspicious activity

---

## 🐛 Troubleshooting

### Dashboard won't start

```bash
# Check Python version
python --version  # Should be 3.8+

# Check dependencies
pip list

# Reinstall dependencies
pip install -r requirements.txt --force-reinstall

# Check for port conflicts
lsof -i :8501
# Kill process if needed: kill -9 <PID>
```

### Out of memory errors

```bash
# Increase swap space (Linux)
sudo fallocate -l 4G /swapfile
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile

# Or reduce dataset size
# Filter data before loading
df = df.sample(frac=0.5)  # Use 50% of data
```

### Slow performance

1. Check Streamlit caching is enabled
2. Reduce dataset size for testing
3. Optimize database queries
4. Use more powerful instance

---

## 📈 Monitoring

### Setup logging

```python
import logging

logging.basicConfig(
    filename='logs/app.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)
logger.info("Dashboard started")
```

### Monitor with systemd

```bash
# View logs
journalctl -u hotel-dashboard -f

# Check resource usage
systemctl status hotel-dashboard
```

---

## 🔄 Updates and Maintenance

### Updating the dashboard

```bash
# Pull latest changes
git pull origin main

# Update dependencies
pip install -r requirements.txt --upgrade

# Restart service
sudo systemctl restart hotel-dashboard
```

### Backup strategy

```bash
# Backup data
rsync -avz /path/to/data /backup/location/

# Backup database (if using PostgreSQL)
pg_dump -U user dbname > backup.sql

# Automate with cron
0 2 * * * /path/to/backup-script.sh
```

---

## 📞 Support

For deployment issues:
1. Check the [Troubleshooting](#-troubleshooting) section
2. Review Streamlit documentation: [docs.streamlit.io](https://docs.streamlit.io)
3. Open an issue on GitHub
4. Contact: [your-email@example.com]

---

**Last Updated**: February 2026  
**Maintained by**: bagus5142
