"""Testes locais com Git temporário e segredos exclusivamente fictícios."""

from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

import handoff


class HandoffTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.git("init", "-b", "teste")
        self.git("config", "user.name", "Teste")
        self.git("config", "user.email", "teste@example.invalid")
        self.git("config", "core.hooksPath", ".hooks-inexistentes")

    def git(self, *args):
        return subprocess.check_output(["git", "-C", str(self.root), *args], encoding="utf-8").strip()

    def write(self, path, text):
        target = self.root / path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(text, encoding="utf-8")

    def commit(self, message):
        self.git("add", ".")
        self.git("commit", "-qm", message)

    def cli(self, *args):
        return subprocess.run([sys.executable, str(Path(handoff.__file__).resolve()),
                               "--repo", str(self.root), *args], capture_output=True, text=True)

    def test_git_tag_checkpoint_redaction_and_overwrite(self):
        self.write("base.txt", "base")
        self.commit("base antiga")
        initial = self.git("rev-parse", "HEAD")
        self.git("tag", "v1")
        self.write("context/orquestrador.md", "- Teste antigo OK\n- Último teste: unittest OK\n")
        self.write("knowledge/conversations/workspace/2026-11-10-velho.md",
                   "- Próximo passo: passo antigo\n")
        self.write("knowledge/conversations/workspace/2026-11-11-novo.md",
                   "- **Próximo passo concreto:** validar acentuação\n- Outro: ignorar\n")
        self.write("alterado.txt", "novo")
        self.commit("Implementa funcionalidade sk-" + "a" * 32)
        self.write("base.txt", "mudou")
        self.write("novo.txt", "não precisa ler o conteúdo")
        result = self.cli()
        self.assertEqual(result.returncode, 0, result.stderr)
        text = (self.root / "HANDOFF.md").read_text(encoding="utf-8")
        for expected in ("teste", "Desde: v1", "alterado.txt", "base.txt", "novo.txt",
                         "unittest OK", "validar acentuação", "[REDIGIDO]"):
            self.assertIn(expected, text)
        self.assertNotIn("base antiga", text)
        self.assertNotIn("passo antigo", text)
        self.assertNotIn("sk-" + "a" * 32, text)
        self.assertLessEqual(len(text), 3000)
        self.write("HANDOFF.md", "MARCADOR ANTIGO\n" * 1000)
        self.assertEqual(self.cli("--since", initial).returncode, 0)
        self.assertNotIn("MARCADOR", (self.root / "HANDOFF.md").read_text(encoding="utf-8"))
        before = (self.root / "HANDOFF.md").read_bytes()
        self.assertNotEqual(self.cli("--since", "referencia-inexistente").returncode, 0)
        self.assertEqual(before, (self.root / "HANDOFF.md").read_bytes())

    def test_empty_repo_no_tag_detached_and_large_output(self):
        target = handoff.generate(self.root)
        self.assertIn("Sem commits", target.read_text(encoding="utf-8"))
        self.write("context/orquestrador.md", "Teste: " + "z" * 8000)
        self.write("knowledge/conversations/workspace/2026-11-11-grande.md",
                   "## Próximo passo\n" + "validar " * 2000)
        self.commit("inicial")
        for i in range(3):
            self.write(f"arquivo{i}.txt", "conteúdo")
            self.commit("mudança " + "x" * 1000)
        self.git("checkout", "--detach", "-q")
        for i in range(80):
            self.write(f"pendente{i}.txt", "x")
        text = handoff.generate(self.root).read_text(encoding="utf-8")
        self.assertLessEqual(len(text), 3000)
        self.assertIn("HEAD destacado", text)
        self.assertIn("sem tag alcançável", text)
        self.assertIn("## Próximo passo", text)
        self.assertIn("validar", text)
        self.assertIn("truncado", text)

    def test_redaction(self):
        secrets = ["ghp_" + "a" * 30, "github_pat_" + "b" * 40,
                   "AKIA" + "A" * 16, "123456789:" + "a" * 35,
                   "eyJhbGciOiJub25l.abc123.signature", "xoxb-123456-abcdef"]
        for secret in secrets:
            self.assertNotIn(secret, handoff.redact(secret))
        for text in ('"api_key": "ficticio"', "TOKEN=ficticio", "senha: ficticio",
                     "Bearer ficticio", "https://nome:ficticio@example.invalid",
                     "https://example.invalid?access_token=ficticio",
                     "-----BEGIN PRIVATE KEY-----\nficticio\n-----END PRIVATE KEY-----"):
            self.assertNotIn("ficticio", handoff.redact(text))


if __name__ == "__main__":
    unittest.main()
