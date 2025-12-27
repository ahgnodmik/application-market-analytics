#!/usr/bin/env python3
"""
OpenAI API 키 설정 확인 스크립트
"""
import os
from dotenv import load_dotenv

# .env 파일과 .env.local 파일 모두 로드 시도
load_dotenv()
load_dotenv('.env.local')

api_key = os.getenv("OPENAI_API_KEY")

print("=" * 50)
print("OpenAI API 키 설정 확인")
print("=" * 50)

if not api_key:
    print("❌ OPENAI_API_KEY가 설정되지 않았습니다.")
    print("\n설정 방법:")
    print("1. 프로젝트 루트에 .env 파일 생성")
    print("2. 다음 내용 추가:")
    print("   OPENAI_API_KEY=your_api_key_here")
    print("\n또는 .env.local 파일에 설정할 수도 있습니다.")
    exit(1)
elif api_key == "your_api_key_here":
    print("⚠️  API 키가 예제 값으로 설정되어 있습니다.")
    print("실제 API 키로 변경해주세요.")
    exit(1)
else:
    # API 키의 일부만 표시 (보안)
    masked_key = api_key[:7] + "..." + api_key[-4:] if len(api_key) > 11 else "***"
    print(f"✅ API 키가 설정되어 있습니다: {masked_key}")
    
    # OpenAI 클라이언트 테스트
    try:
        from openai import OpenAI
        client = OpenAI(api_key=api_key)
        print("✅ OpenAI 클라이언트 생성 성공")
        
        # 간단한 API 테스트 (모델 목록 조회)
        print("\nAPI 연결 테스트 중...")
        models = client.models.list()
        print("✅ OpenAI API 연결 성공!")
        print(f"   사용 가능한 모델 수: {len(list(models))}")
        
    except Exception as e:
        print(f"❌ OpenAI API 연결 실패: {str(e)}")
        print("\n가능한 원인:")
        print("1. API 키가 유효하지 않음")
        print("2. 인터넷 연결 문제")
        print("3. OpenAI 서비스 장애")
        exit(1)

print("\n" + "=" * 50)
print("✅ 모든 검사 통과! AI 리포트 기능을 사용할 수 있습니다.")
print("=" * 50)



