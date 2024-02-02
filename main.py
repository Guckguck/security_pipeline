# app.py
from flask import Flask, request, abort, jsonify
import os
import subprocess
import shlex
import json

app = Flask(__name__)

ALLOWED_COMMANDS = {'ls', 'pwd', 'date'}
COMMON_PASSWORDS = set(line.strip() for line in open('passwords.txt'))

@app.route('/exec', methods=['GET'])
def exec_command():
    # Direkte Ausführung von Benutzereingaben ohne Validierung - FIXING
    command = request.args.get('cmd')
    if command not in ALLOWED_COMMANDS:
        abort(403)
    subprocess.call(shlex.split(command))
    return "Kommando ausgeführt\n"

@app.route('/upload', methods=['POST'])
def upload_file():
    # Unsichere Deserialisierung von Benutzereingaben - FIXING
    file = request.files['file'].read().decode('utf-8')
    try:
        data = json.loads(file)
    except json.JSONDecodeError:
        abort(400, description="Ungültig")
    return "Datei hochgeladen\n"

@app.route('/run', methods=['POST'])
def run_command():
    command = request.form['command']
    # Unsichere Verwendung von os.system für Benutzereingaben - FIXING
    if command not in ALLOWED_COMMANDS:
        abort(403)
    subprocess.call(shlex.split(command))
    return "Kommando ausgeführt\n"

# Auf Passwörter überprüfen
@app.route('/register', methods=['POST'])
def register():
    username = request.form['username']
    password = request.form['password']
    if password in COMMON_PASSWORDS:
        abort(400, description="Passwort ist schwach")
    return "Benutzer registriert\n"

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000)
