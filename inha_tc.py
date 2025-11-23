import requests
from requests.adapters import HTTPAdapter
from urllib3.util import ssl_
import json
import datetime

def find_by_date(date, json_data):
    for data in json_data:
        if data["date"] == date:
            return data
    return "Error: No data matched with date"


# 1️⃣ SECLEVEL=1을 적용하는 커스텀 어댑터 정의
class SSLAdapter(HTTPAdapter):
    def __init__(self, *args, **kwargs):
        self.ssl_context = ssl_.create_urllib3_context()
        self.ssl_context.set_ciphers('DEFAULT:@SECLEVEL=1')
        super().__init__(*args, **kwargs)

    def init_poolmanager(self, *args, **kwargs):
        kwargs['ssl_context'] = self.ssl_context
        return super().init_poolmanager(*args, **kwargs)

def get_inhatc_lunch_menu():
    # 2️⃣ 세션 생성 및 어댑터 등록
    session = requests.Session()
    session.mount("https://", SSLAdapter())

    # 3️⃣ 요청 설정
    url = "https://www.inhatc.ac.kr/haksa/kr/getHaksaFoodMenuList.do"
    today = datetime.date.today()
    start_of_week = today - datetime.timedelta(days=(today.weekday()+1) % 7)
    end_of_week = start_of_week + datetime.timedelta(days=6)

    payload = {
        "gubun": "학생",
        "strDate": start_of_week.strftime("%Y%m%d"),
        "endDate": end_of_week.strftime("%Y%m%d")
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
    # print(response.text)
    data= json.loads(response.text)
    today_menu=find_by_date(today.strftime("%Y%m%d"), data)
    result=f"2️⃣  [인하공전 학생식당 중식] ({today.strftime("%m.%d.")})\n"
    result+="================================\n"
    result+=f"[한식] 5500원\n"
    result+=str(today_menu["lunchNormal"])
    result+="\n--------------------------------\n"
    result+=f"[일품] 6500원\n"
    result+=str(today_menu["lunchSpecial"])
    result+="\n--------------------------------\n"
    return result



if __name__ == "__main__":
    print(get_inhatc_lunch_menu())