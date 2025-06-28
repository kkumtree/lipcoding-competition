#!/bin/bash

# 기존 프로세스 종료
echo "기존 서버 프로세스를 종료합니다..."
pkill -f "uvicorn app.main:app" || true
pkill -f "frontend_server.py" || true
sleep 2

# 가상환경 활성화 및 백엔드 서버 시작 (백그라운드)
echo "백엔드 서버를 시작합니다 (포트 8080)..."
cd /Users/kkumtree/github/lipcoding-competition
source .venv/bin/activate
nohup uvicorn app.main:app --host localhost --port 8080 --reload > backend.log 2>&1 &
BACKEND_PID=$!

# 프론트엔드 서버 시작 (백그라운드)
echo "프론트엔드 서버를 시작합니다 (포트 3000)..."
nohup python frontend_server.py > frontend.log 2>&1 &
FRONTEND_PID=$!

echo "백엔드 서버 PID: $BACKEND_PID"
echo "프론트엔드 서버 PID: $FRONTEND_PID"

# 서버 상태 확인
sleep 5
echo "서버 상태 확인 중..."

# 백엔드 서버 상태 확인 (최대 30초 대기)
for i in {1..15}; do
    if curl -s http://localhost:8080/docs > /dev/null 2>&1; then
        echo "✅ 백엔드 서버가 정상적으로 실행 중입니다 (http://localhost:8080)"
        break
    fi
    echo "백엔드 서버 시작 대기 중... ($i/15)"
    sleep 2
done

# 프론트엔드 서버 상태 확인 (최대 30초 대기)
for i in {1..15}; do
    if curl -s http://localhost:3000 > /dev/null 2>&1; then
        echo "✅ 프론트엔드 서버가 정상적으로 실행 중입니다 (http://localhost:3000)"
        break
    fi
    echo "프론트엔드 서버 시작 대기 중... ($i/15)"
    sleep 2
done

echo ""
echo "📋 서버 관리 명령어:"
echo "  - 백엔드 로그 확인: tail -f backend.log"
echo "  - 프론트엔드 로그 확인: tail -f frontend.log"
echo "  - 모든 서버 종료: pkill -f 'uvicorn app.main:app' && pkill -f 'frontend_server.py'"
echo ""
echo "🌐 접속 URL:"
echo "  - API 문서: http://localhost:8080/docs"
echo "  - 웹 앱: http://localhost:3000"
