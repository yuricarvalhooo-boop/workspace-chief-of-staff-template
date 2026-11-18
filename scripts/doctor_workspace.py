#!/usr/bin/env python3
"""Diagnósticos rápidos e semânticos, somente-leitura, do workspace."""

import argparse
import datetime
import json
import math
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CONTEXT_BUDGETS = {
    "AGENTS.md": 1_000,
    "CLAUDE.md": 10_000,
    "START.md": 8_000,
    "memory/MEMORY.md": 2_500,
}
SKILL_REVIEW_LIMIT = 12_000
SKILL_STRONG_LIMIT = 24_000
SKILL_STATES = {"experimental", "ativa", "obsoleta", "arquivada"}
LEARNING_STATES = {"proposta", "aprovada", "rejeitada", "aplicada"}
LEARNING_FIELDS = (
    "Status",
    "Observação e origem",
    "Generalização proposta",
    "Destino sugerido",
    "Mudança ou diff esperado",
    "Riscos e evidência contrária",
    "Autorização",
    "Aplicação e verificação",
)
SECURITY_SUFFIXES = {".md", ".txt", ".json", ".yaml", ".yml", ".py", ".js", ".ts", ".sh", ".ps1"}
SECURITY_SKIP_DIRS = {".git", "node_modules", "archive", "sources", "repositories", "versions"}
SECURITY_MAX_FILE_BYTES = 1_000_000
SECURITY_RULES = (
    (
        "error",
        "security.private_key",
        re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
        "Material de chave privada encontrado.",
    ),
    (
        "error",
        "security.token_literal",
        re.compile(
            r"\b(?:gh[pousr]_[A-Za-z0-9]{20,}|AKIA[0-9A-Z]{16}|sk-(?:proj-)?[A-Za-z0-9_-]{20,}"
            r"|AIza[0-9A-Za-z_-]{35}|\d{8,10}:AA[A-Za-z0-9_-]{33}|xox[baprs]-[A-Za-z0-9-]{10,})\b"
        ),
        "Literal com formato de credencial encontrado.",
    ),
    (
        "warning",
        "security.possible_secret_assignment",
        re.compile(
            r"(?i)\b(?:api[_-]?key|access[_-]?token|auth[_-]?token|client[_-]?secret|password)\b"
            r"\s*[:=]\s*[\"']?[A-Za-z0-9_./+=-]{16,}"
        ),
        "Possível segredo literal atribuído em arquivo de controle.",
    ),
    (
        "warning",
        "security.prompt_override",
        re.compile(r"(?i)\bignore (?:all |any )?(?:previous|prior|system|developer) instructions\b"),
        "Padrão de tentativa de substituir instruções encontrado.",
    ),
    (
        "warning",
        "security.exfiltration",
        re.compile(r"(?i)\b(?:reveal|print|exfiltrate|send)\b.{0,60}\b(?:secret|token|password|credential|system prompt)\b"),
        "Padrão de possível exfiltração encontrado.",
    ),
    (
        "warning",
        "security.destructive_command",
        re.compile(
            r"(?i)(?:\brm\s+-rf\b|\bgit\s+reset\s+--hard\b|\bInvoke-Expression\b|\biex\s*\(|"
            r"\b(?:curl|wget)\b[^\n|]{0,200}\|\s*(?:sh|bash|zsh|powershell)\b|"
            r"\bRemove-Item\b[^\n]{0,160}(?:-Recurse[^\n]{0,80}-Force|-Force[^\n]{0,80}-Recurse))"
        ),
        "Comando de alto risco encontrado em arquivo de controle.",
    ),
)
INVISIBLE_CONTROL = re.compile(r"[\u200b-\u200f\u202a-\u202e\u2066-\u2069\ufeff]")
NOTE_SCOPES = ("knowledge", "memory", "context", "processes", "people", "meetings", "workflows", "docs")
SUMMARY_LIMIT = 200


def diagnostic(level, code, message, path=None, **details):
    item = {"level": level, "code": code, "message": message}
    if path:
        item["path"] = str(path).replace("\\", "/")
    item.update(details)
    return item


def read_text(root, relative):
    return (root / relative).read_text(encoding="utf-8-sig")


def parse_json_frontmatter(text):
    match = re.match(r"^---\s*\n(.*?)\n---\s*\n", text, re.S)
    if not match or not match.group(1).lstrip().startswith("{"):
        return None
    return json.loads(match.group(1))


def measure_context_sizes(root=ROOT):
    measurements = []
    for relative, limit in CONTEXT_BUDGETS.items():
        path = root / relative
        if path.is_file():
            characters = len(path.read_text(encoding="utf-8-sig"))
            measurements.append(
                {
                    "path": relative,
                    "characters": characters,
                    "estimated_tokens": math.ceil(characters / 4),
                    "target": limit,
                    "status": "warning" if characters >= limit else "ok",
                }
            )
    for path in sorted((root / "skills").glob("*/SKILL.md")):
        characters = len(path.read_text(encoding="utf-8-sig"))
        status = "strong-warning" if characters > SKILL_STRONG_LIMIT else "warning" if characters > SKILL_REVIEW_LIMIT else "ok"
        measurements.append(
            {
                "path": str(path.relative_to(root)).replace("\\", "/"),
                "characters": characters,
                "estimated_tokens": math.ceil(characters / 4),
                "review_target": SKILL_REVIEW_LIMIT,
                "strong_target": SKILL_STRONG_LIMIT,
                "status": status,
            }
        )
    return measurements


def check_context_sizes(root=ROOT):
    results = []
    for relative, limit in CONTEXT_BUDGETS.items():
        path = root / relative
        if not path.is_file():
            results.append(diagnostic("error", "size.missing", "Arquivo de contexto ausente.", relative))
            continue
        characters = len(path.read_text(encoding="utf-8-sig"))
        if characters >= limit:
            results.append(
                diagnostic(
                    "warning",
                    "size.context",
                    f"Arquivo atingiu o alvo de menos de {limit} caracteres.",
                    relative,
                    characters=characters,
                    estimated_tokens=math.ceil(characters / 4),
                    limit=limit,
                )
            )

    skills_dir = root / "skills"
    if not skills_dir.is_dir():
        results.append(diagnostic("error", "size.skills_missing", "Diretório canônico de skills ausente.", "skills"))
        return results

    for path in sorted(skills_dir.glob("*/SKILL.md")):
        characters = len(path.read_text(encoding="utf-8-sig"))
        relative = path.relative_to(root)
        if characters > SKILL_STRONG_LIMIT:
            results.append(
                diagnostic(
                    "warning",
                    "size.skill_strong",
                    "Skill ultrapassou o alerta forte de revisão; nenhuma alteração automática foi feita.",
                    relative,
                    characters=characters,
                    estimated_tokens=math.ceil(characters / 4),
                    limit=SKILL_STRONG_LIMIT,
                )
            )
        elif characters > SKILL_REVIEW_LIMIT:
            results.append(
                diagnostic(
                    "warning",
                    "size.skill_review",
                    "Skill ultrapassou o alerta de revisão; nenhuma alteração automática foi feita.",
                    relative,
                    characters=characters,
                    estimated_tokens=math.ceil(characters / 4),
                    limit=SKILL_REVIEW_LIMIT,
                )
            )
    return results


def _check_forbidden_claims(root, paths, claims, state_name):
    results = []
    for relative in paths:
        path = root / relative
        if not path.is_file():
            results.append(diagnostic("error", "semantic.source_missing", "Fonte ativa ausente.", relative))
            continue
        text = path.read_text(encoding="utf-8-sig")
        for pattern, description in claims:
            if re.search(pattern, text, re.I | re.S):
                results.append(
                    diagnostic(
                        "error",
                        f"semantic.{state_name}.stale_claim",
                        description,
                        relative,
                        pattern=pattern,
                    )
                )
    return results


def check_active_state(root=ROOT):
    results = []
    repos_path = root / "repos.yaml"
    if not repos_path.is_file():
        return [diagnostic("error", "semantic.repos_missing", "Catálogo repos.yaml ausente.", "repos.yaml")]
    try:
        workspace = json.loads(repos_path.read_text(encoding="utf-8-sig"))["workspace"]
    except (json.JSONDecodeError, KeyError) as exc:
        return [diagnostic("error", "semantic.repos_invalid", f"Estado do workspace inválido: {exc}", "repos.yaml")]

    start_path = root / "START.md"
    if not start_path.is_file():
        results.append(diagnostic("error", "semantic.start_missing", "START.md ausente.", "START.md"))
    else:
        try:
            start_meta = parse_json_frontmatter(start_path.read_text(encoding="utf-8-sig")) or {}
        except json.JSONDecodeError as exc:
            results.append(diagnostic("error", "semantic.start_invalid", f"Frontmatter inválido: {exc}", "START.md"))
            start_meta = {}
        if start_meta.get("status") != workspace.get("phase"):
            results.append(
                diagnostic(
                    "error",
                    "semantic.workspace_phase",
                    "START.md e repos.yaml divergem sobre a fase do workspace.",
                    "START.md",
                    start_status=start_meta.get("status"),
                    repos_phase=workspace.get("phase"),
                )
            )

    active_state_sources = ["CLAUDE.md", "context/workspace.md", "docs/migracao.md"]
    if str(workspace.get("git_status", "")).startswith("repo-git-ativo"):
        results.extend(
            _check_forbidden_claims(
                root,
                active_state_sources,
                [
                    (r"n[aã]o h[aá]\s+[`*]*\.git[`*]*\s+ativo", "Fonte ativa ainda afirma que não há Git ativo."),
                    (r"sem\s+[`*]*\.git[`*]*\s+ativo", "Fonte ativa ainda afirma que não há Git ativo."),
                    (r"GitHub pode complementar com hist[oó]rico", "Fonte ativa ainda descreve o Git como possibilidade futura."),
                    (r"publica[cç][aã]o Git.+decis[aã]o posterior", "Fonte ativa ainda descreve o Git como decisão futura."),
                ],
                "git",
            )
        )

    if "confirmad" in str(workspace.get("cloud_status", "")):
        results.extend(
            _check_forbidden_claims(
                root,
                active_state_sources,
                [
                    (
                        r"sincroniza[cç][aã]o e disponibilidade offline.+precisam de confer[eê]ncia pr[oó]pria",
                        "Fonte ativa ainda trata a sincronização geral entre equipamentos como não confirmada.",
                    ),
                    (r"Google Drive [eé] o transporte planejado", "Fonte ativa ainda descreve o Drive como estado apenas planejado."),
                ],
                "cloud",
            )
        )
    return results


def check_skill_catalog(root=ROOT):
    results = []
    catalog_path = root / "knowledge/skills/catalog.json"
    if not catalog_path.is_file():
        return [diagnostic("error", "skills.catalog_missing", "Catálogo de skills ausente.", "knowledge/skills/catalog.json")]
    try:
        catalog = json.loads(catalog_path.read_text(encoding="utf-8-sig"))
    except json.JSONDecodeError as exc:
        return [diagnostic("error", "skills.catalog_invalid", f"Catálogo inválido: {exc}", "knowledge/skills/catalog.json")]

    entries = catalog.get("skills", [])
    names = [entry.get("name") for entry in entries]
    canonical_names = sorted(path.parent.name for path in (root / "skills").glob("*/SKILL.md"))
    if len(names) != len(set(names)):
        results.append(diagnostic("error", "skills.catalog_duplicate", "Catálogo contém nomes duplicados.", "knowledge/skills/catalog.json"))
    if sorted(names) != canonical_names:
        results.append(
            diagnostic(
                "error",
                "skills.catalog_coverage",
                "Catálogo e diretório canônico não contêm o mesmo conjunto de skills.",
                "knowledge/skills/catalog.json",
                catalog=sorted(name for name in names if name),
                canonical=canonical_names,
            )
        )

    required = {
        "name",
        "purpose",
        "triggers",
        "canonical_source",
        "adapters",
        "workflow",
        "templates",
        "references",
        "origin",
        "last_reviewed",
        "criticality",
        "protection",
        "status",
        "related_evaluations",
    }
    for entry in entries:
        name = entry.get("name", "<sem-nome>")
        missing = sorted(required - set(entry))
        if missing:
            results.append(diagnostic("error", "skills.catalog_fields", f"{name}: campos ausentes: {', '.join(missing)}", "knowledge/skills/catalog.json"))
        if entry.get("status") not in SKILL_STATES:
            results.append(diagnostic("error", "skills.catalog_state", f"{name}: estado inválido.", "knowledge/skills/catalog.json"))
        for field in ("canonical_source", "workflow"):
            relative = entry.get(field)
            if relative and not (root / relative).is_file():
                results.append(diagnostic("error", "skills.catalog_path", f"{name}: caminho ausente em {field}.", relative))
        for relative in entry.get("adapters", []) + entry.get("templates", []) + entry.get("references", []):
            if not (root / relative).exists():
                results.append(diagnostic("error", "skills.catalog_path", f"{name}: caminho catalogado ausente.", relative))
    return results


def check_learning_queue(root=ROOT):
    results = []
    proposals_dir = root / "knowledge/learning/proposals"
    if not proposals_dir.is_dir():
        return [diagnostic("error", "learning.queue_missing", "Diretório de propostas ausente.", "knowledge/learning/proposals")]
    for path in sorted(proposals_dir.glob("APR-*.md")):
        text = path.read_text(encoding="utf-8-sig")
        relative = path.relative_to(root)
        missing = [field for field in LEARNING_FIELDS if f"**{field}:**" not in text]
        if missing:
            results.append(
                diagnostic(
                    "error",
                    "learning.fields",
                    f"Proposta sem campos obrigatórios: {', '.join(missing)}.",
                    relative,
                )
            )
        status_match = re.search(r"\*\*Status:\*\*\s*`([^`]+)`", text)
        status = status_match.group(1) if status_match else None
        if status not in LEARNING_STATES:
            results.append(diagnostic("error", "learning.status", "Estado de proposta inválido ou ausente.", relative, status=status))
        authorization_match = re.search(r"\*\*Autorização:\*\*\s*(.+)", text)
        authorization = authorization_match.group(1).strip() if authorization_match else ""
        if status in {"aprovada", "aplicada"} and (not authorization or "pendente" in authorization.casefold()):
            results.append(
                diagnostic(
                    "error",
                    "learning.authorization",
                    "Proposta aprovada/aplicada não possui autorização explícita registrada.",
                    relative,
                )
            )
    return results


def active_security_files(root=ROOT):
    paths = []
    for relative in ("AGENTS.md", "CLAUDE.md", "START.md", "memory/MEMORY.md", "context/workspace.md"):
        path = root / relative
        if path.is_file():
            paths.append(path)
    for pattern in ("skills/*/SKILL.md", "workflows/*.md", "projects/*/AGENTS.md", "projects/*/CLAUDE.md"):
        paths.extend(root.glob(pattern))
    return sorted(set(paths))


def security_candidate_files(path):
    if path.is_file():
        return [path] if path.suffix.casefold() in SECURITY_SUFFIXES else []
    if not path.is_dir():
        return []
    return sorted(
        candidate
        for candidate in path.rglob("*")
        if candidate.is_file()
        and candidate.suffix.casefold() in SECURITY_SUFFIXES
        and not any(part in SECURITY_SKIP_DIRS for part in candidate.parts)
    )


def check_security_files(paths, root=ROOT):
    results = []
    for path in paths:
        try:
            display = path.resolve().relative_to(root.resolve())
        except ValueError:
            display = path.resolve()
        try:
            size = path.stat().st_size
        except OSError as exc:
            results.append(diagnostic("error", "security.unreadable", f"Arquivo não pôde ser inspecionado: {exc}", display))
            continue
        if size > SECURITY_MAX_FILE_BYTES:
            results.append(
                diagnostic(
                    "error",
                    "security.file_too_large",
                    "Arquivo excede o limite da inspeção estática e não foi promovido.",
                    display,
                    bytes=size,
                    limit=SECURITY_MAX_FILE_BYTES,
                )
            )
            continue
        try:
            text = path.read_text(encoding="utf-8-sig")
        except (OSError, UnicodeDecodeError) as exc:
            results.append(diagnostic("error", "security.unreadable", f"Arquivo não pôde ser inspecionado: {exc}", display))
            continue
        for match in INVISIBLE_CONTROL.finditer(text):
            results.append(
                diagnostic(
                    "error",
                    "security.invisible_unicode",
                    "Caractere Unicode invisível/de controle encontrado.",
                    display,
                    line=text.count("\n", 0, match.start()) + 1,
                )
            )
        for level, code, pattern, message in SECURITY_RULES:
            for match in pattern.finditer(text):
                results.append(
                    diagnostic(
                        level,
                        code,
                        message,
                        display,
                        line=text.count("\n", 0, match.start()) + 1,
                    )
                )
    return results


def note_files(root=ROOT):
    for scope in NOTE_SCOPES:
        yield from sorted((root / scope).rglob("*.md"))
    if (root / "START.md").is_file():
        yield root / "START.md"


def check_note_metadata(root=ROOT, today=None):
    """Campos opcionais do frontmatter: revisar, expires e summary. Só alerta; nunca altera a nota."""
    today = today or datetime.date.today()
    results = []
    for path in note_files(root):
        try:
            meta = parse_json_frontmatter(path.read_text(encoding="utf-8-sig"))
        except (OSError, UnicodeDecodeError, json.JSONDecodeError):
            continue
        if not isinstance(meta, dict):
            continue
        relative = path.relative_to(root)
        review = meta.get("revisar")
        if review:
            reason = review if isinstance(review, str) else json.dumps(review, ensure_ascii=False)
            results.append(diagnostic("warning", "metadata.review_flag", f"Nota sinalizada para revisão: {reason}", relative))
        if "expires" in meta:
            try:
                expires = datetime.date.fromisoformat(str(meta["expires"]))
            except ValueError:
                results.append(diagnostic("warning", "metadata.expires_invalid", "Campo expires deve ser AAAA-MM-DD.", relative))
            else:
                if expires < today:
                    results.append(
                        diagnostic(
                            "warning",
                            "metadata.expired",
                            f"Nota vencida em {expires.isoformat()}: fora da busca padrão; renovar, atualizar ou marcar como histórico.",
                            relative,
                        )
                    )
        summary = meta.get("summary")
        if summary is not None and (not isinstance(summary, str) or "\n" in summary or len(summary) > SUMMARY_LIMIT):
            results.append(
                diagnostic("warning", "metadata.summary", f"summary deve ser uma linha de até {SUMMARY_LIMIT} caracteres.", relative)
            )
    return results


def check_git_drive_artifacts(root=ROOT):
    """desktop.ini do Google Drive em .git/refs ou .git/logs quebra o fetch no formato files."""
    git_dir = root / ".git"
    if not git_dir.is_dir():
        return []
    config = git_dir / "config"
    if config.is_file() and re.search(r"(?im)^\s*refstorage\s*=\s*reftable\s*$", config.read_text(encoding="utf-8", errors="replace")):
        return []
    results = []
    for folder in ("refs", "logs"):
        for path in sorted((git_dir / folder).rglob("desktop.ini")):
            results.append(
                diagnostic(
                    "warning",
                    "git.drive_desktop_ini",
                    "desktop.ini do Google Drive dentro das referências do Git; o fetch falha. O pre-commit remove; ou migre para reftable.",
                    path.relative_to(root),
                )
            )
    return results


def check_active_security(root=ROOT):
    return check_security_files(active_security_files(root), root)


def run(mode="all", root=ROOT):
    results = []
    if mode in {"quick", "all"}:
        results.extend(check_context_sizes(root))
    if mode in {"semantic", "all"}:
        results.extend(check_active_state(root))
        results.extend(check_skill_catalog(root))
        results.extend(check_learning_queue(root))
        results.extend(check_note_metadata(root))
        results.extend(check_git_drive_artifacts(root))
    if mode in {"security", "all"}:
        results.extend(check_active_security(root))
    return results


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--mode", choices=("quick", "semantic", "security", "all"), default="all")
    parser.add_argument("--inspect", type=Path, help="Inspeciona um arquivo/diretório candidato e bloqueia em qualquer achado.")
    parser.add_argument("--json", action="store_true", help="Emite relatório JSON.")
    args = parser.parse_args(argv)
    strict_gate = args.inspect is not None
    if strict_gate:
        inspected = args.inspect.expanduser().resolve()
        files = security_candidate_files(inspected)
        if not inspected.exists():
            results = [diagnostic("error", "security.path_missing", "Candidato informado não existe.", inspected)]
        elif not files:
            results = [diagnostic("error", "security.no_files", "Nenhum arquivo textual suportado foi encontrado.", inspected)]
        else:
            results = check_security_files(files)
        mode = "inspect"
        sizes = []
    else:
        results = run(args.mode)
        mode = args.mode
        sizes = measure_context_sizes() if args.mode in {"quick", "all"} else []
    summary = {
        "mode": mode,
        "root": str(ROOT),
        "read_only": True,
        "errors": sum(item["level"] == "error" for item in results),
        "warnings": sum(item["level"] == "warning" for item in results),
        "gate_passed": not results if strict_gate else not any(item["level"] == "error" for item in results),
        "sizes": sizes,
        "diagnostics": results,
    }
    if args.json:
        print(json.dumps(summary, ensure_ascii=False, indent=2))
    else:
        print(f"Doctor workspace ({mode}, somente-leitura): {summary['errors']} erro(s), {summary['warnings']} alerta(s)")
        if sizes:
            context_sizes = [item for item in sizes if not item["path"].startswith("skills/")]
            skill_sizes = [item for item in sizes if item["path"].startswith("skills/")]
            print("- Tamanhos de contexto: " + "; ".join(f"{item['path']}={item['characters']}" for item in context_sizes))
            if skill_sizes:
                largest = max(skill_sizes, key=lambda item: item["characters"])
                print(f"- Skills: {len(skill_sizes)} medidas; maior={largest['path']} ({largest['characters']} caracteres)")
        for item in results:
            location = f" [{item['path']}]" if item.get("path") else ""
            line = f":{item['line']}" if item.get("line") else ""
            print(f"- {item['level'].upper()} {item['code']}{location}{line}: {item['message']}")
        if not results:
            print("- OK: nenhum diagnóstico.")
    return 1 if (summary["errors"] or (strict_gate and summary["warnings"])) else 0


if __name__ == "__main__":
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    raise SystemExit(main())
