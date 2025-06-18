import asyncio
from typing import Dict, List

import aiohttp
import requests
from langchain_core.tools import Tool

from app.utils.env_constants import NAVER_CLIENT_ID, NAVER_CLIENT_SECRET, OPENWEATHER_API_KEY
from app.agents.planner_agent.constants import (
    NAVER_BLOG_SEARCH_URL,
    NAVER_CAFE_SEARCH_URL,
    NAVER_BLOG_SEARCH_TOOL_NAME,
    NAVER_BLOG_SEARCH_TOOL_DESCRIPTION,
    NAVER_CAFE_SEARCH_TOOL_NAME,
    NAVER_CAFE_SEARCH_TOOL_DESCRIPTION,
)

def _validate_naver_api_key():
    """Validate Naver API key"""
    if not NAVER_CLIENT_ID or not NAVER_CLIENT_SECRET:
        raise ValueError("NAVER_CLIENT_ID or NAVER_CLIENT_SECRET is not set. Please set environment variables.")


def _validate_openweather_api_key():
    """Validate OpenWeather API key"""
    if not OPENWEATHER_API_KEY:
        raise ValueError("OPENWEATHER_API_KEY is not set. Please set environment variable.")


def _process_naver_blog_response(data: Dict) -> List[Dict]:
    """Process Naver blog API response data"""
    results = []
    for item in data.get("items", []):
        results.append({
            "title": item.get("title", "").replace("<b>", "").replace("</b>", ""),
            "description": item.get("description", "").replace("<b>", "").replace("</b>", ""),
            "bloggerlink": item.get("bloggerlink", ""),
            "postdate": item.get("postdate", "")
        })
    return results


def _process_naver_cafe_response(data: Dict) -> List[Dict]:
    """Process Naver cafe API response data"""
    results = []
    for item in data.get("items", []):
        results.append({
            "title": item.get("title", "").replace("<b>", "").replace("</b>", ""),
            "link": item.get("link", ""),
            "description": item.get("description", "").replace("<b>", "").replace("</b>", ""),
            "cafename": item.get("cafename", ""),
            "cafeurl": item.get("cafeurl", "")
        })
    return results


def _get_request_params(query: str) -> tuple[Dict, Dict]:
    """Generate request parameters"""
    headers = {
        "X-Naver-Client-Id": NAVER_CLIENT_ID,
        "X-Naver-Client-Secret": NAVER_CLIENT_SECRET
    }
    params = {"query": query, "display": 10}
    return headers, params


def naver_blog_search_sync(query: str) -> List[Dict]:
    """Naver blog search (sync)
    
    Args:
        query (str): search term (e.g. "제주도 여행", "부산 맛집")
        display (int): number of search results (default: 10, maximum: 100)
        
    Returns:
        list[dict]: list of blog search results
    """
    _validate_naver_api_key()
    headers, params = _get_request_params(query)
    
    try:
        response = requests.get(NAVER_BLOG_SEARCH_URL, headers=headers, params=params, timeout=10)
        response.raise_for_status()
        return _process_naver_blog_response(response.json())
    except Exception as e:
        return [{"error": f"Naver blog search error: {str(e)}"}]


def naver_cafe_search_sync(query: str) -> List[Dict]:
    """Naver cafe search (sync)
    
    Args:
        query (str): search term (e.g. "제주도 여행", "부산 관광")
        display (int): number of search results (default: 10, maximum: 100)
        
    Returns:
        list[dict]: list of cafe search results
    """
    _validate_naver_api_key()
    headers, params = _get_request_params(query)
    
    try:
        response = requests.get(NAVER_CAFE_SEARCH_URL, headers=headers, params=params, timeout=10)
        response.raise_for_status()
        return _process_naver_cafe_response(response.json())
    except Exception as e:
        return [{"error": f"Naver cafe search error: {str(e)}"}]


async def naver_blog_search_async(query: str) -> List[Dict]:
    """Naver blog search (asynchronous)
    
    Args:
        query (str): search term
        display (int): number of search results
        
    Returns:
        list[dict]: list of blog search results
    """
    _validate_naver_api_key()
    headers, params = _get_request_params(query)
    
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(NAVER_BLOG_SEARCH_URL, headers=headers, params=params, timeout=10) as response:
                response.raise_for_status()
                data = await response.json()
                return _process_naver_blog_response(data)
    except Exception as e:
        return [{"error": f"Naver blog search error: {str(e)}"}]


async def naver_cafe_search_async(query: str) -> List[Dict]:
    """Naver cafe search (asynchronous)
    
    Args:
        query (str): search term
        display (int): number of search results
        
    Returns:
        list[dict]: list of cafe search results
    """
    _validate_naver_api_key()
    headers, params = _get_request_params(query)
    
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(NAVER_CAFE_SEARCH_URL, headers=headers, params=params, timeout=10) as response:
                response.raise_for_status()
                data = await response.json()
                return _process_naver_cafe_response(data)
    except Exception as e:
        return [{"error": f"Naver cafe search error: {str(e)}"}]


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


if __name__ == "__main__":
    # Test
    tool = get_naver_cafe_search_tool()
    print(tool.invoke("로마 6월 여행 계획"))
