import os
import sys
import pickle
import json
import toml
import hashlib
import base64
import inspect
from typing import Any, Callable, Dict, List, Tuple, NewType, IO, Optional


Data = NewType('Data', Any)
Args = Dict[str, Any]


# Load config file
CFG_PATH = '.pipeit.cfg'
cfg:dict = toml.load(open(CFG_PATH, mode='r')) if os.path.exists(CFG_PATH) else {}

CACHE_RELDIR = cfg.get('cache_dir') or '.pipeit_cache'
CACHE_BINARY_EXT = cfg.get('cache_ext') or '.ppib'
CACHE_META_EXT = cfg.get('cache_metafile_ext') or '.ppibmeta.json'

def HASH_FUNC(v) -> str:
    return base64.urlsafe_b64encode(hashlib.sha224(v).digest()).decode()


def _get_caller_path() -> str:
    return inspect.getmodule(inspect.stack()[2][0]).__file__


def pipeit_with_data(args:Args, proc:Callable[[Data], Data], **options):
    return _pipeit_with_io(_get_caller_path(), args, lambda infile, outfile: _proc_with_pickle(proc, infile, outfile), **options)


def _proc_with_pickle(proc:Callable[[Data], Data], infile:Optional[IO], outfile:IO) -> None:
    indata = pickle.load(infile) if infile else None
    outdata = proc(indata)
    pickle.dump(outdata, outfile)



def pipeit_with_json(args:Args, proc:Callable[[Data], Data], **options):
    return _pipeit_with_io(_get_caller_path(), args, lambda infile, outfile: _proc_with_json(proc, infile, outfile), in_is_binary=False, out_is_binary=False, **options)


def _proc_with_json(proc:Callable[[Data], Data], infile:Optional[IO], outfile:IO) -> None:
    indata = json.load(infile) if infile else None
    outdata = proc(indata)
    json.dump(outdata, outfile)



def pipeit_with_io(args:Args, proc:Callable[[Optional[IO]], IO]):
    return _pipeit_with_io(_get_caller_path(), args, proc)



def _pipeit_with_io(
    program_path:str,
    args:Args,
    proc:Callable[[Optional[IO]], IO],
    **options
):
    return _pipeit_with_iopath(program_path, args, lambda in_path, out_path: _proc_with_io(proc, in_path, out_path, **options), **options)


def _proc_with_io(
    proc:Callable[[Optional[IO]], IO],
    in_path:Optional[str],
    out_path:Optional[str],
    *,
    in_is_binary:bool=True,
    out_is_binary:bool=True,
    **options
):
    with open(out_path, mode=('wb' if out_is_binary else 'w')) as out_file:
        if in_path is None:
            proc(None, out_file)
        else:
            with open(in_path, mode=('rb' if in_is_binary else 'r')) as in_file:
                proc(in_file, out_file)



def _pipeit_with_iopath(
    program_path:str,
    args:Args,
    proc:Callable[[Optional[str]], str],
    *,
    disable_cache:bool=False,
    no_output:bool=False,
    **options
):

    command_line = ' '.join(sys.argv)
    print_log = lambda *args: print(*args, file=sys.stderr)

    program_path = os.path.abspath(program_path)
    program_name = os.path.basename(program_path)

    args = (args if isinstance(args, dict) else vars(args)) if args else {}
    args = dict(sorted(args.items(), key=lambda x: x[0]))


    cache_dir = os.path.abspath(os.path.join(os.path.dirname(program_path), CACHE_RELDIR))

    in_meta:Optional[dict] = None
    in_binary_path:Optional[str] = None

    if not sys.stdin.isatty():
        # in_meta's key: binaries:(path, hash), parameters:(program, input, arguments)
        
        in_meta:Optional[dict] = json.load(sys.stdin)

        if not 'binary' in in_meta or not 'path' in in_meta['binary']:
            raise RuntimeError('Missing path in input metafile.')

        in_binary_path = os.path.join(cache_dir, in_meta['binary']['path'])


    if no_output:
        proc(in_binary_path, None)
        return


    # make parameters in result data
    result_parameters = {
        'program'  : program_name,
        'input'    : in_meta,
        'arguments': args,
    }
    result_hash = HASH_FUNC(json.dumps(result_parameters).encode())

    cache_relpath_noext = os.path.join(program_name, result_hash)
    cache_path_noext = os.path.abspath(os.path.join(cache_dir, cache_relpath_noext))
    cache_binary_path = cache_path_noext + CACHE_BINARY_EXT
    cache_binary_relpath = cache_relpath_noext + CACHE_BINARY_EXT
    cache_meta_path = cache_path_noext + CACHE_META_EXT

    # make cache (data file) if not exists
    if disable_cache or (not os.path.exists(cache_binary_path) or not os.path.exists(cache_meta_path)):
        print_log('Generating...',)

        os.makedirs(os.path.dirname(cache_path_noext), exist_ok=True)

        # process data with input file (if exists) and output file
        proc(in_binary_path, cache_binary_path)

        # generate metafile
        json.dump(
            {
                'binary': {
                    'path': cache_binary_relpath,
                    'hash': HASH_FUNC(open(cache_binary_path, mode='rb').read()),
                },
                'parameters': result_parameters
            },
            open(cache_meta_path, mode='w'),
            ensure_ascii=False, indent=4, separators=(',', ': ')
        )

    else:
        print_log('Using cache')


    if not sys.stdout.isatty():
        print(open(cache_meta_path, mode='r').read())
    
