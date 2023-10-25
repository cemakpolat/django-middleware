# auth_service.py
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/live', methods=['GET'])
def get_liveness():
    return jsonify({"message": "live"})

@app.route('/canBeAuthorized', methods=['GET'])
def get_statistics():
    # Check headers for authentication
    headers = request.headers
    if 'Authorization' not in headers:
        return jsonify({"message": "failure"}), 401

    return jsonify({"message": "ok"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
