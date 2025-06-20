from typing import Annotated, Dict, List, Union
import aiohttp
import requests
from urllib.parse import urlparse
from langchain_core.tools import Tool
from langchain_community.document_loaders import PlaywrightURLLoader

from app.utils.env_constants import NAVER_CLIENT_ID, NAVER_CLIENT_SECRET
from app.agents.planner_agent.constants import (
    NAVER_BLOG_SEARCH_URL,
    NAVER_CAFE_SEARCH_URL,
    NAVER_BLOG_SEARCH_TOOL_NAME,
    NAVER_BLOG_SEARCH_TOOL_DESCRIPTION,
    NAVER_CAFE_SEARCH_TOOL_NAME,
    NAVER_CAFE_SEARCH_TOOL_DESCRIPTION,
    NAVER_SEARCH_DISPLAY_COUNT,
    WEB_LOADER_TOOL_NAME,
    WEB_LOADER_TOOL_DESCRIPTION,
)


def _validate_naver_api_key():
    """Validate Naver API key"""
    if not NAVER_CLIENT_ID or not NAVER_CLIENT_SECRET:
        raise ValueError(
            "NAVER_CLIENT_ID or NAVER_CLIENT_SECRET is not set. Please set environment variables."
        )


def _process_naver_blog_cafe_response(data: Dict) -> List[Dict]:
    """Process Naver blog and cafe API response data"""
    results = []
    for item in data.get("items", []):
        results.append(
            {
                "title": item.get("title", "").replace("<b>", "").replace("</b>", ""),
                "link": item.get("link", ""),
                "description": item.get("description", "").replace("<b>", "").replace("</b>", ""),
            }
        )
    return results


def _get_naver_request_params(query: str) -> tuple[Dict, Dict]:
    """Generate request parameters"""
    headers = {"X-Naver-Client-Id": NAVER_CLIENT_ID, "X-Naver-Client-Secret": NAVER_CLIENT_SECRET}
    params = {"query": query, "display": NAVER_SEARCH_DISPLAY_COUNT}
    return headers, params


def naver_blog_search_sync(query: Annotated[str, "query for naver blog search"]) -> List[Dict]:
    """Naver blog search (synchronous)

    Args:
        query (str): search term (e.g. "제주도 여행", "부산 맛집")

    Returns:
        list[dict]: list of blog search results
    """
    _validate_naver_api_key()
    headers, params = _get_naver_request_params(query)

    try:
        response = requests.get(NAVER_BLOG_SEARCH_URL, headers=headers, params=params, timeout=10)
        response.raise_for_status()
        return _process_naver_blog_cafe_response(response.json())
    except Exception as e:
        return [{"error": f"Naver blog search error: {str(e)}"}]


def naver_cafe_search_sync(query: Annotated[str, "query for naver cafe search"]) -> List[Dict]:
    """Naver cafe search (synchronous)

    Args:
        query (str): search term (e.g. "제주도 여행", "부산 관광")

    Returns:
        list[dict]: list of cafe search results
    """
    _validate_naver_api_key()
    headers, params = _get_naver_request_params(query)

    try:
        response = requests.get(NAVER_CAFE_SEARCH_URL, headers=headers, params=params, timeout=10)
        response.raise_for_status()
        return _process_naver_blog_cafe_response(response.json())
    except Exception as e:
        return [{"error": f"Naver cafe search error: {str(e)}"}]


async def naver_blog_search_async(query: Annotated[str, "query for naver blog search"]) -> List[Dict]:
    """Naver blog search (asynchronous)

    Args:
        query (str): search term

    Returns:
        list[dict]: list of blog search results
    """
    _validate_naver_api_key()
    headers, params = _get_naver_request_params(query)

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(
                NAVER_BLOG_SEARCH_URL, headers=headers, params=params, timeout=10
            ) as response:
                response.raise_for_status()
                data = await response.json()
                return _process_naver_blog_cafe_response(data)
    except Exception as e:
        return [{"error": f"Naver blog search error: {str(e)}"}]


async def naver_cafe_search_async(query: Annotated[str, "query for naver cafe search"]) -> List[Dict]:
    """Naver cafe search (asynchronous)

    Args:
        query (str): search term

    Returns:
        list[dict]: list of cafe search results
    """
    _validate_naver_api_key()
    headers, params = _get_naver_request_params(query)

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(
                NAVER_CAFE_SEARCH_URL, headers=headers, params=params, timeout=10
            ) as response:
                response.raise_for_status()
                data = await response.json()
                return _process_naver_blog_cafe_response(data)
    except Exception as e:
        return [{"error": f"Naver cafe search error: {str(e)}"}]


def to_mobile_view(url: str) -> str:
    """Transform Naver blog URL to mobile view"""
    if "blog.naver.com" in url:
        parsed = urlparse(url)
        user, post = parsed.path.strip("/").split("/")
        return f"https://m.blog.naver.com/{user}/{post}"
    elif "cafe.naver.com" in url:
        parsed = urlparse(url)
        user, post = parsed.path.strip("/").split("/")
        return f"https://m.cafe.naver.com/{user}/{post}"
    return url


def _load_page_content_sync(urls: Annotated[Union[List[str], str], "list of URLs"]) -> List[str]:
    """Load page content from URL (synchronous)

    Args:
        urls (List[str]): list of URLs

    Returns:
        List[str]: list of page contents
    """
    try:
        if isinstance(urls, str):
            mobile_urls = [to_mobile_view(urls)]
        elif isinstance(urls, list):
            mobile_urls = [to_mobile_view(url) for url in urls]
        loader = PlaywrightURLLoader(mobile_urls, continue_on_failure=True)
        docs = loader.load()
        return [doc.page_content for doc in docs]
    except Exception as e:
        return [{"error": f"Web Loader error: {str(e)}"}]


async def _load_page_content_async(urls: Annotated[Union[List[str], str], "list of URLs"]) -> List[str]:
    """Load page content from URL (asynchronous)

    Args:
        urls (List[str]): list of URLs

    Returns:
        List[str]: list of page contents
    """
    contents = []
    try:
        if isinstance(urls, str):
            mobile_urls = [to_mobile_view(urls)]
        elif isinstance(urls, list):
            mobile_urls = [to_mobile_view(url) for url in urls]
        mobile_urls = [to_mobile_view(url) for url in urls]
        loader = PlaywrightURLLoader(mobile_urls, continue_on_failure=True)
        async for doc in loader.aload():
            contents.append(doc.page_content)
        return contents
    except Exception as e:
        return [{"error": f"Web Loader error: {str(e)}"}]


def get_naver_blog_search_tool() -> Tool:
    """Return Naver blog search tool"""
    return Tool.from_function(
        name=NAVER_BLOG_SEARCH_TOOL_NAME,
        func=naver_blog_search_sync,
        coroutine=naver_blog_search_async,
        description=NAVER_BLOG_SEARCH_TOOL_DESCRIPTION,
    )


def get_naver_cafe_search_tool() -> Tool:
    """Return Naver cafe search tool"""
    return Tool.from_function(
        name=NAVER_CAFE_SEARCH_TOOL_NAME,
        func=naver_cafe_search_sync,
        coroutine=naver_cafe_search_async,
        description=NAVER_CAFE_SEARCH_TOOL_DESCRIPTION,
    )


def get_web_loader_tool() -> Tool:
    """Return Web loader tool"""
    return Tool.from_function(
        name=WEB_LOADER_TOOL_NAME,
        func=_load_page_content_sync,
        coroutine=_load_page_content_async,
        description=WEB_LOADER_TOOL_DESCRIPTION,
    )


if __name__ == "__main__":
    # Test
    #tool = get_naver_cafe_search_tool()
    #print(tool.invoke("로마 6월 여행 계획"))
    tool = get_web_loader_tool()
    print(tool.invoke({"urls": ["https://blog.naver.com/mjkwon7471/223904255047"]} ))