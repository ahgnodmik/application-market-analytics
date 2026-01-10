/**
 * Netlify Functions JavaScript 서버 함수
 * 모든 요청을 처리하는 메인 함수
 */

exports.handler = async (event, context) => {
  const path = event.path || event.rawPath || '/';
  const method = event.httpMethod || event.requestContext?.http?.method || 'GET';
  
  // Health check
  if (path === '/health' || path.endsWith('/health')) {
    return {
      statusCode: 200,
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        status: 'ok',
        message: 'JavaScript server function is working',
        path: path,
        method: method,
        functions: {
          javascript: 'working',
          python: 'not supported',
        },
      }),
    };
  }
  
  // Root path - 메인 페이지
  if (path === '/' || path === '') {
    const html = `<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Market Analytics</title>
    <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-gray-50">
    <nav class="bg-white border-b border-gray-200">
        <div class="max-w-7xl mx-auto px-6 py-4">
            <h1 class="text-2xl font-bold">📊 Market Analytics</h1>
        </div>
    </nav>
    <main class="max-w-7xl mx-auto px-6 py-8">
        <div class="bg-white rounded-lg shadow p-6 mb-6">
            <h2 class="text-xl font-semibold mb-4">서비스 상태</h2>
            <div class="space-y-4">
                <div class="p-4 bg-green-50 rounded-lg">
                    <p class="text-green-800 font-medium">✅ JavaScript Functions 작동 중</p>
                    <p class="text-sm text-green-600 mt-1">Netlify Functions는 정상 작동합니다.</p>
                </div>
                <div class="p-4 bg-yellow-50 rounded-lg">
                    <p class="text-yellow-800 font-medium">⚠️ Python FastAPI Functions 제한</p>
                    <p class="text-sm text-yellow-600 mt-1">Python Functions는 Netlify에서 제한적으로 지원됩니다.</p>
                </div>
            </div>
            <div class="mt-6 space-y-2">
                <a href="/health" class="text-blue-600 hover:underline block">Health Check</a>
                <a href="/.netlify/functions/test" class="text-blue-600 hover:underline block">테스트 함수</a>
            </div>
        </div>
    </main>
</body>
</html>`;
    
    return {
      statusCode: 200,
      headers: {
        'Content-Type': 'text/html; charset=utf-8',
      },
      body: html,
    };
  }
  
  // Default response
  return {
    statusCode: 200,
    headers: {
      'Content-Type': 'text/html; charset=utf-8',
    },
    body: `<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Market Analytics</title>
    <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-gray-50">
    <div class="max-w-4xl mx-auto px-4 py-16">
        <div class="bg-white rounded-lg shadow-lg p-8">
            <h1 class="text-3xl font-bold mb-4">📊 Market Analytics</h1>
            <p class="text-gray-600 mb-4">Path: ${path}</p>
            <a href="/" class="text-blue-600 hover:underline">홈으로</a>
        </div>
    </div>
</body>
</html>`,
  };
};
