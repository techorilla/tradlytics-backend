
# def create_redis_key(key, *args, **kwargs):
#     for param in args[1:]:
#         if type(param) is list:
#             list_keys = [str(elem) for elem in param]
#             list_keys.sort()
#             key += list_keys
#         elif type(param) is mb:
#             key.append(param.__name__)
#         else:
#             key.append(str(param))
#
#     for dict_key, param in kwargs.iteritems():
#         if type(param) is list:
#             list_keys = [str(elem) for elem in param]
#             list_keys.sort()
#             key += [dict_key]
#             key += list_keys
#         elif type(param) is mb:
#             key.append(str(dict_key))
#             key.append(param.__name__)
#         else:
#             key.append(str(dict_key))
#             key.append(str(param))
#
#     redis_key = '_'.join(key)
#     print ("Key Created: %s")%(redis_key)
#     return redis_key

# def cache_results(func):
#     def inner(*args, **kwargs):
#         try:
#             refresh=kwargs.pop('refresh')
#         except KeyError:
#             refresh = False
#
#         key = [args[0].__name__, func.func_name] if type(args[0]) is type else [func.func_name]
#         redis_key = create_redis_key(key, *args, **kwargs)
#         if not refresh:
#             try:
#                 cached_results = cache.get(redis_key)
#             except redis.ConnectionError:
#                 return func(*args, **kwargs)
#         else:
#             cached_results = None
#
#         if cached_results:
#             return cached_results
#         else:
#             result = func(*args, **kwargs)
#             cache.set(redis_key, result)
#             return result
#
#     return inner