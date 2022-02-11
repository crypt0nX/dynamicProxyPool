from multiprocessing import Pool
import requests
import util.writeFile

WORKERS = 10


def check(url):
    host = url.split(':')[0]
    port = url.split(':')[1]
    proxy_url = "socks5://%s:%s" % (host, port)
    proxies = {'http': proxy_url, 'https': proxy_url}
    check_url = "https://ipinfo.io"
    try:
        r = requests.get(check_url, proxies=proxies, timeout=1)
        if r.status_code == 200:
            writeFile.writeFile("../alive_host.txt", url)
    except Exception:
        pass
    pass


if __name__ == "__main__":
    with open("../proxylist.txt") as targets:
        targets = targets.read().splitlines()
    with Pool(processes=WORKERS) as executor:
        executor.map(check, targets)

