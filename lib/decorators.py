#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Decorator functions

Created by: Rui Carmo
"""

from bottle import request, response, route, abort
import time, binascii, hashlib, email.utils, functools
import logging

try:
    import json
except ImportError:
    import simplejson as json

log = logging.getLogger()

gmt_format_string = "%a, %d %b %Y %H:%M:%S GMT"


def redis_cache(redis, prefix='url', ttl=3600):
    """Cache route results in Redis"""

    def decorator(callback):
        @functools.wraps(callback)
        def wrapper(*args, **kwargs):
            try:
                item = json.loads(redis.get('url:%s' % request.urlparts.path))
                body = item['body']
                for h in item['headers']:
                    response.set_header(h, item['headers'][h])
                response.set_header('X-Source', 'Redis')
            except:
                body = callback(*args, **kwargs)
                item = {
                    'body': body,
                    'headers': dict(response.headers),
                    'mtime': int(time.time())
                }
                k = '%s:%s' % (prefix, request.urlparts.path)
                redis.set(k, json.dumps(item))
                redis.expire(k, ttl)
            return body
        return wrapper
    return decorator


def cache_results(timeout):
    """Cache route results for a given period of time"""

    def decorator(callback):
        _cache = {}
        _times = {}

        @functools.wraps(callback)
        def wrapper(*args, **kwargs):

            def expire(when):
                for t in [k for k in _times.keys()]:
                    if (when - t) > timeout:
                        del(_cache[_times[t]])
                        del(_times[t])

            now = time.time()
            try:
                item = _cache[request.urlparts]
                if 'If-Modified-Since'  in request.headers:
                    try:
                        since = time.mktime(email.utils.parsedate(request.headers['If-Modified-Since']))
                    except:
                        since = now
                    if item['mtime'] >= since:
                        expire(now)
                        abort(304,'Not modified')
                for h in item['headers']:
                    response.set_header(h, item['headers'][h])
                body = item['body']
            except KeyError:
                body = callback(*args, **kwargs)
                item = {
                    'body': body,
                    'headers': response.headers,
                    'mtime': int(now)
                }
                _cache[request.urlparts] = item
                _times[now] = request.urlparts

            expire(now)
            return body
        return wrapper
    return decorator


def cache_control(seconds = 0):
    """Insert HTTP caching headers"""

    def decorator(callback):
        @functools.wraps(callback)
        def wrapper(*args, **kwargs):
            expires = int(time.time() + seconds)
            expires = time.strftime(gmt_format_string, time.gmtime(expires))
            response.set_header('Expires', expires)
            if seconds:
                pragma = 'public'
            else:
                pragma = 'no-cache, must-revalidate'
            response.set_header('Cache-Control', "%s, max-age=%s" % (pragma, seconds))
            response.set_header('Pragma', pragma)
            return callback(*args, **kwargs)
        return wrapper
    return decorator


def timed(callback):
    """Decorator for timing route processing"""

    @functools.wraps(callback)
    def wrapper(*args, **kwargs):
        start = time.time()
        body = callback(*args, **kwargs)
        end = time.time()
        response.headers['X-Processing-Time'] = str(end - start)
        return body
    return wrapper


def jsonp(callback):
    """Decorator for JSONP handling"""

    @functools.wraps(callback)
    def wrapper(*args, **kwargs):
        body = callback(*args, **kwargs)
        try:
            body = json.dumps(body)
            # Set content type only if serialization succesful
            response.content_type = 'application/json'
        except Exception, e:
            return body

        callback_function = request.query.get('callback')
        if callback_function:
            body = ''.join([callback_function, '(', body, ')'])
            response.content_type = 'text/javascript'

        response.set_header('Last-Modified', time.strftime(gmt_format_string, time.gmtime()))
        response.set_header('ETag', binascii.b2a_base64(hashlib.sha1(body).digest()).strip())
        response.set_header('Content-Length', len(body))
        return body
    return wrapper


def memoize(f):
    """Memoization decorator for functions taking one or more arguments"""

    class memodict(dict):
        def __init__(self, f):
            self.f = f

        def __call__(self, *args):
            return self[args]

        def __missing__(self, key):
            ret = self[key] = self.f(*key)
            return ret
    return memodict(f)


def check(**types):
    """Decorator for parameter checking: @check(a = int, b = bool, c = string.upper)"""

    def decorator(callback):
        farg, _, _, def_params = inspect.getargspec(callback)
        if def_params is None: def_params = []
        farg = farg[:len(farg) - len(def_params)]

        param_info = [(par, ptype, par in farg) for par, ptype in types.iteritems()]

        @functools.wraps(f)
        def wrapper(*args, **kargs):
            getparam = request.GET.get
            for par, ptype, required in param_info:
                value = getparam(par)
                if not value: # None or empty str
                    if required:
                        error = "%s() requires the parameter %s" % (wrapper.__name__, par)
                        raise TypeError(error)
                    continue
                try:
                    kargs[par] = ptype(value)
                except:
                    error = "Cannot convert parameter %s to %s" % (par, ptype.__name__)
                    raise ValueError(error)

            return callback(*args, **kargs)
        return wrapper
    return decorator
