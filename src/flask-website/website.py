from flask import Flask, render_template, request, redirect, url_for
import requests

app = Flask(__name__)
app.secret_key = "secret_tp_key"

# URL de votre API (port 5001)
API_URL = "http://localhost:5001"

# ==========================================
# ROUTES D'ACCUEIL ET IDENTITÉ
# ==========================================

@app.route("/")
def start(): 
    return render_template('start.html')

# Modifiez cette ligne dans votre fichier website.py
@app.route('/login', methods=['GET', 'POST']) 
def login():
    if request.method == 'POST':
        # Logique pour traiter le formulaire (appel à l'API)
        username = request.form.get('username')
        password = request.form.get('password')
        # ... votre code d'appel API ...
        return redirect(url_for('start'))
    
    # Si c'est un GET, on affiche simplement le formulaire
    return render_template('login.html')


@app.route('/list_profile')
def list_profile():
    # Route statique pour l'exemple, ou appel vers l'API si elle gérait une liste d'utilisateurs
    return render_template('profile_list.html')

@app.route('/profile/<username>')
def profile(username):
    response = requests.get(f"{API_URL}/identity/{username}")
    if response.status_code == 200:
        user_data = response.json()
        return render_template('profile_detail.html', user=user_data)
    return "Utilisateur introuvable", 404

@app.route('/list_all')
def list_all():
    # Récupère toutes les configurations en même temps
    ws_data = requests.get(f"{API_URL}/config/ws").json()
    rp_data = requests.get(f"{API_URL}/config/rp").json()
    lb_data = requests.get(f"{API_URL}/config/lb").json()
    return render_template('list_all.html', ws_list=ws_data, rp_list=rp_data, lb_list=lb_data)


# ==========================================
# PARTIE WEBSERVER (ws)
# ==========================================
@app.route('/ws/list')
def list_ws():
    response = requests.get(f"{API_URL}/config/ws")
    return render_template('serveur-web/ws_list.html', servers=response.json())

@app.route('/ws/<id>')
def detail_ws(id):
    response = requests.get(f"{API_URL}/config/ws/{id}")
    if response.status_code == 200:
        return render_template('serveur-web/ws_detail.html', server=response.json())
    return "Serveur Web introuvable", 404

@app.route('/ws/create', methods=['GET', 'POST'])
def create_ws():
    if request.method == 'POST':
        new_data = {
            "name": request.form.get('name'),
            "ip": request.form.get('ip'),
            "port": request.form.get('port'),
            "server_name": request.form.get('serveur_name')
        }
        requests.post(f"{API_URL}/config/ws", json=new_data)
        return redirect(url_for('list_ws'))
    return render_template('serveur-web/ws_form.html')

@app.route('/ws/delete/<id>')
def delete_ws(id):
    requests.delete(f"{API_URL}/config/ws/{id}")
    return redirect(url_for('list_ws'))


# ==========================================
# PARTIE REVERSE PROXY (rp)
# ==========================================
@app.route('/rp/list')
def list_rp():
    response = requests.get(f"{API_URL}/config/rp")
    return render_template('reverse-proxy/rp_list.html', servers=response.json())

@app.route('/rp/<id>')
def detail_rp(id):
    response = requests.get(f"{API_URL}/config/rp/{id}")
    if response.status_code == 200:
        return render_template('reverse-proxy/rp_detail.html', server=response.json())
    return "Reverse Proxy introuvable", 404

@app.route('/rp/create', methods=['GET', 'POST'])
def create_rp():
    if request.method == 'POST':
        new_data = {
            "name": request.form.get('name'),
            "target_ip": request.form.get('target_ip'),
            "target_port": request.form.get('target_port'),
            "domain": request.form.get('domain')
        }
        requests.post(f"{API_URL}/config/rp", json=new_data)
        return redirect(url_for('list_rp'))
    return render_template('reverse-proxy/rp_form.html')

@app.route('/rp/delete/<id>')
def delete_rp(id):
    requests.delete(f"{API_URL}/config/rp/{id}")
    return redirect(url_for('list_rp'))


# ==========================================
# PARTIE LOAD BALANCER (lb)
# ==========================================
@app.route('/lb/list')
def list_lb():
    response = requests.get(f"{API_URL}/config/lb")
    return render_template('load-balancers/lb_list.html', servers=response.json())

@app.route('/lb/<id>')
def detail_lb(id):
    response = requests.get(f"{API_URL}/config/lb/{id}")
    if response.status_code == 200:
        return render_template('load-balancers/lb_detail.html', server=response.json())
    return "Load Balancer introuvable", 404

@app.route('/lb/create', methods=['GET', 'POST'])
def create_lb():
    if request.method == 'POST':
        new_data = {
            "name": request.form.get('name'),
            "algorithm": request.form.get('algorithm'), # ex: round-robin, least_conn
            "backend_servers": request.form.get('backend_servers') # Liste d'IPs séparées par des virgules par ex.
        }
        requests.post(f"{API_URL}/config/lb", json=new_data)
        return redirect(url_for('list_lb'))
    return render_template('load-balancers/lb_form.html')

@app.route('/lb/delete/<id>')
def delete_lb(id):
    requests.delete(f"{API_URL}/config/lb/{id}")
    return redirect(url_for('list_lb'))


if __name__ == '__main__':
    # Le WebGenerator tourne sur le port 5000 par défaut
    app.run(port=5000, debug=True)