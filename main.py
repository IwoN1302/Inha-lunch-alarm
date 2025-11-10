import ssl
import urllib3
from bs4 import BeautifulSoup
import datetime

ctx = ssl.SSLContext(ssl.PROTOCOL_TLS)
ctx.set_ciphers('DEFAULT:@SECLEVEL=1')

http = urllib3.PoolManager(ssl_context=ctx)

url = "https://www.inhatc.ac.kr/kr/485/subview.do"
response = http.request("GET", url)

html = response.data.decode("utf-8", errors="ignore")
# print(html)

soup = BeautifulSoup(html, "html.parser")
tables = soup.find("tbody")
rows = tables.find_all('tr')

print("="*50)
    
print(tables)
print("="*50)
print(rows)