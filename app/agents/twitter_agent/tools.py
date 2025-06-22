import re
from typing import Annotated, Dict

import tweepy
from bs4 import BeautifulSoup
from langchain_core.tools import Tool
from markdown import markdown
from tweepy import Client
from tweepy.asynchronous import AsyncClient
from tweepy.client import BaseClient

from app.agents.twitter_agent.constants import TWEETS_MAX_RESULTS
from app.utils.env_constants import (
    TWITTER_ACCESS_TOKEN,
    TWITTER_ACCESS_TOKEN_SECRET,
    TWITTER_API_KEY,
    TWITTER_API_KEY_SECRET,
    TWITTER_BEARER_TOKEN,
)


def _markdown_to_text(markdown_string: str) -> str:
    """ Converts a markdown string to plaintext """

    html = markdown(markdown_string)

    # remove code snippets
    html = re.sub(r'<pre>(.*?)</pre>', ' ', html)
    html = re.sub(r'<code>(.*?)</code >', ' ', html)

    # extract text
    soup = BeautifulSoup(html, "html.parser")
    text = ''.join(soup.find_all(string=True))

    return text

def _validate_twitter_api_keys():
    """Validate Twitter API keys"""
    if not all([TWITTER_API_KEY, TWITTER_API_KEY_SECRET, TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_TOKEN_SECRET, TWITTER_BEARER_TOKEN]):
        raise ValueError("Twitter API keys are not set. Please set TWITTER_API_KEY, TWITTER_API_KEY_SECRET, TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_TOKEN_SECRET, and TWITTER_BEARER_TOKEN environment variables.")


def _get_twitter_client_v2(async_client=False) -> BaseClient:
    """Get Twitter API v2 client using tweepy"""
    _validate_twitter_api_keys()
    if async_client:
        return AsyncClient(
            consumer_key=TWITTER_API_KEY,
            consumer_secret=TWITTER_API_KEY_SECRET,
            access_token=TWITTER_ACCESS_TOKEN,
            access_token_secret=TWITTER_ACCESS_TOKEN_SECRET,
            bearer_token=TWITTER_BEARER_TOKEN,
            wait_on_rate_limit=True
        )
    return Client(
        consumer_key=TWITTER_API_KEY,
        consumer_secret=TWITTER_API_KEY_SECRET,
        access_token=TWITTER_ACCESS_TOKEN,
        access_token_secret=TWITTER_ACCESS_TOKEN_SECRET,
        bearer_token=TWITTER_BEARER_TOKEN,
        wait_on_rate_limit=True
    )

def post_tweet_sync(text: Annotated[str, "tweet text content"]) -> Dict:
    """Post a tweet to Twitter using tweepy (synchronous)
    
    Args:
        text (str): Tweet text content
        
    Returns:
        dict: Response containing tweet information or error
    """
    try: 
        client = _get_twitter_client_v2()
        
        response = client.create_tweet(text=text)

        return {
            "tweet_id": response.data["id"],
            "message": "Tweet posted successfully"
        }
        
    except tweepy.TooManyRequests:
        return {"error": "Rate limit exceeded. Please wait before posting again."}
    except tweepy.Unauthorized:
        return {"error": "Unauthorized. Please check your Twitter API credentials."}
    except tweepy.TweepyException as e:
        return {"error": f"Twitter API error: {str(e)}"}
    except Exception as e:
        return {"error": f"Failed to post tweet: {str(e)}"}


async def post_tweet_async(text: Annotated[str, "tweet text content"]) -> Dict:
    """Post a tweet to Twitter using tweepy (asynchronous)
    
    Args:
        text (str): Tweet text content
        
    Returns:
        dict: Response containing tweet information or error
    """
    try:
        client = _get_twitter_client_v2(async_client=True)
        response = await client.create_tweet(text=text)
        return {
            "tweet_id": response.data.id,
            "message": "Tweet posted successfully"
        }
    except tweepy.TooManyRequests:
        return {"error": "Rate limit exceeded. Please wait before posting again."}
    except tweepy.Unauthorized:
        return {"error": "Unauthorized. Please check your Twitter API credentials."}
    except tweepy.TweepyException as e:
        return {"error": f"Twitter API error: {str(e)}"}
    except Exception as e:
        return {"error": f"Failed to post tweet: {str(e)}"}

def get_user_tweets_sync(_input: Annotated[str, "Meaningless input"]) -> Dict:
    """Get recent tweets with tweet id and text from a user using tweepy (synchronous)
        
    Returns:
        dict: Response containing user's recent tweets
    """
    try:
        client = _get_twitter_client_v2()
        
        user = client.get_me() 
        user_id = user.data.id
        
        tweets = client.get_users_tweets(
            id=user_id,
            max_results=TWEETS_MAX_RESULTS,
            exclude=['replies', 'retweets'],
            tweet_fields=['id', 'text']
        )
        
        tweet_list = []
        if tweets.data:
            for tweet in tweets.data:
                tweet_list.append({
                    "id": tweet.id,
                    "text": tweet.text,
                })
        
        return {
            "tweets": tweet_list,
            "message": f"Retrieved {len(tweet_list)} tweets from you"
        }
        
    except tweepy.TooManyRequests:
        return {"error": "Rate limit exceeded. Please wait before requesting again."}
    except tweepy.Unauthorized:
        return {"error": "Unauthorized. Please check your Twitter API credentials."}
    except tweepy.TweepyException as e:
        return {"error": f"Twitter API error: {str(e)}"}
    except Exception as e:
        return {"error": f"Failed to get user tweets: {str(e)}"}


async def get_user_tweets_async(_input: Annotated[str, "Meaningless input"]) -> Dict:
    """Get recent tweets with tweet id and text from a user using tweepy (asynchronous)
    
    Returns:
        dict: Response containing user's recent tweets
    """
    try:
        client = _get_twitter_client_v2(async_client=True)
        user = await client.get_me()
        user_id = user.data.id
        tweets = await client.get_users_tweets(
            id=user_id,
            max_results=TWEETS_MAX_RESULTS, 
            exclude=['replies', 'retweets'],
            tweet_fields=['id', 'text']
        )
        
        tweet_list = []
        if tweets.data:
            for tweet in tweets.data:
                tweet_list.append({
                    "id": tweet.id,
                    "text": tweet.text,
                })
        
        return {
            "tweets": tweet_list,
            "message": f"Retrieved {len(tweet_list)} tweets from you"
        }
    except tweepy.TooManyRequests:
        return {"error": "Rate limit exceeded. Please wait before requesting again."}
    except tweepy.Unauthorized:
        return {"error": "Unauthorized. Please check your Twitter API credentials."}
    except tweepy.TweepyException as e:
        return {"error": f"Twitter API error: {str(e)}"}
    except Exception as e:
        return {"error": f"Failed to get user tweets: {str(e)}"}


def delete_tweet_sync(tweet_id: Annotated[str, "ID of the tweet to delete"]) -> Dict:
    """Delete a tweet using tweepy (synchronous)
    
    Args:
        tweet_id (str): ID of the tweet to delete
        
    Returns:
        dict: Response indicating success or error
    """
    try:
        client = _get_twitter_client_v2()
        response = client.delete_tweet(id=tweet_id)
        if response.data.deleted:   
            return {
                "tweet_id": tweet_id,
                "message": "Tweet deleted successfully"
            }
        else:
            return {
                "tweet_id": tweet_id,
                "message": "Tweet deletion failed"
            }
        
    except tweepy.TooManyRequests:
        return {"error": "Rate limit exceeded. Please wait before deleting again."}
    except tweepy.Unauthorized:
        return {"error": "Unauthorized. Please check your Twitter API credentials."}
    except tweepy.NotFound:
        return {"error": f"Tweet with ID {tweet_id} not found or already deleted"}
    except tweepy.Forbidden:
        return {"error": "You don't have permission to delete this tweet"}
    except tweepy.TweepyException as e:
        return {"error": f"Twitter API error: {str(e)}"}
    except Exception as e:
        return {"error": f"Failed to delete tweet: {str(e)}"}


async def delete_tweet_async(tweet_id: Annotated[str, "ID of the tweet to delete"]) -> Dict:
    """Delete a tweet using tweepy (asynchronous)
    
    Args:
        tweet_id (str): ID of the tweet to delete
        
    Returns:
        dict: Response indicating success or error
    """
    try:
        client = _get_twitter_client_v2(async_client=True)
        response = await client.delete_tweet(id=tweet_id)

        if response.data.deleted:   
            return {
                "tweet_id": tweet_id,
                "message": "Tweet deleted successfully"
            }
        else:
            return {
                "tweet_id": tweet_id,
                "message": "Tweet deletion failed"
            }
    
    except tweepy.TooManyRequests:
        return {"error": "Rate limit exceeded. Please wait before deleting again."}
    except tweepy.Unauthorized:
        return {"error": "Unauthorized. Please check your Twitter API credentials."}
    except tweepy.NotFound:
        return {"error": f"Tweet with ID {tweet_id} not found or already deleted"}
    except tweepy.Forbidden:
        return {"error": "You don't have permission to delete this tweet"}
    except tweepy.TweepyException as e:
        return {"error": f"Twitter API error: {str(e)}"}
    except Exception as e:
        return {"error": f"Failed to delete tweet: {str(e)}"}


def get_twitter_post_tool() -> Tool:
    """Return Twitter post tool"""
    return Tool.from_function(
        name="twitter_post",
        func=post_tweet_sync,
        coroutine=post_tweet_async,
        description="Post a tweet to Twitter using tweepy. Use text parameter for the tweet content (max 280 characters). Optionally use reply_to_tweet_id to reply to a specific tweet.",
    )


def get_twitter_user_tweets_tool() -> Tool:
    """Return Twitter user tweets tool"""
    return Tool.from_function(
        name="twitter_user_tweets",
        func=get_user_tweets_sync,
        coroutine=get_user_tweets_async,
        description="Get recent tweets from a Twitter user using tweepy. Use username parameter (without @) and optionally max_results (default: 10, max: 100).",
    )


def get_twitter_delete_tool() -> Tool:
    """Return Twitter delete tool"""
    return Tool.from_function(
        name="twitter_delete",
        func=delete_tweet_sync,
        coroutine=delete_tweet_async,
        description="Delete a tweet from Twitter using tweepy. Use tweet_id parameter for the ID of the tweet to delete.",
    )


if __name__ == "__main__":
    # Test

    #tool = get_twitter_post_tool()
    #print(tool.invoke({"text": "Hello from TRAS! Travel Planning Assistant! 🌏✈️"}))
    
    # # Test user tweets
    #user_tool = get_twitter_user_tweets_tool()
    #print(user_tool.invoke({"_input": "get recent tweets from you"}))
    
    # # Test delete
    delete_tool = get_twitter_delete_tool()
    print(delete_tool.invoke({"tweet_id": "1935946008401477761"}))


#     print(_markdown_to_text("""# 파리 3박 4일 커플 맛집 여행 계획서

# ---

# ## 1. 여행 개요
# - **목적지**: 프랑스 파리
# - **기간**: 3박 4일
# - **테마**: 커플 여행, 맛있는 음식과 로맨틱한 관광지 중심

# ---

# ## 2. 일정별 상세 계획

# ### 1일차: 베르사유 궁전과 에펠탑, 샹젤리제 거리
# - 오전: 베르사유 궁전 및 정원 관람 (정원에서 자전거 대여 추천, 신분증 필요)
# - 오후: 파리 시내로 돌아와 에펠탑 방문 및 사진 촬영
# - 저녁: 샹젤리제 거리 산책 및 개선문 구경
# - 팁: 베르사유 정원은 궁전보다 더 아름다우니 꼭 방문하세요. 정원 내 강가에서 휴식 추천

# ### 2일차: 루브르 박물관과 파리스냅, 센느강 보트 투어
# - 오전: 루브르 박물관 관람 (사전 예매 필수, 모나리자 작품 우선 관람)
# - 오후: 파리 커플 스냅 촬영 (20만원대, 인스타그램용 고퀄 사진)
# - 저녁: 에펠탑 근처에서 센느강 보트 투어 (좌석 위치 잘 잡기)

# ### 3일차: 디즈니랜드 파리
# - 하루 종일 디즈니랜드에서 즐기기 (입장료 약 7만원, 인기 놀이기구 우선 탑승)
# - 저녁: 디즈니랜드 불꽃놀이 관람

# ### 4일차: 오르세 미술관, 샹젤리제, 마카롱 맛집 방문 후 출국
# - 오전: 오르세 미술관 관람 (루브르보다 한적하고 유명 작품 관람 가능)
# - 오후: 샹젤리제 거리에서 쇼핑 및 마카롱 맛집 방문 (1개당 약 5~7천원)
# - 저녁: 호텔에서 짐 찾고 공항 이동

# ---

# ## 3. 숙박 정보
# - 위치: 시내 중심가 (에펠탑, 샹젤리제 인근 추천)
# - 가격대: 1박당 15~25만원대 (중급 호텔 기준)
# - 예약 팁: 조기 예약 시 할인 가능, 에펠탑 뷰 객실 선호

# ---

# ## 4. 식사 계획
# - 베르사유 근처 크로와상 맛집 (베르사유 궁전 앞 작은 숲길 좌측)
# - 파리 전통 비스트로 및 카페 (샹젤리제 주변)
# - 마카롱 맛집 (샹젤리제 인근, 1개당 5~7천원)
# - 디즈니랜드 내 뷔페 및 간식
# - 센느강 주변 레스토랑에서 프랑스 요리

# ---

# ## 5. 관광지 및 활동 정보
# | 관광지           | 입장료          | 운영시간          | 예약 필요 여부          |
# |------------------|-----------------|-------------------|------------------------|
# | 베르사유 궁전     | 약 2만 원       | 09:00~18:30       | 예매 권장              |
# | 루브르 박물관     | 약 1.7만 원     | 09:00~18:00       | 사전 예매 필수         |
# | 에펠탑            | 약 2만 원       | 09:00~23:45       | 현장 구매 가능         |
# | 센느강 보트 투어  | 약 1.5만 원     | 10:00~22:00       | 예약 권장              |
# | 디즈니랜드 파리   | 약 7만 원       | 10:00~22:00       | 사전 예매 필수         |
# | 오르세 미술관     | 약 1.4만 원     | 09:30~18:00       | 현장 구매 가능         |

# ---

# ## 6. 쇼핑 및 기념품 정보
# - 샹젤리제 거리 명품 브랜드 및 기념품 샵
# - 마카롱, 프랑스 와인, 치즈, 향수 등 추천
# - 기념품 예산: 5~10만원

# ---

# ## 7. 예상 총 비용 (2인 기준)
# | 항목           | 비용(원)          | 비고                      |
# |----------------|-------------------|---------------------------|
# | 항공권         | 100~150만원       | 왕복, 시즌에 따라 변동    |
# | 숙박 (3박)     | 45~75만원         | 중급 호텔 기준            |
# | 식사           | 20~30만원         | 맛집 위주, 2인 기준       |
# | 관광지 입장료  | 15~20만원         | 주요 관광지 포함          |
# | 교통비         | 5~10만원          | 지하철, 버스, 택시 등     |
# | 쇼핑 및 기타   | 10~20만원         | 기념품 및 개인 지출       |
# | **총합계**     | **195~305만원**   | 대략적인 예상 비용        |

# ---

# ## 8. 준비물 체크리스트
# - 여권 및 비자 (필요 시)
# - 신용카드 및 현금 (유로)
# - 편한 신발 (도보 많음)
# - 카메라 또는 스마트폰 (스냅 촬영용)
# - 여행용 어댑터
# - 자전거 대여 시 신분증 (베르사유 정원)
# - 우산 또는 우비 (날씨 대비)
# - 마스크 및 개인 위생용품

# ---

# ## 9. 주의사항 및 긴급 연락처
# - 소매치기 주의 (특히 관광지 및 대중교통)
# - 긴급 연락처: 프랑스 경찰 112, 한국 대사관 +33 1 43 12 88 99
# - 현지 교통카드 구매 추천 (메트로, 버스 이용 편리)
# - 예약 시간 엄수 (루브르, 베르사유 등)

# ---

# ## 10. 날씨별/상황별 대안 계획
# - 비 올 경우: 루브르 박물관, 오르세 미술관 등 실내 관광지 집중
# - 더운 날씨: 센느강 보트 투어, 카페에서 휴식
# - 일정 변경 시: 파리 시내 카페 투어, 쇼핑 및 맛집 탐방으로 대체 가능

# ---

# ## 참고 출처
# - 파리 3박4일 커플 여행 추천 루트 및 맛집 정보  
#   [https://blog.naver.com/mjkwon7471/223904255047](https://blog.naver.com/mjkwon7471/223904255047)

# ---

# 즐거운 파리 여행 되시길 바랍니다! 필요하시면 교통편, 맛집 상세 정보도 추가로 안내해 드릴 수 있습니다."""))