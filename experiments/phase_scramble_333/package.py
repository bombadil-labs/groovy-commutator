"""Bind frozen #333 replay outputs to their source files without changing scores."""
import argparse
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
HERE = "experiments/phase_scramble_333/"
P = "docs/research/protocols/2026-11-21-phase-scramble-333"
SOURCES = {
    "oscillator": (HERE+"run.py", P+".md"),
    "transfer": (HERE+"transfer.py", P+"-transfer.md", "src/groovy/nonuniform.py", "src/groovy/ca.py"),
}

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("oscillator",type=Path)
    ap.add_argument("transfer",type=Path)
    args = ap.parse_args()
    out = {}
    hashes = {}
    for name, sources in SOURCES.items():
        data = json.loads(getattr(args, name).read_text())
        assert hashlib.sha256((ROOT / sources[0]).read_bytes()).hexdigest() == data["runner_sha256"]
        out[name] = data
        for path in sources:
            hashes[path] = hashlib.sha256((ROOT/path).read_bytes()).hexdigest()
    out["source_hashes"] = hashes
    print(json.dumps(out,ensure_ascii=True,indent=2,sort_keys=True,allow_nan=False))

if __name__ == "__main__":
    main()
