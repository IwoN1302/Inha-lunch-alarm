@echo off
:: 1. 프로젝트 폴더로 이동 (본인의 실제 경로로 수정하세요)
cd /d "E:\python\Inha-lunch-alarm\main.py"

:: 2. 가상환경 활성화 (만약 venv를 쓴다면)
:: venv가 없다면 이 줄은 지우고 바로 python main.py 하시면 됩니다.
call venv\Scripts\activate

:: 3. 파이썬 실행
echo 학식 알리미를 실행합니다...
python main.py

:: 4. (선택사항) 창이 바로 꺼지지 않게 하려면 아래 줄 유지
:: 자동화할 때는 이 줄을 지우는 게 좋습니다.
timeout /t 3