// 분석 페이지 스크립트

document.addEventListener('DOMContentLoaded', async () => {
    await loadMatrix();
    
    // 필터 폼 제출
    document.getElementById('filter-form').addEventListener('submit', async (e) => {
        e.preventDefault();
        await loadRecommendations();
    });
    
    // 초기 추천 로드
    await loadRecommendations();
});

async function loadMatrix() {
    const chartEl = document.getElementById('matrix-chart');
    chartEl.innerHTML = '<p class="text-notion-textLight">로딩 중...</p>';
    
    try {
        const response = await fetch('/api/analysis/matrix');
        const data = await response.json();
        
        if (data.apps.length === 0) {
            chartEl.innerHTML = '<p class="text-notion-textLight">데이터가 없습니다.</p>';
            return;
        }
        
        // 매트릭스 차트 그리기
        const width = 700;
        const height = 500;
        const padding = 80;
        
        chartEl.innerHTML = `
            <svg width="${width}" height="${height}" class="border border-notion-border rounded-lg bg-white">
                <text x="${width/2}" y="30" text-anchor="middle" class="font-semibold" fill="#37352f">2축 매트릭스</text>
                <line x1="${padding}" y1="${height-padding}" x2="${width-padding}" y2="${height-padding}" stroke="#e9e9e7" stroke-width="2"/>
                <line x1="${padding}" y1="${padding}" x2="${padding}" y2="${height-padding}" stroke="#e9e9e7" stroke-width="2"/>
                
                <text x="${width/2}" y="${height-30}" text-anchor="middle" fill="#787774" font-size="14">구현 난이도 (낮을수록 우수)</text>
                <text x="30" y="${height/2}" text-anchor="middle" transform="rotate(-90, 30, ${height/2})" fill="#787774" font-size="14">시장성 점수 (높을수록 우수)</text>
                
                ${data.apps.map((app, idx) => {
                    const x = padding + (app.difficulty / 2) * (width - 2*padding);
                    const y = height - padding - (app.marketability / 10) * (height - 2*padding);
                    return `<circle cx="${x}" cy="${y}" r="6" fill="#0b85f3" opacity="0.7" class="cursor-pointer hover:r="8"">
                        <title>${app.name}\n난이도: ${app.difficulty.toFixed(2)}\n시장성: ${app.marketability.toFixed(2)}</title>
                    </circle>`;
                }).join('')}
            </svg>
        `;
    } catch (error) {
        console.error('Error loading matrix:', error);
        chartEl.innerHTML = '<p class="text-red-600">매트릭스 데이터를 불러오는 중 오류가 발생했습니다.</p>';
    }
}

async function loadRecommendations() {
    const minMarketability = parseFloat(document.getElementById('min-marketability').value);
    const maxDifficulty = parseFloat(document.getElementById('max-difficulty').value);
    const maxFeatures = parseInt(document.getElementById('max-features').value);
    
    const listEl = document.getElementById('recommendations-list');
    listEl.innerHTML = '<p class="text-notion-textLight">로딩 중...</p>';
    
    try {
        const response = await fetch(
            `/api/analysis/recommendations?min_marketability=${minMarketability}&max_difficulty=${maxDifficulty}&max_features=${maxFeatures}`
        );
        const recommendations = await response.json();
        
        if (recommendations.length === 0) {
            listEl.innerHTML = '<p class="text-notion-textLight">조건에 맞는 추천 항목이 없습니다. 필터를 조정해보세요.</p>';
            return;
        }
        
        listEl.innerHTML = recommendations.map(type => `
            <div class="border border-notion-border rounded-lg p-5 hover:bg-notion-sidebar transition-colors">
                <h4 class="text-xl font-semibold text-notion-text mb-3">${type.name}</h4>
                <p class="text-sm text-notion-textLight mb-3"><strong>핵심 기능:</strong> ${type.core_features.join(', ')}</p>
                <div class="flex flex-wrap gap-2 mb-3">
                    <span class="px-3 py-1 bg-red-100 text-red-700 rounded text-sm font-medium">난이도: ${type.avg_difficulty.toFixed(2)}</span>
                    <span class="px-3 py-1 bg-green-100 text-green-700 rounded text-sm font-medium">시장성: ${type.avg_marketability.toFixed(2)}</span>
                    <span class="px-3 py-1 bg-blue-100 text-blue-700 rounded text-sm font-medium">앱 수: ${type.app_count}</span>
                    <span class="px-3 py-1 bg-purple-100 text-purple-700 rounded text-sm font-medium">화면: ${type.mvp_screens}개</span>
                    <span class="px-3 py-1 bg-yellow-100 text-yellow-700 rounded text-sm font-medium">기간: ${type.build_time}</span>
                </div>
                ${type.notes ? `<p class="text-sm text-notion-text"><strong>참고:</strong> ${type.notes}</p>` : ''}
            </div>
        `).join('');
    } catch (error) {
        console.error('Error loading recommendations:', error);
        listEl.innerHTML = '<p class="text-red-600">추천 목록을 불러오는 중 오류가 발생했습니다.</p>';
    }
}




