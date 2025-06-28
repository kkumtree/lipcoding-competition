# Python 버전 호환성 가이드

## 권장 Python 버전
- **Python 3.12.x** (권장)
- **Python 3.11.x** (호환)
- **Python 3.10.x** (최소 요구사항)

## GitHub Actions 설정

만약 GitHub Actions에서 Python 버전을 지정하려면 다음과 같이 설정하세요:

```yaml
- name: Set up Python
  uses: actions/setup-python@v4
  with:
    python-version: '3.12'
```

## 의존성 설치

```bash
# 가상환경 생성
python3 -m venv .venv

# 가상환경 활성화
source .venv/bin/activate  # Linux/macOS
# 또는
.venv\Scripts\activate  # Windows

# 의존성 설치
pip install -r requirements.txt
```

## 알려진 이슈

### Pillow 호환성
- Python 3.13에서 Pillow 10.0.0 설치 시 빌드 오류 발생 가능
- requirements.txt에서 pillow>=10.0.0으로 범위 지정하여 최신 호환 버전 자동 설치

### 해결책
1. Python 3.12 사용 권장
2. 의존성 범위 지정으로 유연성 확보
3. pip 업그레이드: `pip install --upgrade pip`
