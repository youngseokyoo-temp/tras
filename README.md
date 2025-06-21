# 🌏 TRAS!  - 나만의 여행 플랜 어시스턴트

[gif]

**TRAS**는 대화만으로 여행의 시작부터 끝까지 함께하는 **멀티 에이전트 여행 플래너**입니다. 
여러 AI 에이전트들이 협력하여 여행 계획을 수립하고, 완성된 계획을 캘린더에 등록하고 이를 SNS에 공유할 수 있는 기능을 제공합니다.

### 🚀 How to run

패키지 매니저로 uv를 사용하였습니다. 아래 커맨드를 통해 UI를 활성화합니다.

```
uv run streamlit run app/main.py
```

다양한 기능을 활용하기 위해 아래와 같이 `.env` 파일을 생성하여 값들을 등록해 주세요.

```
# KEY
OPENAI_API_KEY=""

TAVILY_API_KEY=""

KAKAO_REST_API_KEY=""

NAVER_CLIENT_ID=""
NAVER_CLIENT_SECRET=""

GPLACES_API_KEY=""
GOOGLE_CREDENTIALS_PATH=""
GOOGLE_SECRET_PATH=""

TWITTER_API_KEY=""
TWITTER_API_KEY_SECRET=""
TWITTER_BEARER_TOKEN=""
TWITTER_ACCESS_TOKEN=""
TWITTER_ACCESS_TOKEN_SECRET=""

# LangSmith
LANGSMITH_TRACING=true
LANGSMITH_ENDPOINT="https://api.smith.langchain.com"
LANGSMITH_API_KEY=""
LANGSMITH_PROJECT="tras"

# Application Environments
LOGS_DIR = ""
```

### 📂 Folder Structure

```
├── README.md                           # 프로젝트 소개 및 사용법 문서
├── app                                 # 메인 애플리케이션 디렉토리
│   ├── __init__.py                     
│   ├── agents                          # AI 에이전트들
│   │   ├── calendar_agent              
│   │   │   ├── agent.py                # 캘린더 에이전트 구현
│   │   │   ├── constants.py            # 캘린더 에이전트 관련 상수
│   │   │   └── tools.py                # 캘린더 도구들 (Google Calendar Tool)
│   │   ├── planner_agent      
│   │   │   ├── agent.py                # 플래너 에이전트 구현
│   │   │   ├── constants.py            # 플래너 관련 상수
│   │   │   └── tools.py                # 계획 수립 도구들 (Naver blog, cafe, Web Loading)
│   │   ├── research_agent     
│   │   │   ├── agent.py                # 리서치 에이전트 구현
│   │   │   ├── constants.py            # 리서치 관련 상수
│   │   │   └── tools.py                # 정보 수집 도구들 (Kakao, Google, Wikipedia, Tavily)
│   │   └── twitter_agent               
│   │       ├── agent.py                # 트위터 에이전트 구현
│   │       ├── constants.py            # 트위터 관련 상수
│   │       └── tools.py                # 트위터 관련 도구들 (Twitter API)
│   ├── llms                   
│   │   ├── config.py                   # LLM 설정 관리
│   │   └── factory.py                  # LLM 팩토리 패턴 구현
│   ├── main.py                         # Streamlit 메인 애플리케이션
│   ├── supervisor             
│   │   ├── chatbot.py                  # 챗봇(감독자) 인터페이자
│   │   ├── constants.py                # 챗봇 관련 상수
│   │   ├── hooks.py                    # 챗봇 관련 훅 함수 (가드레일)
│   │   └── prompts.py        
│   └── utils                           # 유틸리티 함수들
│       ├── callbacks.py                # LangChain 콜백 핸들러 (로깅)
│       ├── create_react_agent.py       # ReAct 에이전트 생성 (라이브러리 함수 변형)
│       ├── env_constants.py            # 환경 변수 상수
│       ├── langsmith_manger.py         # LangSmith 로깅 및 프롬프트 매니저
│       ├── logger.py                   # 로깅 설형
│       ├── streamlit_helpers.py        # Streamlit 사용 함수
│       └── ui_constants.py             # UI 관련 상수
├── credentials.json                    # Google API 인증 정보 (미포함)
├── logs                                # 로그 파일 저장 디렉토리
├── media                               # 미디어 파일 저장 디렉토리
├── pyproject.toml                      # 프로젝트 의존성 및 설정 (uv)
├── secret.json                         # API 키 등 비밀 정보 (미포함)
├── token.json                          # OAuth 토큰 정보 (미포함)
└── uv.lock                             # 의존성 잠금 파일 
```

## Agents

[graph image]

에이전트들은 모두 ReACT()
모든 Tool들은 비동기

### research agent
### planner_agent
### calendar_agent
### twitter_agent
### supervisor

handoff 방식으로 각 agent tool화

# Code Implementation Points

> 각 모둘에 대한 테스트는 __main__을 수정한 뒤, uv run {module}.py 로 호출할 수 있습니다.

1. LLM 팩토리 및 캐싱

2. streaming - create_react_agent

3. Logging

4. Guardrail

google check 은 입력 크기 너무 작아
huggingface llama7b

## Logging & Prompt

[langsmith_image]

TRAS는 모든 AI 에이전트의 실행 과정을 체계적으로 모니터링하고 분석하기 위해 **LangSmith**와 완전히 연동되어 있습니다. 활용한 주요 기능은 아래와 같습니다.
* 실시간 트레이싱: 모든 에이전트와 툴 호출의 실시간 추적
* 성능 모니터링: 각 에이전트별 응답 시간 및 토큰 사용량 측정
* 에러 추적: 툴 실행 실패 및 에러 상황의 상세 로깅
* 비용 분석: API 호출별 비용 추적 및 최적화 지원

프롬프트의 지속적인 개선과 체계적 관리를 위해 **LangSmith Prompt Hub**을 사용하였습니다. TRAS에서 사용 중인 각 에이전트와 챗봇(supervisor)의 시스템 프롬프트는 아래의 링크에서 확인하실 수 있습니다.

https://smith.langchain.com/hub/tras/

## Production Architecture



## Continous Validation




## 🔧 Dev Tools
* uv: 패키지 매니저로 사용
* ruff: 

Cursor IDE:  

## Addtional Screenshots

[img]

## TODO

이번 프로젝트에서 보강하고 싶은 점은 아래와 같습니다.

* Logging: 
* Checkpoint: 
* Managing Tokens: 
* Credentails: 더 나은 사용성을 위해서는 사용자가 직접 UI로 각종 Key와 Credentials를 지급해야 할 것입니다.
* RAG: 








🚀

🏗️

🔧

🌐

🛡️

📊

🔄

