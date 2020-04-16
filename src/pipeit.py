import pipeit_core
import json
import pickle
import inspect
from typing import Any, Callable, Dict, List, Tuple, NewType, IO, Optional


Data = NewType('Data', Any)
Args = Dict[str, Any]

def _get_caller_path() -> str:
    return inspect.getmodule(inspect.stack()[2][0]).__file__


def pipeit_with_data(args:Args, proc:Callable[[Data], Data], **options):
    return pipeit_core._pipeit_with_io(
        _get_caller_path(),
        args,
        lambda infile, outfile: _proc_with_pickle(proc, infile, outfile),
        **options
    )


def _proc_with_pickle(proc:Callable[[Data], Data], infile:Optional[IO], outfile:Optional[IO]) -> None:
    indata = pickle.load(infile) if infile else None
    outdata = proc(indata)
    if outfile: pickle.dump(outdata, outfile)



def pipeit_with_json(args:Args, proc:Callable[[Data], Data], **options):
    return pipeit_core._pipeit_with_io(
        _get_caller_path(),
        args,
        lambda infile, outfile: _proc_with_json(proc, infile, outfile),
        in_is_binary=False,
        out_is_binary=False,
        **options
    )


def _proc_with_json(proc:Callable[[Data], Data], infile:Optional[IO], outfile:Optional[IO]) -> None:
    indata = json.load(infile) if infile else None
    outdata = proc(indata)
    if outfile: json.dump(outdata, outfile)



def pipeit_with_io(args:Args, proc:Callable[[Optional[IO]], IO], **options):
    return pipeit_core._pipeit_with_io(
        _get_caller_path(),
        args,
        proc,
        **options
    )

