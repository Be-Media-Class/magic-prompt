import json
import os
from datetime import datetime
from pathlib import Path

DB_PATH = Path(__file__).parent / "data" / "carrosseis.json"


def _garantir_db():
    DB_PATH.parent.mkdir(exist_ok=True)
    if not DB_PATH.exists():
        DB_PATH.write_text("[]")


def listar_todos() -> list[dict]:
    _garantir_db()
    return json.loads(DB_PATH.read_text())


def buscar_por_id(id: str) -> dict | None:
    return next((c for c in listar_todos() if c["id"] == id), None)


def salvar(carrossel: dict) -> dict:
    _garantir_db()
    todos = listar_todos()
    existente = next((i for i, c in enumerate(todos) if c["id"] == carrossel["id"]), None)
    if existente is not None:
        todos[existente] = carrossel
    else:
        todos.append(carrossel)
    DB_PATH.write_text(json.dumps(todos, ensure_ascii=False, indent=2))
    return carrossel


def atualizar_status(id: str, status: str, **kwargs) -> dict | None:
    carrossel = buscar_por_id(id)
    if not carrossel:
        return None
    carrossel["status"] = status
    carrossel["atualizado_em"] = datetime.now().isoformat()
    carrossel.update(kwargs)
    return salvar(carrossel)
