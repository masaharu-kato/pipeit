import sys
import pickle
import hashlib
from typing import Any, Callable, Dict, List, Tuple, Generic


Data = Generic('Data')
Args = Dict[str, Any]

def pipeit(
    args:Args,
    proc:Callable[[Data], Data]
):
    # TODO: Full Implementation
    
    args_str = ';'.join(k + '=' + v for k, v in args.items())

    input_path = (input() if not sys.stdin.isatty() else '').strip()
    input_hash = hashlib.sha256(open(input_path, mode='rb').read()).hexdigest()
    
    # LOAD DATA #

    # Process and make cache if not exists
    # outdata = proc(indata)
    
