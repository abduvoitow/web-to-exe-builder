import webview
import sys
import os

# These will be replaced by the GitHub Action during build
TARGET_URL = "https://google.com"
APP_NAME = "WebToEXE App"

# Optimized Injection Script using MutationObserver (Fast & Stable)
INJECTION_JS = f"""
(function() {{
    const TOOLBAR_ID = 'pywebview-topbar';
    const STYLE_ID = 'pywebview-styles';
    
    const css = `
        #${{TOOLBAR_ID}} {{
            position: fixed !important; top: 0 !important; left: 0 !important;
            width: 100% !important; height: 40px !important;
            background: rgba(20, 20, 20, 0.98) !important;
            backdrop-filter: blur(12px) !important;
            -webkit-backdrop-filter: blur(12px) !important;
            display: flex !important; align-items: center !important;
            justify-content: space-between !important; padding: 0 15px !important;
            color: #fff !important; z-index: 2147483647 !important;
            box-sizing: border-box !important; border-bottom: 1px solid rgba(255, 255, 255, 0.1) !important;
            font-family: -apple-system, system-ui, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif !important;
            user-select: none !important;
        }}
        .pywebview-drag-region {{
            position: absolute !important; width: 100% !important; height: 100% !important;
            top: 0 !important; left: 0 !important; z-index: -1 !important;
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
        .window-controls {{ display: flex !important; gap: 12px !important; z-index: 10 !important; padding-right: 15px !important; }}
        .win-btn {{ width: 12px !important; height: 12px !important; border-radius: 50% !important; cursor: pointer !important; border: none !important; outline: none !important; }}
        .close {{ background: #ff5f56 !important; }}
        .min {{ background: #ffbd2e !important; }}
        .max {{ background: #27c93f !important; }}
        html, body {{ padding-top: 40px !important; margin-top: 0 !important; }}
    `;

    const html = `
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

    function inject() {{
        if (document.getElementById(TOOLBAR_ID)) return;
        if (!document.body) return;

        // Styles
        if (!document.getElementById(STYLE_ID)) {{
            const style = document.createElement('style');
            style.id = STYLE_ID;
            style.innerHTML = css;
            document.head.appendChild(style);
        }}

        // Toolbar
        const bar = document.createElement('div');
        bar.id = TOOLBAR_ID;
        bar.className = 'pywebview-drag-region';
        bar.innerHTML = html;
        document.body.appendChild(bar);
        document.body.style.paddingTop = '40px';
    }}

    // Use MutationObserver for high-speed persistent injection
    const observer = new MutationObserver((mutations) => {{
        if (!document.getElementById(TOOLBAR_ID)) inject();
    }});
    
    observer.observe(document.documentElement, {{ childList: true, subtree: true }});
    
    // Initial calls
    if (document.readyState === 'loading') {{
        document.addEventListener('DOMContentLoaded', inject);
    }} else {{
        inject();
    }}
}})();
"""

class API:
    def __init__(self):
        self.window = None
    def close(self): self.window.destroy()
    def minimize(self): self.window.minimize()
    def maximize(self): self.window.toggle_fullscreen()

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
        frameless=True,
        background_color='#000000'
    )
    api.window = window
    
    # Inject UI once on load, the MutationObserver inside INJECTION_JS handles the rest.
    window.events.loaded += lambda: window.run_js(INJECTION_JS)
    
    # Standard Chrome User-Agent
    ua = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
    webview.start(user_agent=ua)

if __name__ == "__main__":
    start_webview()
