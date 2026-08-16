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
        if not client:
            logger.error("OpenAI client is None - API key may not be set")
            return {
                "success": False,
                "error": "OpenAI API 키가 설정되지 않았습니다. Railway 환경 변수에서 OPENAI_API_KEY를 확인해주세요."
            }
        
        # API 키가 설정되었는지 추가 확인
        from app.config import settings
        import os
        
        env_key = os.getenv("OPENAI_API_KEY")
        settings_key = settings.OPENAI_API_KEY
        
        if not settings_key and not env_key:
            logger.error("OPENAI_API_KEY is not set in both settings and environment")
            return {
                "success": False,
                "error": "OpenAI API 키가 설정되지 않았습니다. Railway Variables에서 OPENAI_API_KEY를 확인해주세요."
            }
        
        # 실제 사용되는 키 확인
        actual_key = settings_key or env_key
        if actual_key:
            key_prefix = actual_key[:15] if len(actual_key) > 15 else "***"
            key_suffix = actual_key[-10:] if len(actual_key) > 10 else "***"
            logger.info(f"OpenAI client initialized (API key: {key_prefix}...{key_suffix}, length: {len(actual_key)})")
            
            # 키 길이 검증 (일반적으로 OpenAI API 키는 50자 이상)
            if len(actual_key) < 40:
                logger.warning(f"API key seems too short (length: {len(actual_key)}), may be incomplete")
                return {
                    "success": False,
                    "error": f"OpenAI API 키가 너무 짧습니다 (길이: {len(actual_key)}). 키 전체를 복사했는지 확인해주세요."
                }
        
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

이 카테고리를 분석하여 다음 내용을 마크다운 형식으로 작성해주세요:

## 📊 카테고리 특성 분석

### 주요 트렌드
- 이 카테고리의 주요 트렌드 3-5개

### 사용자 니즈와 동기
- 사용자들이 이 카테고리의 앱을 사용하는 주요 동기

### 경쟁 강도
- 현재 시장의 경쟁 강도 평가

## ✨ 성공 패턴 분석

### 공통점
- 높은 순위를 차지한 앱들의 공통된 특징

### 평점과 리뷰 수의 관계
- 평점과 리뷰 수의 상관관계 분석

### 무료 vs 유료 모델
- 무료 모델과 유료 모델의 차이점 및 시장 전략

## 🎯 기회 분석

### 시장 공백 (Gap)
- 현재 시장에서 채워지지 않은 니즈

### 진입 가능성
- 새로운 앱이 진입하기 좋은 이유와 주의사항

### 추천 앱 타입
- 구현 난이도가 낮고 시장성이 검증된 앱 타입 제안

## 🚀 구체적인 추천 앱

최대 5개의 앱 아이디어를 다음 형식으로 제시해주세요:

### [앱 아이디어 1]
**핵심 기능:**
- 기능 1
- 기능 2
- 기능 3

**예상 지표:**
- 구현 난이도: X점 (0-2점)
- 시장성 점수: X점 (0-10점)
- 예상 화면 수: X개
- 예상 개발 기간: X개월

(다음 앱 아이디어들도 동일한 형식으로...)

답변은 한국어로, 깔끔하고 읽기 쉬운 마크다운 형식으로 작성해주세요.
"""

        # GPT 호출
        try:
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
        except Exception as api_error:
            error_str = str(api_error)
            logger.error(f"OpenAI API call failed: {api_error}")
            # 401 에러인 경우 더 명확한 메시지
            if "401" in error_str or "invalid_api_key" in error_str or "Incorrect API key" in error_str:
                raise ValueError("OpenAI API 키가 유효하지 않습니다. Railway 환경 변수에서 OPENAI_API_KEY를 확인하고 올바른 키로 업데이트해주세요.")
            # 기타 API 에러는 그대로 전파
            raise
        
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
        
        # API 키 관련 에러인 경우 더 명확한 메시지 제공
        error_str = str(e)
        if "401" in error_str or "invalid_api_key" in error_str or "Incorrect API key" in error_str:
            return {
                "success": False,
                "error": "OpenAI API 키가 유효하지 않습니다. Railway 환경 변수에서 OPENAI_API_KEY를 확인하고 올바른 키로 업데이트해주세요. https://platform.openai.com/api-keys 에서 새 API 키를 생성할 수 있습니다."
            }
        
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
