# coding=utf-8

__all__ = ("redis", "cache")


from redis import Redis
from redis import exceptions as redis_exceptions
from werkzeug.contrib.cache import SimpleCache, RedisCache


class CustomCache(object):
    """客制化RedisCache"""

    @classmethod
    def create_cache(cls):
        cache = RedisCache()
        try:
            cache._client.ping()
            print("cache is RedisCache")
        except redis_exceptions.ConnectionError:
            del cache
            cache = SimpleCache()
            print("cache is SimpleCache")

        return cache

    def ping(self):
        if isinstance(RedisCache, self.cache):
            try:
                return self._client.ping()
            except redis.exceptions.ConnectionError:
                return False


cache = CustomCache.create_cache()

redis = Redis()
try:
    redis.ping()
except redis_exceptions.ConnectionError:
    print("redis is not running!")
    redis = None
