import requests
import yaml
from flask import Flask, request
import jwt
import django.utils.encoding as encoding

app = Flask(__name__)

# Exemple 1 : requête HTTP (requests vulnérable)
def fetch_url(url):
    response = requests.get(url, verify=False)  # mauvaise pratique
    return response.text

# Exemple 2 : parsing YAML non sécurisé
def parse_yaml(data):
    return yaml.load(data, Loader=yaml.FullLoader)

# Exemple 3 : JWT vulnérable
def decode_token(token):
    return jwt.decode(token, verify=False)

# Exemple 4 : fonction Django importée (version vulnérable)
def encode_data(data):
    return encoding.force_text(data)

@app.route("/")
def index():
    url = request.args.get("url", "https://example.com")
    data = fetch_url(url)
    return data

if __name__ == "__main__":
    app.run(debug=True)
