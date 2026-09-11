# Queue migration v4 trace-2 protocol note

This is a second application of the frozen `queue-migration-v4` protocol, not a mutation of the first receipt.

Source:

```text
conversation/subagents/worker-7/records.jsonl
```

Source SHA-256:

```text
6903037bdbad8b0fc3b6d48d61e264bc8a30cbe1a3808ca9ecbb56581b067c9e
```

The same metadata-only rule applies: timestamps and role labels are used; message content is excluded from emitted artifacts. The same generation-capacity sweep, capacity-release ladder, finite drain bound, and independent flow audit are applied without retuning.

This is an independent archive trace within the same exported corpus, not an independent organization or external deployment. It therefore tests trace sensitivity, not population generality.
