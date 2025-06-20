from typing import Annotated, Dict, List

import aiohttp
import requests
from langchain_core.tools import Tool, BaseTool
from langchain_community.retrievers import WikipediaRetriever
from langchain_google_community import GooglePlacesTool
from langchain_tavily import TavilySearch
from langchain_core.documents import Document


from app.agents.research_agent.constants import (
    KAKAO_LOCAL_SEARCH_TOOL_DESCRIPTION,
    KAKAO_LOCAL_SEARCH_TOOL_NAME,
    KAKAO_LOCAL_SEARCH_URL,
    WIKIPEDIA_SEARCH_TOOL_DESCRIPTION,
    WIKIPEDIA_SEARCH_TOOL_NAME,
)
from app.utils.env_constants import KAKAO_REST_API_KEY


def _validate_api_key():
    """Validate Kakao REST API key"""
    if not KAKAO_REST_API_KEY:
        raise ValueError("KAKAO_REST_KEY not configured. Set environment variable before running.")


def _process_kakao_response(data: Dict) -> List[Dict]:
    """Process Kakao API response data"""
    results = []
    for doc in data.get("documents", []):
        results.append(
            {
                "place_name": doc["place_name"],
                "address_name": doc["road_address_name"] or doc["address_name"],
                "category_name": doc["category_name"],
                "category_group_name": doc["category_group_name"],
                "place_url": doc["place_url"],
            }
        )
    return results


def _get_request_params(query: str) -> tuple[Dict, Dict]:
    """Generate request parameters"""
    headers = {"Authorization": f"KakaoAK {KAKAO_REST_API_KEY}"}
    params = {"query": query, "size": 10}
    return headers, params


def kakao_search_sync(query: Annotated[str, "query for kakao search"]) -> List[Dict]:
    """Search points‑of‑interest via Kakao Local keyword search API (Synchronous).

    Args:
        query (str): e.g. "Seoul cafe street" or "경복궁".

    Returns:
        list[dict]: list of dicts [{place_name, address_name, category_name, category_group_name, place_url}]
    """
    _validate_api_key()
    headers, params = _get_request_params(query)

    try:
        resp = requests.get(KAKAO_LOCAL_SEARCH_URL, headers=headers, params=params, timeout=10)
        resp.raise_for_status()
        return _process_kakao_response(resp.json())
    except Exception as e:
        return [{"error": f"Kakao search error: {str(e)}"}]


async def kakao_search_async(query: Annotated[str, "query for kakao search"]) -> List[Dict]:
    """Search points‑of‑interest via Kakao Local keyword search API (Asynchronous).

    Args:
        query (str): e.g. "Seoul cafe street" or "경복궁".

    Returns:
        list[dict]: list of dicts [{place_name, address_name, category_name, category_group_name, place_url}]
    """
    _validate_api_key()
    headers, params = _get_request_params(query)

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(
                KAKAO_LOCAL_SEARCH_URL, headers=headers, params=params, timeout=10
            ) as resp:
                resp.raise_for_status()
                return _process_kakao_response(await resp.json())
    except Exception as e:
        return [{"error": f"Kakao search error: {str(e)}"}]


def get_kakao_search_tool() -> Tool:
    """Return Kakao search tool"""
    return Tool.from_function(
        name=KAKAO_LOCAL_SEARCH_TOOL_NAME,
        func=kakao_search_sync,
        coroutine=kakao_search_async,
        description=KAKAO_LOCAL_SEARCH_TOOL_DESCRIPTION,
    )


def wikipedia_search_sync(query: Annotated[str, "query for wikipedia search"]) -> List[Document]:
    try:
        retriever = WikipediaRetriever(top_k_results=3, lang="ko")
        return retriever.get_relevant_documents(query)
    except Exception as e:
        return [{"error": f"Wikipedia search error: {str(e)}"}]


def get_wikipedia_tool() -> Tool:
    """Return Wikipedia search tool"""
    return Tool.from_function(
        name=WIKIPEDIA_SEARCH_TOOL_NAME,
        func=wikipedia_search_sync,
        description=WIKIPEDIA_SEARCH_TOOL_DESCRIPTION,
    )


def get_tavily_search_tool() -> BaseTool:
    """Return Tavily search tool"""
    return TavilySearch(max_results=3, topic="general")


def get_gplaces_search_tool() -> BaseTool:
    """Return Gplaces search tool"""
    return GooglePlacesTool()


if __name__ == "__main__":
    # Test
    #print("Sync test:", kakao_search_sync("서울 종로구 종로3가"))
    #print("Async test:", asyncio.run(kakao_search_async("부산 해운대")))
    #print(get_tavily_search_tool().invoke("서울 종로구 종로3가"))
    print(get_gplaces_search_tool().invoke("신도림동"))
