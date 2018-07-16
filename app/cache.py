# coding=utf-8

##########################################################################
# 建议使用 flask_caching
# docs: http://www.pythondoc.com/flask-cache/index.html
# from flask_cache import Cache

# docs: https://pythonhosted.org/Flask-Caching/

import os
from flask_caching import Cache


class CachingConfig(object):

    # null: NullCache (default)
    # simple: SimpleCache
    # memcached: MemcachedCache (pylibmc or memcache required)
    # gaememcached: GAEMemcachedCache
    # redis: RedisCache (Werkzeug 0.7 required)
    # filesystem: FileSystemCache
    # saslmemcached: SASLMemcachedCache (pylibmc required)
    CACHE_TYPE = "simple"


cache = Cache()

if os.getenv("REDIS_ENABLE"):
    pass
