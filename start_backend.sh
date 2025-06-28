#!/bin/bash

# 백엔드 서버를 백그라운드에서 시작하는 스크립트
# GitHub Actions에서 사용됨

echo "백엔드 서버를 백그라운드에서 시작합니다..."

# Python 버전 확인 및 가상환경 설정
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
pkill -f "uvicorn app.main:app" || true

# 가상환경 생성 또는 활성화
if [ ! -d "$VENV_DIR" ]; then
    echo "가상환경 생성 중: $VENV_DIR"
    $PYTHON_CMD -m venv $VENV_DIR
fi

source $VENV_DIR/bin/activate
echo "가상환경 활성화됨: $VENV_DIR"

# 필요한 패키지 설치
if [ -f "requirements.txt" ]; then
    echo "패키지 설치 중..."
    pip install -r requirements.txt || {
        echo "❌ 패키지 설치에 실패했습니다. 대체 방법을 시도합니다..."
        pip install --upgrade pip
        pip install -r requirements.txt --no-cache-dir || {
            echo "❌ 패키지 설치에 완전히 실패했습니다."
            exit 1
        }
    }
    echo "✅ 패키지 설치 완료"
fi

# 백엔드 서버 백그라운드 시작
nohup uvicorn app.main:app --host 0.0.0.0 --port 8080 > backend.log 2>&1 &
BACKEND_PID=$!

echo "백엔드 서버 시작됨 (PID: $BACKEND_PID)"

# 서버 시작을 위한 초기 대기
sleep 3

# 서버가 준비될 때까지 대기
# echo "백엔드 서버 준비 대기 중..."
# for i in {1..30}; do
#     if nc -z localhost 8080 2>/dev/null; then
#         echo "✅ 백엔드 서버가 준비되었습니다 (http://localhost:8080)"
#         exit 0
#     fi
#     echo "대기 중... ($i/30)"
#     sleep 2
# done

# echo "❌ 백엔드 서버 시작에 실패했습니다"
# exit 1
