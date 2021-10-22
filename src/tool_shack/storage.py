import os
import hashlib

def translate(base_path: str, filename: str, create_hashdirs: bool = True) -> str: 
    '''
    translate logical path to hash-based system path, reducing 
    the number of files stored in `real` directories. this may 
    speed up disk seeking.

    input path should comply with `base_path/filename`. translated path: 
    `base_path/../filename`
    '''
    hashlib.sha1(filename.encode('utf-8')).digest()
