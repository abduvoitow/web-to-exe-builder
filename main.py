import webview
import sys
import os
import threading
import time

# These will be replaced by the GitHub Action during build
TARGET_URL = "https://google.com"
APP_NAME = "WebToEXE App"

# Highly resilient CSS and HTML for the top bar
TOOLBAR_JS = f"""
(function() {{
    const css = `
        #pywebview-topbar {{
            position: fixed !important;
            top: 0 !important;
            left: 0 !important;
            width: 100% !important;
            height: 40px !important;
            background: rgba(25, 25, 25, 0.95) !important;
            backdrop-filter: blur(15px) !important;
            -webkit-backdrop-filter: blur(15px) !important;
            display: flex !important;
            align-items: center !important;
            justify-content: space-between !important;
            padding: 0 15px !important;
            color: #fff !important;
            z-index: 2147483647 !important;
            box-sizing: border-box !important;
            border-bottom: 1px solid rgba(255, 255, 255, 0.1) !important;
            font-family: -apple-system, system-ui, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif !important;
            user-select: none !important;
        }}
        .pywebview-drag-region {{
            position: absolute !important;
            width: 100% !important;
            height: 100% !important;
            top: 0 !important;
            left: 0 !important;
            z-index: -1 !important;
        }}
        .nav-controls {{ display: flex !important; gap: 15px !important; z-index: 10 !important; }}
        .nav-btn {{ cursor: pointer !important; opacity: 0.7 !important; transition: 0.2s !important; display: flex !important; align-items: center !important; }}
        .nav-btn:hover {{ opacity: 1 !important; }}
        .nav-btn svg {{ width: 18px !important; height: 18px !important; fill: #fff !important; }}
        .title-logo {{ 
            position: absolute !important; left: 50% !important; transform: translateX(-50%) !important;
            font-size: 13px !important; font-weight: 600 !important; color: rgba(255, 255, 255, 0.9) !important;
            pointer-events: none !important;
        }}
        .window-controls {{ display: flex !important; gap: 12px !important; z-index: 10 !important; padding-right: 10px !important; }}
        .win-btn {{ width: 12px !important; height: 12px !important; border-radius: 50% !important; cursor: pointer !important; border: none !important; }}
        .close {{ background: #ff5f56 !important; }}
        .min {{ background: #ffbd2e !important; }}
        .max {{ background: #27c93f !important; }}
        body {{ padding-top: 40px !important; }}
    `;

    function inject() {{
        if (document.getElementById('pywebview-topbar')) return;
        if (!document.body) return;

        const style = document.createElement('style');
        style.id = 'pywebview-styles';
        style.innerHTML = css;
        document.head.appendChild(style);

        const bar = document.createElement('div');
        bar.id = 'pywebview-topbar';
        bar.className = 'pywebview-drag-region';
        bar.innerHTML = `
            <div class="nav-controls">
                <div class="nav-btn" onclick="history.back()"><svg viewBox="0 0 24 24"><path d="M15.41 7.41L14 6l-6 6 6 6 1.41-1.41L10.83 12z"/></svg></div>
                <div class="nav-btn" onclick="history.forward()"><svg viewBox="0 0 24 24"><path d="M10 6L8.59 7.41 13.17 12l-4.58 4.59L10 18l6-6z"/></svg></div>
                <div class="nav-btn" onclick="location.reload()"><svg viewBox="0 0 24 24"><path d="M17.65 6.35C16.2 4.9 14.21 4 12 4c-4.42 0-7.99 3.58-7.99 8s3.57 8 7.99 8c3.73 0 6.84-2.55 7.73-6h-2.08c-.82 2.33-3.04 4-5.65 4-3.31 0-6-2.69-6-6s2.69-6 6-6c1.66 0 3.14.69 4.22 1.78L13 11h7V4l-2.35 2.35z"/></svg></div>
            </div>
            <div class="title-logo">{APP_NAME}</div>
            <div class="window-controls">
                <div class="win-btn min" onclick="window.pywebview.api.minimize()"></div>
                <div class="win-btn max" onclick="window.pywebview.api.maximize()"></div>
                <div class="win-btn close" onclick="window.pywebview.api.close()"></div>
            </div>
        `;
        document.body.appendChild(bar);
        document.body.style.paddingTop = '40px';
    }}

    setInterval(inject, 1000);
    inject();
}})();
"""

class API:
    def __init__(self):
        self.window = None

    def close(self):
        self.window.destroy()

    def minimize(self):
        self.window.minimize()

    def maximize(self):
        self.window.toggle_fullscreen()

def start_webview():
    api = API()
    window = webview.create_window(
        APP_NAME, 
        url=TARGET_URL,
        js_api=api,
        width=1280,
        height=720,
        resizable=True,
        min_size=(800, 600),
        frameless=True
    )
    api.window = window
    
    # We use a secondary thread to keep injecting the UI if it disappears
    def maintain_ui():
        while True:
            try:
                window.run_js(TOOLBAR_JS)
            except:
                pass
            time.sleep(2)

    threading.Thread(target=maintain_ui, daemon=True).start()
    
    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
    webview.start(user_agent=user_agent)

if __name__ == "__main__":
    start_webview()
