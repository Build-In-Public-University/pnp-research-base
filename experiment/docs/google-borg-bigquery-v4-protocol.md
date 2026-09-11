# Google Borg BigQuery v4 protocol

This protocol joins the first-24-hour attempt-level reconstruction to five-minute event buckets from the same public Borg `instance_events` table. It emits aggregate arrival counts (`SUBMIT`), admissions (`SCHEDULE`), terminal/interruption events, closed attempts, right-censored attempts, and per-bucket attempt-duration summaries.

The query preserves arrival buckets even when no attempt aggregate is present. Bucket 0 is reported separately because the trace begins with a large startup population and therefore contains left-truncation/boundary contamination. Missing bucket indices are retained in the receipt.

No raw task rows, IDs, user fields, or names are exported.
