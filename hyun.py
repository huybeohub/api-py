from flask import Flask, jsonify, request
import requests
import time

app = Flask(__name__)

PLACE_ID = 2753915549  # Blox Fruits main world

def get_servers(cursor=""):
    """Gọi Roblox API lấy servers public"""
    url = f"https://games.roblox.com/v1/games/{PLACE_ID}/servers/Public?sortOrder=Asc&limit=100"
    if cursor:
        url += f"&cursor={cursor}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    return None

@app.route('/api/servers', methods=['GET'])
def servers():
    boss = request.args.get('boss', '').lower()
    servers = []
    cursor = ""
    
    while True:
        data = get_servers(cursor)
        if not data or not data.get('data'):
            break
        for server in data['data']:
            # Giả lập filter Rip Indra (thực tế check in-game hoặc external service)
            if boss == 'rip_indra' and server['playing'] > 0:  # Filter server active
                servers.append({
                    'jobId': server['id'],
                    'playing': server['playing'],
                    'maxPlayers': server['maxPlayers'],
                    'ping': server.get('ping', 0),
                    'hasBoss': f"Rip Indra suspected (check in-game)"  # Placeholder
                })
        cursor = data.get('nextPageCursor', '')
        if not cursor:
            break
        time.sleep(0.1)  # Rate limit
    
    return jsonify({
        'servers': servers[:10],  # Top 10
        'total': len(servers),
        'timestamp': int(time.time())
    })

@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'OK'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
