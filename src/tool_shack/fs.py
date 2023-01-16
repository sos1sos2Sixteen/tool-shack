import os.path as osp
import os
import math
import hashlib
import sys
from typing import Callable, TextIO, Any, TypeVar, Generic, Union

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
    '''defers a `FileNotFound` error till the loaded content is actually being read, instead of on initialization.
    
    parameters: 
    * `filename`: path to the file to be read. will be passed to `loader`.
    * `loader`: maps an open file handler or a path string to the loaded data structure.
        if a `FileNotFoundError` is raised within this call, this instance enters a deferred read error state,
        where any actual attempts to read the loaded data will result in a `FileNotFoundError` to be raised
        at the time of reading.
    * do_open: determines the type of the loader. if set (default), loader: (TextIO) -> T, 
        if not set, loader: (str) -> T.

    usage: 
    ```

    # initialization (continues if file does not exist)
    data_wrapped = DeferedReadError(
        'path/to/file', 
        lambda f: {maps a TextIO handle to a memory data structure}
    )

    # read (access through wrapped.loaded), crashes if io had failed on initialization.
    data_line = data_wrapped.loaded.attribute...
    ```
    
    '''
    def __init__(self, filename: str, loader: Callable[[Union[TextIO, str]], T], do_open: bool = True) -> None: 
        self._loaded = None
        self.filename = filename
        try: 
            if do_open: 
                with open(filename) as f: 
                    self._loaded = loader(f)
            else: 
                self._loaded = loader(filename)
        except FileNotFoundError: 
            print(f'warn: file [{filename}] cannot be loaded but carry on.', file=sys.stderr)
    
    @property
    def loaded(self, ) -> T: 
        if self._loaded is not None: 
            return self._loaded
        else: 
            raise FileNotFoundError(f'error: file [{self.filename}] not found, but was acutally read!')
