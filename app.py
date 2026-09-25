import os
from flask import Flask, request, jsonify
from pocketoptionapi.stable_api import PocketOption

app = Flask(__name__)

# Remplacez par votre identifiant PHPSESSID de Pocket Option
SSID = "VOTRE_SESSION_SSID_ICI"

@app.route('/', methods=['GET'])
def home():
    return "Bot Pocket Option en ligne !", 200

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json
    if not data:
        return jsonify({"status": "error", "message": "Aucune donnée reçue"}), 400

    action = data.get("action")
    pair = data.get("pair", "EURUSD_otc")
    amount = data.get("amount", 1)
    timeframe = data.get("timeframe", 60)

    try:
        api = PocketOption(SSID)
        api.connect()
        
        if action == "call":
            status, buy_info = api.buy(amount, pair, "call", timeframe)
        elif action == "put":
            status, buy_info = api.buy(amount, pair, "put", timeframe)
        else:
            return jsonify({"status": "error", "message": "Action invalide"}), 400

        return jsonify({"status": "success", "result": buy_info}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
