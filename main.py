import os
import re
import requests
from flask import Flask, redirect

app = Flask(__name__)

SOURCE_URL = "https://la.drmlive.net/tp/playlist"
USER_AGENT = "TiviMate/4.7.0 (Linux; Android 11; Build/RK3328)"

@app.route('/playlist.mpd')
def get_token_link():
    try:
        headers = {'User-Agent': USER_AGENT}
        response = requests.get(SOURCE_URL, headers=headers, timeout=10)
        response.raise_for_status()
        match = re.search(r'https?://\S*token=\S*', response.text)
        if match:
            url = match.group(0).split('"')[0].split("'")[0].split('<')[0]
            return redirect(url, code=302)
        return "Token not found", 404
    except Exception as e:
        return f"Error: {str(e)}", 500

@app.route('/')
def index():
    return redirect('/playlist.mpd', code=302)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
