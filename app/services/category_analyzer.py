"""
카테고리별 앱 분석 서비스 (GPT 사용)
"""
from typing import List, Dict, Optional
import logging

logger = logging.getLogger(__name__)

try:
    from app.services.openai_service import get_openai_client
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False
    logger.warning("OpenAI service not available")


async def analyze_category_with_gpt(
    apps_data: List[Dict],
    category_name: str,
    limit: int = 100
) -> Dict:
    """
    카테고리별 앱 목록을 GPT로 분석
    
    Args:
        apps_data: 앱 데이터 리스트
        category_name: 카테고리 이름
        limit: 분석할 앱 수
    
    Returns:
        분석 결과 딕셔너리
    """
    if not OPENAI_AVAILABLE:
        return {
            "success": False,
            "error": "OpenAI service not available"
        }
    
    if not apps_data:
        return {
            "success": False,
            "error": "앱 데이터가 없습니다."
        }
    
    try:
        client = get_openai_client()
        
        # 분석할 앱 데이터 요약 (너무 길면 잘라냄)
        apps_summary = []
        for app in apps_data[:limit]:
            apps_summary.append({
                "name": app.get("name", "Unknown"),
                "rating": app.get("rating", 0.0),
                "review_count": app.get("review_count", 0),
                "description": (app.get("description", "") or "")[:200],  # 설명 일부만
                "price_model": app.get("price_model", "free"),
            })
        
        # GPT 프롬프트 구성
        prompt = f"""
다음은 {category_name} 카테고리의 Google Play Store 상위 {len(apps_summary)}개 앱 목록입니다.

앱 목록:
{format_apps_for_analysis(apps_summary)}

이 카테고리에서 다음을 분석해주세요:

1. **카테고리 특성 분석**
   - 이 카테고리의 주요 트렌드
   - 사용자 니즈와 동기
   - 경쟁 강도

2. **성공 패턴 분석**
   - 높은 순위를 차지한 앱들의 공통점
   - 평점과 리뷰 수의 관계
   - 무료 vs 유료 모델 분석

3. **기회 분석**
   - 시장 공백 (Gap)
   - 진입 가능성
   - 추천 앱 타입 (구현 난이도가 낮고 시장성이 검증된)

4. **구체적인 추천**
   - 빠르게 구축 가능한 앱 아이디어 (최대 5개)
   - 각 아이디어의 핵심 기능 (3-5개)
   - 예상 구현 난이도 (0-2점)
   - 예상 시장성 점수 (0-10점)
   - 예상 화면 수
   - 예상 개발 기간

답변은 한국어로, 구조화된 JSON 형식으로 제공해주세요.
"""

        # GPT 호출
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": "당신은 모바일 앱 시장 분석 전문가입니다. 데이터를 분석하여 실행 가능한 인사이트를 제공합니다."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.7,
            max_tokens=2000
        )
        
        analysis_text = response.choices[0].message.content
        
        return {
            "success": True,
            "category": category_name,
            "apps_analyzed": len(apps_summary),
            "analysis": analysis_text,
            "report": analysis_text,  # 프론트엔드 호환성을 위해 report 필드도 추가
            "raw_apps": apps_summary
        }
        
    except Exception as e:
        logger.error(f"Error analyzing category with GPT: {e}")
        import traceback
        logger.error(traceback.format_exc())
        return {
            "success": False,
            "error": f"GPT 분석 중 오류 발생: {str(e)}"
        }


def format_apps_for_analysis(apps: List[Dict]) -> str:
    """앱 목록을 분석용 텍스트로 포맷"""
    formatted = []
    for i, app in enumerate(apps, 1):
        formatted.append(
            f"{i}. {app['name']}\n"
            f"   - 평점: {app['rating']}/5.0\n"
            f"   - 리뷰 수: {app['review_count']:,}\n"
            f"   - 가격 모델: {app['price_model']}\n"
            f"   - 설명: {app['description'][:150]}..."
        )
    return "\n\n".join(formatted)


async def analyze_multiple_categories_with_gpt(
    category_apps_map: Dict[str, List[Dict]],
    limit_per_category: int = 50
) -> Dict:
    """
    여러 카테고리별 앱 목록을 GPT로 분석
    
    Args:
        category_apps_map: {카테고리명: 앱리스트} 딕셔너리
        limit_per_category: 카테고리당 분석할 앱 수
    
    Returns:
        분석 결과 딕셔너리
    """
    if not OPENAI_AVAILABLE:
        return {
            "success": False,
            "error": "OpenAI service not available"
        }
    
    try:
        client = get_openai_client()
        
        # 모든 카테고리 데이터 요약
        categories_summary = {}
        for category, apps in category_apps_map.items():
            categories_summary[category] = []
            for app in apps[:limit_per_category]:
                categories_summary[category].append({
                    "name": app.get("name", "Unknown"),
                    "rating": app.get("rating", 0.0),
                    "review_count": app.get("review_count", 0),
                    "price_model": app.get("price_model", "free"),
                })
        
        # GPT 프롬프트 구성
        prompt = f"""
다음은 여러 카테고리의 Google Play Store 상위 앱 목록입니다.

{format_categories_for_analysis(categories_summary)}

전체 카테고리를 비교 분석하여 다음을 분석해주세요:

1. **카테고리별 비교 분석**
   - 각 카테고리의 시장 특성
   - 경쟁 강도 비교
   - 성장 잠재력 비교

2. **종합 추천**
   - 가장 진입하기 좋은 카테고리 (최대 3개)
   - 각 카테고리의 추천 앱 타입
   - 빠르게 구축 가능한 앱 아이디어 (카테고리별 최대 3개)

3. **우선순위 제안**
   - 구현 난이도 vs 시장성 기준으로 우선순위 제안
   - 각 아이디어의 핵심 기능, 예상 화면 수, 개발 기간

답변은 한국어로, 구조화된 형식으로 제공해주세요.
"""

        # GPT 호출
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": "당신은 모바일 앱 시장 분석 전문가입니다. 여러 카테고리를 비교 분석하여 실행 가능한 인사이트를 제공합니다."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.7,
            max_tokens=3000
        )
        
        analysis_text = response.choices[0].message.content
        
        return {
            "success": True,
            "categories_analyzed": list(category_apps_map.keys()),
            "analysis": analysis_text,
            "categories_data": categories_summary
        }
        
    except Exception as e:
        logger.error(f"Error analyzing multiple categories with GPT: {e}")
        import traceback
        logger.error(traceback.format_exc())
        return {
            "success": False,
            "error": f"GPT 분석 중 오류 발생: {str(e)}"
        }


def format_categories_for_analysis(categories_summary: Dict[str, List[Dict]]) -> str:
    """카테고리별 앱 목록을 분석용 텍스트로 포맷"""
    formatted = []
    for category, apps in categories_summary.items():
        formatted.append(f"## {category} 카테고리 ({len(apps)}개 앱)")
        for i, app in enumerate(apps[:10], 1):  # 카테고리당 상위 10개만 표시
            formatted.append(
                f"  {i}. {app['name']} - 평점: {app['rating']}/5.0, "
                f"리뷰: {app['review_count']:,}, 가격: {app['price_model']}"
            )
        formatted.append("")  # 빈 줄
    
    return "\n".join(formatted)
