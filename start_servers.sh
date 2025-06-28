#!/bin/bash

# 기존 프로세스 종료
echo "기존 서버 프로세스를 종료합니다..."
pkill -f "uvicorn app.main:app"
pkill -f "frontend_server.py"
sleep 2

# 가상환경 활성화 및 백엔드 서버 시작 (백그라운드)
echo "백엔드 서버를 시작합니다 (포트 8080)..."
cd /Users/kkumtree/github/lipcoding-competition
source .venv/bin/activate
nohup uvicorn app.main:app --host 0.0.0.0 --port 8080 --reload > backend.log 2>&1 &
BACKEND_PID=$!

# 프론트엔드 서버 시작 (백그라운드)
echo "프론트엔드 서버를 시작합니다 (포트 3000)..."
nohup python frontend_server.py > frontend.log 2>&1 &
FRONTEND_PID=$!

echo "백엔드 서버 PID: $BACKEND_PID"
echo "프론트엔드 서버 PID: $FRONTEND_PID"

# 서버 상태 확인
sleep 3
echo "서버 상태 확인 중..."

if curl -s http://localhost:8080/docs > /dev/null; then
    echo "✅ 백엔드 서버가 정상적으로 실행 중입니다 (http://localhost:8080)"
else
    echo "❌ 백엔드 서버 시작에 실패했습니다"
fi

if curl -s http://localhost:3000 > /dev/null; then
    echo "✅ 프론트엔드 서버가 정상적으로 실행 중입니다 (http://localhost:3000)"
else
    echo "❌ 프론트엔드 서버 시작에 실패했습니다"
fi

echo ""
echo "📋 서버 관리 명령어:"
echo "  - 백엔드 로그 확인: tail -f backend.log"
echo "  - 프론트엔드 로그 확인: tail -f frontend.log"
echo "  - 모든 서버 종료: pkill -f 'uvicorn app.main:app' && pkill -f 'frontend_server.py'"
echo ""
echo "🌐 접속 URL:"
echo "  - API 문서: http://localhost:8080/docs"
echo "  - 웹 앱: http://localhost:3000"
