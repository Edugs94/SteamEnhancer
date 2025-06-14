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

        if isinstance(data, list) and all(isinstance(i, list) and len(i) == 2 for i in data):
            return jsonify(data)
        else:
            return jsonify({"error": "Formato inesperado"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ✅ NUEVA RUTA para el número de jugadores actuales
@app.route('/currentplayers/<int:appid>', methods=['GET'])
def proxy_current_players(appid):
    url = f'https://api.steampowered.com/ISteamUserStats/GetNumberOfCurrentPlayers/v1/?appid={appid}'
    headers = {'User-Agent': 'Mozilla/5.0'}

    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        return jsonify(response.json())
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
