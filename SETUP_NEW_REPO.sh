#!/bin/bash

# 새 GitHub 저장소 설정 스크립트

echo "🚀 새 GitHub 저장소 설정을 시작합니다..."
echo ""

# 1. 현재 원격 저장소 확인
echo "1. 현재 원격 저장소 확인:"
git remote -v
echo ""

# 2. 기존 원격 저장소 제거
echo "2. 기존 원격 저장소 제거 중..."
git remote remove origin
echo "✅ 완료"
echo ""

# 3. 변경사항 확인
echo "3. 변경사항 확인:"
git status --short | head -5
echo ""

echo "=========================================="
echo "✅ 준비 완료!"
echo "=========================================="
echo ""
echo "다음 단계:"
echo "1. GitHub에서 새 저장소 생성:"
echo "   - 이름: app-market-analytics"
echo "   - README, .gitignore, license 추가하지 마세요"
echo ""
echo "2. 다음 명령어 실행:"
echo "   git remote add origin https://github.com/YOUR_USERNAME/app-market-analytics.git"
echo "   git add ."
echo "   git commit -m 'Initial commit: Application Market Analytics'"
echo "   git push -u origin main"
echo ""

