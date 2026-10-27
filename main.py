import os
import re
import requests
from flask import Flask, Response

app = Flask(name)

SOURCE_URL = "https://la.drmlive.net/tp/playlist"
USER_AGENT = "TiviMate/4.7.0 (Linux; Android 11; Build/RK3328)"

@app.route('/')
def get_token_link():
    try:
        headers = {'User-Agent': USER_AGENT}
        response = requests.get(SOURCE_URL, headers=headers, timeout=10)
        response.raise_for_status()
        match = re.search(r'https?://[^\s"'<>]+token=[^\s"'<>]+', response.text)
        if match:
            return Response(match.group(0), mimetype='text/plain')
        return "Error: Token not found", 404
    except Exception as e:
        return f"Error: {str(e)}", 500

if name == "main":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
