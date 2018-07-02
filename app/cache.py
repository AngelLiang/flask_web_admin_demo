# coding=utf-8

__all__ = ("redis", "cache")

import redis
from redis import Redis
from redis import exceptions as redis_exceptions
from werkzeug.contrib.cache import SimpleCache, RedisCache


class CustomCache(object):
    """客制化RedisCache"""

    def __init__(self):
        self.cache = RedisCache()
        try:
            self.ping()
            print("cache is RedisCache")
        except redis_exceptions.ConnectionError:
            del cache
            self.cache = SimpleCache()
            print("cache is SimpleCache")

    def init_app(self, app):
        pass

        return self.cache

    def ping(self):
        if isinstance(self.cache, RedisCache):
            try:
                return self.cache._client.ping()
            except redis.exceptions.ConnectionError:
                return False
        return True


cache = CustomCache()

# redis = Redis()
# try:
#     redis.ping()
# except redis_exceptions.ConnectionError:
#     print("redis is not running!")
#     redis = None


##########################################################################
#
# docs: http://www.pythondoc.com/flask-cache/index.html


# from flask_cache import Cache


class CacheConfig(object):

    # null: NullCache (default)
    # simple: SimpleCache
    # memcached: MemcachedCache (pylibmc or memcache required)
    # gaememcached: GAEMemcachedCache
    # redis: RedisCache (Werkzeug 0.7 required)
    # filesystem: FileSystemCache
    # saslmemcached: SASLMemcachedCache (pylibmc required)
    CACHE_TYPE = "simple"

# cache = Cache()
