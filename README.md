# Self-Serve User Metrics System (Prototype)

A simple prototype so Data Analysts can define customer metrics in YAML + SQL and materialize them in DuckDB.

## Requirements

- Python 3.9+
- pip

Install dependencies:

```bash
pip install -r requirements.txt
```

## Dataset

We include a tiny sample of the Olist dataset under `/data` for quick testing. The scripts will load:
- `data/customers.csv`
- `data/orders.csv`
- `data/order_items.csv`

In a real run, replace these with the full CSVs from the assignment.

## Validate metric YAMLs

Checks required fields and basic SQL presence.

```bash
python src/validate_yaml.py metrics
```

Output shows `OK:` or specific errors for each YAML file.

## Execute metrics

Loads CSVs into DuckDB, then creates or replaces a table for each metric.

```bash
python src/run_metrics.py
```

Results:
- DuckDB database at `metrics.duckdb`
- Metric tables, e.g. `lifetime_revenue`, `avg_order_revenue`
- Registry table `metric_registry` with metadata (name, description, owner, schedule)

You can inspect results with DuckDB CLI:

```bash
duckdb metrics.duckdb
-- then inside DuckDB
SELECT * FROM lifetime_revenue;
SELECT * FROM avg_order_revenue;
SELECT * FROM metric_registry;
```

## Add a new metric

1. Create a new YAML in `/metrics`, for example `total_orders_last_10_days.yaml`:

```yaml
metric_name: total_orders_last_10_days
description: Total number of orders placed by each customer in the last 10 days
owner: data.analyst@shopback.com
schedule: "0 8 * * *" # metadata only
sql: |
  SELECT
    o.customer_id,
    COUNT(*) AS total_orders_last_10_days
  FROM orders o
  WHERE o.order_purchase_timestamp >= DATE '2023-09-01'
  GROUP BY 1
```

2. Validate it:

```bash
python src/validate_yaml.py metrics
```

3. Execute metrics to materialize the table:

```bash
python src/run_metrics.py
```

The new table will be created or replaced in `metrics.duckdb` with the name `total_orders_last_10_days`.

## Notes

- The `schedule` field is stored as metadata only; no scheduler is implemented.
- For production, validation would run in CI on pull requests.
- Include `metrics.duckdb` in submissions if desired to show results.
