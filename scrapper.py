from flask import Flask, render_template_string, request, redirect, url_for, send_from_directory, flash
import os, re, csv, sys, time, random, requests, pandas as pd, matplotlib.pyplot as plt
from bs4 import BeautifulSoup
from datetime import datetime
from urllib.parse import urlparse
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

app = Flask(__name__)
app.secret_key = 'secret'

def get_headless_browser(proxy=None):
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--disable-blink-features=AutomationControlled')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument(f'user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{random.randint(90,120)} Safari/537.36')
    if proxy:
        chrome_options.add_argument(f'--proxy-server={proxy}')
    return webdriver.Chrome(options=chrome_options)

@app.route('/')
def index():
    DASHBOARD_HTML = '''<!DOCTYPE html><html><head><title>🕷️ Smart Web Scraper</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <style>body{background:#f4f6f8;} .card{border-radius:15px;box-shadow:0 4px 10px rgba(0,0,0,0.1);} footer{text-align:center;padding:10px;color:gray;}</style>
    </head><body><nav class="navbar navbar-dark bg-dark"><div class="container-fluid"><span class="navbar-brand">🕷️ Smart Web Scraper Dashboard</span></div></nav>
    <div class="container py-5"><div class="row justify-content-center"><div class="col-md-8"><div class="card p-4">
    <h4 class="text-center">Enter URL to Scrape</h4>
    <form method="post" action="/scrape">
      <input type="url" name="url" class="form-control mb-3" placeholder="https://example.com" required>
      <input type="text" name="proxy" class="form-control mb-3" placeholder="Optional proxy (http://proxy:port)">
      <button class="btn btn-dark w-100">Start Scraping</button>
    </form></div></div></div></div>
    <footer>© 2025 Intelligent Scraper</footer></body></html>'''
    return render_template_string(DASHBOARD_HTML)

@app.route('/scrape', methods=['POST'])
def scrape():
    url = request.form.get('url')
    proxy = request.form.get('proxy')
    if not url.startswith('http'):
        flash('Invalid URL')
        return redirect(url_for('index'))

    try:
        driver = get_headless_browser(proxy)
        driver.get(url)
        time.sleep(random.uniform(3, 6))
        html = driver.page_source
        domain = urlparse(url).netloc.replace(':', '_')
        folder_path = os.path.join('scraped_data', domain)
        os.makedirs(folder_path, exist_ok=True)
        screenshot_path = os.path.join(folder_path, 'screenshot.png')
        driver.save_screenshot(screenshot_path)
        driver.quit()
    except Exception as e:
        print(f"[!] Selenium failed: {e}")
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100 Safari/537.36"}
        html = requests.get(url, headers=headers, proxies={"http": proxy, "https": proxy} if proxy else None).text

    soup = BeautifulSoup(html, 'html.parser')
    text_content = soup.get_text(' ', strip=True)
    sentences = re.split(r'(?<=[.!?]) +', text_content)
    readable_preview = ' '.join(sentences[:20])

    domain = urlparse(url).netloc.replace(':', '_')
    folder_path = os.path.join('scraped_data', domain)
    os.makedirs(folder_path, exist_ok=True)

    with open(os.path.join(folder_path, 'page.html'), 'w', encoding='utf-8') as f:
        f.write(html)
    with open(os.path.join(folder_path, 'content.txt'), 'w', encoding='utf-8') as f:
        f.write(readable_preview)

    pdf_path = os.path.join(folder_path, 'report.pdf')
    doc = SimpleDocTemplate(pdf_path, pagesize=A4)
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name='Justify', alignment=4, leading=14))

    Story = []
    Story.append(Paragraph(f"<b>Intelligent Web Scrape Report</b>", styles['Title']))
    Story.append(Spacer(1, 0.2*inch))
    Story.append(Paragraph(f"<b>Source:</b> {url}", styles['Normal']))
    Story.append(Paragraph(f"<b>Generated:</b> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", styles['Normal']))
    Story.append(Spacer(1, 0.3*inch))

    if os.path.exists(os.path.join(folder_path, 'screenshot.png')):
        Story.append(Image(os.path.join(folder_path, 'screenshot.png'), width=5.5*inch, height=3*inch))
        Story.append(Spacer(1, 0.3*inch))

    Story.append(Paragraph("<b>Readable Extract (Reconstructed):</b>", styles['Heading2']))
    Story.append(Paragraph(' '.join([s.capitalize() for s in sentences[:25]]), styles['Justify']))

    word_count = len(text_content.split())
    char_count = len(text_content)
    sentence_count = len(sentences)
    avg_sentence_length = round(word_count / max(sentence_count, 1), 2)

    Story.append(PageBreak())
    Story.append(Paragraph("<b>Data Insights and Analytics</b>", styles['Heading1']))
    Story.append(Spacer(1, 0.2*inch))

    data_summary = [['Metric', 'Value'], ['Total Words', word_count], ['Character Count', char_count], ['Sentence Count', sentence_count], ['Average Words per Sentence', avg_sentence_length]]
    table = Table(data_summary, hAlign='LEFT')
    table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#212529')),
        ('TEXTCOLOR', (0,0), (-1,0), colors.whitesmoke),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,-1), 10),
        ('BOTTOMPADDING', (0,0), (-1,0), 12),
        ('BACKGROUND', (0,1), (-1,-1), colors.HexColor('#f8f9fa')),
        ('GRID', (0,0), (-1,-1), 0.5, colors.grey)
    ]))
    Story.append(table)
    Story.append(Spacer(1, 0.4*inch))

    # Charts section
    plt.figure(figsize=(6,4))
    lengths = [len(s.split()) for s in sentences if len(s.split()) < 50]
    plt.hist(lengths, bins=10, color='steelblue', edgecolor='black')
    plt.title('Sentence Length Distribution')
    plt.xlabel('Words per Sentence')
    plt.ylabel('Frequency')
    chart_path = os.path.join(folder_path, 'sentence_length_distribution.png')
    plt.savefig(chart_path)
    plt.close()
    Story.append(Image(chart_path, width=5.5*inch, height=3*inch))
    Story.append(Spacer(1, 0.3*inch))

    plt.figure(figsize=(5,4))
    words = text_content.split()
    word_freq = pd.Series(words).value_counts().head(10)
    word_freq.plot(kind='bar', color='darkgreen', title='Top 10 Frequent Words')
    plt.ylabel('Frequency')
    plt.tight_layout()
    freq_chart = os.path.join(folder_path, 'top_words.png')
    plt.savefig(freq_chart)
    plt.close()
    Story.append(Image(freq_chart, width=5.5*inch, height=3*inch))

    Story.append(PageBreak())
    Story.append(Paragraph("<b>Interpretation and Insights:</b>", styles['Heading2']))
    Story.append(Paragraph(f"The scraped content consists of approximately {word_count} words, structured across {sentence_count} sentences. The average sentence contains {avg_sentence_length} words, suggesting a {'concise' if avg_sentence_length < 12 else 'detailed'} narrative style. Common words such as {', '.join(word_freq.index[:5])} dominate the text, indicating key topics of discussion.", styles['Justify']))
    Story.append(Spacer(1, 0.3*inch))
    Story.append(Paragraph("This report provides both visual and textual summaries, making it suitable for strategic analysis, research comparison, or trend identification.", styles['Justify']))

    doc.build(Story)

    RESULT_HTML = '''<!DOCTYPE html><html><head><title>Scrape Results</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <style>body{background:#f4f6f8;} pre{background:#eef;padding:10px;border-radius:10px;white-space:pre-wrap;} .card{border-radius:15px;box-shadow:0 4px 10px rgba(0,0,0,0.1);} </style></head><body>
    <div class="container py-4"><div class="card p-4"><h3>🕷️ Scrape Results</h3><p><b>Source:</b> {{source_url}}</p>
    <h5>Preview (Readable Extract):</h5><pre>{{preview}}</pre>
    <p class="mt-3">A detailed analytical report and charts have been saved in: <code>scraped_data/{{domain}}</code></p>
    <a href="/" class="btn btn-dark mt-3">Back</a></div></div></body></html>'''

    return render_template_string(RESULT_HTML, source_url=url, preview=readable_preview, domain=domain)

if __name__ == '__main__':
    os.makedirs('scraped_data', exist_ok=True)

    print("Starting development server at http://127.0.0.1:5000 — use Gunicorn or Waitress for production.")
    app.run(host='127.0.0.1', port=5000, debug=False)

