#!/usr/bin/env python3
"""
API 엔드포인트를 통한 수집 및 분석 프로세스 확인
"""
import requests
import json
import time

BASE_URL = "https://app-analytics.up.railway.app"

def test_api_endpoint(endpoint, method="GET", params=None, json_data=None):
    """API 엔드포인트 테스트"""
    url = f"{BASE_URL}{endpoint}"
    print(f"\n{'='*60}")
    print(f"🔍 Testing: {method} {endpoint}")
    print(f"{'='*60}")
    
    try:
        if method == "GET":
            response = requests.get(url, params=params, timeout=30)
        elif method == "POST":
            response = requests.post(url, params=params, json=json_data, timeout=60)
        else:
            print(f"❌ Unsupported method: {method}")
            return None
        
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            try:
                data = response.json()
                print(f"✅ Success!")
                print(f"Response (first 500 chars): {json.dumps(data, indent=2, ensure_ascii=False)[:500]}")
                return data
            except:
                print(f"Response Text: {response.text[:500]}")
                return {"text": response.text[:500]}
        else:
            print(f"❌ Error!")
            try:
                error_data = response.json()
                print(f"Error: {json.dumps(error_data, indent=2, ensure_ascii=False)}")
            except:
                print(f"Error Text: {response.text[:500]}")
            return None
            
    except Exception as e:
        print(f"❌ Exception: {e}")
        import traceback
        traceback.print_exc()
        return None

def test_app_collection():
    """앱 수집 테스트"""
    print("\n" + "="*60)
    print("📥 앱 수집 테스트")
    print("="*60)
    
    # 생산성 앱 수집 테스트 (작은 수량으로)
    endpoint = "/api/playstore/fetch-rankings"
    params = {
        "category": "top_free",
        "limit": "5",  # 작은 수량으로 테스트
        "play_category": "APPLICATION_PRODUCTIVITY",
        "force": "true"
    }
    
    result = test_api_endpoint(endpoint, method="POST", params=params)
    
    if result:
        if "apps" in result:
            print(f"\n✅ 수집된 앱 수: {len(result.get('apps', []))}")
            for app in result.get('apps', [])[:3]:
                print(f"  - {app.get('name', 'Unknown')} (난이도: {app.get('difficulty_score', 0):.2f})")
        elif "saved_count" in result or "updated_count" in result:
            saved = result.get("saved_count", 0)
            updated = result.get("updated_count", 0)
            print(f"\n✅ 저장된 앱: {saved}개, 업데이트된 앱: {updated}개")
    else:
        print("\n❌ 앱 수집 실패")
    
    return result

def test_statistics():
    """통계 API 테스트"""
    print("\n" + "="*60)
    print("📊 통계 확인")
    print("="*60)
    
    endpoint = "/api/apps/stats"
    result = test_api_endpoint(endpoint, method="GET")
    
    if result:
        print(f"\n✅ 전체 앱 수: {result.get('total_apps', 0)}")
        print(f"   난이도 점수가 있는 앱: {result.get('apps_with_difficulty', 0)}")
        print(f"   시장성 점수가 있는 앱: {result.get('apps_with_marketability', 0)}")
    
    return result

def test_mvp_apps():
    """MVP 앱 목록 테스트"""
    print("\n" + "="*60)
    print("💡 MVP 앱 목록 확인")
    print("="*60)
    
    endpoint = "/api/playstore/mvp-productivity-apps"
    params = {
        "limit": "5"
    }
    
    result = test_api_endpoint(endpoint, method="GET", params=params)
    
    if result:
        apps = result.get("apps", [])
        print(f"\n✅ MVP 앱 수: {len(apps)}")
        for app in apps[:3]:
            print(f"  - {app.get('name', 'Unknown')} (난이도: {app.get('difficulty_score', 0):.2f}, 시장성: {app.get('marketability_score', 0):.2f})")
    
    return result

if __name__ == "__main__":
    print("="*60)
    print("🚀 앱 수집 및 분석 프로세스 확인")
    print("="*60)
    print(f"Base URL: {BASE_URL}")
    
    # 1. 통계 확인
    test_statistics()
    
    # 2. 앱 수집 테스트
    collection_result = test_app_collection()
    
    # 3. 수집 후 통계 재확인
    time.sleep(2)
    test_statistics()
    
    # 4. MVP 앱 목록 확인
    test_mvp_apps()
    
    print("\n" + "="*60)
    print("✅ 테스트 완료")
    print("="*60)
