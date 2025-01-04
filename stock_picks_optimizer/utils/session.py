from requests import Session
from requests_cache import CacheMixin
from requests_cache.backends.sqlite import SQLiteCache
from requests_ratelimiter import LimiterMixin, MemoryQueueBucket
from pyrate_limiter import Duration, RequestRate, Limiter


class CachedLimiterSession(CacheMixin, LimiterMixin, Session):
    pass


class CachedLimiterSessionBuilder:
    def __init__(self) -> None:
        self.__cache_path = ""
        self.__user_agent_header = ""

    def cache_path(self, path: str) -> "CachedLimiterSessionBuilder":
        self.__cache_path = path
        return self

    def user_agent_header(self, name: str) -> "CachedLimiterSessionBuilder":
        self.__user_agent_header = name
        return self

    def build(self) -> CachedLimiterSession:
        session = CachedLimiterSession(
            limiter=Limiter(RequestRate(2, Duration.SECOND * 5)),
            bucket_class=MemoryQueueBucket,
            backend=SQLiteCache(self.__cache_path),
        )
        session.headers["User-agent"] = self.__user_agent_header
        return session
