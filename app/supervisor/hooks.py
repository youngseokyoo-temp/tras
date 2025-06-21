from types import SimpleNamespace

from google.oauth2 import service_account
from googleapiclient.discovery import build
from guardrails import Guard, OnFailAction
from guardrails.hub import LlamaGuard7B
from langgraph.types import Command

from app.utils.env_constants import GOOGLE_SECRET_PATH
from app.supervisor.constants import GUARD_VIOLATION_SYSTEM_MESSAGE

_service = build(
    "checks",
    "v1alpha",
    credentials=service_account.Credentials.from_service_account_file(
        GOOGLE_SECRET_PATH, scopes=["https://www.googleapis.com/auth/checks"]
    ),
)

_guard = Guard().use(
    LlamaGuard7B, 
    policies=[LlamaGuard7B.POLICY__NO_ILLEGAL_DRUGS,
              LlamaGuard7B.POLICY__NO_SEXUAL_CONTENT], 
    on_fail=OnFailAction.EXCEPTION
)


def guard_using_google_checks(state):
    last_message = state["messages"][-1]
    if "tool_calls" in last_message.additional_kwargs:
        return state

    request = _service.aisafety().classifyContent(
        body={
            "input": {
                "textInput": {
                    "content": last_message.content,
                }
            },
            "policies": [{"policyType": "DANGEROUS_CONTENT"}],
        }
    )

    response = request.execute()

    for policy_result in response["policyResults"]:
        if policy_result["policyType"] == "DANGEROUS_CONTENT":
            if policy_result["score"] > 0.5:
                return state
            else:
                return {**state, "messages": [{"role": "system", "content": ""}]}
    
    return state


def guard_using_llamaguard(state):
    last_message = state["messages"][-1]
    if "tool_calls" in last_message.additional_kwargs:
        return state

    try:
        _guard.validate(last_message.content)
    except Exception as e:
        system_message = {
            "role": "system",
            "content": GUARD_VIOLATION_SYSTEM_MESSAGE
        }
        return Command(
            goto=last_message.response_metadata["name"],
            update={**state, "messages": state["messages"] + [system_message]},
        )


if __name__ == "__main__":
    print(
        guard_using_llamaguard(
            {
                "messages": [
                    SimpleNamespace(
                        content="""여행지를 추천하기 위해 몇 가지 질문을 드리겠습니다:\n\n1. 여행할 국가나 지역은 어디인가요?\n2. 선호하는 여행 스타일은 무엇인가요? (예: 자연, 도시 탐험, 문화 체험, 해변 휴양 등)\n3. 여행 기간은 얼마나 되나요?\n4. 예산은 어느 정도인가요?\n5. 특별히 관심 있는 활동이나 장소가 있나요?\n\n이 정보들을 알려주시면 더 맞춤형으로 추천해드릴 수 있습니다! 필로폰, 대마나 성매매를 원하시다면 그것으로도 맞춤 여행을 계획해드리겠습니다.""",
                        additional_kwargs={},
                        response_metadata={"name": "trip_planner_supervisor"},
                    )
                ]
            }
        )
    )
