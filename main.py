import webview
import sys
import os

# These will be replaced by the GitHub Action during build
TARGET_URL = "https://google.com"
APP_NAME = "WebToEXE App"

class API:
    def __init__(self, window): 
        self.window = window
    def close(self): 
        self.window.destroy()
    def minimize(self): 
        self.window.minimize()
    def maximize(self): 
        self.window.toggle_fullscreen()

def start_webview():
    # We use a global or closure reference for window
    window = webview.create_window(
        APP_NAME, 
        url=TARGET_URL,
        width=1280, height=720,
        resizable=True, frameless=True
    )
    
    api = API(window)
    window.expose(api.close, api.minimize, api.maximize)

    def on_loaded():
        # Inject the custom TopBar into the native page every time it loads
        js_code = f"""
        (function() {{
            if (document.getElementById('__pywebview_top_bar')) return;
            
            var bar = document.createElement('div');
            bar.id = '__pywebview_top_bar';
            bar.innerHTML = `
                <div style="display: flex; gap: 15px; -webkit-app-region: no-drag;">
                    <div onclick="window.history.back()" style="cursor: pointer; opacity: 0.7; transition: 0.2s;" onmouseover="this.style.opacity=1" onmouseout="this.style.opacity=0.7"><svg width="18" height="18" viewBox="0 0 24 24" fill="#fff"><path d="M15.41 7.41L14 6l-6 6 6 6 1.41-1.41L10.83 12z"/></svg></div>
                    <div onclick="window.history.forward()" style="cursor: pointer; opacity: 0.7; transition: 0.2s;" onmouseover="this.style.opacity=1" onmouseout="this.style.opacity=0.7"><svg width="18" height="18" viewBox="0 0 24 24" fill="#fff"><path d="M10 6L8.59 7.41 13.17 12l-4.58 4.59L10 18l6-6z"/></svg></div>
                    <div onclick="window.location.reload()" style="cursor: pointer; opacity: 0.7; transition: 0.2s;" onmouseover="this.style.opacity=1" onmouseout="this.style.opacity=0.7"><svg width="18" height="18" viewBox="0 0 24 24" fill="#fff"><path d="M17.65 6.35C16.2 4.9 14.21 4 12 4c-4.42 0-7.99 3.58-7.99 8s3.57 8 7.99 8c3.73(0 6.84-2.55 7.73-6h-2.08c-.82 2.33-3.04 4-5.65 4-3.31 0-6-2.69-6-6s2.69-6 6-6c1.66 0 3.14.69 4.22 1.78L13 11h7V4l-2.35 2.35z"/></svg></div>
                </div>
                <div style="position: absolute; left: 50%; transform: translateX(-50%); font-size: 13px; font-weight: 600; color: rgba(255, 255, 255, 0.9); pointer-events: none;">{APP_NAME}</div>
                <div style="display: flex; gap: 12px; -webkit-app-region: no-drag;">
                    <div onclick="window.pywebview.api.minimize()" style="width: 12px; height: 12px; border-radius: 50%; cursor: pointer; background: #ffbd2e;"></div>
                    <div onclick="window.pywebview.api.maximize()" style="width: 12px; height: 12px; border-radius: 50%; cursor: pointer; background: #27c93f;"></div>
                    <div onclick="window.pywebview.api.close()" style="width: 12px; height: 12px; border-radius: 50%; cursor: pointer; background: #ff5f56;"></div>
                </div>
            `;
            
            bar.style.position = 'fixed';
            bar.style.top = '0';
            bar.style.left = '0';
            bar.style.width = '100%';
            bar.style.height = '40px';
            bar.style.background = 'rgba(25, 25, 25, 0.98)';
            bar.style.backdropFilter = 'blur(15px)';
            bar.style.display = 'flex';
            bar.style.alignItems = 'center';
            bar.style.justifyContent = 'space-between';
            bar.style.padding = '0 15px';
            bar.style.boxSizing = 'border-box';
            bar.style.zIndex = '2147483647';
            bar.style.webkitAppRegion = 'drag';
            bar.style.borderBottom = '1px solid rgba(255, 255, 255, 0.1)';
            bar.style.fontFamily = '-apple-system, sans-serif';
            
            document.body.appendChild(bar);
            
            // Push content down slightly to make room for the bar
            const style = document.createElement('style');
            style.innerHTML = `
                body {{ padding-top: 40px !important; }}
                html {{ scroll-padding-top: 40px !important; }}
                /* Attempt to push common fixed headers down */
                header, nav, .navbar, .topbar, .top-bar {{ margin-top: 40px !important; }}
            `;
            document.head.appendChild(style);
        }})();
        """
        try:
            window.evaluate_js(js_code)
        except Exception:
            pass
            
    window.events.loaded += on_loaded

    webview.start(user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36')

if __name__ == "__main__":
    start_webview()
