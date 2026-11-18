#!/usr/bin/env python3
"""Executa avaliações determinísticas e lista casos de modelo sem chamadas externas."""

import argparse
import json
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CASES_DIR = ROOT / "evals/agent-behavior"


def load_cases(name):
    return json.loads((CASES_DIR / name).read_text(encoding="utf-8-sig"))["cases"]


def load_bundle(name):
    return json.loads((CASES_DIR / name).read_text(encoding="utf-8-sig"))


def run_deterministic(root=ROOT):
    results = []
    for case in load_cases("deterministic.json"):
        failures = []
        for check in case["checks"]:
            path = root / check["path"]
            if not path.is_file():
                failures.append(f"arquivo ausente: {check['path']}")
                continue
            text = path.read_text(encoding="utf-8-sig")
            if "contains" in check and check["contains"] not in text:
                failures.append(f"trecho ausente em {check['path']}: {check['contains']}")
            if "regex" in check and not re.search(check["regex"], text, re.I | re.S):
                failures.append(f"padrão ausente em {check['path']}: {check['regex']}")
        results.append({"id": case["id"], "passed": not failures, "failures": failures})
    return results


def list_model_cases():
    bundle = load_bundle("model.json")
    status = "executed" if str(bundle.get("execution_status", "")).startswith("executed") else "pending"
    return [
        {"id": case["id"], "status": status, "rubric_items": len(case["rubric"])}
        for case in bundle["cases"]
    ]


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--mode", choices=("deterministic", "list-model", "all"), default="deterministic")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)

    deterministic = run_deterministic() if args.mode in {"deterministic", "all"} else []
    model = list_model_cases() if args.mode in {"list-model", "all"} else []
    report = {
        "mode": args.mode,
        "external_calls": False,
        "deterministic": deterministic,
        "model": model,
        "model_execution_status": load_bundle("model.json").get("execution_status") if model else None,
        "passed": all(item["passed"] for item in deterministic),
    }
    if args.json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        if deterministic:
            passed = sum(item["passed"] for item in deterministic)
            print(f"Avaliações determinísticas: {passed}/{len(deterministic)} aprovadas")
            for item in deterministic:
                marker = "PASS" if item["passed"] else "FAIL"
                print(f"- {marker} {item['id']}")
                for failure in item["failures"]:
                    print(f"  - {failure}")
        if model:
            print(f"Casos dependentes de modelo: {len(model)} — {report['model_execution_status']}")
            for item in model:
                print(f"- {item['status'].upper()} {item['id']} ({item['rubric_items']} critérios)")
    return 0 if report["passed"] else 1


if __name__ == "__main__":
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    raise SystemExit(main())
