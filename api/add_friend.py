from flask import Flask, request, jsonify
import httpx
from concurrent.futures import ThreadPoolExecutor
import random
import time
import threading

app = Flask(__name__)

last_sent_cache = {}
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
        if resp.status_code == 200:
            return {"token": token[:20] + "...", "status": "success"}
        else:
            return {"token": token[:20] + "...", "status": f"failed ({resp.status_code})"}
    except httpx.RequestError as e:
        return {"token": token[:20] + "...", "status": f"error ({e})"}

@app.route("/send_friend", methods=["GET"])
def send_friend():
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

    if seconds_since_last < 86400:  # 24 ساعة
        remaining = int(86400 - seconds_since_last)
        return jsonify({
            "error": "Friend requests already sent within last 24 hours",
            "seconds_until_next_allowed": remaining
        }), 429

    # جلب التوكنات من API خارجي
    try:
        token_data = httpx.get("https://auto-token-bngx.onrender.com/api/get_jwt", timeout=15).json()
        tokens = token_data.get("tokens", [])
        if not tokens:
            return jsonify({"error": "No tokens found"}), 500
        random.shuffle(tokens)  # خلط التوكنات عشوائياً
    except Exception as e:
        return jsonify({"error": f"Failed to fetch tokens: {e}"}), 500

    results = []
    failed_tokens = set()
    requests_sent = 0
    max_successful = 40  # نريد 40 طلب ناجح فقط

    def worker(token):
        nonlocal requests_sent
        if token in failed_tokens:
            return None

        with lock:
            if requests_sent >= max_successful:
                return None

        res = send_friend_request(token, player_id_int)

        if "failed" in res["status"] or "error" in res["status"]:
            failed_tokens.add(token)
            return None

        with lock:
            if requests_sent < max_successful:
                requests_sent += 1
                return res
            else:
                return None

    with ThreadPoolExecutor(max_workers=40) as executor:
        futures = []
        # لأننا نريد 40 طلب ناجح، نشغل كل التوكنات حتى نصل للعدد المطلوب
        for token in tokens:
            futures.append(executor.submit(worker, token))
        # ننتظر النتائج مع كسر الحلقة إذا وصلنا للعدد المطلوب
        for future in futures:
            result = future.result()
            if result:
                results.append(result)
            with lock:
                if requests_sent >= max_successful:
                    break

    last_sent_cache[player_id_int] = now

    return jsonify({
        "player_id": player_id_int,
        "friend_requests_sent": requests_sent,
        "seconds_until_next_allowed": 86400,
        "details": results
    })
