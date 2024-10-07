import ctypes
import json
import os
import time
import random
import threading
import re
import sys
import datetime

try:
    import pystyle
    import colorama
    import tls_client
    import httpx
    import user_agent
except ModuleNotFoundError:
    os.system("pip install pystyle colorama tls_client httpx user_agent")

from pystyle import Write, System, Colorate, Colors
from colorama import Fore, Style, init

# Color definitions
red = Fore.RED
yellow = Fore.YELLOW
green = Fore.GREEN
blue = Fore.BLUE
reset = Fore.RESET
magenta = Fore.MAGENTA

success = 0
failed = 0
generated_agents = 0
total = 1

start = time.time()
ctypes.windll.kernel32.SetConsoleTitleW('[ Tiktok MassReport ] By H4cK3dR4Du & 452b')

def save_proxies(proxies):
    with open("proxies.txt", "w") as file:
        file.write("\n".join(proxies))

def get_proxies():
    try:
        url = "https://api.proxyscrape.com/v2/?request=getproxies&protocol=http&timeout=10000&country=all"
        response = httpx.get(url, timeout=60)

        if response.status_code == 200:
            proxies = response.text.splitlines()
            save_proxies(proxies)
        else:
            time.sleep(1)
            get_proxies()
    except Exception:
        time.sleep(1)
        get_proxies()

def check_proxies_file():
    if not os.path.exists("proxies.txt") or os.path.getsize("proxies.txt") == 0:
        get_proxies()

# Load configuration
try:
    with open("config.json") as f:
        data = json.load(f)
except (FileNotFoundError, json.JSONDecodeError) as e:
    print(f"Error loading config.json: {e}")
    sys.exit(1)

if data.get("proxy_scraper") in ["y", "yes"]:
    check_proxies_file()

def update_console_title():
    global success, failed, total
    success_rate = round(success / total * 100, 2) if total > 0 else 0
    ctypes.windll.kernel32.SetConsoleTitleW(f'[ Tiktok MassReport ] | Reports Sent: {success} | Failed: {failed} | Success Rate: {success_rate}%')

def get_time_rn():
    return datetime.datetime.now().strftime("%H:%M:%S")

def check_ui():
    output_lock = threading.Lock()
    while True:
        success_rate = round(success / total * 100, 2) if total > 0 else 0
        System.Clear()
        with output_lock:
            Write.Print(f"""
            Sent Reports: [ {success} ] ~ Failed: [ {failed} ] ~ Success Rate: [ {success_rate}% ]
            """, Colors.blue_to_red, interval=0.000)
            time.sleep(10)

def mass_report():
    global success, total, failed
    with open("proxies.txt", "r") as f:
        proxy_list = f.readlines()
    proxy = random.choice(proxy_list).strip() if proxy_list else None

    session = tls_client.Session(client_identifier="chrome_113", random_tls_extension_order=True)

    if proxy:
        user_pass = proxy.split("@")
        if len(user_pass) == 2:
            user, ip_port = user_pass
            user, password = user.split(":")
            ip, port = ip_port.split(":")
            proxy_string = f"http://{user}:{password}@{ip}:{port}"
        else:
            ip, port = proxy.split(":")
            proxy_string = f"http://{ip}:{port}"
        session.proxies = {"http": proxy_string, "https": proxy_string}

    url = data['report_url']
    report_types = data['report_types']
    report_type_mapping = {
        "Violence": 90013,
        "Sexual Abuse": 90014,
        # Add other report types as necessary
    }
    report_type = next((code for key, code in report_type_mapping.items() if report_types.get(key) in ["y", "yes"]), None)

    headers = {
        "User-Agent": "Mozilla/5.0 ..."
    }

    try:
        match_reason = re.search(r'reason=(\d+)', url)
        match_nickname = re.search(r'nickname=([^&]+)', url)
        match_owner_id = re.search(r'owner_id=([^&]+)', url)

        username = match_nickname.group(1) if match_nickname else None
        iduser = match_owner_id.group(1) if match_owner_id else None

        if match_reason and report_type:
            new_url = url.replace(f"reason={match_reason.group(1)}", f"reason={report_type}")
            report = session.get(new_url, headers=headers)

            with output_lock:
                time_rn = get_time_rn()
                if "Thanks for your feedback" in report.text or report.status_code == 200:
                    print(f"[ {magenta}{time_rn}{reset} ] | ( {green}+{reset} ) {blue}Reported successfully to {username} ~ {iduser}\n")
                    success += 1
                else:
                    print(f"[ {magenta}{time_rn}{reset} ] | ( {red}-{reset} ) {yellow}Cannot report to {username} ~ {iduser}\n")
                    failed += 1
                total += 1
                update_console_title()
                mass_report()  # consider changing to a loop instead of recursion
    except Exception as e:
        failed += 1
        total += 1
        update_console_title()
        print(f"Error occurred: {e}")

def mass_report_thread():
    mass_report()

def check_ui_thread():
    check_ui()

num_threads = data.get('threads', 1)
threads = []

for _ in range(num_threads):
    thread = threading.Thread(target=mass_report_thread)
    thread.start()
    threads.append(thread)

check_ui_thread = threading.Thread(target=check_ui)
check_ui_thread.start()
threads.append(check_ui_thread)

for thread in threads:
    thread.join()
