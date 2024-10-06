import ctypes, json, os, time, random, string, getpass, threading, re, sys
import datetime

try:
    import pystyle
    import colorama
    import tls_client
    import httpx
    import user_agent
except ModuleNotFoundError:
    os.system("pip install pystyle")
    os.system("pip install colorama")
    os.system("pip install tls_client")
    os.system("pip install httpx")
    os.system("pip install user_agent")

from pystyle import Write, System, Colorate, Colors
from colorama import Fore, Style, init

red = Fore.RED
yellow = Fore.YELLOW
green = Fore.GREEN
blue = Fore.BLUE
orange = Fore.RED + Fore.YELLOW
pretty = Fore.LIGHTMAGENTA_EX + Fore.LIGHTCYAN_EX
magenta = Fore.MAGENTA
lightblue = Fore.LIGHTBLUE_EX
cyan = Fore.CYAN
gray = Fore.LIGHTBLACK_EX + Fore.WHITE
reset = Fore.RESET
pink = Fore.LIGHTGREEN_EX + Fore.LIGHTMAGENTA_EX
dark_green = Fore.GREEN + Style.BRIGHT

success = 0
failed = 0
generated_agents = 0
total = 1

start = time.time()
ctypes.windll.kernel32.SetConsoleTitleW(f'[ Tiktok MassReport ] By H4cK3dR4Du & 452b')

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
    except (httpx.ProxyError, httpx.ReadError, httpx.ConnectTimeout, httpx.ReadTimeout, httpx.ConnectError, httpx.ProtocolError):
        get_proxies()

def check_proxies_file():
    file_path = "proxies.txt"
    if not os.path.exists(file_path) or os.path.getsize(file_path) == 0:
        get_proxies()

with open(f"config.json") as f:
    data = json.load(f)
    if data.get("proxy_scraper") in ["y", "yes"]:
        check_proxies_file()

def update_console_title():
    global success, failed, generated_agents, total
    success_rate = round(success / total * 100, 2) if total > 0 else 0
    ctypes.windll.kernel32.SetConsoleTitleW(f'[ Tiktok MassReport ] By H4cK3dR4Du & 452b | Reports Sent: {success} ~ Failed: {failed} ~ Success Rate: {success_rate}%')

def get_time_rn():
    date = datetime.datetime.now()
    return "{:02d}:{:02d}:{:02d}".format(date.hour, date.minute, date.second)

def check_ui():
    output_lock = threading.Lock()
    while True:
        success_rate = round(success / total * 100, 2) if total > 0 else 0
        System.Clear()
        with output_lock:
            Write.Print(f"""
\t\t\t▄▄▄▄▄▪  ▄ •▄ ▄▄▄▄▄      ▄ •▄     ▄▄▄  ▄▄▄ . ▄▄▄·      ▄▄▄  ▄▄▄▄▄
\t\t\t•██  ██ █▌▄▌▪•██  ▪     █▌▄▌▪    ▀▄ █·▀▄.▀·▐█ ▄█▪     ▀▄ █·•██  
\t\t\t ▐█.▪▐█·▐▀▀▄· ▐█.▪ ▄█▀▄ ▐▀▀▄·    ▐▀▀▄ ▐▀▀▪▄ ██▀· ▄█▀▄ ▐▀▀▄  ▐█.▪
\t\t\t ▐█▌·▐█▌▐█.█▌ ▐█▌·▐█▌.▐▌▐█.█▌    ▐█•█▌▐█▄▄▌▐█▪·•▐█▌.▐▌▐█•█▌ ▐█▌·
\t\t\t ▀▀▀ ▀▀▀·▀  ▀ ▀▀▀  ▀█▄▀▪·▀  ▀    .▀  ▀ ▀▀▀ .▀    ▀█▄▀▪.▀  ▀ ▀▀▀ 

----------------------------------------------------------------------------------------------------------------------
\t\t\tSent Reports: [ {success} ] ~ Failed: [ {failed} ] ~ Success Rate: [ {success_rate}% ]
----------------------------------------------------------------------------------------------------------------------
""", Colors.blue_to_red, interval=0.000)
            time.sleep(10)

def mass_report():
    global success, total, failed, generated_agents
    with open("proxies.txt", "r") as f:
        proxy_list = f.readlines()
    proxy = random.choice(proxy_list).strip() if proxy_list else None

    session = tls_client.Session(
        client_identifier="chrome_113",
        random_tls_extension_order=True
    )

    if proxy and "@" in proxy:
        user_pass, ip_port = proxy.split("@")
        user, password = user_pass.split(":")
        ip, port = ip_port.split(":")
        proxy_string = f"http://{user}:{password}@{ip}:{port}"
    elif proxy:
        ip, port = proxy.split(":")
        proxy_string = f"http://{ip}:{port}"
    else:
        proxy_string = None

    if proxy_string:
        session.proxies = {
            "http": proxy_string,
            "https": proxy_string
        }

    with open(f"config.json") as f:
        data = json.load(f)
        url = data['report_url']
        report_types = data['report_types']

        report_type_mapping = {
            "Violence": 90013,
            "Sexual Abuse": 90014,
            "Animal Abuse": 90016,
            "Criminal Activities": 90017,
            "Hate": 9020,
            "Bullying": 9007,
            "Suicide Or Self-Harm": 90061,
            "Dangerous Content": 90064,
            "Sexual Content": 90084,
            "Porn": 90085,
            "Drugs": 90037,
            "Firearms Or Weapons": 90038,
            "Sharing Personal Info": 9018,
            "Human Exploitation": 90015,
            "Under Age": 91015
        }

        report_type = None
        for key, code in report_type_mapping.items():
            if report_types.get(key) in ["y", "yes"]:
                report_type = code
                break

        output_lock = threading.Lock()
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36 Edg/116.0.1938.62"
        }

        try:
            match_reason = re.search(r'reason=(\d+)', url)
            match_nickname = re.search(r'nickname=([^&]+)', url)
            match_owner_id = re.search(r'owner_id=([^&]+)', url)

            username = match_nickname.group(1) if match_nickname else None
            iduser = match_owner_id.group(1) if match_owner_id else None

            if match_reason:
                reason_number = match_reason.group(1)
                new_url = url.replace(f"reason={reason_number}", f"reason={report_type}")
                report = session.get(new_url, headers=headers)

                if "Thanks for your feedback" in report.text or report.status_code == 200:
                    with output_lock:
                        time_rn = get_time_rn()
                        print(f"[ {magenta}{time_rn}{reset} ] | ( {green}+{reset} ) {blue}Reported successfully to {username} ~ {iduser}\n")
                        success += 1
                        total += 1
                        update_console_title()
                        mass_report()
                else:
                    with output_lock:
                        time_rn = get_time_rn()
                        print(f"[ {magenta}{time_rn}{reset} ] | ( {red}-{reset} ) {yellow}Cannot report to {username} ~ {iduser}\n")
                        failed += 1
                        total += 1
                        update_console_title()
                        mass_report()
            else:
                mass_report()
        except Exception as e:
            failed += 1
            total += 1
            update_console_title()
            mass_report()

def mass_report_thread():
    mass_report()

def check_ui_thread():
    check_ui()

num_threads = data['threads']
threads = []

with threading.Lock():
    for _ in range(num_threads - 1):
        thread = threading.Thread(target=mass_report_thread)
        thread.start()
        threads.append(thread)

    check_ui_thread = threading.Thread(target=check_ui_thread)
    check_ui_thread.start()
    threads.append(check_ui_thread)

    for thread in threads:
        thread.join()
