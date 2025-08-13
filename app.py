from urllib.parse import urlparse, urlunparse

from flask import Flask, redirect, render_template, request


app = Flask(__name__)


APP_STORE_HTTPS_URL = "https://apps.apple.com/us/app/thrifty-ai-profit-identifier/id6749215897"


def is_in_app_browser(user_agent: str) -> bool:
    if not user_agent:
        return False
    ua = user_agent.lower()
    indicators = [
        "musical_ly_",  # legacy TikTok
        "bytedancewebview",  # TikTok/CapCut webview
        "tiktok",  # general TikTok UA
        "ttwebview",  # TikTok webview
        "fban",  # Facebook app
        "fbav",  # Facebook app
        "instagram",
        "messenger",
        "snapchat",
        "pinterest",
        "wechat",
        "weibo",
        "line/",
    ]
    return any(token in ua for token in indicators)


def ensure_https(url: str) -> str:
    try:
        parsed = urlparse(url)
        if parsed.scheme in ("http", "https"):
            return urlunparse(parsed._replace(scheme="https"))
    except Exception:
        pass
    return APP_STORE_HTTPS_URL


@app.route("/app", methods=["GET"])
def appstore_redirect():
    user_agent = request.headers.get("User-Agent", "")
    if is_in_app_browser(user_agent):
        # Show instruction page to escape in-app browser; keep target available in template if needed
        return render_template("appstore_blocked.html", target_url=APP_STORE_HTTPS_URL)

    # Outside in-app browsers → redirect to App Store
    app_store_url = ensure_https(APP_STORE_HTTPS_URL)
    return redirect(app_store_url, code=302)


@app.get("/")
def root():
    # Keep existing static behavior if served by Flask: forward to your bridge page target
    return redirect("https://thrifty-tau.vercel.app/", code=302)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)


