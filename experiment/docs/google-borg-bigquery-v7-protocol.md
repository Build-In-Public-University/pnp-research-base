# Google Borg BigQuery v7 protocol

This protocol applies the frozen first-24-hour attempt reconstruction to cell `b` and stratifies each attempt by the scheduler-relevant metadata present in `instance_events`: `priority`, `scheduling_class`, `collection_type`, and coarse bins of `resource_request.cpus` and `resource_request.memory`.

The query emits aggregate counts, terminal outcomes, right-censoring, and duration quantiles per stratum. Resource bins are deliberately coarse. The query excludes user, collection-name, and constraint content.

An independent conservation audit must reconcile every stratum total with the v3 cell-b attempt total before interpretation.
