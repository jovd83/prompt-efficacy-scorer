from __future__ import annotations

import json
import sys
from pathlib import Path


REQUIRED_FILES = [
    "SKILL.md",
    "README.md",
    "LICENSE",
    "VERSION",
    "agents/openai.yaml",
    "evals/evals.json",
    "references/rubric.md",
    "references/evaluation-guide.md",
    "references/model-specific-examples.md",
]


def fail(message: str) -> int:
    print(f"FAIL: {message}")
    return 1


def main() -> int:
    repo_root = Path(__file__).resolve().parents[1]

    for relative_path in REQUIRED_FILES:
        if not (repo_root / relative_path).exists():
            return fail(f"Missing required file: {relative_path}")

    version = (repo_root / "VERSION").read_text(encoding="utf-8").strip()
    if not version:
        return fail("VERSION is empty")

    skill_text = (repo_root / "SKILL.md").read_text(encoding="utf-8")
    if "Prompt Efficacy Scorecard" not in skill_text:
        return fail("SKILL.md is missing the response contract heading")

    readme_text = (repo_root / "README.md").read_text(encoding="utf-8")
    if version not in readme_text:
        return fail("README.md does not mention the current version")
    if "MIT" not in readme_text:
        return fail("README.md does not mention the MIT license")

    openai_yaml = (repo_root / "agents" / "openai.yaml").read_text(encoding="utf-8")
    for key in ("display_name:", "short_description:", "default_prompt:"):
        if key not in openai_yaml:
            return fail(f"agents/openai.yaml is missing {key}")

    evals_path = repo_root / "evals" / "evals.json"
    eval_data = json.loads(evals_path.read_text(encoding="utf-8"))
    evals = eval_data.get("evals", [])
    if len(evals) < 5:
        return fail("evals/evals.json must contain at least 5 evals")

    sample_outputs_dir = repo_root / "sample-outputs"
    if not sample_outputs_dir.exists():
        return fail("sample-outputs directory is missing")

    sample_outputs = list(sample_outputs_dir.glob("*.md"))
    if len(sample_outputs) < 3:
        return fail("sample-outputs must contain at least 3 markdown examples")

    model_examples = (repo_root / "references" / "model-specific-examples.md").read_text(
        encoding="utf-8"
    )
    for model_name in ("gpt-5.2", "gpt-5.2-codex", "gpt-5-mini", "gpt-5-nano"):
        if model_name not in model_examples:
            return fail(f"model-specific examples are missing {model_name}")

    print("PASS: repository structure and validation checks look good")
    print(f"PASS: version {version}")
    print(f"PASS: eval count {len(evals)}")
    print(f"PASS: sample outputs {len(sample_outputs)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
