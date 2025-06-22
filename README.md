# 🌏 TRAS!  - 나만의 여행 플랜 어시스턴트

![main](https://github.com/user-attachments/assets/dd47a45d-dc97-495c-99bc-08fdd345861b)
(참고 - (1) 위 영상은 편집으로 실제 응답보다 빠르게 보입니다. (2) 편집으로 인해 필연적으로 워터마크가 포함되어 있습니다.)

**TRAS**는 대화만으로 여행의 시작부터 끝까지 함께하는 **멀티 에이전트 여행 플래너**입니다. 
여러 AI 에이전트들이 협력하여 여행 계획을 수립하고, 완성된 계획을 캘린더에 등록하고 이를 SNS에 공유할 수 있는 기능을 제공합니다.

## 🚀 How to run

TRAS는 패키지 매니저로 uv를 사용하였습니다. 따라서 PC에 uv가 설치되어있어야 합니다.
uv 설치는 [uv - installation](https://docs.astral.sh/uv/getting-started/installation/)를 참고해 주세요.

설치가 완료된 후에는, 아래 커맨드를 통해 가상환경을 띄우고 UI를 활성화하여 시작할 수 있습니다.

```
git clone https://github.com/youngseokyoo-temp/tras.git
cd tras
uv run streamlit run app/main.py
```

### ❗️ 주의
에이전트의 다양한 기능을 활용하기 위해 아래와 같이 `.env` 파일을 생성하여 값들을 등록해 주세요.
등록이 되지 않으면 앱을 시작할 수 없습니다.

<details>
<summary> .env</summary>

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

</details>

### 📂 Folder Structure

폴더 구조와 각 디렉토리 밑 파일들에 대한 설명은 아래에서 확인하실 수 있습니다.

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
├── logs                                # 로그 파일 저장 디렉토리 (미포함)
├── media                               # 미디어 파일 저장 디렉토리
├── pyproject.toml                      # 프로젝트 의존성 및 설정 (uv)
├── secret.json                         # API 키 등 비밀 정보 (미포함)
├── token.json                          # OAuth 토큰 정보 (미포함)
└── uv.lock                             # 의존성 잠금 파일 
```

## 🤖 Agents

TRAS는 5개의 전문 AI 에이전트가 협력하여 복잡한 여행 계획 업무를 수행합니다.
모든 에이전트는 ReAct (Reasoning + Acting) 구조를 채택하여 다음과 같은 사고 과정을 거칩니다.



에이전트들은 Supervisor 패턴을 통해 체계적으로 협력합니다:

요청 분석: Supervisor가 사용자 요청을 분석하고 적절한 에이전트 선택  
순차 실행: 각 에이전트가 전문 영역에서 최적의 결과 도출  
결과 통합: Supervisor가 모든 결과를 종합하여 일관된 응답 제공

research_agent의 흐름 (예시)

* Thought: 사용자가 제주도 3박 4일 여행을 원한다. 먼저 제주도 관광지 정보를 조사해야 한다.
* Action: kakao_local_search("제주도 관광지")
* Observation: 성산일출봉, 한라산, 우도 등 주요 관광지 정보 수집 완료
* Thought: 이제 실제 여행 후기를 확인해서 생생한 정보를 얻어보자.
* Action: naver_blog_search("제주도 3박4일 여행 후기")

직접 구현한 Tool의 함수들은 에이전트의 동기/비동기 구동을 모두 지원하기 위해 각각 `sync`, `async` 함수를 따로 지원하였습니다.

> 각각의 agent에 의한 Tool 기능은 모두 실제로 동작함을 확인하였습니다.

> 각각의 agnet에 의한 Tool 기능은 발생 가능한 Error를 핸들링하여 Runtime raise를 발생시키지 않고 에러메시지만을 에이전트에 전달하여 에이전트가 해당 Tool을 현재 사용할 수 없음을 알립니다. 

### Research agent

**정보 수집 전문가**로 여행지에 대한 종합적인 정보를 수집합니다.
이를 기반으로 사용자에게 여행지의 대한 정보를 제공하고, 추천함으로써 여행지 선정을 돕습니다.

**사용된 Tool**

1. `Kakao Local API`: 키워드로 기반 검색으로 국내 방문지에 대한 상세 정보를 수집합니다.
2. `Google Places API`: 전 세계 방문지에 대한 상세 정보를 수집합니다. 
3. `Tavily Search`: 여행지에 대한 일반적인 정보를 웹에서 검색합니다.
4. `Wikipedia Search`: 특정 장소나 문화에 대한 보다 검증된 자료를 수집합니다.

추가 정보

> Google Places API: Kakao Local 서비스는 국내로 범위가 한정되어 있습니다. 국내가 아닌 해외 여행을 계획하는 사용자가 더 많을 것이라 생각하여 추가하였습니다.

### Planner agent

**여행 계획 수립 전문가**로 사용자의 요구 사항을 최대로 반영하여 실용적인 여행 계획서를 작성합니다.

**사용된 Tool**

1. `Naver blog Search API`: 네이버 블로그에서 여행지에 대한 검색결과를 수집합니다. 
2. `Naver Cafe Search API`: 네이버 카페에서 여행지에 대한 검색결과를 수집합니다.
3. `Playwright WebLoader`: 검색 결과에서 특정 웹페이지의 상세 내용을 수집합니다.
4. `Kakao Local API`: 위 research agent가 사용하는 Tool과 동일
5. `Google Places API`: 위 research agent가 사용하는 Tool과 동일

추가 정보

> 실제로 여행 계획을 수립할 때 블로그와 카페 글에서 가장 많은 정보와 레퍼런스를 얻기 때문에 Naver blog, cafe를 선택하였습니다. 티스토리의 개발자 API 서의스는 종료되었습니다.

> 네이버 블로그와 카페에서 수집된 검색 결과는 확인 결과, 실제 글에 대한 내용은 매우 일부만 포함이 되어있었습니다. 이 결과는 에이전트가 여행 계획을 레퍼런스하는 데에 크게 도움이 되지 않을 것이었습니다. 따라서, 검색 결과를 토대로 실제 전체 글 내용을 크롤링 하는 Web-based Loader가 필요하다고 판단하였습니다. 실험 결과 네이버 블로그 및 카페 글은 단순 HTML이 아닌 자바스크립트 내에 담겨있어 Playwright을 활용하게 되었습니다.

### Calendar agent

**일정 관리 전문가**로 여행 계획을 사용자의 캘린더에 등록하고 관리합니다.

**사용된 Tool**

1. `Google Calendar Create`: 새로운 일정을 사용자의 Google Calendar에 생성합니다.
2. `Google Calendar Delete`: 기존 일정을 사용자의 Google Calendar에서 삭제합니다.
3. `Google Calendar Update`: 기존 일정의 정보를 수정합니다.
4. `Google Calendar Search`: 사용자의 Calendar에서 특정 조건에 맞는 일정을 검색합니다.
5. `Google Calendar info`: 사용자의 Calendar 목록과 정보를 조회합니다.
6. `Current datetime`: 현재 날짜와 시간 정보를 제공합니다.

> 사용자가 명확하게 시간을 알려주지 않아도 이를 최대한 유추하기 위해 Current datetime을 활용하였습니다.

> Update, Delete 시 해당 일정에 대한 정보를 가져오기 위해 Search, Info를 활용하였습니다.

### Twitter agent

**소셜 미디어 전문가**로 여행 계획을 SNS에 공유합니다.

**사용된 Tool**

1. `Twitter Post API`: 새로운 트윗을 게시합니다. 텍스트 내용과 선택적으로 답글할 트윗 ID를 사용할 수 있습니다.
2. `Twitter User Tweets API`: 특정 사용자의 최근 트윗을 조회합니다.
3. `Twitter Delete API`: 특정 트윗을 삭제합니다. 삭제할 트윗의 ID를 사용합니다.

> 여행 계획은 챗봇 화면에서 사용자에게 보기 좋게 제공하기 위해 마크다운 형식으로 제공합니다. 하지만, 트위터의 프소트는 마크다운 형식을 지원하지 않습니다. 이를 위해 Post 시 마크다운을 plaintext로 변환하는 함수를 추가했습니다.

### supervisor

**전체 시스템 감독자**로 모든 에이전트의 협업을 조율하고 사용자와의 대화를 관리합니다.

**주요 기능:**
- 대화 관리: 사용자 요청을 분석하고 적절한 에이전트로 작업 위임
- 에이전트 조율: 각 전문 에이전트 간 작업 분배 및 협업 관리
- 품질 관리: 각 에이전트의 결과물 검증 및 개선 요청
- 히스토리 관리: 저장 공간을 위해 오래된 대화 내용을 압축합니다.
- 가드레일: 부적절한 요청 필터링 및 안전성 확보

상위 에이전트인 Supervisor는 이러한 tool들을 순차적으로 `handoff` 방식으로 호출하며, 사용자의 요청을 단계별로 처리합니다.

## 🎥 Logging & Prompt

![Langsmith](https://github.com/user-attachments/assets/832865c3-0de4-4657-934e-25764888479f)

TRAS는 모든 AI 에이전트의 실행 과정을 체계적으로 모니터링하고 분석하기 위해 **LangSmith**와 완전히 연동되어 있습니다. 활용한 주요 기능은 아래와 같습니다.
* 실시간 트레이싱: 모든 에이전트와 툴 호출의 실시간 추적
* 성능 모니터링: 각 에이전트별 응답 시간 및 토큰 사용량 측정
* 에러 추적: 툴 실행 실패 및 에러 상황의 상세 로깅
* 비용 분석: API 호출별 비용 추적 및 최적화 지원

프롬프트의 지속적인 개선과 체계적 관리를 위해 **LangSmith Prompt Hub**을 사용하였습니다. TRAS에서 사용 중인 각 에이전트와 챗봇(supervisor)의 시스템 프롬프트는 아래의 링크에서 확인하실 수 있습니다.

https://smith.langchain.com/hub/tras/

프롬프트 Hub과 추후에도 이용 가능하게 될 다양한 LangSmith 관련 기능들을 위해 Langsmith Manager 를 만들었습니다. 이는 `Singleton` 패턴으로 구현되어 LLM(에이전트)가 매 구동될 때마다 새로운 매니저 인스턴스가 만들어지는 것을 방지하였습니다.

# 📊 Code Implementation Points

> 각 모둘에 대한 테스트는 __main__을 수정한 뒤, uv run {module}.py 로 호출할 수 있습니다.

 1. **LLM 팩토리 및 캐싱**

TRAS의 LLM 관리 시스템은 확장성, 효율성, 유지보수성을 모두 고려한 뛰어난 `Factory` 패턴으로 제작되었습니다. 계층화된 Configuration에 모델 정보를 등록하면 Factory 인스턴스는 동적으로 파라미터에 따라 그에 맞는 LLM 인스턴스를 제공합니다. 또한 내부적으로 `Cache` 를 사용하여, 동일한 세팅값으로 API가 연결된 LLM(Langchain의 ChatModel) 인스턴스가 있는 경우, 즉시 이를 반환하도록 하였습니다.

사용자는 왼쪽의 사이드바에서 자신이 진행하고자 하는 모델을 선택하고 temparture 매개변수를 설정할 수 있습니다.
streamlit은 매 이벤트마다 스크립트를 다시 불러오는 치명적인 단점이 존재합니다. 이를 위해, 세션에 사용자의 챗봇 인스턴스를 유지하고, 사용자가 모델 정보를 변경한 경우에만 챗봇 인스턴스를 갈아 끼웁니다.

![model_change](https://github.com/user-attachments/assets/a4417322-7665-414a-8487-3cec391422b0)

2. **Streaming - create_react_agent**

의외로 이번 프로젝트에서 복병이였던 부분이 스트리밍이었습니다. 전체 Multi-agent 시스템을 만든 뒤, 토큰 별 스트리밍을 위해 stream_mode를 messages로 하여 스트리밍 하고 이를 UI와 연결하였습니다. 허나 문제는 스트리밍이 모든 LLM의 출력에 대하여 나온다는 것이었습니다. 이 시스템에는 모델(에이전트)가 총 5개가 있고, 보통 `supervisor - {sub-agent}` 의 흐름을 가지고 있기에 스트리밍도 sub-agent의 출력까지 비슷한(또는 같은) 출력이 연속해서 두 번 스트리밍 되어 써졌습니다. 따라서 아래와 같은 방법들을 고안/시도 해보았습니다.

* sub-agent에 streaming 모드가 disable된 llm 인스턴스를 새로 할당 -> 실패
* supervisor 앞에 echo 노드를 사용해서 분리 시도 -> 실패
* invoke가 끝난 후 가상으로 스트리밍 시뮬레이션 -> 근본적으로, 스트리밍이라고 볼 수 없음.

### ✨ 내가 적용한 해결책 ✨ 

먼저, streaming의 결과를 분석해 보았습니다. stream_mode를 messages로 하면 chunk와 metadata가 존재하는 metadata에 `langgraph_node` 라는 필드가 존재합니다. 이는 해당 LLM이 돌아가는 노드의 이름을 나타냅니다. 이 값이 전부다 **agent**라는 동일한 값으로 chunk를 반환했습니다.

저는 초기에 agent는 `create_react_agent`, supervisor는 `create_supervisor` 이라는 라이브러리 함수를 사용했습니다. 분명 제가 직접 ReAct 에이전트를 구상하는 것보다 품질이 보장되고 안정적일 것입니다. 그런데 이 create_react_agent 함수를 직접 들어가서 확인해보니, LLM 노드의 이름이 **agent**로 하드코딩 되어 있었습니다.

![create_react_agent](https://github.com/user-attachments/assets/22011e1c-e99c-453e-8fd9-effa4f786f6e)

물론, 이렇게 동작하도록 한 이유는 있었을 겁니다.(유명하고 보증된 라이브러리라면 더더욱) 하지만, 이것은 적어도 이 프로젝트에서 제가 원하는 방향은 아니었습니다. 이렇게 되면 이 시스템과 같이 **Multi-agent** 시스템에서 에이전트를 `create_react_agent`로 생성하였을 경우, **노드 단위**로는 에이전트를 구분할 수 없게 됩니다. `name` 파라미터로 에이전트가 구분되기를 기대했던 저는 이 라이브러리 함수를 그대로 `utils` 로 가져와 노드의 이름을 name 파라미터로 수정한 `create_react_agent` 함수를 생성하였습니다. 물론, 이렇게 코드를 통째로 가져오는 방식이 이상적이라고 할 수는 없지만 정해진 기한 내에 원하는 동작을 빠르게 유도하고자 적용하였습니다. 이를 통해 저는 스트리밍 시 chunk의 메타 데이터로 supervisor 응답만을 구분하여 스트리밍 할 수 있었습니다한

TMI) 여전히 이 문제에 대한 간편한 해결책은 없는 듯합니다. 참고: https://github.com/langchain-ai/langgraph/issues/137, https://www.reddit.com/r/LangChain/comments/1d54v75/how_to_stream_the_last_message_final_response_in/?onetap_auto=true&one_tap=true

3. **Logging**

TRAS는 LLM API 호출과 Tool 실행 과정 전반에 걸쳐 세션 기반 로깅 시스템을 도입하여 시스템의 투명성과 안정성을 강화합니다.

모든 로그는 .env 파일의 LOGS_DIR 환경변수로 지정된 경로 아래에 다음과 같은 구조로 저장됩니다:

```
{날짜}/log_{session_id}.log
예: logs/2025-06-22/log_abcd1234efgh5678.log
```

이 파일을 통해 개발자는 Langsmith를 통해서는 확인할 수 있는 **Code-level** 문제를 확인할 수 있습니다. 어느 시간에 어떤 세션에서 어떤 Traceback 에러가 발생했는지를 확인할 수 있으며, 날짜별 폴더 분리를 통해 오래된 날짜에 대한 Cleanup도 손쉽게 적용할 수 있습니다.

> FYI

에이전트 동작 시 발생하는 LLM, Tool 등의 에러를 로깅하기 위해 TRAS는 별도의 `LoggingCallback`을 활용하였습니다.

4. **Guardrail**

Guardrail은 최근 들어 AI 신뢰성에 대한 주제가 화두 되면서 보편화되기 시작한 기능입니다.  
TRAS는 LLM의 응답 신뢰성과 서비스 안정성을 확보하기 위해 Guardrail 시스템을 도입하였습니다.
모델의 응답에 대해 형식, 내용, 정책 위반 여부를 사전 정의된 기준에 따라 검사하며, 기준을 벗어날 경우 적절한 후속 처리(수정 요청, 차단 등)를 수행합니다.

이를 통해 아래와 같은 내용이 사용자에게 제공되지 않도록 합니다. 

* 마약 및 불법 약물 관련 내용
* 성매매 등 성적인 내용

위 내용들은 한국인이 해외 여행을 하는 데 있어 취약해질 수 있는 내용입니다. 따라서 챗봇이 혹시라도 여행지에 대해 위와 같은 내용이 포함되지 않도록 하였습니다.

> FYI

처음 도입하고자 했던 Guardrail 서비스는 `Google Checks`의 [Guardrail API](https://developers.google.com/checks/guide/ai-safety/guardrails) 입니다. 하지만, 해당 API에 대한 권한을 받아 동작시켰을 경우, 길지 않은 텍스트임에도 제한이 걸려 request fail이 발생하였습니다. 확인해보니 해당 서비스는 현재 `beta` 버전 상태로 긴 텍스트에 대한 요청을 보내기 위해서는 Google Developers로 메일을 보내 별도의 승인 절차를 받아야 했습니다. 과제 구현 기간 상 무리라고 판단하였습니다.

`Guardrail AI`는 가드레일을 위한 오픈소스 프레임워크입니다. 이 플랫폼을 택한 이유는 자체적으로 Guardrail `Hub` 을 제공하여 상황에 맞는 다양한 가드레일 모델을 제공한다는 점입니다. 보통 LLM의 답변을 검증하는 가드레일은 이를 위한 다른 **LLM** 을 통해 진행됩니다. 이 모델은 가드레일이라는 특정 Task만을 수행하기 위한 모델이기 때문에 general한 LLM을 사용하는 것은 불필요한 리소스라고 생각하였습니다. 따라서, 저는 [Llama7B Guardrail](https://hub.guardrailsai.com/validator/guardrails/llamaguard_7b)을 채택하였습니다.

가드 레일은 최종적인 챗봇(supervisor)의 output에 적용되어야 합니다. 이를 위해 최종 output만을 필터링하여 가드레일은 적용하는 함수(노드)를 supervisor의 `post_model_hook` 에 적용해주었습니다.

5. **Others**

* History Summary: 대화 내용에 대한 히스토리가 계속해서 쌓이면 모델의 입력에 문제가 발생하기 때문에 이를 관리해주는 것이 필요합니다. 이를 위해 챗봇에 들어가기 전 `pre_model_hook` 을 통해 오래된 대화 내용을 요약하여 전체 context를 유지하도록 하였습니다.

## 🏛️ Production Architecture

![architecture](https://github.com/user-attachments/assets/d9b6c786-00e4-4857-9c5d-22f2eaa991b5)

멀티 에이전트 기반 여행 일정 서비스의 아키텍처의 각 요소와 그 흐름을 소개합니다.
위 아키텍처의 각 요소들의 플랫폼(그림)은 에시일 뿐, 고정되지 않습니다.

### Components

그림의 각 Component에 대한 설명은 아래와 같습니다.

* `Web Server` .

웹 서버로 간단한 정적 파일 제공 및 Frontend로 리버스 프록시 처리, HTTPS 인증서(TLS)를 관리합니다.

* `Frontend`

사용자 입력 기반 챗 인터페이스를 UI로 제공합니다. 

* `Backend(Langgraph)`

멀티 에이전트의 요청을 받아

* `Vectorstore`

* `In Memory DB/Queue`

* `Database`:

* `Task workers`:

* `LLMops`

* `Monitoring`

* `Deployment`

* `Image Registry`

* `Agent Monitor`

* `Prompt Hub`

* `Agent Monitor`

* `Prompt Hub`:

* `LLM API`

* `External API`

### Flows



## 🛡️ Continous Validation



## 🔧 Dev Tools

* uv: Rust로 개발된 초고속 파이썬 패키지 매니저 
* ruff: Rust로 개발된 초경량 파이썬 린터 및 포매터
* Cursor IDE: AI 코드 보조 기능을 탑재한 VsCode 기반 코드 에디터

> FYI

**Cursor IDE 회고**

코드를 이어나가거나 간단한(네이밍/변수 분리 등) 수정 사항을 이어나갈 때는 Tab 자동 완성 기능을 사용하여 Typing 시간을 줄여 생산성이 증가하였습니다. Agent 모드는 거의 사용하지 않았습니다. Agent 모드를 사용하면 확실히 원하는 기능을 뚝딱 만들기는 하지만, 제 자신의 입맛에 맞게끔 개발을 해주는 느낌은 아니었습니다. 또한 AI의 코드를 자신이 이해해야 하는 상황이 발생해 추후에 다른 모듈 및 컴포넌트들과 연결이 용이하지 않았습니다. 따라서, 저는 필요한 경우는 Cmd + K 의 partial agent를 활용하고 대부분은 일반 챗봇인 Ask 기능을 활용하였습니다. Ask 기능을 통해 나온 내용을 확인하고 유용한 것은 부부적으로 골라 코드에 반영하였습니다. 

하지만 언급했듯, 자동 완성이나 수정 사항 반영 그리고 이번 프로젝트에서는 프롬프트의 초안을 작성하는 데에는 AI 덕분에 큰 생산성을 누릴 수 있었습니다. 분명히 지금도 Coding의 **서포터** 로서는 매우 훌륭하고 큰 의미가 있는 것 같습니다.

바이브 코딩을 하는 것이 아닌 이상, 아직은 AI에게 주도권을 완전히 넘겨주기에는 다소 무리가 있다고 생각합니다. 물론 Cursor의 rule 기능을 잘 다듬는 다거나 계속해서 모델이 발전하면 다가올 미래라고 생각합니다. 그 미래를 대비하기 위해 발전하는 AI와 함께 나 자신도 발전되어야 한다고 생각합니다.

## 📄 TODO

이번 프로젝트에서 보강하고 싶은 점은 아래와 같습니다.

### Code Level

* Logging: 이 프로젝트는 로그를 파일 단위로 저장합니다. 따라서, 운영자가 모니터링을 위해서는 각 로그 파일들을 확인해야 합니다. 이보다는 로깅 및 모니터링 플랫폼과 연동하여 보다 편리하게 모니터링하고, 무엇보다 에러가 발생했을 떄 `event`를 통해 운영자에게 notice해주는 기능이 필요합니다.
* Checkpoint: 현재 이 프로젝트는 대화 내용을 유지하기 위한 메모리(체크포인트)로 In-memory 구조를 사용중입니다. 이는 서버의 메모리(RAM) 리소스가 부족하거나 사용자가 많은 경우 매우 취약합니다. 따라서, 이를 `DB` 기반 메모리로 관리해야 합니다.
* RAG: 실제로 이번 프로젝트에서 여행에 대한 정보를 외부 API와 Web loading을 통해 수집하니, idle time이 길고, 때에 따라 도움이 되는 정보들이 부족한 경우가 많았습니다. 따라서, 이보다는 보다 검증된 최신 정보를 유지하는 `vectorstore`을 따로 관리하고 여기서 Retrival을 하는 방식도 도입하는 것이 좋을 것이라 느꼈습니다. (TMI: RAG 관련 정보 https://velog.io/@richpin/LLM-RAG-1-Overview)  
* Prompt: 그 때마다 Prompt Hub 에서 pull 하는 것은 I/O 적으로 매우 비효율적이라고 생각합니다. 이를 위해 서버 내에 프롬프트 세트를 저장(캐싱)해두고 이를 주기적으로, 더 이상적으로 새로운 버전이 commit 되었을 경우 교체하면 보다 빠른 프롬프트 세팅이 될 것 같습니다.
* Unit Test: 코드 함수에 대한 각각의 Unit TC를 추가하여 코드 정확성을 유지하는 것이 좋습니다.
* History: 대화 히스토리를 관리하는 것을 대화가 없을 때 비동기 기반 큐 시스템으로 독립적으로 유지하는 것이 응답 속도를 최적화하는 데 도움이 될 것이라 생각합니다. 

### UX Level

* Credentials: 더 나은 사용성을 위해서는 사용자가 직접 UI로 각종 Key와 Credentials 등 자신의 외부 정보를 지급해야 할 것입니다.
* User Info: Long-term 메모리의 일환으로 사용자의 정보를 저장하는 DB나 Langgraph의 `Store` 기능을 사용하여 보다 사용자 맞춤형 챗봇을 제공할 수 있습니다.

## Addtional Screenshots

#### 기본 화면

![basic](https://github.com/user-attachments/assets/ce14e351-3bea-47c9-83bb-3871bfebfc45)

#### 여행지 추천

![research_chile](https://github.com/user-attachments/assets/6704a612-e5fb-408b-b72b-ce924b24bbe5)
![research_paris](https://github.com/user-attachments/assets/2a0421a5-9685-419a-89ac-4b452d2f95e4)
![research_southeastern](https://github.com/user-attachments/assets/2a872597-ec00-4372-a304-667faf48fb12)

#### 여행 계획 수립

![planner_borakai](https://github.com/user-attachments/assets/ff576e61-8623-490a-9b31-610ccdc4bb6c)
![planner_rome](https://github.com/user-attachments/assets/fb55d2b2-5955-445a-be55-6563c9a55f1e)
![planner_sanghai](https://github.com/user-attachments/assets/064a9413-02f0-4b64-843d-2434a2228029)

### 여행 일정 관리

![calendar_busan](https://github.com/user-attachments/assets/7ef47ac0-57f6-42cd-b0be-9d8b813d9022)
![calendar_busan_move](https://github.com/user-attachments/assets/329a63a7-6a00-426b-8080-ec5ca8b73de5)
![calendar_mongol](https://github.com/user-attachments/assets/83a19f4b-534f-424c-89f2-1d8f7fe3c373)

### SNS 공유

![twitter_mongol](https://github.com/user-attachments/assets/fafd07b3-71a7-4d70-a42b-3abaccbe8fa8)
![twitter_sanghai](https://github.com/user-attachments/assets/2fac3bad-cf91-473b-b7bf-3c3586161020)
![twitter_sanghai_del](https://github.com/user-attachments/assets/42a3d1af-007e-4a5b-8297-8f2442ac8942)




