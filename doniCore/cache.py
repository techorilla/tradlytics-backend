import json
import redis

from django.conf import settings
from django.db.models.base import ModelBase as mb


from copy import deepcopy


DEFAULT_SHARD = "REDIS-LOCAL"
MIQ_REDIS = {
    'REDIS-LOCAL': {
        'IP': '127.0.0.1',
        'PORT': '6379',
        'NAME': 'cash-one',
    },
}

for key in MIQ_REDIS:
    MIQ_REDIS[key]['POOL'] = redis.ConnectionPool(
        host=MIQ_REDIS[key]['IP'],
        port=MIQ_REDIS[key]['PORT'],
        db=0)


DEFAULT_TIMEOUT = None

class MIQRedis(object):
    """
    Interface for the MIQ redis cluster.

    Along with reading functionality, it provides methods to access certain
    json
    objects.

    """

    #TODO: Moving forward as write functionality also comes in more
    # interaction happens,
    # methods for accessing and understanding certain objects should be
    # moved out of this class.

    def __init__(self):
        self.redis = redis.Redis(connection_pool=MIQ_REDIS[DEFAULT_SHARD]['POOL'])

    #------Read/Write---------#
    def get(self, key, subs=None):
        re = self.redis.get(key)
        if (re):
            re = self.load_json(re)
        elif (re is None):
            re = subs
        return re


    def ltrim(self,key,start,stop):
        resp = self.redis.ltrim(key,start,stop)
        return resp

    def set_many(self,dict,timeout=DEFAULT_TIMEOUT):

        pipe = self.redis.pipeline()
        for key,value in dict.items():
            this_value = self.dump_json(value)
            pipe.set(key,this_value)
            if timeout: pipe.expire(key,timeout)
        result = pipe.execute()

    def get_many(self,keys):

        # pipe = self.redis.pipeline()

        # result = []
        # for item in key:
        #     pipe.get(item)

        # result = pipe.execute()

        # this_dict = {}
        # for i,item in enumerate(keys):
        #     this_dict[item] = self.load_json(result[i])

        this_dict = {}
        for key in keys:
            this_dict[key] = self.load_json(self.get(key))

        return this_dict

    def set(self, key, obj, timeout=DEFAULT_TIMEOUT):
        val = self.dump_json(deepcopy(obj))
        if val:
            self.redis.set(key,val)
            if timeout is not None:
                self.redis.expire(key,timeout)

    def set_add(self,key,value):
        return self.redis.sadd(key,value)

    def set_random_remove(self,key):
        return self.redis.spop(key)

    def set_members(self,key):
        val = self.redis.smembers(key)
        return val

    def exists(self,key):
        return self.redis.exists(key)

    @staticmethod
    def dump_json(val):
        try:
            return json.dumps(val)
        except Exception,e:
            return val

    @staticmethod
    def load_json(val):
        try:
            return json.loads(val)
        except Exception:
            return val

    #------Object methods---------#
    def get_securities(self, detailed=False):
        if detailed:
            return self.get(KEYS['security_list_full'])
        return self.get(KEYS['security_list'])

    def get_fields(self):
        return self.get(KEYS['field_list'])

    def get_list(self,key,start=0,end=-1):
        resp = self.redis.lrange(key,start,end)
        for i in range(len(resp)):
            resp[i] = self.load_json(resp[i])
        return resp

    def push_to_multiple_lists(self,dic,timeout=None,
        debug=False,append=False,limit_list=None):

        dic = deepcopy(dic)
        keys = dic.keys()

        for key in keys:
            for i in range(len(dic[key])):
                dic[key][i] = self.dump_json(dic[key][i])

        pipe = self.redis.pipeline()

        if append:
            func = 'rpush'
        else:
            func = 'lpush'

        for key in keys:

            getattr(pipe,func)(key,*dic[key])
            if(limit_list):
                pipe.ltrim(key,-1*limit_list,-1)
            if(timeout):
                pipe.expire(key,timeout)

        resp = pipe.execute()

        return resp

    def incr(self,key,timeout=None,debug=False,value=None):
        pipe = self.redis.pipeline()
        if(value):
            pipe.incr(key,value)
        else:
            pipe.incr(key)
        if(timeout): pipe.expire(key,timeout)
        re = pipe.execute()
        return re


    def keys(self,*args,**kwargs):
        return self.redis.keys(
            *args,**kwargs)

    def delete(self,key):
        return self.redis.delete(key)

    def clear_cache(self,*args,**kwargs):
        sure = input('Are you sure you want to clear?? (y/n)')
        if sure.lower() == 'y':
            keys = self.keys("*")
            for i,key in enumerate(keys):
                cache.delete(key)

cache = MIQRedis()

def create_redis_key(key, *args, **kwargs):
    for param in args[1:]:
        if type(param) is list:
            list_keys = [str(elem) for elem in param]
            list_keys.sort()
            key += list_keys
        elif type(param) is mb:

            key.append(param.__name__)
        else:
            key.append(str(param))

    for dict_key, param in kwargs.iteritems():
        if type(param) is list:
            list_keys = [str(elem) for elem in param]
            list_keys.sort()
            key += [dict_key]
            key += list_keys
        elif type(param) is mb:
            key.append(str(dict_key))
            key.append(param.__name__)
        else:
            key.append(str(dict_key))
            key.append(str(param))

    redis_key = '_'.join(key)

    print ("Key Created: %s")%(redis_key)
    return redis_key


def cache_results(func):
    def inner(*args, **kwargs):
        try:
            refresh=kwargs.pop('refresh')
        except KeyError:
            refresh = False

        key = [args[0].__name__, func.func_name] if type(args[0]) is type else [func.func_name]
        redis_key = create_redis_key(key, *args, **kwargs)
        if not refresh:
            try:
                print 'finding cached result'
                cached_results = cache.get(redis_key)
            except redis.ConnectionError:
                print 'print connection error'
                return func(*args, **kwargs)
        else:
            cached_results = None

        if cached_results:
            return cached_results
        else:
            result = func(*args, **kwargs)
            print 'Creating Cache'
            cache.set(redis_key, result)
            return result
    return inner
