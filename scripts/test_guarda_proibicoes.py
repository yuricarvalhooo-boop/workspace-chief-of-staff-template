#!/usr/bin/env python3
"""Testes do hook guarda_proibicoes.py . Uso: python scripts/test_guarda_proibicoes.py"""
import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "hooks"))
import guarda_proibicoes as g  # noqa: E402


def bash(cmd):
    return {"tool_name": "Bash", "tool_input": {"command": cmd}}


class Guarda(unittest.TestCase):
    def test_bloqueia(self):
        for ev in [
            bash("git push --force origin main"),
            bash("git push -f"),
            bash("git reset --hard HEAD~3"),
            bash("gh pr merge 5 --squash"),
            bash("gh secret set X"),
            bash("psql -c 'DROP TABLE clientes'"),
            bash("psql -c 'DELETE FROM clientes'"),
            {"tool_name": "mcp__claude_ai_Gmail__send_message", "tool_input": {}},
            {"tool_name": "mcp__claude_ai_Supabase__apply_migration", "tool_input": {}},
            {"tool_name": "mcp__claude_ai_Supabase__execute_sql", "tool_input": {"query": "TRUNCATE TABLE x"}},
        ]:
            self.assertIsNotNone(g.motivo(ev), ev)

    def test_libera(self):
        for ev in [
            bash("git push origin main"),
            bash("git status"),
            bash("gh pr merge 5 --squash  # autorizado-dono: pergunta 5 de 11/11"),
            bash("gh pr view 5"),
            bash("gh pr diff 5"),
            bash("psql -c 'SELECT 1'"),
            bash("psql -c \"DELETE FROM t WHERE id=1\""),
            {"tool_name": "mcp__claude_ai_Gmail__create_draft", "tool_input": {}},
            {"tool_name": "mcp__claude_ai_Supabase__execute_sql", "tool_input": {"query": "SELECT * FROM cron.job"}},
            {"tool_name": "Read", "tool_input": {"file_path": "x"}},
        ]:
            self.assertIsNone(g.motivo(ev), ev)


if __name__ == "__main__":
    unittest.main()
