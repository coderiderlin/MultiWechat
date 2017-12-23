# -*- coding: utf-8 -*-
import json
import threading
from utils import *

SingletonLock = threading.Lock()


class Singleton(object):
    # 定义静态变量实例
    __instance = None

    def __init__(self):
        pass

    def __new__(cls, *args, **kwargs):
        if not cls.__instance:
            try:
                SingletonLock.acquire()
                # double check
                if not cls.__instance:
                    cls.__instance = super(Singleton, cls).__new__(cls, *args, **kwargs)
            finally:
                SingletonLock.release()
        return cls.__instance


class ProxyManager(Singleton):
    __first_init = True

    def __init__(self):
        if self.__first_init:
            self.__first_init = False
            self.proxyLock = threading.Lock()
            self.proxies = []
            self.proxy_pool_url = "http://127.0.0.1:8000"
            self.refresh()
            logl("init..")
            self.count = 0

    def refresh(self):
        response = GetUrlContent2(self.proxy_pool_url)
        self.proxies = json.loads(response)

    def pop(self):
        proxy = None
        try:
            self.proxyLock.acquire()
            if len(self.proxies) < 1:
                self.refresh()
            proxy = self.proxies.pop(0)
            self.proxies.append(proxy)
            # self.count += 1
            # logl(self.count)

        finally:
            self.proxyLock.release()
        return proxy

    def popProxies(self):
        proxy = self.pop()
        proxies = {"http": "http://%s:%s" % (proxy[0], proxy[1]), "https": "http://%s:%s" % (proxy[0], proxy[1]), }
        return proxies


man = ProxyManager()


def test_singleton_in_thread():
    # logl(id(man))
    tp = man.popProxies()
    logl(str(tp))
    try:
        response = GetUrlContent2("http://pv.sohu.com/cityjson", proxies=tp)
    except BaseException as e:
        logl(e.message)
        response = str(e.message)
    logl("proxies:%s result:%s" % (str(tp), response))


if __name__ == "__main__":
    man = ProxyManager()
    threadList = []
    for i in range(100):
        t = threading.Thread(target=test_singleton_in_thread, args=[])
        t.setDaemon(True)
        t.start()
        threadList.append(t)
    for th in threadList:
        th.join()
    logl("all threads end.")
