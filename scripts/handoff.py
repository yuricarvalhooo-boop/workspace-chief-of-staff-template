"""Gera HANDOFF.md local, sob demanda, com até 3.000 caracteres; só biblioteca padrão."""

import argparse
from pathlib import Path
import re
import subprocess
import unicodedata


LIMIT = 3000


def redact(text):
    """Redação preventiva por padrões; não lê conteúdo de arquivos alterados."""
    text = re.sub(r"-----BEGIN [^-\n]*PRIVATE KEY-----.*?(?:-----END [^-\n]*PRIVATE KEY-----|\Z)",
                  "[REDIGIDO]", text, flags=re.S)
    text = re.sub(r"(?i)\b(?:sk-[\w-]{8,}|(?:gh[pousr]_|github_pat_)[\w]{8,}|"
                  r"AIza[\w-]{12,}|(?:AKIA|ASIA)[A-Z0-9]{16}|xox[baprs]-[\w-]+|"
                  r"eyJ[\w-]+\.[\w-]+\.[\w-]+|\d{6,}:[\w-]{20,})", "[REDIGIDO]", text)
    text = re.sub(r"(?i)\bBearer\s+\S+", "Bearer [REDIGIDO]", text)
    text = re.sub(r"(https?://)[^\s/@]+:[^\s/@]+@", r"\1[REDIGIDO]@", text)
    # Valores rotulados, inclusive JSON, env e parâmetros de URL; até fim da linha.
    text = re.sub(r'''(?im)((?:[\w.-]*(?:token|secret|password|passwd|senha|api[_-]?key|access[_-]?key|private[_-]?key)[\w.-]*)["']?\s*[:=]\s*).*?$''',
                  r"\1[REDIGIDO]", text)
    return text


def git(root, *args, optional=False):
    result = subprocess.run(["git", "-c", "core.quotepath=false", "-C", str(root), *args],
                            capture_output=True, encoding="utf-8", errors="replace")
    if result.returncode and not optional:
        raise ValueError("Git não conseguiu consultar o repositório ou a referência indicada.")
    return result.stdout.strip() if result.returncode == 0 else ""


def read(path):
    return path.read_text(encoding="utf-8-sig", errors="replace") if path.is_file() else ""


def normalized(text):
    return "".join(c for c in unicodedata.normalize("NFD", text.lower())
                   if not unicodedata.combining(c)).replace("*", "")


def next_step(text):
    lines = text.splitlines()
    for index, line in enumerate(lines):
        if re.search(r"proximo passo", normalized(line)):
            following = []
            for other in lines[index + 1:]:
                if other.startswith("#") or re.match(r"^-\s+\*?\*?[A-ZÁÉÍÓÚÂÊÔÃÕÇ][^:]*:", other):
                    break
                following.append(other)
            return "\n".join([line, *following]).strip()
    return ""


def checkpoint(root):
    candidates = []
    for path in (root / "knowledge/conversations/workspace").glob("*.md"):
        step = next_step(read(path))
        if step:
            # Data do nome; desempate pela última alteração no Git, depois nome.
            stamp = git(root, "log", "-1", "--format=%ct", "--", str(path.relative_to(root)), optional=True)
            candidates.append((path.name[:10], int(stamp or 0), path.name, path, step))
    if not candidates:
        return "Checkpoint com próximo passo não encontrado."
    *_, path, step = max(candidates, key=lambda item: item[:3])
    return f"{path.relative_to(root).as_posix()}\n{step}"


def clipped(text, limit):
    text = redact(text)
    return text if len(text) <= limit else text[:limit - 16] + "\n[... truncado]"


def generate(root, since=None):
    root = Path(git(root, "rev-parse", "--show-toplevel"))
    head = git(root, "rev-parse", "--verify", "HEAD", optional=True)
    branch = git(root, "symbolic-ref", "--short", "-q", "HEAD", optional=True) or "HEAD destacado"
    if since:
        base = git(root, "rev-parse", "--verify", "--end-of-options", since + "^{commit}")
        if not head:
            raise ValueError("Repositório sem commits não aceita --since.")
        base_label = since
    else:
        tag = git(root, "describe", "--tags", "--abbrev=0", "HEAD", optional=True) if head else ""
        base = git(root, "rev-parse", "--verify", "--end-of-options", tag + "^{commit}") if tag else ""
        base_label = tag or "início (sem tag alcançável)"
    revision = [f"{base}..{head}" if base else head] if head else []
    commits = git(root, "log", "--format=%h %s", *revision) if head else "Sem commits."
    changed = git(root, "diff", "--name-status", base, head, "--") if base else (
        git(root, "log", "--format=", "--name-status", *revision) if head else "Sem commits.")
    status = git(root, "status", "--short", "--untracked-files=all")
    tests = [line for line in read(root / "context/orquestrador.md").splitlines()
             if re.search(r"test|verific|pytest|unittest|doctor", normalized(line))]
    sections = [
        ("Git", f"Branch: {branch}\nHEAD: {head or 'sem commits'}\nDesde: {base_label}", 320),
        ("Commits", commits or "Nenhum desde a base.", 420),
        ("Status (inclui arquivos locais)", status or "Limpo.", 420),
        ("Arquivos no histórico indicado", changed or "Nenhum.", 420),
        ("Últimos testes citados (relato, não reexecutados)", "\n".join(tests[-4:]) or "Não citados.", 450),
        ("Próximo passo do checkpoint", checkpoint(root), 600),
    ]
    output = "# HANDOFF\n\n" + "\n\n".join(f"## {title}\n{clipped(body, size)}" for title, body, size in sections) + "\n"
    assert len(output) <= LIMIT
    target = root / "HANDOFF.md"
    if target.is_symlink():
        raise ValueError("HANDOFF.md é link simbólico; gravação recusada.")
    target.write_text(output, encoding="utf-8", newline="\n")
    return target


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", type=Path, default=Path.cwd(), help="Repositório/worktree existente.")
    parser.add_argument("--since", help="Tag, branch ou commit de partida; padrão: última tag alcançável.")
    args = parser.parse_args()
    try:
        target = generate(args.repo, args.since)
    except (ValueError, OSError):
        parser.exit(1, "Não foi possível gerar o handoff; confira repositório, referência e permissões.\n")
    print(f"Gerado: {target.name} (máximo {LIMIT} caracteres).")


if __name__ == "__main__":
    main()
