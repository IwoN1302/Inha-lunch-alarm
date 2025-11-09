import requests
import ssl
from requests.adapters import HTTPAdapter
from urllib3 import poolmanager # <<< [수정] 이 라인이 누락되었습니다.

# --- [수정된 부분 시작] ---
# TLS 1.2 이상만 사용하도록 강제하는 '연결 규칙(Adapter)' 클래스를 정의합니다.
class TLSv1_2Adapter(HTTPAdapter):
    def init_poolmanager(self, connections, maxsize, block=False):
        # 'poolmanager'를 여기서 사용합니다.
        self.poolmanager = poolmanager.PoolManager(
            num_pools=connections,
            maxsize=maxsize,
            block=block,
            ssl_version=ssl.PROTOCOL_TLSv1_2, # 이 부분이 핵심
        )

# Session 객체를 만들어서 위에서 정의한 연결 규칙을 적용합니다.
session = requests.Session()
session.mount('https://', TLSv1_2Adapter()) # 모든 https:// 접속에 이 규칙을 적용
# --- [수정된 부분 끝] ---

# 이제 requests.get() 대신 session.get()을 사용합니다.
url = "https://www.inhatc.ac.kr/kr/485/subview.do" # 테스트할 URL

try:
    response = session.get(url, verify=False) # 수정된 코드로 접속 시도

    if response.status_code == 200:
        print("접속 성공! SSL/TLS 문제가 해결되었습니다.")
        # 여기에 BeautifulSoup을 이용한 파싱 코드를 이어서 작성하면 됩니다.
    else:
        print(f"접속은 되었으나 상태 코드가 다릅니다: {response.status_code}")

except requests.exceptions.SSLError as e:
    print(f"여전히 SSL 에러가 발생합니다: {e}")
except Exception as e:
    print(f"다른 에러가 발생했습니다: {e}")