import ssl
import urllib3
from urllib3 import PoolManager
from bs4 import BeautifulSoup

# TLS 1.0, 1.1까지 허용 (보안적으로는 낮지만, 테스트용으로 가능)
ctx = ssl.SSLContext(ssl.PROTOCOL_TLS)
ctx.set_ciphers('DEFAULT:@SECLEVEL=1')

http = PoolManager(ssl_context=ctx)
url = "https://www.inhatc.ac.kr/kr/485/subview.do"

response = http.request('GET', url)
html = response.data.decode('utf-8', errors='ignore')

soup = BeautifulSoup(html, "html.parser")
print(soup.title)
rows = soup.find_all("tr")  
print(f"행 개수: {len(rows)}")
