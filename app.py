from flask import Flask, request, render_template, send_file, redirect, url_for
from datetime import datetime
import io, os, requests
from zipfile import ZipFile

app = Flask(__name__)
STATIC_DIR = os.path.join(app.root_path, "static")

# ========== Sitemap Generators ==========
def generate_sitemap_xml(urls):
    now = datetime.today().strftime('%Y-%m-%d')
    output = io.StringIO()
    output.write('<?xml version="1.0" encoding="UTF-8"?>\n')
    output.write('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n')
    for url in urls:
        output.write("  <url>\n")
        output.write(f"    <loc>{url}</loc>\n")
        output.write(f"    <lastmod>{now}</lastmod>\n")
        output.write("    <changefreq>weekly</changefreq>\n")
        output.write("    <priority>0.8</priority>\n")
        output.write("  </url>\n")
    output.write('</urlset>\n')
    return output.getvalue()

def generate_sitemap_html(urls):
    now = datetime.today().strftime('%Y-%m-%d')
    output = io.StringIO()
    output.write("<!DOCTYPE html>\n<html lang='vi'>\n<head>\n")
    output.write("<meta charset='UTF-8'>\n<title>Sitemap HTML</title>\n")
    output.write("<style>body{font-family:sans-serif;padding:2em;}li{margin:0.5em 0}</style>\n")
    output.write("</head>\n<body>\n")
    output.write(f"<h1>Sitemap - Cập nhật: {now}</h1>\n<ul>\n")
    for url in urls:
        output.write(f"<li><a href='{url}' target='_blank'>{url}</a></li>\n")
    output.write("</ul>\n</body>\n</html>")
    return output.getvalue()

# ========== Routes ==========
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        urls_raw = request.form.get("urls")
        urls = [u.strip() for u in urls_raw.splitlines() if u.strip()]

        xml_content = generate_sitemap_xml(urls)
        html_content = generate_sitemap_html(urls)

        # Save to /static/
        with open(os.path.join(STATIC_DIR, "sitemap.xml"), "w", encoding="utf-8") as f:
            f.write(xml_content)
        with open(os.path.join(STATIC_DIR, "sitemap.html"), "w", encoding="utf-8") as f:
            f.write(html_content)

        # Try to ping Google
        try:
            ping_url = f"https://www.google.com/ping?sitemap=https://<your-app>.onrender.com/static/sitemap.xml"
            requests.get(ping_url, timeout=3)
        except:
            pass

        # Zip download
        zip_stream = io.BytesIO()
        with ZipFile(zip_stream, 'w') as zf:
            zf.writestr("sitemap.xml", xml_content)
            zf.writestr("sitemap.html", html_content)
        zip_stream.seek(0)

        return send_file(zip_stream, as_attachment=True, download_name="sitemaps.zip", mimetype="application/zip")

    return render_template("index.html")
