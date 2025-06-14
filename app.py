from flask import Flask, jsonify
import requests
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Habilita CORS

@app.route('/steamcharts/<int:appid>', methods=['GET'])
def proxy_steamcharts(appid):
    url = f'https://steamcharts.com/app/{appid}/chart-data.json'
    headers = {'User-Agent': 'Mozilla/5.0'}

    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        return jsonify({"data": response.json()})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run()
