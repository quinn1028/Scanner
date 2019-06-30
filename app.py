import threading
from flask import Flask, send_from_directory, jsonify
import scan

scan_thread = threading.Thread(target=scan.scan, daemon=True)
scan_thread.start()

app = Flask(__name__)

@app.route("/", methods=['GET'])
def main():
    return send_from_directory('assets', 'index.html')

@app.route("/assets/<path:path>", methods=['GET'])
def house(path):
    return send_from_directory('assets', path)

@app.route("/users", methods=['GET'])
def users():
    return jsonify(scan.macs_home)
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=80)