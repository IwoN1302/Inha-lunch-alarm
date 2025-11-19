import time
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

def get_inha_uni_lunch_final():
    print("--- 인하대 학생식당 [중식] 정밀 추출 ---")

    # 1. 오늘 날짜 검색어 (예: 11.19.)
    now = datetime.now()
    today_str = now.strftime("%m.%d.")
    
    # [디버깅] 테스트를 위해 캡처에 있는 날짜로 고정해볼 수 있습니다.
    # today_str = "11.17." 
    
    print(f"검색 날짜: '{today_str}' / 목표: '중식'")

    # 2. 스텔스 옵션 (유지)
    options = Options()
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-gpu")
    options.add_argument("--headless")

    driver = webdriver.Chrome(options=options)
    
    driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
        "source": """Object.defineProperty(navigator, 'webdriver', { get: () => undefined })"""
    })

    try:
        url = "https://www.inha.ac.kr/kr/1072/subview.do"
        driver.get(url)
        time.sleep(4)
        driver.execute_script("window.scrollTo(0, 500);")

        # 3. [최종 필살기] XPath 복합 조건 검색
        # 해석:
        # //h2[contains(text(), '11.19.')]   -> 오늘 날짜가 적힌 제목(h2)을 모두 찾아라.
        # /following-sibling::div[1]         -> 그 제목 바로 뒤에 있는 div(내용 박스)를 봐라.
        # [.//h3[contains(text(), '중식')]]  -> 근데 그 div 안에 '중식'이라고 적힌 h3가 들어있는 녀석만 골라라.
        # //table                            -> 그 div 안에 있는 테이블을 가져와라.
        
        xpath = f"//h2[contains(text(), '{today_str}')]/following-sibling::div[1][.//h3[contains(text(), '중식')]]//table"
        
        try:
            target_table = driver.find_element(By.XPATH, xpath)
            print("-> '오늘 날짜' + '중식' 조건을 모두 만족하는 테이블을 찾았습니다!")

            # 4. 데이터 추출 (기존과 동일)
            # 인하대 테이블 구조: th(코너명), td.left(메뉴), td(가격)
            rows = target_table.find_elements(By.CSS_SELECTOR, "tbody tr")
            
            result_text = f"1️⃣  [인하대 학생식당 중식] ({today_str})\n"
            result_text += "================================\n"

            for row in rows:
                try:
                    # 코너 이름 (th)
                    corner = row.find_element(By.TAG_NAME, "th").text.strip()
                    
                    # 메뉴 내용 (td class="left")
                    menu_cell = row.find_element(By.CSS_SELECTOR, "td.left")
                    menu_content = menu_cell.text.strip()
                    
                    # 가격 (마지막 td)
                    price = row.find_elements(By.TAG_NAME, "td")[-1].text.strip()

                    result_text += f"[{corner}] {price}원\n"
                    result_text += f"{menu_content}\n"
                    result_text += "--------------------------------\n"
                except:
                    continue
            
            return result_text

        except Exception as e:
            return f"실패: 오늘({today_str}) 중식 메뉴를 찾지 못했습니다. (메뉴가 없거나 XPath가 빗나갔습니다.)\n오류: {e}"

    except Exception as e:
        return f"시스템 에러: {e}"
    
    finally:
        driver.quit()

if __name__ == "__main__":
    print(get_inha_uni_lunch_final())