import requests
import yaml
from flask import Flask, request
import jwt
import django.utils.encoding as encoding
import os
import sqlite3
import subprocess

app = Flask(__name__)

# Exemple 1 : requête HTTP (requests vulnérable)
def fetch_url(url):
    response = requests.get(url, verify=False)  # ❌ SSL verification désactivée
    return response.text

# Exemple 2 : parsing YAML non sécurisé
def parse_yaml(data):
    return yaml.load(data, Loader=yaml.FullLoader)  # ❌ potentielle RCE

# Exemple 3 : JWT vulnérable
def decode_token(token):
    return jwt.decode(token, verify=False)  # ❌ bypass signature

# Exemple 4 : fonction Django importée (version vulnérable)
def encode_data(data):
    return encoding.force_text(data)

# 🔴 SAST 1 : Command Injection
def ping_host(host):
    return subprocess.check_output(f"ping -c 1 {host}", shell=True)

# 🔴 SAST 2 : SQL Injection
def get_user(user_id):
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    query = f"SELECT * FROM users WHERE id = {user_id}"  # ❌ injection
    cursor.execute(query)
    return cursor.fetchall()

# 🔴 SAST 3 : Path Traversal
def read_file(filename):
    with open(f"/tmp/{filename}", "r") as f:  # ❌ traversal possible
        return f.read()

# 🔴 SAST 4 : Hardcoded secret
SECRET_KEY = "super-secret-key"  # ❌ secret exposé

# 🔴 SAST 5 : Unsafe deserialization (pickle)
import pickle
def load_data(data):
    return pickle.loads(data)  # ❌ RCE possible

@app.route("/")
def index():
    url = request.args.get("url", "https://example.com")
    data = fetch_url(url)
    return data

@app.route("/ping")
def ping():
    host = request.args.get("host", "localhost")
    return ping_host(host)

@app.route("/user")
def user():
    user_id = request.args.get("id", "1")
    return str(get_user(user_id))

@app.route("/file")
def file():
    filename = request.args.get("name", "test.txt")
    return read_file(filename)

if __name__ == "__main__":
    app.run(debug=True)  # ❌ debug activé en prod
