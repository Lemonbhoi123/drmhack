from flask import Flask, redirect
import requests
import re
import os

app = Flask(__name__)
SOURCE_URL = "https://la.drmlive.net/tp/playlist"
USER_AGENT = 'TiviMate/4.7.0 (Linux; Android 11)'

@app.route('/get-token')
def get_token():
    try:
        headers = {'User-Agent': USER_AGENT}
        response = requests.get(SOURCE_URL, headers=headers, timeout=10)
        match = re.search(r'https://mix\.drmlive\.net/mix/actchaljabsdk\.mpd\?token=[^ \n\r]+', response.text)
        if match:
            return redirect(match.group(0))
        return "Token not found!", 404
    except Exception as e:
        return f"Error: {str(e)}", 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)