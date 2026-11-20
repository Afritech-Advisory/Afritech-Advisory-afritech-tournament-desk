"""Writes src/i18n/fr.json, sw.json and pt.json from dict_a.py and dict_b.py (the editable source)."""
import json, pathlib, sys
here = pathlib.Path(__file__).parent
sys.path.insert(0, str(here))
from dict_a import E as A
from dict_b import E as B, JS
import re
# One word list per language, so a country or football term reads the same everywhere on the page.
SW_WORDS = {"Croatia": "Kroatia", "Cuba": "Kuba", "Ecuador": "Ekwado", "Mexico": "Meksiko", "New Caledonia": "Kaledonia Mpya",
            "Denmark": "Denmaki", "Costa Rica": "Kosta Rika", "Venezuela": "Venezuela",
            "mwamba wa karibu": "nguzo ya karibu ya goli", "muda wa nyongeza": "dakika za majeruhi",
            "Dunia nzima": "Nje ya Afrika", "Kadi za uskauti": "Ripoti fupi za ufuatiliaji"}
PT_WORDS = {"à fase de 32": "à fase eliminatória com 32 seleções", "na fase de 32": "na fase eliminatória com 32 seleções",
            "Fase de 32": "Fase eliminatória com 32 seleções", "fase de 32": "fase eliminatória com 32 seleções", "CAN Sub-17": "Copa Africana de Nações Sub-17", "Fichas de scouting": "Relatórios de observação"}
FR_WORDS = {"Fiches de scouting": "Fiches d'observation", "fiches de scouting": "fiches d'observation", "contre Danemark": "contre le Danemark"}
FIXW = {"sw": SW_WORDS, "pt": PT_WORDS, "fr": FR_WORDS}

def words(code, v):
    for a, b in FIXW[code].items():
        v = re.sub(r"(?<![\w-])" + re.escape(a) + r"(?![\w-])", b, v)
    return v

for i, code in enumerate(["fr", "sw", "pt"], start=1):
    d = {e[0]: words(code, e[i]) for e in A + B}
    d["__js__"] = {e[0]: e[i] for e in JS}
    (here / f"{code}.json").write_text(json.dumps(d, ensure_ascii=False, indent=1, sort_keys=True))
    print(code, len(d) - 1)
