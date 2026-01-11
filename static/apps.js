// 앱 관리 페이지 스크립트

let currentAppId = null;

document.addEventListener('DOMContentLoaded', async () => {
    await loadApps();
});

async function loadApps() {
    const listEl = document.getElementById('apps-list');
    listEl.innerHTML = '<p class="text-notion-text-light">로딩 중...</p>';
    
    try {
        const response = await fetch('/api/apps/playstore?limit=1000');
        const apps = await response.json();
        
        if (apps.length === 0) {
            listEl.innerHTML = `
                <div class="text-center py-12">
                    <p class="text-notion-text-light mb-4">Play Store에서 가져온 앱이 없습니다.</p>
                    <a href="/category-analysis" class="notion-button notion-button-blue no-underline inline-block">
                        카테고리 분석에서 앱 가져오기
                    </a>
                </div>
            `;
            return;
        }
        
        listEl.innerHTML = apps.map(app => `
            <div class="flex items-center justify-between p-4 border border-notion-border rounded hover:bg-notion-hover transition-colors cursor-pointer" onclick="showAppDetail(${app.id})">
                <div class="flex-1">
                    <h3 class="font-semibold text-lg text-notion-text mb-1">${app.name}</h3>
                    <div class="text-sm text-notion-text-light">
                        ${app.category || '카테고리 없음'} • 
                        평점: ${app.rating ? app.rating.toFixed(1) : 'N/A'} ⭐ • 
                        리뷰: ${app.review_count ? app.review_count.toLocaleString() : '0'}개
                    </div>
                    ${app.description ? `<p class="text-sm text-notion-text-light mt-2 line-clamp-2">${app.description.substring(0, 150)}...</p>` : ''}
                </div>
                <div class="flex flex-col gap-2 ml-6 items-end">
                    <div class="flex gap-2">
                        <span class="px-2 py-1 text-xs rounded ${app.difficulty_score <= 1.0 ? 'bg-green-50 text-green-700 border border-green-200' : 'bg-gray-50 text-gray-700 border border-gray-200'}">
                            난이도 ${app.difficulty_score ? app.difficulty_score.toFixed(1) : 'N/A'}
                        </span>
                        <span class="px-2 py-1 text-xs rounded ${app.marketability_score >= 6.0 ? 'bg-blue-50 text-blue-700 border border-blue-200' : 'bg-gray-50 text-gray-700 border border-gray-200'}">
                            시장성 ${app.marketability_score ? app.marketability_score.toFixed(1) : 'N/A'}
                        </span>
                    </div>
                    <div class="text-xs text-notion-text-light">
                        ${app.price_model === 'free' ? '무료' : app.price_model === 'paid' ? '유료' : app.price_model === 'subscription' ? '구독' : 'N/A'}
                    </div>
                </div>
            </div>
        `).join('');
    } catch (error) {
        console.error('Error loading apps:', error);
        listEl.innerHTML = '<p class="text-red-600">앱 목록을 불러오는 중 오류가 발생했습니다.</p>';
    }
}

async function showAppDetail(appId) {
    currentAppId = appId;
    const modal = document.getElementById('app-detail-modal');
    const content = document.getElementById('app-detail-content');
    
    modal.classList.remove('hidden');
    modal.classList.add('flex');
    content.innerHTML = '<p class="text-notion-text-light">로딩 중...</p>';
    
    try {
        const appRes = await fetch(`/api/apps/${appId}`);
        const app = await appRes.json();
        
        const featuresRes = await fetch(`/api/apps/${appId}/features`);
        const features = await featuresRes.json();
        
        content.innerHTML = `
            <div class="space-y-6">
                <div>
                    <h2 class="text-2xl font-semibold text-notion-text mb-4">${app.name}</h2>
                    <div class="grid grid-cols-2 md:grid-cols-4 gap-4">
                        <div>
                            <div class="text-sm text-notion-text-light mb-1">카테고리</div>
                            <div class="font-medium">${app.category || 'N/A'}</div>
                        </div>
                        <div>
                            <div class="text-sm text-notion-text-light mb-1">평점</div>
                            <div class="font-medium">${app.rating ? app.rating.toFixed(1) : 'N/A'} ⭐</div>
                        </div>
                        <div>
                            <div class="text-sm text-notion-text-light mb-1">리뷰 수</div>
                            <div class="font-medium">${app.review_count ? app.review_count.toLocaleString() : '0'}개</div>
                        </div>
                        <div>
                            <div class="text-sm text-notion-text-light mb-1">가격 모델</div>
                            <div class="font-medium">${app.price_model === 'free' ? '무료' : app.price_model === 'paid' ? '유료' : app.price_model === 'subscription' ? '구독' : 'N/A'}</div>
                        </div>
                        <div>
                            <div class="text-sm text-notion-text-light mb-1">난이도 점수</div>
                            <div class="font-medium">${app.difficulty_score ? app.difficulty_score.toFixed(2) : '0.00'}</div>
                        </div>
                        <div>
                            <div class="text-sm text-notion-text-light mb-1">시장성 점수</div>
                            <div class="font-medium">${app.marketability_score ? app.marketability_score.toFixed(2) : '0.00'}</div>
                        </div>
                    </div>
                </div>
                
                ${app.description ? `
                <div>
                    <h3 class="text-lg font-semibold text-notion-text mb-2">설명</h3>
                    <p class="text-notion-text-light whitespace-pre-wrap">${app.description}</p>
                </div>
                ` : ''}
                
                <div>
                    <h3 class="text-lg font-semibold text-notion-text mb-2">기능 (${features.length}개)</h3>
                    ${features.length > 0 ? `
                        <div class="space-y-2">
                            ${features.map(f => `
                                <div class="p-3 border border-notion-border rounded">
                                    <div class="font-medium text-notion-text">${f.name}</div>
                                    <div class="text-sm text-notion-text-light mt-1">
                                        타입: ${f.feature_type || 'N/A'} • 
                                        난이도: ${f.difficulty_score ? f.difficulty_score.toFixed(2) : 'N/A'}
                                    </div>
                                </div>
                            `).join('')}
                        </div>
                    ` : '<p class="text-notion-text-light">기능이 없습니다.</p>'}
                </div>
            </div>
        `;
    } catch (error) {
        console.error('Error loading app detail:', error);
        content.innerHTML = '<p class="text-red-600">앱 정보를 불러오는 중 오류가 발생했습니다.</p>';
    }
}

window.showAppDetail = showAppDetail;
