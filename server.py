import json

from flask import Flask
from gpu import parse_nvidia_smi


app = Flask(__name__)

@app.route('/')
def index():
    return json.dumps(parse_nvidia_smi())

if __name__ == '__main__':
    app.run(host='0.0.0.0', port='3333')
