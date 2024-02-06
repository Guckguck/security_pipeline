from flask import Flask, request, abort, json
import subprocess

app = Flask(__name__)

@app.route('/exec', methods=['GET'])
def exec_command():
    # Direkte Ausführung von Benutzereingaben ohne Validierung - FIXING
    command = request.args.get('cmd')
    if not command:
        abort(400, "Invalider Befehl")
    subprocess.run(command, shell=False)
    return "Kommando ausgeführt\n"

@app.route('/upload', methods=['POST'])
def upload_file():
    # Unsichere Deserialisierung von Benutzereingaben - FIXING
    file = request.files['file'].read()
    try:
        json.loads(file.decode('utf-8'))
    except json.JSONDecodeError:
        abort(400, "Invalides Format")
    return "Datei hochgeladen\n"

@app.route('/run', methods=['POST'])
def run_command():
    command = request.form['command']
    # Unsichere Verwendung von os.system für Benutzereingaben - FIXING
    if not command:
        abort(400, "Invalider Befehl")
    subprocess.run(command.split(), shell=False)
    return "Kommando ausgeführt\n"


if __name__ == '__main__':
    app.run(debug=False, host='127.0.0.1', port=5000)