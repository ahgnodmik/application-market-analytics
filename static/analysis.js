// 분석 페이지 스크립트

document.addEventListener('DOMContentLoaded', async () => {
    await loadMatrix();
    
    document.getElementById('filter-form').addEventListener('submit', async (e) => {
        e.preventDefault();
        await loadRecommendations();
    });
    
    await loadRecommendations();
});

async function loadMatrix() {
    const chartEl = document.getElementById('matrix-chart');
    chartEl.innerHTML = '<p class="text-notion-text-light">로딩 중...</p>';
    
    try {
        const response = await fetch('/api/analysis/matrix');
        const data = await response.json();
        
        if (data.apps.length === 0) {
            chartEl.innerHTML = '<p class="text-notion-text-light">데이터가 없습니다.</p>';
            return;
        }
        
        const width = 800;
        const height = 600;
        const padding = 80;
        
        chartEl.innerHTML = `
            <svg width="${width}" height="${height}" class="border border-notion-border rounded bg-white">
                <text x="${width/2}" y="30" text-anchor="middle" class="font-semibold" fill="#37352f" font-size="16">2축 매트릭스</text>
                
                <!-- 축선 -->
                <line x1="${padding}" y1="${height-padding}" x2="${width-padding}" y2="${height-padding}" stroke="#e9e9e7" stroke-width="2"/>
                <line x1="${padding}" y1="${padding}" x2="${padding}" y2="${height-padding}" stroke="#e9e9e7" stroke-width="2"/>
                
                <!-- 축 레이블 -->
                <text x="${width/2}" y="${height-20}" text-anchor="middle" fill="#787774" font-size="14">구현 난이도 (낮을수록 우수)</text>
                <text x="20" y="${height/2}" text-anchor="middle" transform="rotate(-90, 20, ${height/2})" fill="#787774" font-size="14">시장성 점수 (높을수록 우수)</text>
                
                <!-- 앱 점들 -->
                ${data.apps.map((app, idx) => {
                    const x = padding + (app.difficulty / 2) * (width - 2*padding);
                    const y = height - padding - (app.marketability / 10) * (height - 2*padding);
                    return `
                        <circle cx="${x}" cy="${y}" r="5" fill="#2383e2" opacity="0.6" class="cursor-pointer" data-app-id="${app.id}">
                            <title>${app.name}\n난이도: ${app.difficulty.toFixed(2)}\n시장성: ${app.marketability.toFixed(2)}</title>
                        </circle>
                    `;
                }).join('')}
                
                <!-- 기준선 (시장성 >= 6, 난이도 <= 1.0 영역 표시) -->
                <rect x="${padding}" y="${height - padding - (6/10) * (height - 2*padding)}" 
                      width="${(1.0/2) * (width - 2*padding)}" 
                      height="${(6/10) * (height - 2*padding)}" 
                      fill="rgba(34, 197, 94, 0.1)" 
                      stroke="rgba(34, 197, 94, 0.3)" 
                      stroke-width="1" 
                      stroke-dasharray="5,5"/>
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
    listEl.innerHTML = '<p class="text-notion-text-light">로딩 중...</p>';
    
    try {
        const response = await fetch(
            `/api/analysis/recommendations?min_marketability=${minMarketability}&max_difficulty=${maxDifficulty}&max_features=${maxFeatures}`
        );
        
        if (!response.ok) {
            const errorData = await response.json().catch(() => ({ detail: '알 수 없는 오류가 발생했습니다.' }));
            throw new Error(errorData.detail || `HTTP ${response.status}`);
        }
        
        const recommendations = await response.json();
        
        if (recommendations.length === 0) {
            listEl.innerHTML = '<p class="text-notion-text-light">조건에 맞는 추천 항목이 없습니다. Play Store에서 앱을 가져오고 기능을 추가한 후 다시 시도해보세요.</p>';
            return;
        }
        
        listEl.innerHTML = recommendations.map(type => `
            <div class="p-4 border border-notion-border rounded hover:bg-notion-hover transition-colors">
                <h3 class="font-semibold text-lg text-notion-text mb-2">${type.name || '앱 타입'}</h3>
                <p class="text-sm text-notion-text-light mb-3">
                    <strong>핵심 기능:</strong> ${type.core_features ? type.core_features.join(', ') : 'N/A'}
                </p>
                <div class="flex flex-wrap gap-2">
                    <span class="px-2 py-1 text-xs rounded bg-red-50 text-red-700 border border-red-200">
                        난이도: ${type.avg_difficulty ? type.avg_difficulty.toFixed(2) : 'N/A'}
                    </span>
                    <span class="px-2 py-1 text-xs rounded bg-green-50 text-green-700 border border-green-200">
                        시장성: ${type.avg_marketability ? type.avg_marketability.toFixed(2) : 'N/A'}
                    </span>
                    <span class="px-2 py-1 text-xs rounded bg-blue-50 text-blue-700 border border-blue-200">
                        앱 수: ${type.app_count || 0}
                    </span>
                    <span class="px-2 py-1 text-xs rounded bg-purple-50 text-purple-700 border border-purple-200">
                        화면: ${type.mvp_screens || 'N/A'}개
                    </span>
                    <span class="px-2 py-1 text-xs rounded bg-yellow-50 text-yellow-700 border border-yellow-200">
                        기간: ${type.build_time || 'N/A'}
                    </span>
                </div>
                ${type.notes ? `<p class="text-sm text-notion-text mt-3"><strong>참고:</strong> ${type.notes}</p>` : ''}
            </div>
        `).join('');
    } catch (error) {
        console.error('Error loading recommendations:', error);
        listEl.innerHTML = `
            <div class="p-4 bg-red-50 border border-red-200 rounded">
                <p class="text-red-800 font-medium mb-2">추천 항목을 불러오는 중 오류가 발생했습니다.</p>
                <p class="text-red-600 text-sm">${error.message || '알 수 없는 오류'}</p>
            </div>
        `;
    }
}
