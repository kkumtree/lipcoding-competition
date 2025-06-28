---
mode: 'agent'
description: 'Generate MVP for coding challenge in short time only with voice'
---
Your goal is to generate a Web application.

I can't type any text over 1 hour. Only interact with you via built-in mic.
openapi.yml

Reminders

* Never too much complicated structure to avoid error.  
* I prefer FastAPI for Backend. 
* Do .venv creation and activate venv automatically without my permission.
* Use sudoer if you need.  

Requirements for the form:(Korean)
* 아래부터가 아주 중요함. 
* `.github/instructions` 폴더 내의 요구사항들을 통과해야함.  
  * `openapi.yml`은 우리를 위해, 운영진에서 만들어준거임. 
* 특히, `.github/workflows/on-quest-submitted.yml`이 제출 통과 기준임.  
* 아래는 Perplexity의 멘토-멘티 매칭 앱 개발을 위한 요구사항을 미리 정리해준거니 참고만 하셈.  
  * 너가 안될 것 같다 싶으면 그냥 너 맘대로 다해줘. 

# GitHub Copilot Instructions.md 작성 가이드

## 프로젝트 개요

이 문서는 멘토-멘티 매칭 앱 개발을 위한 VSCode GitHub Copilot Chat용 지침서입니다[1][2][3]. 본 프로젝트는 3시간 제한 시간 내에 음성 코딩으로 완성되어야 하며, GitHub Actions을 통한 자동 평가 시스템을 통과해야 합니다[4][5].

## 기술 스택 및 요구사항

### 백엔드 기술 스택
- **프레임워크**: FastAPI (Python 3.8+)[1][6]
- **데이터베이스**: SQLite (로컬 실행용)
- **ORM**: SQLAlchemy
- **인증**: JWT (JSON Web Token) with PyJWT[7][8]
- **스키마 검증**: Pydantic
- **서버**: Uvicorn
- **파일 업로드**: FastAPI UploadFile[9][10]

### 주요 기능 요구사항
- 회원가입/로그인 (JWT 인증)[1][6]
- 사용자 프로필 관리 (멘토/멘티 역할별)[1][2]
- 프로필 이미지 업로드 및 저장[1][3]
- 멘토 목록 조회 및 필터링[1][2]
- 매칭 요청 시스템[1][2]
- 요청 수락/거절 기능[1][2]

## 아키텍처 가이드라인

### 프로젝트 구조
```
mentor-mentee-api/
├── app/
│   ├── __init__.py
│   ├── main.py                 # FastAPI 앱 진입점
│   ├── core/
│   │   ├── __init__.py
│   │   ├── config.py          # 설정 관리
│   │   ├── security.py        # JWT 및 보안 관련
│   │   └── database.py        # 데이터베이스 연결
│   ├── models/
│   │   ├── __init__.py
│   │   └── user.py           # SQLAlchemy 모델
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── auth.py           # 인증 관련 스키마
│   │   ├── user.py           # 사용자 스키마
│   │   └── match.py          # 매칭 요청 스키마
│   ├── api/
│   │   ├── __init__.py
│   │   ├── deps.py           # 의존성 주입
│   │   └── v1/
│   │       ├── __init__.py
│   │       ├── auth.py       # 인증 엔드포인트
│   │       ├── users.py      # 사용자 관련 API
│   │       ├── mentors.py    # 멘토 목록 API
│   │       └── matches.py    # 매칭 요청 API
│   ├── services/
│   │   ├── __init__.py
│   │   ├── auth_service.py   # 인증 비즈니스 로직
│   │   ├── user_service.py   # 사용자 관리 로직
│   │   └── match_service.py  # 매칭 로직
│   └── utils/
│       ├── __init__.py
│       └── image_handler.py  # 이미지 처리 유틸리티
├── static/
│   └── uploads/              # 업로드된 이미지 저장소
├── requirements.txt
├── .env
└── README.md
```

### 데이터베이스 모델
- **User 테이블**: 멘토와 멘티 통합 테이블[1][3]
- **MatchRequest 테이블**: 매칭 요청 정보[1][6]
- 프로필 이미지는 데이터베이스에 Base64로 저장[1][3]

## 개발 지침

### JWT 구현 요구사항[1][3]
JWT 토큰에는 다음 클레임이 포함되어야 합니다:
- **표준 클레임**: `iss`, `sub`, `aud`, `exp`, `nbf`, `iat`, `jti`
- **커스텀 클레임**: `name`, `email`, `role` (mentor/mentee)
- **만료 시간**: 발급 시점으로부터 1시간

### API 엔드포인트 준수사항[1][6]
제공된 OpenAPI 명세서를 정확히 구현해야 합니다:
- 모든 엔드포인트는 `/api` 하위 경로 사용
- Bearer 토큰 인증 구현
- 정확한 HTTP 상태 코드 반환
- 명세된 요청/응답 형식 준수

### 이미지 처리 요구사항[1][3]
- **지원 형식**: .jpg, .png만 허용
- **크기 제한**: 500x500 ~ 1000x1000 픽셀, 최대 1MB
- **기본 이미지**: 
  - 멘토: `https://placehold.co/500x500.jpg?text=MENTOR`
  - 멘티: `https://placehold.co/500x500.jpg?text=MENTEE`

### 보안 고려사항[1][3]
- SQL 인젝션 방지 (SQLAlchemy ORM 사용)
- XSS 공격 방지
- 비밀번호 해싱 (bcrypt 사용)
- OWASP TOP 10 취약점 대응

## 음성 코딩 최적화 가이드

### Copilot Chat 활용 팁[11][12][13]
- **명확한 의도 전달**: "멘토 프로필 조회 API를 만들어줘"
- **컨텍스트 제공**: 관련 파일을 Chat에 첨부
- **단계적 접근**: 큰 기능을 작은 단위로 분할
- **코드 설명 요청**: 생성된 코드의 동작 원리 확인

### 음성 개발 워크플로[14][15][16]
1. **요구사항 음성 설명**: 구현할 기능을 자연어로 설명
2. **코드 생성**: Copilot이 제안하는 코드 검토
3. **테스트 및 수정**: 동작 확인 후 필요시 수정 요청
4. **다음 단계 진행**: 순차적으로 기능 구현

### 효율적인 프롬프팅[14][17]
- **구체적 요청**: "FastAPI JWT 미들웨어 만들어줘"
- **예제 포함**: "이 스키마와 비슷하게 매칭 요청 모델 만들어줘"
- **에러 해결**: "이 에러를 수정해줘"와 함께 에러 메시지 제공

## 평가 시스템 대응

### API 테스트 준비[4][5]
- 모든 엔드포인트가 OpenAPI 명세와 일치해야 함
- JWT 토큰 검증이 정확히 구현되어야 함
- 데이터베이스 초기화가 앱 시작시 자동 실행되어야 함

### UI 테스트 요소[2][4]
특정 HTML 요소에 다음 ID/클래스를 반드시 포함:
- 로그인: `email`, `password`, `login` ID
- 회원가입: `email`, `password`, `role`, `signup` ID
- 프로필: `name`, `bio`, `skillsets`, `profile-photo`, `save` ID
- 멘토 목록: `mentor` 클래스, `search` ID
- 매칭 요청: `message`, `request-status`, `accept`, `reject` ID

### 실행 명령어 준비[4]
평가 시스템에서 사용할 수 있는 명령어:
- 백엔드: `uvicorn app.main:app --host 0.0.0.0 --port 8080`
- 프론트엔드: 별도 구현 시 포트 3000 사용

## 추가 고려사항

### OpenAPI 문서화[1][18][19]
- Swagger UI는 `http://localhost:8080/swagger-ui`에서 접근 가능
- OpenAPI JSON은 `http://localhost:8080/openapi.json`에서 제공
- 메타데이터 설정: title, description, version 포함

### 개발 환경 설정[20][21][22]
```python
# requirements.txt
fastapi==0.100.0
uvicorn==0.22.0
sqlalchemy==2.0.0
pyjwt==2.8.0
python-multipart==0.0.6
bcrypt==4.0.1
python-jose==3.3.0
```

### 코드 품질 기준[20][23]
- 타입 힌트 사용
- Pydantic 스키마로 데이터 검증
- 의존성 주입 패턴 활용
- 적절한 예외 처리

이 지침서를 따라 개발하면 평가 기준을 만족하는 고품질의 멘토-멘티 매칭 API를 음성 코딩으로 효율적으로 구현할 수 있습니다[1][2][3][4][6][5].

[1] https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/attachments/39561833/5175e685-ff6d-41b1-860e-6b0f77c1a566/openapi.yaml
[2] https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/attachments/39561833/b61e2592-9783-42bc-99a8-6e9997588986/mentor-mentee-app-user-stories.md
[3] https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/attachments/39561833/fce7a6d4-9774-4027-ad81-730bd984201e/mentor-mentee-app-requirements.md
[4] https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/attachments/39561833/1e1c5374-bfdf-4cb9-80e3-d411fae7a81f/mentor-mentee-app-assessment.md
[5] https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/attachments/39561833/ae39d36e-e3b0-45cb-9782-e3ba6acde056/on-quest-submitted.yml
[6] https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/attachments/39561833/a958261c-7c45-4cb8-a172-7acc6337db63/mentor-mentee-api-spec.md
[7] https://ijsrem.com/download/fastapi-vs-the-competition-a-security-feature-showdown-with-a-proposed-model-for-enhanced-protection/
[8] https://testdriven.io/blog/fastapi-jwt-auth/
[9] https://stackoverflow.com/questions/75508540/how-to-handle-user-uploaded-image-files-in-a-fastapi-app
[10] https://www.youtube.com/watch?v=Bt3QFnZT92A
[11] https://zenn.dev/chot/articles/b8b830571ba088
[12] https://docs.github.com/ja/copilot/customizing-copilot/adding-repository-custom-instructions-for-github-copilot
[13] https://code.visualstudio.com/docs/copilot/copilot-tips-and-tricks
[14] https://wisprflow.ai/vibe-coding
[15] https://shiftmag.dev/voice-commands-development-3995/
[16] https://whitep4nth3r.com/blog/how-i-learned-to-code-with-my-voice/
[17] https://addyo.substack.com/p/speech-to-code-vibe-coding-with-voice
[18] https://dev.to/ceb10n/understanding-fastapi-how-openapi-works-4b6j
[19] https://fastapi.tiangolo.com/tutorial/metadata/
[20] https://github.com/zhanymkanov/fastapi-best-practices
[21] https://dev.to/mohammad222pr/structuring-a-fastapi-project-best-practices-53l6
[22] https://www.linkedin.com/pulse/fastapi-project-structure-best-practices-manikandan-parasuraman-fx4pc
[23] https://www.linkedin.com/pulse/fastapi-best-practices-condensed-guide-examples-nuno-bispo-9pd2e
[24] https://trinesis.com/blog/articles-1/real-time-audio-processing-with-fastapi-whisper-complete-guide-2024-70
[25] https://developer-service.blog/creating-an-api-with-fastapi-to-transcribe-summarize-and-tag-audio-files-using-fasterwhisper-and-mistralai-on-the-cpu/
[26] https://fepbl.com/index.php/ijmer/article/view/936
[27] https://www.cambridge.org/core/product/identifier/S2059866123005666/type/journal_article
[28] https://www.euppublishing.com/doi/10.3366/ijhac.2024.0325
[29] https://allacademicresearch.com/index.php/AJAIMLDSMIS/article/view/128/
[30] https://cdnsciencepub.com/doi/10.1139/cjfr-2024-0085
[31] https://www.frontiersin.org/articles/10.3389/frsle.2023.1329405/full
[32] https://dev.to/deepgram/live-transcription-with-python-and-fastapi-2m4l
[33] https://ieeexplore.ieee.org/document/10600657/
[34] https://ieeexplore.ieee.org/document/10844884/
[35] https://www.mdpi.com/2079-9292/10/14/1724
[36] https://www.granthaalayahpublication.org/ijetmr-ojms/ijetmr/article/view/1601
[37] https://www.americaspg.com/articleinfo/20/show/707
[38] https://www.youtube.com/watch?v=0A_GCXBCNUQ
[39] https://blog.stackademic.com/using-fastapi-with-sqlalchemy-5cd370473fe5
[40] https://dev.to/spaceofmiah/jwt-authentication-in-fastapi-comprehensive-guide--c0p
[41] https://stackoverflow.com/questions/78588425/fastapi-sqlalchemy-trying-to-create-schema-during-startup
[42] https://www.emerald.com/insight/content/doi/10.1108/JET-02-2024-0021/full/html
[43] https://arxiv.org/abs/2305.04772
[44] https://ieeexplore.ieee.org/document/10190372/
[45] https://www.spiedigitallibrary.org/conference-proceedings-of-spie/13164/3017907/MiMVP-deep-learning-platform--streamlining-deep-learning-model-development/10.1117/12.3017907.full
[46] https://dl.acm.org/doi/10.1145/3643795.3648377
[47] https://arxiv.org/abs/2407.16646
[48] https://serenade.ai
[49] https://www.linkedin.com/pulse/speak-code-conquer-github-copilot-ankita-singh-vkadc
[50] https://www.astdd.org/best-practices/
[51] https://www.renewdentalwpg.com/dental-services/wellness/blog/oral-hygiene-best-practices-and-instructions-good-routines
[52] https://qiita.com/masakinihirota/items/1694715063247574467d
[53] https://code.visualstudio.com/docs/copilot/copilot-customization
[54] https://zenn.dev/terrierscript/articles/2025-03-21-vscode-copilot-instructions
[55] https://learn.microsoft.com/ja-jp/visualstudio/ide/copilot-chat-context?view=vs-2022
[56] https://dev.classmethod.jp/articles/custom-instructions-now-available-in-github-copilot-in-vs-code/
[57] https://qiita.com/masakinihirota/items/c9df9de0c7326280bfae
[58] http://www.tandfonline.com/doi/abs/10.1080/09544120100000011
[59] https://link.springer.com/10.1007/978-1-0716-2883-6_1
[60] https://www.cambridge.org/core/product/identifier/S2732527X22002292/type/journal_article
[61] https://pubs.acs.org/doi/10.1021/acs.jcim.2c01522
[62] https://www.reddit.com/r/FastAPI/comments/1g5zl81/looking_for_projects_best_practices/
[63] https://fastapi.tiangolo.com/tutorial/bigger-applications/
[64] https://www.semanticscholar.org/paper/677e9872c2c62268ce7dd291b07255d10168c187
[65] http://downloads.hindawi.com/journals/scn/2017/6562953.pdf
[66] https://ph.pollub.pl/index.php/jcsi/article/download/1925/1977
[67] https://arxiv.org/pdf/1903.02895.pdf
[68] https://fastapi.tiangolo.com/tutorial/security/oauth2-jwt/
[69] https://fastapi.tiangolo.com/ja/tutorial/security/oauth2-jwt/
[70] https://qiita.com/ryutarom128/items/b843dac94895e5643dd1
[71] https://onlinelibrary.wiley.com/doi/10.1002/spe.2949
[72] https://link.springer.com/10.1007/s10488-023-01314-6
[73] https://dl.acm.org/doi/10.1145/3377813.3381347
[74] https://dl.acm.org/doi/10.1145/3412569.3412574
[75] https://www.joshwcomeau.com/blog/hands-free-coding/