import os
import re
import requests
from flask import Flask, redirect

app = Flask(__name__)

SOURCE_URL = "https://la.drmlive.net/tp/playlist"
USER_AGENT = "TiviMate/4.7.0 (Linux; Android 11)"

@app.route('/')
def redirect_to_token():
    try:
        headers = {'User-Agent': USER_AGENT}
        response = requests.get(SOURCE_URL, headers=headers, timeout=10)
        response.raise_for_status()
        match = re.search(r'https?://[^\s"\'<>]+token=[^\s"\'<>]+', response.text)
        if match:
            return redirect(match.group(0))
        return "Token not found", 404
    except Exception as e:
        return str(e), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
