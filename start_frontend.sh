#!/bin/bash

# 프론트엔드 서버를 백그라운드에서 시작하는 스크립트
# GitHub Actions에서 사용됨

echo "프론트엔드 서버를 백그라운드에서 시작합니다..."

# Python 버전 확인
if command -v python3.13 &> /dev/null; then
    PYTHON_CMD=python3.13
    VENV_DIR=".venv313"
    echo "Python 3.13 사용: $(python3.13 --version)"
elif command -v python3 &> /dev/null; then
    PYTHON_CMD=python3
    VENV_DIR=".venv"
    echo "Python 3 사용: $(python3 --version)"
else
    echo "❌ Python 3가 설치되지 않았습니다"
    exit 1
fi

# 기존 프로세스 종료 (에러 무시)
pkill -f "frontend_server.py" || true

# 가상환경 활성화 (있는 경우)
if [ -d "$VENV_DIR" ]; then
    source $VENV_DIR/bin/activate
    echo "가상환경 활성화됨: $VENV_DIR"
    
    # 의존성 확인 및 설치 (필요시)
    if ! python -c "import http.server, os, json" 2>/dev/null; then
        echo "기본 Python 모듈 확인 중..."
        # 기본 모듈이므로 추가 설치 불필요
    fi
elif [ -d ".venv" ]; then
    source .venv/bin/activate
    echo "기본 가상환경 활성화됨: .venv"
fi

# 프론트엔드 서버 백그라운드 시작
nohup python frontend_server.py > frontend.log 2>&1 &
FRONTEND_PID=$!

echo "프론트엔드 서버 시작됨 (PID: $FRONTEND_PID)"

# 서버가 준비될 때까지 대기
echo "프론트엔드 서버 준비 대기 중..."
for i in {1..30}; do
    if curl -s http://localhost:3000 > /dev/null 2>&1; then
        echo "✅ 프론트엔드 서버가 준비되었습니다 (http://localhost:3000)"
        exit 0
    fi
    echo "대기 중... ($i/30)"
    sleep 2
done

echo "❌ 프론트엔드 서버 시작에 실패했습니다"
exit 1
