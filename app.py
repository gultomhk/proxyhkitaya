import os
from fastapi import FastAPI
import requests
from fastapi.responses import StreamingResponse

app = FastAPI(title="M3U8 Proxy Server")

# Ambil proxy & referer dari environment
PROXY = os.getenv("PROXY_URL", None)
REFERER = os.getenv("REFERER_URL")  # 

@app.get("/")
def home():
    return {"message": "M3U8 Proxy Server. Gunakan /proxy.m3u8?url=<URL>"}

@app.get("/proxy.m3u8")
def proxy_m3u8(url: str):
    if not PROXY:
        return {"error": "Proxy tidak diset di environment variable"}

    try:
        r = requests.get(
            url,
            headers={
                "User-Agent": "Mozilla/5.0",
                "Referer": REFERER
            },
            proxies={"http": PROXY, "https": PROXY},
            stream=True,
            timeout=30
        )
        return StreamingResponse(
            r.iter_content(chunk_size=8192),
            media_type=r.headers.get("Content-Type", "application/vnd.apple.mpegurl")
        )
    except Exception as e:
        return {"error": str(e)}
