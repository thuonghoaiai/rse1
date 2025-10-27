import os
import glob
import yaml
import duckdb
from typing import Dict, Any
import re

HERE = os.path.dirname(__file__)
ROOT = os.path.abspath(os.path.join(HERE, ".."))
METRICS_DIR = os.path.join(ROOT, "metrics")
DATA_DIR = os.path.join(ROOT, "data")
DB_PATH = os.path.join(ROOT, "metrics.duckdb")

REQUIRED_FIELDS = ["metric_name", "description", "owner", "schedule", "sql"]


def load_csvs(connection: duckdb.DuckDBPyConnection) -> None:
    # Load or replace base tables
    connection.execute("CREATE OR REPLACE TABLE customers AS SELECT * FROM read_csv_auto(?)", [os.path.join(DATA_DIR, "customers.csv")])
    connection.execute("CREATE OR REPLACE TABLE orders AS SELECT * FROM read_csv_auto(?)", [os.path.join(DATA_DIR, "orders.csv")])
    connection.execute("CREATE OR REPLACE TABLE order_items AS SELECT * FROM read_csv_auto(?)", [os.path.join(DATA_DIR, "order_items.csv")])


def run_one_metric(connection: duckdb.DuckDBPyConnection, metric: Dict[str, Any]) -> None:
    metric_name = metric["metric_name"]
    sql = metric["sql"]
    # Ensure metric_name is a safe SQL identifier
    if not re.match(r"^[A-Za-z_][A-Za-z0-9_]*$", metric_name):
        raise ValueError(
            f"Invalid metric_name '{metric_name}'. Use letters, numbers, and underscores only, starting with a letter/underscore."
        )
    # Materialize the result into a table named after the metric
    connection.execute(f"CREATE OR REPLACE TABLE {metric_name} AS {sql}")

    # Store metric metadata in a registry table for visibility
    connection.execute(
        """
        CREATE TABLE IF NOT EXISTS metric_registry (
            metric_name TEXT PRIMARY KEY,
            description TEXT,
            owner TEXT,
            schedule TEXT
        )
        """
    )
    connection.execute(
        "INSERT OR REPLACE INTO metric_registry VALUES (?, ?, ?, ?)",
        [metric.get("metric_name"), metric.get("description"), metric.get("owner"), metric.get("schedule")],
    )


def main() -> int:
    # Connect to DuckDB
    con = duckdb.connect(DB_PATH)

    # Load base data
    load_csvs(con)

    # Read metrics
    metric_files = sorted(glob.glob(os.path.join(METRICS_DIR, "*.yaml")))
    if not metric_files:
        print(f"No metric YAML files found in {METRICS_DIR}")
        return 1

    for path in metric_files:
        with open(path, "r", encoding="utf-8") as f:
            metric = yaml.safe_load(f)
        # Validate minimal fields before execution
        for field in REQUIRED_FIELDS:
            if field not in metric or (isinstance(metric[field], str) and not metric[field].strip()):
                raise ValueError(f"{os.path.basename(path)} is missing required field: {field}")
        print(f"Executing metric: {metric['metric_name']}")
        run_one_metric(con, metric)

    print(f"Done. DuckDB at: {DB_PATH}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
