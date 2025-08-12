from flask import Flask, request, jsonify
import httpx
from concurrent.futures import ThreadPoolExecutor, as_completed
import threading

app = Flask(__name__)

lock = threading.Lock()

def send_friend_request(token, uid):
    url = f"https://add-friend-bngx.vercel.app/add_friend?token={token}&uid={uid}"
    headers = {
        'User-Agent': 'Dalvik/2.1.0 (Linux; U; Android 9; ASUS_Z01QD Build/PI)',
        'Connection': 'Keep-Alive',
        'Expect': '100-continue',
    }
    try:
        resp = httpx.get(url, headers=headers, timeout=10)
        return resp.status_code == 200
    except httpx.RequestError:
        return False

@app.route("/send_friend", methods=["GET"])
def send_friend():
    player_id = request.args.get("player_id")

    if not player_id:
        return jsonify({"error": "player_id is required"}), 400

    try:
        player_id_int = int(player_id)
    except ValueError:
        return jsonify({"error": "player_id must be an integer"}), 400

    # جلب التوكنات من API خارجي
    try:
        token_data = httpx.get("https://auto-token-bngx.onrender.com/api/get_jwt", timeout=15).json()
        tokens = token_data.get("tokens", [])
        if not tokens:
            return jsonify({"error": "No tokens found"}), 500
    except Exception as e:
        return jsonify({"error": f"Failed to fetch tokens: {e}"}), 500

    results = []
    requests_sent = 0
    max_successful = 40
    token_index = 0

    with ThreadPoolExecutor(max_workers=40) as executor:
        futures = {}
        while requests_sent < max_successful and token_index < len(tokens):
            # إرسال دفعة جديدة من الطلبات حتى نصل إلى 40
            while len(futures) < 40 and token_index < len(tokens) and requests_sent + len(futures) < max_successful:
                token = tokens[token_index]
                token_index += 1
                futures[executor.submit(send_friend_request, token, player_id_int)] = token

            # انتظار النتائج
            done, _ = as_completed(futures), futures.copy()
            for future in list(futures.keys()):
                token = futures[future]
                try:
                    success = future.result()
                except Exception:
                    success = False

                with lock:
                    if success:
                        requests_sent += 1
                        results.append({"token": token[:20] + "...", "status": "success"})
                    else:
                        results.append({"token": token[:20] + "...", "status": "failed"})

                del futures[future]

                if requests_sent >= max_successful:
                    break

    return jsonify({
        "player_id": player_id_int,
        "friend_requests_sent": requests_sent,
        "details": results
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
