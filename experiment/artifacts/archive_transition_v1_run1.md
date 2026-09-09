# Archive transition interaction calibration v1

| Case | Singleton exact | State exact | Transition exact | Oracle artifacts |
|---|---|---|---|---|
| manifest_only | True | True | True | compatibility-check,manifest-check,provenance |
| compat_only | True | True | True | compatibility-check,manifest-check,provenance |
| both | False | False | True | compatibility-check,manifest-check,migration-approval,provenance |

The transition rule is explicit and application-specific; it is not inferred semantic evidence.
