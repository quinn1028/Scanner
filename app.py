#!/usr/bin/env python

import threading
from flask import Flask, send_from_directory, jsonify
import scan

scan_thread = threading.Thread(target=scan.scan)
scan_thread.daemon = True
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
    serializable_macs = dict(scan.macs_home)
    for mac in serializable_macs:
        if 'led' in serializable_macs[mac]:
            del serializable_macs[mac]['led']
    return jsonify(serializable_macs)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=80)
