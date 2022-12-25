import os.path as osp
import os
import math
import hashlib
import sys
from typing import Callable, TextIO, Any, TypeVar, Generic

class HashFilenameMapper(): 
    def __init__(self,  parent_dir: str, n_bins: int = 128, debug=False) -> None: 
        self.debug = debug
        mod_depth = math.log2(n_bins)
        assert int(mod_depth) == mod_depth, f'n_bins must be a power of 2'
        self.mod_depth = mod_depth
        self.mod_depth_hex = int(math.ceil(mod_depth / 4))
        self.n_bins = n_bins

        self.parent_dir = parent_dir
        self.prepare_parent_dir()
    
    def prepare_parent_dir(self, ) -> None: 
        if not self.debug: 
            for i in range(self.n_bins): 
                os.makedirs(f'i', exist_ok=True)

    def __call__(self, p: str) -> str: 
        parent = osp.dirname(p)
        assert parent == self.parent_dit
        filename = osp.basename(p)

        m = int(hashlib.md5().update(filename).hexdigest()[-self.mod_depth_hex:], base=16)
        target = m % self.mod_depth
        return osp.join(parent, target, filename)


T = TypeVar('T')
class DeferedReadError(Generic[T]): 
    '''defers a `FileNotFound` error till the loaded content is actually being read, instead of on initialization.'''
    def __init__(self, filename: str, loader: Callable[[TextIO], T]) -> None: 
        self._loaded = None
        self.filename = filename
        try: 
            with open(filename) as f: 
                self._loaded = loader(f)
        except FileNotFoundError: 
            print(f'warn: file [{filename}] cannot be loaded but carry on.', file=sys.stderr)
    
    @property
    def loaded(self, ) -> T: 
        if self._loaded is not None: 
            return self._loaded
        else: 
            raise FileNotFoundError(f'error: file [{self.filename}] not found, but was acutally read!')
