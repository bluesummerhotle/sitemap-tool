from flask import Flask, request, render_template, send_file
from datetime import datetime
import io

app = Flask(__name__)

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
    output.write("<meta charset='UTF-8'>\n<title>Sitemap HTML</title>\n</head>\n<body>\n")
    output.write(f"<h1>Sitemap - Cập nhật: {now}</h1>\n<ul>\n")
    for url in urls:
        output.write(f"<li><a href='{url}' target='_blank'>{url}</a></li>\n")
    output.write("</ul>\n</body>\n</html>")
    return output.getvalue()

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        urls_raw = request.form["urls"]
        urls = [u.strip() for u in urls_raw.splitlines() if u.strip()]

        xml = generate_sitemap_xml(urls)
        html = generate_sitemap_html(urls)

        zip_stream = io.BytesIO()
        from zipfile import ZipFile
        with ZipFile(zip_stream, 'w') as zf:
            zf.writestr("sitemap.xml", xml)
            zf.writestr("sitemap.html", html)
        zip_stream.seek(0)

        return send_file(zip_stream, as_attachment=True, download_name="sitemaps.zip", mimetype="application/zip")

    return render_template("index.html")
