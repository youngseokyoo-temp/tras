PROJECT_TITLE = "TRAS! - 나만의 여행 플랜 어시스턴트"
PROJECT_ICON = "🌏"
PROJECT_LOGO_HTML = """
    <style>
        .title-container {
            background-image: url('https://images.unsplash.com/photo-1507525428034-b723cf961d3e');
            background-size: cover;
            padding: 20px;
            border-radius: 12px;
            text-align: center;
            color: white;
        }
        .title-text {
            background-color: rgba(0, 0, 0, 0.4);
            display: inline-block;
            padding: 10px 20px;
            border-radius: 8px;
            font-size: 28px;
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
        }
    </style>
    <div class='title-container'>
        <div class='title-text'>🌏 TRAS! - 나만의 여행 플랜 어시스턴트</div>
    </div>
"""
CHAT_INPUT_PLACEHOLDER = "여행 플랜 작성을 시작해보세요."
GREETING_MESSAGE = """
**TRAS**는 대화만으로 여행의 시작부터 끝까지 함께하는 **멀티 에이전트 여행 플래너**입니다. 🧭  
어떻게 도와드릴까요?

---

#### 🗺️ 여행 계획 세우기

- 여행지를 고르고 싶으신가요?  
  → 저와 함께 여행지를 탐색해보세요.

- 여행지가 정해졌다면?  
  → 일정을 구성하고 여행 계획서를 만들어 드릴게요.

---

#### 📅 캘린더 등록 및 공유

- 완성된 여행 계획을 캘린더에 등록해보세요.  
- 필요하다면 지인과 링크로 손쉽게 공유할 수도 있어요!

---

💡 *대화를 시작하기 전, 왼쪽 사이드바에서 원하는 AI 모델을 선택해주세요.*  
선택하지 않으면 기본 모델이 사용되며, 대화 중에도 언제든 변경할 수 있습니다.
"""
MODEL_LOADING_ERROR_MESSAGE = """
### 😥 모델을 불러오는 중 문제가 발생했어요.

지금 선택된 모델 대신,  
왼쪽 사이드바에서 **다른 모델을 선택**해 주세요!
"""