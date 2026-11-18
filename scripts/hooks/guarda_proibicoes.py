#!/usr/bin/env python3
"""Hook PreToolUse: bloqueia ações da lista fechada da política de perguntas.

Lê o JSON do hook na entrada padrão. Para bloquear,
escreve o motivo na saída de erro e sai com código 2; caso contrário, sai com 0.
Ative em .claude/settings.json (PreToolUse) quando adotar docs/politica-de-perguntas.md. Teste: python scripts/test_guarda_proibicoes.py
"""
import json
import re
import sys

# (nome da ferramenta Bash/PowerShell) padrões no comando
COMANDOS = [
    (r"git\s+push\b.*(--force\b|--force-with-lease\b|\s-f\b)", "push forçado (irreversível, caso 3)"),
    (r"git\s+(reset\s+--hard|clean\s+-[a-z]*f)", "descarte de trabalho sem cópia (caso 3)"),
    (r"git\s+(branch\s+-D|push\s+\S+\s+--delete|push\s+\S+\s+:)", "apagar branch (caso 3)"),
    (r"gh\s+pr\s+merge\b", "merge de PR (produção/terceiros, casos 2 e 4)"),
    (r"gh\s+(repo\s+(delete|edit|transfer)|secret\s+(set|delete)|issue\s+delete)", "mudança em repositório ou segredo (casos 2 e 5)"),
    (r"\b(DROP|TRUNCATE)\s+(TABLE|DATABASE|SCHEMA)\b", "SQL destrutivo (caso 2)"),
    (r"\bDELETE\s+FROM\b(?!.*\bWHERE\b)", "DELETE sem WHERE (caso 2)"),
]

FERRAMENTAS_BLOQUEADAS = {
    "mcp__claude_ai_Gmail__send_message": "envio de e-mail a terceiros (caso 4)",
    "mcp__claude_ai_Gmail__forward": "envio de e-mail a terceiros (caso 4)",
    "mcp__claude_ai_Gmail__reply": "envio de e-mail a terceiros (caso 4)",
    "mcp__claude_ai_Supabase__apply_migration": "migração em banco (caso 2)",
    "mcp__claude_ai_Supabase__create_edge_function_secret": "segredo (caso 5)",
    "mcp__claude_ai_Supabase__deploy_edge_function": "publicação em produção (caso 2)",
    "mcp__claude_ai_Supabase__delete_branch": "apagar branch de banco (caso 3)",
    "mcp__claude_ai_Supabase__reset_branch": "reset de banco (caso 3)",
}


def motivo(evento):
    nome = evento.get("tool_name", "")
    entrada = evento.get("tool_input", {}) or {}
    if nome in FERRAMENTAS_BLOQUEADAS:
        return FERRAMENTAS_BLOQUEADAS[nome]
    if nome == "mcp__claude_ai_Supabase__execute_sql":
        consulta = str(entrada.get("query", ""))
        for padrao, texto in COMANDOS[5:7]:
            if re.search(padrao, consulta, re.I | re.S):
                return texto
    if nome in ("Bash", "PowerShell"):
        comando = str(entrada.get("command", ""))
        # o dono autorizou na conversa: o agente acrescenta "# autorizado-dono: motivo" ao comando
        if re.search(r"#\s*autorizado-dono:\s*\S+", comando):
            return None
        for padrao, texto in COMANDOS:
            if re.search(padrao, comando, re.I | re.S):
                return texto
    return None


def main():
    try:
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass
    try:
        evento = json.load(sys.stdin)
    except Exception:
        return 0  # entrada ilegível: nunca travar o agente por falha do próprio hook
    razao = motivo(evento)
    if razao:
        sys.stderr.write(
            "Bloqueado pela política de perguntas: %s. Pergunte ao dono antes "
            "(uma pergunta, com recomendação) e só execute com a autorização dele.\n" % razao
        )
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
