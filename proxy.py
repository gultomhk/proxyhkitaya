
from flask import Flask, request, Response
import proxy  # Ini adalah proxy.so
from urllib.parse import urlparse

app = Flask(__name__)

# Domain yang diizinkan (opsional untuk keamanan)
ALLOWED_DOMAINS = [
    "alldownplay.xyz",
    "watch.rkplayer.xyz",
    "key.keylocking.ru",
    "fhsport121.fhs36f7.xyz",
]

@app.route("/proxy")
def proxy_handler():
    url = request.args.get("url")
    if not url:
        return {"error": "Missing 'url' parameter"}, 400

    # Validasi domain (opsional tapi disarankan)
    parsed = urlparse(url)
    if parsed.hostname not in ALLOWED_DOMAINS:
        return {"error": "Forbidden domain"}, 403

    try:
        result = proxy.go(url)
        return Response(result, status=200, content_type="application/vnd.apple.mpegurl")
    except Exception as e:
        return {"error": str(e)}, 500

@app.route("/")
def index():
    return {
        "message": "Use /proxy?url=https://example.com to proxy a stream via proxy.so"
    }
