"""Verifica relações documentais, cobertura e limite sem dependências externas."""

import json
import tempfile
import unittest
from pathlib import Path

from mapa_workspace import collect, render


class MapaTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        for folder in ("knowledge/projects", "processes", "people"):
            (self.root / folder).mkdir(parents=True)
        (self.root / "repos.yaml").write_text(json.dumps({"projects": [
            {"id": "PROJ-app", "memory_file": "knowledge/projects/app.md"}
        ]}), encoding="utf-8")
        self.write("knowledge/projects/app.md", "# App\nConteúdo longo " * 1000)
        self.write("knowledge/projects/extra.md", "# Extra")
        self.write("people/PES-001-teste.md", "# Pessoa")
        self.write("processes/PRC-001-teste.md",
                   "# Processo\n[[PES-001]] [App](../knowledge/projects/app.md)")

    def write(self, path, content):
        (self.root / path).write_text(content, encoding="utf-8")

    def test_coverage_relations_and_compactness(self):
        result = render(self.root)
        self.assertEqual(result, render(self.root))
        self.assertLessEqual(len(result), 6000)
        self.assertNotIn("Conteúdo longo", result)
        rows = [line for line in result.splitlines() if line.startswith("- ")]
        self.assertEqual(len(rows), 3)
        app = next(row for row in rows if row.startswith("- [PROJ-app]"))
        self.assertIn("[PRC-001]", app)
        process = next(row for row in rows if row.startswith("- [PRC-001]"))
        self.assertIn("[PES-001]", process)
        self.assertIn("[PROJ-extra]", result)

    def test_duplicate_id_rejected(self):
        self.write("knowledge/projects/extra.md", '---\n{"id":"PROJ-app"}\n---\n')
        with self.assertRaisesRegex(ValueError, "ID duplicado"):
            collect(self.root)

    def test_overflow_preserves_previous_file(self):
        for number in range(100):
            self.write(f"knowledge/projects/projeto-{number:03}.md", "# Projeto")
        with self.assertRaisesRegex(ValueError, "limite 6000"):
            render(self.root)


if __name__ == "__main__":
    unittest.main()
