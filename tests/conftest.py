"""Shared test setup.

Two portability shims, so the suite runs from a plain checkout on any platform:

* put ``src`` on the import path when the package is not installed;
* provide a stand-in for the Unix-only ``resource`` module on Windows. Several
  experiment runners import it to record peak memory. Their bytes are part of
  recorded results (see scripts/check_result_integrity.py), so they are not
  edited; the stand-in reports zero.
"""
import pathlib
import sys
import types

_SRC = pathlib.Path(__file__).resolve().parent.parent / "src"
if str(_SRC) not in sys.path:
    sys.path.insert(0, str(_SRC))

try:
    import resource  # noqa: F401
except ModuleNotFoundError:
    _shim = types.ModuleType("resource")
    _shim.RUSAGE_SELF = 0
    _shim.RUSAGE_CHILDREN = -1

    class _Usage:
        ru_maxrss = 0
        ru_utime = 0.0
        ru_stime = 0.0

    _shim.getrusage = lambda _who: _Usage()
    sys.modules["resource"] = _shim
