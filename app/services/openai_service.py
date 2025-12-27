"""
OpenAI ChatGPT API 서비스
안드로이드 마켓 앱 분석 리포트 생성
"""

import os
from typing import List, Dict, Optional
from openai import OpenAI
from dotenv import load_dotenv

# .env 파일과 .env.local 파일 모두 로드 시도
load_dotenv()  # .env 파일
load_dotenv('.env.local')  # .env.local 파일도 시도

client = None

def get_openai_client():
    """OpenAI 클라이언트 가져오기"""
    global client
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        return None
    if client is None:
        client = OpenAI(api_key=api_key)
    return client


def analyze_apps_with_ai(apps_data: List[Dict]) -> Dict:
    """
    ChatGPT를 사용하여 앱 목록 분석 및 리포트 생성
    
    Args:
        apps_data: 분석할 앱 데이터 리스트
        
    Returns:
        분석 리포트 딕셔너리
    """
    client = get_openai_client()
    if not client:
        raise ValueError("OpenAI API 키가 설정되지 않았습니다. .env 파일에 OPENAI_API_KEY를 설정해주세요.")
    
    # 앱 데이터를 텍스트로 변환
    apps_summary = "\n\n".join([
        f"앱 이름: {app['name']}\n"
        f"카테고리: {app.get('category', 'N/A')}\n"
        f"평점: {app.get('rating', 'N/A')}\n"
        f"리뷰 수: {app.get('review_count', 'N/A')}\n"
        f"가격 모델: {app.get('price_model', 'N/A')}\n"
        f"난이도 점수: {app.get('difficulty_score', 0)}\n"
        f"시장성 점수: {app.get('marketability_score', 0)}\n"
        f"기능: {', '.join([f['name'] for f in app.get('features', [])])}\n"
        f"설명: {app.get('description', 'N/A')}"
        for app in apps_data
    ])
    
    # 프롬프트 구성
    prompt = f"""당신은 안드로이드 앱 마켓 분석 전문가입니다. 아래 앱 목록을 분석하여 리포트를 작성해주세요.

## 분석 대상 앱 목록:

{apps_summary}

## 리포트 작성 요구사항:

1. **전체 요약**: 전체적인 앱 마켓 트렌드 분석 (200-300자)

2. **카테고리별 분석**: 카테고리별로 그룹화하여 각 카테고리의 특징, 인기 앱, 시장성 분석

3. **구현 난이도가 낮으면서 시장성이 높은 앱 타입 추천**: 
   - 난이도 점수 ≤ 1.0
   - 시장성 점수 ≥ 6.0
   - 각 추천 앱 타입에 대해:
     * 타입 이름
     * 핵심 기능 (3-5개)
     * 예상 구현 기간
     * 시장성 근거
     * 차별화 포인트

4. **시장 기회 분석**: 
   - 현재 부족한 앱 타입
   - 성장 가능성이 높은 영역
   - 추천 우선순위

5. **실행 가능한 액션 아이템**: 
   - 1인 개발자가 빠르게 구현 가능한 앱 타입 TOP 5
   - 각각에 대한 구현 로드맵 (간단한 버전)

## 출력 형식:
마크다운 형식으로 작성해주세요. 한국어로 작성해주세요.
"""
    
    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {
                    "role": "system",
                    "content": "당신은 안드로이드 앱 마켓 분석 전문가입니다. 정확하고 실용적인 분석 리포트를 제공합니다."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.7,
            max_tokens=4000
        )
        
        report_content = response.choices[0].message.content
        
        return {
            "success": True,
            "report": report_content,
            "model": "gpt-4",
            "apps_count": len(apps_data)
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "message": "AI 분석 중 오류가 발생했습니다."
        }


def generate_single_app_analysis(app_data: Dict) -> Dict:
    """
    단일 앱에 대한 상세 분석 생성
    """
    client = get_openai_client()
    if not client:
        raise ValueError("OpenAI API 키가 설정되지 않았습니다.")
    
    app_summary = f"""
앱 이름: {app_data['name']}
카테고리: {app_data.get('category', 'N/A')}
평점: {app_data.get('rating', 'N/A')}
리뷰 수: {app_data.get('review_count', 'N/A')}
가격 모델: {app_data.get('price_model', 'N/A')}
난이도 점수: {app_data.get('difficulty_score', 0)}
시장성 점수: {app_data.get('marketability_score', 0)}
기능 목록:
{chr(10).join([f"- {f['name']} ({f.get('feature_type', 'N/A')}): 난이도 {f.get('difficulty_score', 0)}" for f in app_data.get('features', [])])}
설명: {app_data.get('description', 'N/A')}
"""
    
    prompt = f"""아래 앱 정보를 분석하여 다음을 작성해주세요:

{app_summary}

1. 앱의 핵심 가치 제안
2. 주요 기능 분석
3. 시장성 평가
4. 구현 난이도 평가
5. 개선 제안사항
6. 유사 앱과의 차별화 포인트

마크다운 형식으로 한국어로 작성해주세요.
"""
    
    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "당신은 앱 분석 전문가입니다."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=2000
        )
        
        return {
            "success": True,
            "analysis": response.choices[0].message.content,
            "app_name": app_data['name']
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }

