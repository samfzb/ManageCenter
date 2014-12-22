# -*- encoding: utf-8 -*-

__author__ = 'shuhao.wang'

import threading

from Desire.BaseFramework.Resource.CacheManager import ResCacheManager
from Desire.ManageCenter.ModelResources.Resource import store

_RES_CACHE = None
_RES_CACHE_MUTEX = threading.Lock()

def get_res_cache():
    global _RES_CACHE, _RES_CACHE_MUTEX

    _RES_CACHE_MUTEX.aquire()
    if _RES_CACHE is None:
        _RES_CACHE = ResCacheManager(store.load_resource_by_id, store.store_resource)
    _RES_CACHE_MUTEX.release()

    return _RES_CACHE
