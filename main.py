import webview
import sys
import os
import threading
import requests
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
import socket

# These will be replaced by the GitHub Action during build
TARGET_URL = "https://google.com"
APP_NAME = "WebToEXE App"

# Port acquisition
def get_free_port():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('', 0))
    port = s.getsockname()[1]
    s.close()
    return port

PORT = get_free_port()
LOCAL_URL = f"http://127.0.0.1:{PORT}"

# Sophisticated TopBar CSS and HTML
SHELL_HTML = f"""
<!DOCTYPE html>
<html>
<head>
    <style>
        body, html {{ margin: 0; padding: 0; height: 100%; overflow: hidden; background: #000; font-family: -apple-system, sans-serif; }}
        #top-bar {{
            height: 40px; background: rgba(25, 25, 25, 0.98); backdrop-filter: blur(15px);
            display: flex; align-items: center; justify-content: space-between;
            padding: 0 15px; color: #fff; z-index: 1000; border-bottom: 1px solid rgba(255, 255, 255, 0.1);
            position: relative; -webkit-app-region: drag;
        }}
        .nav-controls {{ display: flex; gap: 15px; -webkit-app-region: no-drag; }}
        .nav-btn {{ cursor: pointer; opacity: 0.7; transition: 0.2s; display: flex; align-items: center; }}
        .nav-btn:hover {{ opacity: 1; }}
        .nav-btn svg {{ width: 18px; height: 18px; fill: #fff; }}
        .title-logo {{ 
            position: absolute; left: 50%; transform: translateX(-50%);
            font-size: 13px; font-weight: 600; color: rgba(255, 255, 255, 0.9);
            pointer-events: none;
        }}
        .window-controls {{ display: flex; gap: 12px; -webkit-app-region: no-drag; }}
        .win-btn {{ width: 12px; height: 12px; border-radius: 50%; cursor: pointer; border: none; }}
        .close {{ background: #ff5f56; }}
        .min {{ background: #ffbd2e; }}
        .max {{ background: #27c93f; }}
        iframe {{ width: 100%; height: calc(100% - 40px); border: none; background: #fff; }}
    </style>
</head>
<body>
    <div id="top-bar">
        <div class="nav-controls">
            <div class="nav-btn" onclick="goBack()"><svg viewBox="0 0 24 24"><path d="M15.41 7.41L14 6l-6 6 6 6 1.41-1.41L10.83 12z"/></svg></div>
            <div class="nav-btn" onclick="goForward()"><svg viewBox="0 0 24 24"><path d="M10 6L8.59 7.41 13.17 12l-4.58 4.59L10 18l6-6z"/></svg></div>
            <div class="nav-btn" onclick="reload()"><svg viewBox="0 0 24 24"><path d="M17.65 6.35C16.2 4.9 14.21 4 12 4c-4.42 0-7.99 3.58-7.99 8s3.57 8 7.99 8c3.73(0 6.84-2.55 7.73-6h-2.08c-.82 2.33-3.04 4-5.65 4-3.31 0-6-2.69-6-6s2.69-6 6-6c1.66 0 3.14.69 4.22 1.78L13 11h7V4l-2.35 2.35z"/></svg></div>
        </div>
        <div class="title-logo">{APP_NAME}</div>
        <div class="window-controls">
            <div class="win-btn min" onclick="window.pywebview.api.minimize()"></div>
            <div class="win-btn max" onclick="window.pywebview.api.maximize()"></div>
            <div class="win-btn close" onclick="window.pywebview.api.close()"></div>
        </div>
    </div>
    <iframe id="main-frame" src="{LOCAL_URL}/proxy?url={TARGET_URL}"></iframe>
    <script>
        const frame = document.getElementById('main-frame');
        function goBack() {{ try {{ frame.contentWindow.history.back(); }} catch(e) {{}} }}
        function goForward() {{ try {{ frame.contentWindow.history.forward(); }} catch(e) {{}} }}
        function reload() {{ frame.src = frame.src; }}
    </script>
</body>
</html>
"""

class ProxyHandler(BaseHTTPRequestHandler):
    def log_message(self, format, *args): return # Silent logs

    def do_GET(self):
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(SHELL_HTML.encode())
            return

        if self.path.startswith('/proxy'):
            query = parse_qs(urlparse(self.path).query)
            url = query.get('url', [None])[0]
            if not url:
                self.send_error(400, "Missing URL")
                return
            
            try:
                headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'}
                # Bypass SSL verification if needed for certain sites, though generally safer to verify
                resp = requests.get(url, headers=headers, timeout=15)
                
                self.send_response(resp.status_code)
                for key, value in resp.headers.items():
                    # STRIP security headers to allow framing
                    if key.lower() not in ['x-frame-options', 'content-security-policy', 'frame-ancestors']:
                        self.send_header(key, value)
                self.end_headers()
                self.wfile.write(resp.content)
            except Exception as e:
                self.send_error(500, str(e))
            return
        
        # Default fallback
        self.send_error(404)

class API:
    def __init__(self, window): self.window = window
    def close(self): self.window.destroy()
    def minimize(self): self.window.minimize()
    def maximize(self): self.window.toggle_fullscreen()

def run_server():
    httpd = HTTPServer(('127.0.0.1', PORT), ProxyHandler)
    httpd.serve_forever()

def start_webview():
    threading.Thread(target=run_server, daemon=True).start()
    
    window = webview.create_window(
        APP_NAME, 
        url=f"{LOCAL_URL}/",
        width=1280, height=720,
        resizable=True, frameless=True
    )
    api = API(window)
    window.expose(api.close, api.minimize, api.maximize)
    
    webview.start(user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36')

if __name__ == "__main__":
    start_webview()
