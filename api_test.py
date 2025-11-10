import requests
import ssl
from requests.adapters import HTTPAdapter
from urllib3.poolmanager import PoolManager
from urllib3.util import ssl_

# 1️⃣ SECLEVEL=1을 적용하는 커스텀 어댑터 정의
class SSLAdapter(HTTPAdapter):
    def __init__(self, *args, **kwargs):
        self.ssl_context = ssl_.create_urllib3_context()
        self.ssl_context.set_ciphers('DEFAULT:@SECLEVEL=1')
        super().__init__(*args, **kwargs)

    def init_poolmanager(self, *args, **kwargs):
        kwargs['ssl_context'] = self.ssl_context
        return super().init_poolmanager(*args, **kwargs)

# 2️⃣ 세션 생성 및 어댑터 등록
session = requests.Session()
session.mount("https://", SSLAdapter())

# 3️⃣ 요청 설정
url = "https://www.inhatc.ac.kr/haksa/kr/getHaksaFoodMenuList.do"
payload = {
    "gubun": "학생",
    "strDate": "20251109",
    "endDate": "20251115"
}
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/140.0.0.0 Whale/4.34.340.19 Safari/537.36",
    "Referer": "https://www.inhatc.ac.kr/kr/485/subview.do",
    "Origin": "https://www.inhatc.ac.kr",
    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
    "X-Requested-With": "XMLHttpRequest"
}

# 4️⃣ POST 요청
response = session.post(url, data=payload, headers=headers)

# 5️⃣ 결과 출력
print("Status:", response.status_code)
print(response.text)
