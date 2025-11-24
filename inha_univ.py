import time
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By


def get_inha_uni_lunch_final():
    """
    인하대 학생식당 중식 메뉴를 스크래핑하여 반환합니다.
    
    Returns:
        str: 포맷팅된 중식 메뉴 문자열
    """
    # 오늘 날짜 검색어 생성 (예: 11.24.)
    today_str = datetime.now().strftime("%m.%d.")
    print(f"검색 날짜: '{today_str}' / 목표: '중식'")

    # Chrome 옵션 설정
    options = Options()
    # 스텔스 모드 설정 (봇 감지 회피)
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
    options.add_argument("--headless")  # 헤드리스 모드
    
    driver = webdriver.Chrome(options=options)
    
    # webdriver 속성 숨기기 (봇 감지 회피)
    driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
        "source": """Object.defineProperty(navigator, 'webdriver', { get: () => undefined })"""
    })

    try:
        # 인하대 학생식당 메뉴 페이지 접속
        url = "https://www.inha.ac.kr/kr/1072/subview.do"
        driver.get(url)
        time.sleep(4)  # 페이지 로딩 대기
        driver.execute_script("window.scrollTo(0, 500);")  # 스크롤 다운

        # XPath로 오늘 날짜의 중식 테이블 찾기
        # //h2[contains(text(), '11.24.')] -> 오늘 날짜가 적힌 제목(h2) 찾기
        # /following-sibling::div[1] -> 그 제목 바로 뒤의 div(내용 박스)
        # [.//h3[contains(text(), '중식')]] -> 그 div 안에 '중식' h3가 있는 것만 선택
        # //table -> 그 div 안의 테이블
        xpath = f"//h2[contains(text(), '{today_str}')]/following-sibling::div[1][.//h3[contains(text(), '중식')]]//table"
        
        try:
            target_table = driver.find_element(By.XPATH, xpath)
            print("-> '오늘 날짜' + '중식' 조건을 모두 만족하는 테이블을 찾았습니다!")

            # 테이블 데이터 추출
            rows = target_table.find_elements(By.CSS_SELECTOR, "tbody tr")
            
            result_text = f"1️⃣  [인하대 학생식당 중식] ({today_str})\n"
            result_text += "=================================\n"

            for row in rows:
                try:
                    corner = row.find_element(By.TAG_NAME, "th").text.strip()
                    menu_cell = row.find_element(By.CSS_SELECTOR, "td.left")
                    menu_content = menu_cell.text.strip()
                    price = row.find_elements(By.TAG_NAME, "td")[-1].text.strip()

                    result_text += f"[{corner}] {price}원\n"
                    result_text += f"{menu_content}\n"
                    result_text += "---------------------------------\n"
                except Exception:
                    # 개별 행 처리 실패 시 건너뛰기
                    continue
            
            return result_text

        except Exception as e:
            return f"실패: 오늘({today_str}) 중식 메뉴를 찾지 못했습니다. (메뉴가 없거나 XPath가 빗나갔습니다.)\n오류: {e}"

    except Exception as e:
        return f"시스템 에러: {e}"
    
    finally:
        driver.quit()

if __name__ == "__main__":
    print("--- 인하대 학생식당 [중식] 정밀 추출 ---")
    print(get_inha_uni_lunch_final())