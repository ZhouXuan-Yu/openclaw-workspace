#!/usr/bin/env python3
"""Helper to persist collected data via pipeline functions without stdin encoding issues."""
import importlib.util
import sys
from pathlib import Path

here = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("pipeline", here / "pipeline.py")
p = importlib.util.module_from_spec(spec)
spec.loader.exec_module(p)

which = sys.argv[1]
data = Path(sys.argv[2]).read_text(encoding="utf-8")

if which == "websearch":
    print(p.save_websearch(data))
elif which == "social":
    print(p.save_social(data))
elif which == "younavi":
    print(p.save_younavi(data))
else:
    print("unknown:", which)
    sys.exit(1)
