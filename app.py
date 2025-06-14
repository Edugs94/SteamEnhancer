from flask import Flask, jsonify
import requests
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/steamcharts/<int:appid>', methods=['GET'])
def proxy_steamcharts(appid):
    url = f'https://steamcharts.com/app/{appid}/chart-data.json'
    headers = {'User-Agent': 'Mozilla/5.0'}

    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        data = response.json()

        # Asegurarse de que es un array válido de [timestamp, valor]
        if isinstance(data, list) and all(isinstance(i, list) and len(i) == 2 for i in data):
            return jsonify(data)  # ✅ devuelves el array directamente
        else:
            return jsonify({"error": "Formato inesperado"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500
