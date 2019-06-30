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
    serializable_macs = {}
    for mac in scan.macs_home:
        serializable_macs[mac] = {
                'GPIO_pin': scan.macs_home[mac]['GPIO_pin'],
                'connected': scan.macs_home[mac]['connected'] if 'connected' in scan.macs_home[mac] else False,
                'house': scan.macs_home[mac]['house'],
                'last_seen': scan.macs_home[mac]['last_seen'],
                'name': scan.macs_home[mac]['name'],
        }

    return jsonify(serializable_macs)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=80)
