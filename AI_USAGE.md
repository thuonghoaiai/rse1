# AI Usage Notes

This file documents how I used AI to complete the assignment.

## 1) Scaffold project and dataset
- Prompt: "Create a minimal, clear folder structure for a self-serve metrics system using YAML + DuckDB."
- Outcome: I created `/data`, `/metrics`, `/src`, and generated tiny CSV samples so scripts run end-to-end. Learned to keep structure simple and explain it in README.

## 2) YAML validation logic
- Prompt: "Write a Python function to validate YAML has keys: metric_name, description, owner, schedule, sql; include basic checks."
- Outcome: Generated initial function using PyYAML, then I added stricter SQL shape check (must start with SELECT or WITH). Learned to keep error messages actionable.

## 3) DuckDB execution and safety
- Prompt: "Safely create or replace a table from SQL in DuckDB given a metric name; escape identifier."
- Outcome: AI suggested escaping; my environment lacked `duckdb.escape_identifier` so I used a conservative regex to validate `metric_name` and interpolated safely. Learned to adapt suggestions to installed package APIs.

## 4) Designing example metrics
- Prompt: "Write SQL for lifetime revenue per customer and average order revenue using orders and order_items tables."
- Outcome: Implemented two metrics via a reusable `order_revenue` CTE. Validated results with sample data.

## 5) Documentation flow
- Prompt: "Write a concise README: setup, validate, run, add a metric."
- Outcome: Produced a short, step-by-step README with commands and tips about the `schedule` metadata.

Optional: I can share the full AI chat log on request.
