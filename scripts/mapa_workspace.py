#!/usr/bin/env python3
"""Índice compacto local, sem dependências; falha antes de gravar se exceder 6.000 caracteres."""

import json
import re
from pathlib import Path
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parents[1]
LIMIT = 6_000


def metadata(text):
    match = re.match(r"^---\s*\n(.*?)\n---", text, re.S)
    return json.loads(match[1]) if match else {}


def collect(root):
    records = {}
    registry = json.loads((root / "repos.yaml").read_text(encoding="utf-8"))
    registered = {p["memory_file"]: p["id"] for p in registry["projects"]}
    for scope, prefix in (("knowledge/projects", "PROJ"), ("processes", "PRC"),
                          ("people", "PES")):
        for path in sorted((root / scope).glob("*.md")):
            if path.name == "INDEX.md":
                continue
            text = path.read_text(encoding="utf-8")
            relative = path.relative_to(root).as_posix()
            # Sem ID declarado, o caminho canônico fornece um ID estável;
            # renomear a fonte nesse caso implica mudar o ID.
            declared = metadata(text).get("id")
            filename_id = re.match(r"(?:PRC|PES)-\d+", path.stem)
            identifier = registered.get(relative) or declared or (
                filename_id[0] if filename_id else f"{prefix}-{path.stem}")
            if identifier in records:
                raise ValueError(f"ID duplicado: {identifier}")
            records[identifier] = (relative, text, prefix)
    return records


def render(root=ROOT):
    records = collect(root)
    by_path = {(root / p).resolve(): ident for ident, (p, _, _) in records.items()}
    edges = {ident: set() for ident in records}
    for ident, (path, text, _) in records.items():
        refs = set(re.findall(r"\b(?:PES-\d+|PRC-\d+|PROJ-[\w-]+)\b", text))
        for target in re.findall(r"\]\(([^)]+)\)", text):
            resolved = (root / path).parent / unquote(target.split("#", 1)[0])
            linked = by_path.get(resolved.resolve())
            if linked:
                refs.add(linked)
        for linked in refs & records.keys() - {ident}:
            # Relações são menções documentais, nunca atribuições de responsabilidade.
            edges[ident].add(linked)
            edges[linked].add(ident)
    lines = ["# Mapa consultável do workspace", "",
             "Gerado por `python scripts/mapa_workspace.py`; não editar à mão.",
             "Projetos/sistemas: memórias + repos.yaml; processos: processes/. Pessoas são destinos de ligações.",
             "Ligações = IDs ou links explícitos nas fontes, em ambos os sentidos; não validam papéis nem estado atual.",
             "Sem ID declarado: PROJ-<nome do arquivo> (renomear muda o ID). Sem ligação: —.", ""]
    for ident, (path, _, kind) in sorted(records.items()):
        if kind == "PES":
            continue
        links = []
        for linked in sorted(edges[ident]):
            target, _, target_kind = records[linked]
            if target_kind in {"PES", "PRC"} or kind == "PRC":
                links.append(f"[{linked}](../{target})")
        lines.append(f"- [{ident}](../{path}) | {', '.join(links) or '—'}")
    result = "\n".join(lines) + "\n"
    if len(result) > LIMIT:
        raise ValueError(f"Mapa com {len(result)} caracteres; limite {LIMIT}. Reduza ligações/fontes sem truncar linhas.")
    return result


def main():
    result = render()
    destination = ROOT / "knowledge/mapa-workspace.md"
    destination.write_text(result, encoding="utf-8", newline="\n")
    print(f"knowledge/mapa-workspace.md: {len(result)} caracteres (limite {LIMIT})")


if __name__ == "__main__":
    main()
