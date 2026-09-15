#!/usr/bin/env python3
"""Path-only launcher for the frozen, independently executed replay source."""
import argparse
from pathlib import Path
import sys
import replay_relations as replay

parser=argparse.ArgumentParser(description=__doc__)
parser.add_argument('--archive',type=Path,required=True)
parser.add_argument('--manifest',type=Path,required=True)
parser.add_argument('--full',type=Path,required=True)
parser.add_argument('--prior',type=Path,required=True)
parser.add_argument('--output',type=Path,required=True)
parser.add_argument('--controls-only',action='store_true')
args=parser.parse_args()
replay.ARCHIVE=args.archive
replay.MANIFEST=args.manifest
replay.FULL=args.full
replay.PRIOR=args.prior
replay.OUT=args.output
sys.argv=[str(Path(replay.__file__))]+(['--controls-only'] if args.controls_only else [])
replay.main()
