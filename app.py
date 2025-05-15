from flask import Flask, request, render_template, send_file
from datetime import datetime
import io

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    sitemap_content = None
    if request.method == "POST":
        urls_raw = request.form["urls"]
        urls = [u.strip() for u in urls_raw.splitlines() if u.strip()]
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
        sitemap_content = output.getvalue()
        output.close()

        return send_file(
            io.BytesIO(sitemap_content.encode("utf-8")),
            mimetype="application/xml",
            as_attachment=True,
            download_name="sitemap.xml"
        )

    return render_template("index.html")
