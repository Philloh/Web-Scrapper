# Web-Scrapper
A smart web srcaping tool that generates reports and creates directories for the PNG files and also charts. Scraps all websites

# 🕷️ Smart Web Scraper — Development Version

This is the **development-focused** version of the Smart Web Scraper. It includes debugging tools, live reload, and development-only features.

---

## 🧩 Overview
A Python-based Flask web scraper for structured data extraction, visualization, and report generation. The development mode enables developers to test scraping logic, tweak analysis, and improve the UI before production deployment.

---

## ⚙️ Setup for Development

### 1️⃣ Clone the repository
```bash
git clone https://github.com/<your-username>/smart-web-scraper.git
cd smart-web-scraper
```

### 2️⃣ Create and activate a virtual environment
```bash
python3 -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate
```

### 3️⃣ Install dependencies
```bash
pip install -r requirements.txt
```

If you don’t have a `requirements.txt`, create one with:
```bash
Flask
requests
beautifulsoup4
pandas
matplotlib
selenium
reportlab
waitress
pytest
black
flake8
dotenv
```

---

## 🧠 Running the Scraper in Development Mode
Run Flask in debug mode to enable auto-reload and error logs:
```bash
flask --app scrapper run --debug
```

Or run directly:
```bash
python3 scrapper.py
```

---

## 🧪 Testing
Use **pytest** for development testing:
```bash
pytest tests/
```

---

## 🧱 Directory Structure
```
scrapper-dev/
 ├── scrapper.py              # Core logic
 ├── templates/               # Dashboard HTML templates
 ├── static/                  # Frontend assets
 ├── modules/                 # Selenium and utility modules
 ├── scraped_data/            # Per-domain data folders
 ├── tests/                   # Unit/integration tests
 ├── requirements.txt
 └── README.md
```

---

## 🧰 Developer Tools
- **Black** for formatting: `black .`
- **Flake8** for linting: `flake8 .`
- **Selenium** for dynamic pages
- **Requests + BeautifulSoup** for static scraping

---

## 🧮 Data Insight Development
The `analyze_and_visualize()` function automatically detects numeric columns and generates multiple chart types:
- Histograms
- Pie charts
- Correlation heatmaps
- Line charts for time-based trends

Developers can extend this with new charting logic or integrate AI-assisted data summaries.

---

## 💡 Development Notes
- Use proxy rotation for heavy scraping
- Implement `time.sleep()` or randomized delays to mimic human browsing
- Use environment variables from `.env` for configuration
- For headless scraping on Linux:
```bash
xvfb-run python3 scrapper.py
```

---

## 🧑‍💻 Contributing
1. Fork the repo
2. Create a new branch: `git checkout -b dev-feature`
3. Commit and push changes
4. Open a pull request

---

## 👥 Maintainer
**philip** — Lead developer and maintainer.

---

## 📜 License
MIT License — free for personal and educational development use.
