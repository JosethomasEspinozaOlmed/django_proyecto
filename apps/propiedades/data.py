import json
from pathlib import Path

_BASE = Path(__file__).parent
_JSON_PATH = _BASE / "ciudades_paraguay.json"

try:
    with open(_JSON_PATH, "r", encoding="utf-8") as f:
        DEPARTAMENTOS_CIUDADES = json.load(f)
except Exception:
    DEPARTAMENTOS_CIUDADES = {}


def get_ciudades_for_departamento(departamento):
    return DEPARTAMENTOS_CIUDADES.get(departamento, [])
