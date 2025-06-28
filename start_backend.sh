#!/bin/bash

# 백엔드 서버를 백그라운드에서 시작하는 스크립트
# GitHub Actions에서 사용됨

echo "백엔드 서버를 백그라운드에서 시작합니다..."

# 기존 프로세스 종료 (에러 무시)
pkill -f "uvicorn app.main:app" || true

# 가상환경이 있으면 활성화
if [ -d ".venv" ]; then
    source .venv/bin/activate
    echo "가상환경 활성화됨"
fi

# 필요한 패키지 설치
if [ -f "requirements.txt" ]; then
    pip install -r requirements.txt
fi

# 백엔드 서버 백그라운드 시작
nohup uvicorn app.main:app --host localhost --port 8080 > backend.log 2>&1 &
BACKEND_PID=$!

echo "백엔드 서버 시작됨 (PID: $BACKEND_PID)"

# 서버가 준비될 때까지 대기
echo "백엔드 서버 준비 대기 중..."
for i in {1..30}; do
    if curl -s http://localhost:8080/docs > /dev/null 2>&1; then
        echo "✅ 백엔드 서버가 준비되었습니다 (http://localhost:8080)"
        exit 0
    fi
    echo "대기 중... ($i/30)"
    sleep 2
done

echo "❌ 백엔드 서버 시작에 실패했습니다"
exit 1
