"""
환경 정보 확인 스크립트
노트북과 데스크톱의 환경 차이를 확인하기 위한 스크립트
"""
import sys
import ssl
import requests
import urllib3
from urllib3.util import ssl_

print("=" * 60)
print("환경 정보 확인")
print("=" * 60)

print(f"\n1. Python 버전: {sys.version}")
print(f"2. Python 실행 경로: {sys.executable}")

print(f"\n3. requests 버전: {requests.__version__}")
print(f"4. urllib3 버전: {urllib3.__version__}")

print(f"\n5. OpenSSL 버전: {ssl.OPENSSL_VERSION}")
print(f"6. SSL 버전: {ssl.OPENSSL_VERSION_NUMBER}")

# SECLEVEL 지원 여부 확인
try:
    context = ssl_.create_urllib3_context()
    context.set_ciphers('DEFAULT:@SECLEVEL=1')
    print("7. SECLEVEL=1 지원: ✅ 지원됨")
except Exception as e:
    print(f"7. SECLEVEL=1 지원: ❌ 오류 발생 - {e}")

# 인증서 검증 테스트
print("\n8. SSL 인증서 검증 테스트:")
try:
    response = requests.get("https://www.inhatc.ac.kr", timeout=5, verify=True)
    print("   ✅ 인증서 검증 성공 (verify=True)")
except requests.exceptions.SSLError as e:
    print(f"   ❌ 인증서 검증 실패 (verify=True): {type(e).__name__}")
except Exception as e:
    print(f"   ⚠️  기타 오류: {type(e).__name__}")

try:
    response = requests.get("https://www.inhatc.ac.kr", timeout=5, verify=False)
    print("   ✅ 인증서 검증 우회 성공 (verify=False)")
except Exception as e:
    print(f"   ❌ 인증서 검증 우회 실패: {type(e).__name__}")

print("\n" + "=" * 60)

