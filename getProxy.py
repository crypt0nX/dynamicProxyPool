import sys
import time
import requests
from bs4 import BeautifulSoup
import re
import base64
import os
import util.check

proxies = {
    'http': 'http://127.0.0.1:7890',
    'https': 'http://127.0.0.1:7890',
}

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; rv:91.0) Gecko/20100101 Firefox/91.0',
    'Cookie': 'fp=1153964d9bd67113bd8a6c7b34cb68c1'
}


def returnProxy(url):
    if os.path.exists("proxylist.txt"):
        os.remove("proxylist.txt")
    regex_of_host = '(?<=document.write[(]Base64.decode[(]").*?(?="[)])'
    main_url = url
    r = requests.get(main_url, proxies=proxies, headers=headers)
    soup = BeautifulSoup(r.content, 'lxml')
    host_list = soup.find("table", id="proxy_list")
    try:
        for i in host_list.find_all('tr'):
            host_port = i.find('span').text
            host_html_text = i.find('script')
            if host_html_text and "Base64" in str(host_html_text):
                host_base64_encode = re.findall(regex_of_host, str(host_html_text))[0]
                host_base64_decode = str(base64.b64decode(host_base64_encode).decode('utf-8'))
            util.writeFile.writeFile("proxylist.txt", host_base64_decode + ":" + host_port)
            print(host_base64_decode + ":" + host_port)
        os.system("python3 util/check.py")
    except Exception:
        print("错误，ip被拒绝")
        sys.exit()
        pass


url = "http://free-proxy.cz/zh/proxylist/country/CN/socks5/ping/all"
for i in range(1, 5):
    if i == 1:
        main_url = url
    else:
        main_url = url + '/' + str(i)
    returnProxy(main_url)
    time.sleep(2)
