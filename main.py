import os
import re
import requests
from flask import Flask, redirect, make_response

app = Flask(__name__)

SOURCE_URL = "https://la.drmlive.net/tp/playlist"
USER_AGENT = "TiviMate/4.7.0 (Linux; Android 11; Build/RK3328)"

@app.route('/')
def redirect_to_token():
    try:
        headers = {'User-Agent': USER_AGENT}
        response = requests.get(SOURCE_URL, headers=headers, timeout=10)
        response.raise_for_status()
        match = re.search(r'https?://[^\s"\'<>]+token=[^\s"\'<>]+', response.text)
        if match:
            token_url = match.group(0)
            resp = make_response(redirect(token_url, code=302))
            resp.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
            resp.headers['Pragma'] = 'no-cache'
            resp.headers['Expires'] = '0'
            return resp
        return "Token not found", 404
    except Exception as e:
        return f"Error: {str(e)}", 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
