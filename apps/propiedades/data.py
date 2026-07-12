import json
from pathlib import Path


_BASE = Path(__file__).parent
_JSON_PATH = _BASE / "ciudades_paraguay.json"


try:
    with open(_JSON_PATH, "r", encoding="utf-8") as f:
        DEPARTAMENTOS_CIUDADES = json.load(f)

except Exception:
    DEPARTAMENTOS_CIUDADES = {
        "Itapúa": [
            "Encarnación",
            "Hohenau",
            "Obligado",
            "Bella Vista",
            "Pirapó",
            "Capitán Meza",
            "Fram",
            "Carmen del Paraná",
            "Coronel Bogado",
            "San Juan del Paraná",
            "Cambyretá",
            "Natalio",
            "Edelira",
            "Tomás Romero Pereira",
            "Mayor Otaño",
        ],
        "Alto Paraná": [
            "Ciudad del Este",
            "Hernandarias",
            "Presidente Franco",
            "Minga Guazú",
            "Santa Rita",
            "Naranjal",
            "Juan León Mallorquín",
        ],
        "Central": [
            "San Lorenzo",
            "Luque",
            "Capiatá",
            "Fernando de la Mora",
            "Lambaré",
            "Mariano Roque Alonso",
            "Limpio",
            "Ñemby",
            "Villa Elisa",
            "Itauguá",
        ],
        "Asunción": [
            "Asunción",
        ],
    }


def get_ciudades_for_departamento(departamento):
    return DEPARTAMENTOS_CIUDADES.get(departamento, [])