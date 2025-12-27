// 앱 관리 페이지 스크립트

let currentAppId = null;

// 페이지 로드 시 앱 목록 불러오기
document.addEventListener('DOMContentLoaded', async () => {
    await loadApps();
    
    // 앱 추가 폼 제출
    document.getElementById('add-app-form').addEventListener('submit', async (e) => {
        e.preventDefault();
        await addApp();
    });
    
    // CSV 업로드 폼 제출
    document.getElementById('upload-form').addEventListener('submit', async (e) => {
        e.preventDefault();
        await uploadCSV();
    });
});

async function loadApps() {
    const listEl = document.getElementById('apps-list');
    listEl.innerHTML = '<p class="text-notion-textLight">로딩 중...</p>';
    
    try {
        const response = await fetch('/api/apps/');
        const apps = await response.json();
        
        if (apps.length === 0) {
            listEl.innerHTML = '<p class="text-notion-textLight">등록된 앱이 없습니다. 앱을 추가해보세요.</p>';
            return;
        }
        
        listEl.innerHTML = apps.map(app => `
            <div class="bg-white border border-notion-border rounded-lg p-4 hover:shadow-md transition-all cursor-pointer" onclick="showAppDetail(${app.id})">
                <div class="flex justify-between items-start">
                    <div class="flex-1">
                        <h3 class="font-semibold text-lg text-notion-text mb-2">${app.name}</h3>
                        <div class="flex flex-wrap gap-3 text-sm text-notion-textLight">
                            <span>${app.category || '카테고리 없음'}</span>
                            <span>평점: ${app.rating ? app.rating.toFixed(1) : 'N/A'}</span>
                            <span>리뷰: ${app.review_count ? app.review_count.toLocaleString() : 'N/A'}</span>
                        </div>
                    </div>
                    <div class="flex gap-2">
                        <span class="px-2 py-1 bg-red-100 text-red-700 rounded text-xs font-medium">난이도: ${app.difficulty_score.toFixed(2)}</span>
                        <span class="px-2 py-1 bg-green-100 text-green-700 rounded text-xs font-medium">시장성: ${app.marketability_score.toFixed(2)}</span>
                    </div>
                </div>
            </div>
        `).join('');
    } catch (error) {
        console.error('Error loading apps:', error);
        listEl.innerHTML = '<p class="text-red-600">앱 목록을 불러오는 중 오류가 발생했습니다.</p>';
    }
}

async function addApp() {
    const form = document.getElementById('add-app-form');
    const formData = new FormData(form);
    
    const appData = {
        name: formData.get('name'),
        category: formData.get('category') || null,
        rating: formData.get('rating') ? parseFloat(formData.get('rating')) : null,
        review_count: formData.get('review_count') ? parseInt(formData.get('review_count')) : null,
        price_model: formData.get('price_model') || null,
        last_update: formData.get('last_update') || null,
        description: formData.get('description') || null
    };
    
    try {
        const response = await fetch('/api/apps/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(appData)
        });
        
        if (response.ok) {
            const app = await response.json();
            closeModal('add-app-modal');
            form.reset();
            await loadApps();
            alert('앱이 추가되었습니다.');
        } else {
            const error = await response.json();
            alert(`오류: ${error.detail || '앱 추가에 실패했습니다.'}`);
        }
    } catch (error) {
        console.error('Error adding app:', error);
        alert('앱 추가 중 오류가 발생했습니다.');
    }
}

async function uploadCSV() {
    const form = document.getElementById('upload-form');
    const formData = new FormData(form);
    const resultEl = document.getElementById('upload-result');
    
    resultEl.innerHTML = '<p class="text-notion-textLight">업로드 중...</p>';
    
    try {
        const response = await fetch('/api/upload/csv', {
            method: 'POST',
            body: formData
        });
        
        const result = await response.json();
        
        if (response.ok) {
            resultEl.innerHTML = `
                <div class="p-4 bg-green-50 border border-green-200 rounded-md mb-4">
                    <p class="text-green-800 font-medium">${result.message}</p>
                    <p class="text-sm text-green-600 mt-1">생성된 앱 수: ${result.created_count}</p>
                    ${result.errors ? `<p class="text-sm text-orange-600 mt-1">오류 발생: ${result.errors.length}건</p>` : ''}
                </div>
            `;
            form.reset();
            await loadApps();
            setTimeout(() => {
                closeModal('upload-modal');
                resultEl.innerHTML = '';
            }, 2000);
        } else {
            resultEl.innerHTML = `<div class="p-4 bg-red-50 border border-red-200 rounded-md"><p class="text-red-800">오류: ${result.detail}</p></div>`;
        }
    } catch (error) {
        console.error('Error uploading CSV:', error);
        resultEl.innerHTML = '<div class="p-4 bg-red-50 border border-red-200 rounded-md"><p class="text-red-800">CSV 업로드 중 오류가 발생했습니다.</p></div>';
    }
}

async function showAppDetail(appId) {
    currentAppId = appId;
    const modal = document.getElementById('app-detail-modal');
    const contentEl = document.getElementById('app-detail-content');
    
    try {
        const response = await fetch(`/api/apps/${appId}`);
        const app = await response.json();
        
        const featuresResponse = await fetch(`/api/apps/${appId}/features`);
        const features = await featuresResponse.json();
        
        contentEl.innerHTML = `
            <div class="space-y-6">
                <div>
                    <h3 class="text-2xl font-bold text-notion-text mb-4">${app.name}</h3>
                    <div class="grid grid-cols-2 gap-4 text-sm">
                        <div>
                            <span class="text-notion-textLight">카테고리:</span>
                            <span class="ml-2 text-notion-text">${app.category || 'N/A'}</span>
                        </div>
                        <div>
                            <span class="text-notion-textLight">평점:</span>
                            <span class="ml-2 text-notion-text">${app.rating ? app.rating.toFixed(1) : 'N/A'}</span>
                        </div>
                        <div>
                            <span class="text-notion-textLight">리뷰 수:</span>
                            <span class="ml-2 text-notion-text">${app.review_count ? app.review_count.toLocaleString() : 'N/A'}</span>
                        </div>
                        <div>
                            <span class="text-notion-textLight">가격 모델:</span>
                            <span class="ml-2 text-notion-text">${app.price_model || 'N/A'}</span>
                        </div>
                        <div>
                            <span class="text-notion-textLight">난이도 점수:</span>
                            <span class="ml-2 px-2 py-1 bg-red-100 text-red-700 rounded text-xs font-medium">${app.difficulty_score.toFixed(2)}</span>
                        </div>
                        <div>
                            <span class="text-notion-textLight">시장성 점수:</span>
                            <span class="ml-2 px-2 py-1 bg-green-100 text-green-700 rounded text-xs font-medium">${app.marketability_score.toFixed(2)}</span>
                        </div>
                    </div>
                    ${app.description ? `<p class="mt-4 text-notion-text"><strong>설명:</strong> ${app.description}</p>` : ''}
                </div>
                
                <div class="border-t border-notion-border pt-6">
                    <div class="flex justify-between items-center mb-4">
                        <h4 class="text-lg font-semibold text-notion-text">기능 목록</h4>
                        <button onclick="showAddFeatureModal()" class="px-3 py-1.5 bg-notion-blue text-white rounded-md hover:bg-blue-600 transition-colors text-sm">기능 추가</button>
                    </div>
                    <div id="features-list" class="space-y-2">
                        ${features.length === 0 ? '<p class="text-notion-textLight">기능이 없습니다.</p>' : ''}
                        ${features.map(f => `
                            <div class="flex justify-between items-center p-3 bg-notion-sidebar rounded-md">
                                <span class="text-notion-text"><strong>${f.name}</strong> (${f.feature_type}) - 난이도: ${f.difficulty_score.toFixed(2)}</span>
                                <button onclick="deleteFeature(${f.id})" class="px-3 py-1 bg-red-600 text-white rounded-md hover:bg-red-700 transition-colors text-sm">삭제</button>
                            </div>
                        `).join('')}
                    </div>
                </div>
            </div>
        `;
        
        showModal('app-detail-modal');
    } catch (error) {
        console.error('Error loading app detail:', error);
        alert('앱 상세 정보를 불러오는 중 오류가 발생했습니다.');
    }
}

async function deleteFeature(featureId) {
    if (!confirm('이 기능을 삭제하시겠습니까?')) {
        return;
    }
    
    try {
        const response = await fetch(`/api/apps/${currentAppId}/features/${featureId}`, {
            method: 'DELETE'
        });
        
        if (response.ok) {
            await showAppDetail(currentAppId);
        } else {
            alert('기능 삭제에 실패했습니다.');
        }
    } catch (error) {
        console.error('Error deleting feature:', error);
        alert('기능 삭제 중 오류가 발생했습니다.');
    }
}

function showAddAppModal() {
    showModal('add-app-modal');
}

function showUploadModal() {
    showModal('upload-modal');
}

function showAddFeatureModal() {
    const featureName = prompt('기능 이름:');
    if (!featureName) return;
    
    const featureType = prompt('기능 타입 (input, storage, query, notification, media):');
    if (!featureType) return;
    
    const description = prompt('기능 설명 (선택사항):') || '';
    
    addFeature({
        name: featureName,
        feature_type: featureType,
        description: description
    });
}

async function addFeature(featureData) {
    try {
        const response = await fetch(`/api/apps/${currentAppId}/features`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(featureData)
        });
        
        if (response.ok) {
            await showAppDetail(currentAppId);
        } else {
            const error = await response.json();
            alert(`오류: ${error.detail || '기능 추가에 실패했습니다.'}`);
        }
    } catch (error) {
        console.error('Error adding feature:', error);
        alert('기능 추가 중 오류가 발생했습니다.');
    }
}

function showModal(modalId) {
    document.getElementById(modalId).classList.remove('hidden');
    document.getElementById(modalId).classList.add('flex');
}

function closeModal(modalId) {
    document.getElementById(modalId).classList.add('hidden');
    document.getElementById(modalId).classList.remove('flex');
}




