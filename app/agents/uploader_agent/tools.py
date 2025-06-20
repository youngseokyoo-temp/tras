from typing import Dict, Annotated

import tweepy
from tweepy import Client
from tweepy.asynchronous import AsyncClient
from tweepy.client import BaseClient
from langchain_core.tools import Tool

from app.utils.env_constants import (
    TWITTER_ACCESS_TOKEN,
    TWITTER_ACCESS_TOKEN_SECRET,
    TWITTER_API_KEY,
    TWITTER_API_KEY_SECRET,
    TWITTER_BEARER_TOKEN,
)


def _validate_twitter_api_keys():
    """Validate Twitter API keys"""
    if not all([TWITTER_API_KEY, TWITTER_API_KEY_SECRET, TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_TOKEN_SECRET, TWITTER_BEARER_TOKEN]):
        raise ValueError("Twitter API keys are not set. Please set TWITTER_API_KEY, TWITTER_API_KEY_SECRET, TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_TOKEN_SECRET, and TWITTER_BEARER_TOKEN environment variables.")


def _get_twitter_client_v2() -> BaseClient:
    """Get Twitter API v2 client using tweepy"""
    _validate_twitter_api_keys()
   
    return Client(
        consumer_key=TWITTER_API_KEY,
        consumer_secret=TWITTER_API_KEY_SECRET,
        access_token=TWITTER_ACCESS_TOKEN,
        access_token_secret=TWITTER_ACCESS_TOKEN_SECRET,
        bearer_token=TWITTER_BEARER_TOKEN,
        wait_on_rate_limit=True
    )

def get_async_twitter_client_v2() -> BaseClient:
    """Get Twitter API v2 client using tweepy (asynchronous)"""
    _validate_twitter_api_keys()

    return AsyncClient(
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
        text (str): Tweet text content (max 280 characters)
        
    Returns:
        dict: Response containing tweet information or error
    """
    try: 
        client = _get_twitter_client_v2()
        
        response = client.create_tweet(text=text)
        
        return {
            "success": True,
            "tweet_id": response.data["id"],
            "text": response.data["text"],
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
        text (str): Tweet text content (max 280 characters)
        reply_to_tweet_id (str, optional): ID of tweet to reply to
        
    Returns:
        dict: Response containing tweet information or error
    """
    pass


def get_user_tweets_sync(username: str, max_results: int = 10) -> Dict:
    """Get recent tweets from a user using tweepy (synchronous)
    
    Args:
        username (str): Twitter username (without @)
        max_results (int): Maximum number of tweets to retrieve (default: 10, max: 100)
        
    Returns:
        dict: Response containing user's recent tweets
    """
    try:
        # Get Twitter client
        client = _get_twitter_client_v2()
        
        # Get user ID first
        user = client.get_user(username=username)
        if not user.data:
            return {"error": f"User @{username} not found"}
        
        user_id = user.data.id
        
        # Get user's tweets
        tweets = client.get_users_tweets(
            id=user_id,
            max_results=min(max_results, 100),
            tweet_fields=['created_at', 'public_metrics', 'context_annotations']
        )
        
        tweet_list = []
        if tweets.data:
            for tweet in tweets.data:
                tweet_list.append({
                    "id": tweet.id,
                    "text": tweet.text,
                    "created_at": tweet.created_at.isoformat() if tweet.created_at else None,
                    "public_metrics": tweet.public_metrics._json if hasattr(tweet, 'public_metrics') else None
                })
        
        return {
            "success": True,
            "username": username,
            "tweets": tweet_list,
            "tweet_count": len(tweet_list),
            "message": f"Retrieved {len(tweet_list)} tweets from @{username}"
        }
        
    except tweepy.TooManyRequests:
        return {"error": "Rate limit exceeded. Please wait before requesting again."}
    except tweepy.Unauthorized:
        return {"error": "Unauthorized. Please check your Twitter API credentials."}
    except tweepy.TweepyException as e:
        return {"error": f"Twitter API error: {str(e)}"}
    except Exception as e:
        return {"error": f"Failed to get user tweets: {str(e)}"}


async def get_user_tweets_async(username: str, max_results: int = 10) -> Dict:
    """Get recent tweets from a user using tweepy (asynchronous)
    
    Args:
        username (str): Twitter username (without @)
        max_results (int): Maximum number of tweets to retrieve (default: 10, max: 100)
        
    Returns:
        dict: Response containing user's recent tweets
    """
    pass


def delete_tweet_sync(tweet_id: str) -> Dict:
    """Delete a tweet using tweepy (synchronous)
    
    Args:
        tweet_id (str): ID of the tweet to delete
        
    Returns:
        dict: Response indicating success or error
    """
    try:
        # Get Twitter client
        client = _get_twitter_client_v2()
        
        # Delete tweet
        response = client.delete_tweet(id=tweet_id)
        
        return {
            "success": True,
            "tweet_id": tweet_id,
            "message": "Tweet deleted successfully"
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


async def delete_tweet_async(tweet_id: str) -> Dict:
    """Delete a tweet using tweepy (asynchronous)
    
    Args:
        tweet_id (str): ID of the tweet to delete
        
    Returns:
        dict: Response indicating success or error
    """
    pass


def search_tweets_sync(query: str, max_results: int = 10) -> Dict:
    """Search tweets using tweepy (synchronous)
    
    Args:
        query (str): Search query
        max_results (int): Maximum number of tweets to retrieve (default: 10, max: 100)
        
    Returns:
        dict: Response containing search results
    """
    try:
        # Get Twitter client
        client = _get_twitter_client_v2()
        
        # Search tweets
        tweets = client.search_recent_tweets(
            query=query,
            max_results=min(max_results, 100),
            tweet_fields=['created_at', 'public_metrics', 'author_id']
        )
        
        tweet_list = []
        if tweets.data:
            for tweet in tweets.data:
                tweet_list.append({
                    "id": tweet.id,
                    "text": tweet.text,
                    "created_at": tweet.created_at.isoformat() if tweet.created_at else None,
                    "author_id": tweet.author_id,
                    "public_metrics": tweet.public_metrics._json if hasattr(tweet, 'public_metrics') else None
                })
        
        return {
            "success": True,
            "query": query,
            "tweets": tweet_list,
            "tweet_count": len(tweet_list),
            "message": f"Found {len(tweet_list)} tweets for query: {query}"
        }
        
    except tweepy.TooManyRequests:
        return {"error": "Rate limit exceeded. Please wait before searching again."}
    except tweepy.Unauthorized:
        return {"error": "Unauthorized. Please check your Twitter API credentials."}
    except tweepy.TweepyException as e:
        return {"error": f"Twitter API error: {str(e)}"}
    except Exception as e:
        return {"error": f"Failed to search tweets: {str(e)}"}


async def search_tweets_async(query: str, max_results: int = 10) -> Dict:
    """Search tweets using tweepy (asynchronous)
    
    Args:
        query (str): Search query
        max_results (int): Maximum number of tweets to retrieve (default: 10, max: 100)
        
    Returns:
        dict: Response containing search results
    """
    pass


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


def get_twitter_search_tool() -> Tool:
    """Return Twitter search tool"""
    return Tool.from_function(
        name="twitter_search",
        func=search_tweets_sync,
        coroutine=search_tweets_async,
        description="Search recent tweets using tweepy. Use query parameter for the search term and optionally max_results (default: 10, max: 100).",
    )


if __name__ == "__main__":
    # Test
    tool = get_twitter_post_tool()
    print(tool.invoke("Hello from TRAS! Travel Planning Assistant! 🌏✈️"))
    
    # Test user tweets
    user_tool = get_twitter_user_tweets_tool()
    print(user_tool.invoke("elonmusk"))
    
    # Test search
    search_tool = get_twitter_search_tool()
    print(search_tool.invoke("travel planning"))
