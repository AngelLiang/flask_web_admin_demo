# coding=utf-8

from . import cache


class ModelCacheMixin(object):
    """Model缓存模型"""

    _cache = cache

    def add_cache(self, prefix: str):
        key = "{}:{}".format(prefix, self.id)
        # print(key)
        self._cache.set(key, self)

    @classmethod
    def has_cache(cls, prefix: str, id):
        key = "{}:{}".format(prefix, id)
        # print(key)
        return cls._cache.has(key)

    @classmethod
    def get_cache_by_id(cls, prefix: str, id):
        key = "{}:{}".format(prefix, id)
        model = cls._cache.get(key)
        return model

    def del_cache(self, prefix: str):
        key = "{}:{}".format(prefix, self.id)
        self._cache.delete(key)
