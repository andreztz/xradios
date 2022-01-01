from xmlrpc.client import ServerProxy


class Proxy:
    def __init__(self, url):
        self._xmlrpc_server_proxy = ServerProxy(url)
    def __getattr__(self, name):
        call_proxy = getattr(self._xmlrpc_server_proxy, name)
        def _call(*args, **kwargs):
            return call_proxy(args, kwargs)
        return _call


proxy = Proxy('http://localhost:10000')
