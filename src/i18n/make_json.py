"""Writes src/i18n/fr.json, sw.json and pt.json from dict_a.py and dict_b.py (the editable source)."""
import json, pathlib, sys
here = pathlib.Path(__file__).parent
sys.path.insert(0, str(here))
from dict_a import E as A
from dict_b import E as B, JS
for i, code in enumerate(["fr", "sw", "pt"], start=1):
    d = {e[0]: e[i] for e in A + B}
    d["__js__"] = {e[0]: e[i] for e in JS}
    (here / f"{code}.json").write_text(json.dumps(d, ensure_ascii=False, indent=1, sort_keys=True))
    print(code, len(d) - 1)
