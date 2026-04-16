from flask import Flask, jsonify, request
import json
import os
import uuid

app = Flask(__name__)

# Fichier JSON de base de données
DB_FILE = 'db_servers.json'

# ==========================================
# GESTION DE LA BASE DE DONNÉES (JSON)
# ==========================================
def read_db():
    """Lit le fichier JSON et retourne son contenu. Crée la structure si elle n'existe pas."""
    if not os.path.exists(DB_FILE):
        return {"ws": [], "rp": [], "lb": []}
    with open(DB_FILE, 'r') as f:
        return json.load(f)

def write_db(data):
    """Sauvegarde les données modifiées dans le fichier JSON."""
    with open(DB_FILE, 'w') as f:
        json.dump(data, f, indent=4)


# ==========================================
# ROUTES D'IDENTITÉ (Mock pour le TP)
# ==========================================

@app.route("/")
def hello():
    return "Hello, API!"


# Dans api.py
@app.route('/login', methods=['GET'])
def api_login():
    # On utilise request.args pour un GET
    username = request.args.get('username')
    password = request.args.get('password')
    # ... vérification ...
    return jsonify({"status": "success"})

@app.route('/identity', methods=['GET'])
def get_identity():
    return jsonify({"status": "success", "username": "admin", "role": "administrator"})

@app.route('/identity/<username>', methods=['GET'])
def get_user_identity(username):
    return jsonify({"status": "success", "username": username})



# ==========================================
# PARTIE LOAD BALANCER (lb)
# ==========================================
@app.route('/config/lb', methods=['GET'])
def get_lb_list():
    db = read_db()
    return jsonify(db["lb"])

@app.route('/config/lb/<id>', methods=['GET'])
def get_lb_by_id(id):
    db = read_db()
    server = next((item for item in db["lb"] if item.get("id") == id), None)
    if server:
        return jsonify(server)
    return jsonify({"error": "Load Balancer non trouvé"}), 404

@app.route('/config/lb', methods=['POST'])
def create_lb():
    data = request.json
    data['id'] = str(uuid.uuid4())
    db = read_db()
    db["lb"].append(data)
    write_db(db)
    return jsonify({"status": "success", "message": "Load Balancer ajouté", "id": data['id']}), 201

@app.route('/config/lb/<id>', methods=['DELETE'])
def delete_lb(id):
    db = read_db()
    initial_length = len(db["lb"])
    db["lb"] = [item for item in db["lb"] if item.get("id") != id]
    if len(db["lb"]) < initial_length:
        write_db(db)
        return jsonify({"status": "success", "message": "Load Balancer supprimé"})
    return jsonify({"error": "Load Balancer non trouvé"}), 404



# ==========================================
# PARTIE REVERSE PROXY (rp)
# ==========================================
@app.route('/config/rp', methods=['GET'])
def get_rp_list():
    db = read_db()
    return jsonify(db["rp"])

@app.route('/config/rp/<id>', methods=['GET'])
def get_rp_by_id(id):
    db = read_db()
    server = next((item for item in db["rp"] if item.get("id") == id), None)
    if server:
        return jsonify(server)
    return jsonify({"error": "Reverse Proxy non trouvé"}), 404

@app.route('/config/rp', methods=['POST'])
def create_rp():
    data = request.json
    data['id'] = str(uuid.uuid4())
    db = read_db()
    db["rp"].append(data)
    write_db(db)
    return jsonify({"status": "success", "message": "Reverse Proxy ajouté", "id": data['id']}), 201

@app.route('/config/rp/<id>', methods=['DELETE'])
def delete_rp(id):
    db = read_db()
    initial_length = len(db["rp"])
    db["rp"] = [item for item in db["rp"] if item.get("id") != id]
    if len(db["rp"]) < initial_length:
        write_db(db)
        return jsonify({"status": "success", "message": "Reverse Proxy supprimé"})
    return jsonify({"error": "Reverse Proxy non trouvé"}), 404


# ==========================================
# PARTIE WEBSERVER (ws)
# ==========================================
@app.route('/config/ws', methods=['GET'])
def get_ws_list():
    db = read_db()
    return jsonify(db["ws"])

@app.route('/config/ws/<id>', methods=['GET'])
def get_ws_by_id(id):
    db = read_db()
    # Cherche le serveur correspondant à l'ID
    server = next((item for item in db["ws"] if item.get("id") == id), None)
    if server:
        return jsonify(server)
    return jsonify({"error": "Serveur Web non trouvé"}), 404

@app.route('/config/ws', methods=['POST'])
def create_ws():
    data = request.json
    # Génération d'un ID unique pour le nouveau serveur
    data['id'] = str(uuid.uuid4())
    db = read_db()
    db["ws"].append(data)
    write_db(db)
    return jsonify({"status": "success", "message": "Serveur Web ajouté", "id": data['id']}), 201

@app.route('/config/ws/<id>', methods=['DELETE'])
def delete_ws(id):
    db = read_db()
    initial_length = len(db["ws"])
    # Filtre la liste pour enlever l'élément avec l'ID correspondant
    db["ws"] = [item for item in db["ws"] if item.get("id") != id]
    if len(db["ws"]) < initial_length:
        write_db(db)
        return jsonify({"status": "success", "message": "Serveur Web supprimé"})
    return jsonify({"error": "Serveur Web non trouvé"}), 404



if __name__ == '__main__':
    # Le port 5001 est utilisé pour FLASK-API
    app.run(port=5001, debug=True)