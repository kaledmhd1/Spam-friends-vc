from flask import Flask, request, jsonify
import requests
import random
from concurrent.futures import ThreadPoolExecutor, wait, FIRST_COMPLETED
from byte import Encrypt_ID, encrypt_api

app = Flask(__name__)

def send_friend_request(token, uid):
    try:
        uid = int(uid)
        id_encrypted = Encrypt_ID(uid)
        data0 = "08c8b5cfea1810" + id_encrypted + "18012008"
        data = bytes.fromhex(encrypt_api(data0))

        url = "https://clientbp.common.ggbluefox.com/RequestAddingFriend"
        headers = {
            'User-Agent': 'Dalvik/2.1.0 (Linux; U; Android 9; ASUS_Z01QD Build/PI)',
            'Connection': 'Keep-Alive',
            'Expect': '100-continue',
            'Authorization': f'Bearer {token}',
            'X-Unity-Version': '2018.4.11f1',
            'X-GA': 'v1 1',
            'ReleaseVersion': 'OB50',
            'Content-Type': 'application/x-www-form-urlencoded',
        }

        response = requests.post(url, headers=headers, data=data, verify=False)
        if response.status_code == 200:
            return True, response.text
        else:
            return False, response.text
    except Exception as e:
        return False, str(e)

@app.route("/add_friend", methods=["GET"])
def add_friend():
    uid = request.args.get("uid")
    if not uid:
        return jsonify({"error": "Missing uid"}), 400

    try:
        tokens_resp = requests.get("https://auto-token-bngx.onrender.com/api/get_jwt")
        tokens_resp.raise_for_status()
        tokens_json = tokens_resp.json()
        tokens_list = tokens_json.get("tokens", [])
        if not tokens_list:
            return jsonify({"error": "No tokens found"}), 500
    except Exception as e:
        return jsonify({"error": f"Failed to get tokens: {str(e)}"}), 500

    max_success = 100
    max_workers = 40
    successful_requests = 0

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = set()
        for _ in range(max_workers):
            token = random.choice(tokens_list)
            futures.add(executor.submit(send_friend_request, token, uid))

        while futures and successful_requests < max_success:
            done, futures = wait(futures, return_when=FIRST_COMPLETED)
            for future in done:
                try:
                    success, _ = future.result()
                    if success:
                        successful_requests += 1
                        if successful_requests >= max_success:
                            break
                    if successful_requests < max_success:
                        token = random.choice(tokens_list)
                        futures.add(executor.submit(send_friend_request, token, uid))
                except Exception:
                    if successful_requests < max_success:
                        token = random.choice(tokens_list)
                        futures.add(executor.submit(send_friend_request, token, uid))

    return jsonify({"status": "done", "successful_requests": successful_requests})


def handler(request, context=None):
    return app(request.environ, context)
