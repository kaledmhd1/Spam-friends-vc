from flask import Flask, request, jsonify
import httpx
from concurrent.futures import ThreadPoolExecutor
import random
import time

app = Flask(__name__)

last_sent_cache = {}

def send_friend_request(token, uid):
    url = f"https://add-friend-bngx.vercel.app/add_friend?token={token}&uid={uid}"
    try:
        resp = httpx.get(url, timeout=10)
        if resp.status_code == 200:
            return {"token": token[:20] + "...", "status": "success"}
        else:
            return {"token": token[:20] + "...", "status": f"failed ({resp.status_code})"}
    except httpx.RequestError as e:
        return {"token": token[:20] + "...", "status": f"error ({e})"}

@app.route("/send_like", methods=["GET"])
def send_like():
    player_id = request.args.get("player_id")

    if not player_id:
        return jsonify({"error": "player_id is required"}), 400

    try:
        player_id_int = int(player_id)
    except ValueError:
        return jsonify({"error": "player_id must be an integer"}), 400

    now = time.time()
    last_sent = last_sent_cache.get(player_id_int, 0)
    seconds_since_last = now - last_sent

    if seconds_since_last < 86400:
        remaining = int(86400 - seconds_since_last)
        return jsonify({
            "error": "Requests already sent within last 24 hours",
            "seconds_until_next_allowed": remaining
        }), 429

    # جلب التوكنات من API
    try:
        token_data = httpx.get("https://auto-token-bngx.onrender.com/api/get_jwt", timeout=10).json()
        tokens = token_data.get("tokens", [])
        if not tokens:
            return jsonify({"error": "No tokens found"}), 500
    except Exception as e:
        return jsonify({"error": f"Failed to fetch tokens: {e}"}), 500

    tokens = random.sample(tokens, min(50, len(tokens)))

    results = []

    def worker(token):
        return send_friend_request(token, player_id_int)

    with ThreadPoolExecutor(max_workers=20) as executor:
        futures = [executor.submit(worker, token) for token in tokens]
        for future in futures:
            result = future.result()
            if result:
                results.append(result)

    success_count = sum(1 for r in results if r["status"] == "success")
    failed_count = len(results) - success_count

    last_sent_cache[player_id_int] = now

    return jsonify({
        "player_id": player_id_int,
        "requests_sent": len(results),
        "success_count": success_count,
        "failed_count": failed_count,
        "seconds_until_next_allowed": 86400,
        "details": results
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
