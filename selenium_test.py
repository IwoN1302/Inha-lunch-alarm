import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

def get_inha_uni_menu_success():
    print("--- 인하대학교 학생식당 최종 추출 시작 ---")

    # 1. 스텔스 모드 설정 (성공했던 설정 그대로 유지)
    options = Options()
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-gpu")
    # options.add_argument("--headless") # 최종 배포 시 주석 해제

    driver = webdriver.Chrome(options=options)
    
    # WebDriver 감지 우회
    driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
        "source": """Object.defineProperty(navigator, 'webdriver', { get: () => undefined })"""
    })

    try:
        url = "https://www.inha.ac.kr/kr/1072/subview.do"
        driver.get(url)
        
        # 로딩 대기
        time.sleep(4)
        
        try:
            body_text = driver.find_element(By.TAG_NAME, "body").text
            return body_text  # 전체 텍스트라도 반환

        except Exception as e:
            
            return f"No data available"

    except Exception as e:
        return f"시스템 에러: {e}"
    
    finally:
        driver.quit()

# 실행
if __name__ == "__main__":
    result=get_inha_uni_menu_success()
    print(type(result))