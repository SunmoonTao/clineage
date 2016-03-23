
def _iterate_nested_items(nested_dict):
    if isinstance(nested_dict, dict):
        for k, inner_d in nested_dict.iteritems():
            for inner_k, v in _iterate_nested_items(inner_d):
                yield ((k,) + inner_k), v
    else:
        yield tuple(), nested_dict


def _deinterlace(interlaced):
    d = {}
    for frame in interlaced:
        for k, v in frame.iteritems():
            d.setdefault(k,[]).append(v)
    return d


def _update_deinterlaced_dict(d, e):
    for k, v in e.iteritems():
        a = d.setdefault(k,[])
        a += v


def FlatDict(nested_dict, deinterlaced_keys=None):
    fd = _FlatDict(nested_dict, deinterlaced_keys)
    return fd.sub(())


class _FlatDict(object):

    def __init__(self, nested_dict, deinterlaced_keys=None):
        self._d = {}
        self._keys_tree = {}
        if deinterlaced_keys is not None:
            self._deinterlaced_keys = deinterlaced_keys
            self._has_default = True
        else:
            self._deinterlaced_keys = []
            self._has_default = False
        for nk, nv in _iterate_nested_items(nested_dict):
            denv = _deinterlace(nv)
            for i in xrange(1,len(nk)+1):
                a = self._d.setdefault(nk[:i],
                    {k: [] for k in self._deinterlaced_keys})
                _update_deinterlaced_dict(a, denv)
            for i in xrange(0,len(nk)):
                a = self._keys_tree.setdefault(nk[:i],set())
                a.add(nk[i])
            self._keys_tree[nk] = set()

    def keys(self, nk=()):
        return iter(self._keys_tree[nk])

    def items(self, nk=()):
        for k in self.keys(nk):
            yield k, _SubFlatDict(self, nk + (k,))

    def reads(self, nk=()):
        for k in self.keys(nk):
            yield k, self[nk + (k,)]

    def __getitem__(self, nk=()):
        if self._has_default:
            return self._d.get(nk, {k: [] for k in self._deinterlaced_keys})
        else:
            return self._d[nk]

    def sub(self, nk=()):
        return _SubFlatDict(self, nk)


def _safe_tup(t):
    if not isinstance(t, tuple):
        return (t,)
    return t


def _submethod(method):
    def _method(self, nk=()):
        return getattr(self._fd, method)(self._prefix_keys + _safe_tup(nk))
    return _method


class _SubFlatDict(object):
    
    def __init__(self, fd, prefix_keys):
        if isinstance(fd, _FlatDict):
            self._fd = fd
            self._prefix_keys = _safe_tup(prefix_keys)
        elif isinstance(fd, _SubFlatDict):
            self._fd = fd._fd
            self._prefix_keys = fd._prefix_keys + _safe_tup(prefix_keys)
        else:
            raise TypeError()

    keys = _submethod("keys")
    items = _submethod("items")
    reads = _submethod("reads")
    __getitem__ = _submethod("__getitem__")
    sub = _submethod("sub")
