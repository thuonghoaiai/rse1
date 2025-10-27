import sys
import os
import glob
import yaml
from typing import List, Tuple

REQUIRED_FIELDS = ["metric_name", "description", "owner", "schedule", "sql"]


def validate_yaml_file(path: str) -> Tuple[bool, List[str]]:
    errors: List[str] = []
    try:
        with open(path, "r", encoding="utf-8") as f:
            doc = yaml.safe_load(f)
    except Exception as e:
        return False, [f"YAML parse error in {path}: {e}"]

    if not isinstance(doc, dict):
        return False, [f"YAML root must be a mapping/object in {path}"]

    for field in REQUIRED_FIELDS:
        if field not in doc:
            errors.append(f"Missing required field: {field}")

    # Basic content checks
    if "metric_name" in doc and not str(doc["metric_name"]).strip():
        errors.append("metric_name cannot be empty")

    if "sql" in doc:
        sql_val = str(doc["sql"]).strip()
        if not sql_val:
            errors.append("sql cannot be empty")
        # quick sanity check: allow SELECT ... or WITH ...
        sql_lower = sql_val.lower()
        if not (sql_lower.startswith("select") or sql_lower.startswith("with")):
            errors.append("sql should start with SELECT or WITH")

    ok = len(errors) == 0
    return ok, errors


def main() -> int:
    metrics_dir = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(__file__), "..", "metrics")
    metrics_dir = os.path.abspath(metrics_dir)
    paths = sorted(glob.glob(os.path.join(metrics_dir, "*.yaml")))
    if not paths:
        print(f"No YAML files found in {metrics_dir}")
        return 1

    overall_ok = True
    for path in paths:
        ok, errors = validate_yaml_file(path)
        if ok:
            print(f"OK: {os.path.basename(path)}")
        else:
            overall_ok = False
            print(f"ERRORS in {os.path.basename(path)}:")
            for e in errors:
                print(f"  - {e}")

    return 0 if overall_ok else 2


if __name__ == "__main__":
    raise SystemExit(main())
