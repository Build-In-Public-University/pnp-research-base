# History v1.1 — reviewer corrections and current results

Current receipt: artifacts/history_v1_1.json; generated summary: artifacts/history_v1_1-summary.md. These supersede COST comparisons in v1, while original receipts and their source commit febc3e6 remain intact. The frozen original protocol has a separately frozen amendment in docs/protocol-history-v1.1.md. No workload or policy retuning.

## Reviewer findings resolved

1. Total updates executed two reads/writes but counted one each. Counts now charge two of each. New regression initially FAILED (4 != 8), then passes.
2. Runner could execute a differently resolved package while hashing local source. It now verifies imported module path matches checkout before invoking experiment. Wrong-package regression initially FAILED because foreign experiment executed; now fails closed with explicit mismatch and no receipt.
3. Empty-feed hidden-change regression could miss an omniscient read during dirty repair. Added a delivered and omitted mutation sharing a dirty subproblem, requiring output from cached observations only. It passes; no actual state leak was found. Post-run randomized property coverage also remains.
4. Generated readable summary now includes strict observed-correctness winners separately from unrestricted priced winners. Eligibility is retrospective, not a future safety guarantee.

## Corrected representative counts

n=64, seed=1, initialization plus 32 updates. Unit-weight listed operation proxy, NOT runtime/energy.

| Changes/update | Cold | Snapshot repair | Unchecked | Complete-feed repair |
|---|---:|---:|---:|---:|
| 0 | 40,161 | 8,065 | 1,249 | 1,921 |
| 1 | 40,161 | 11,425 | 1,249 | 5,377 |
| 16 | 40,161 | 46,633 | 1,249 | 42,025 |
| 64 | 40,161 | 75,649 | 1,249 | 75,649 |

Cold and snapshot remain exact. With complete feed, feed repair remains exact. Unchecked wrong-output counts remain 0/32/32/24 in these rows. Omitted-feed repair retains all its original errors; only work accounting changes.

Important reversed result: at n=64, 16 changes/update, complete-feed repair loses to cold recomputation for all three seeds. v1's claimed advantage in these cells was an accounting artifact. Across 48 cells, strict observed-correctness winners are now unchecked 12 (no-change controls), feed repair 6, snapshot repair 6, cold 24. Do not count paired feed conditions or identical seeded worlds as independent population observations.

Sparse omitted-feed snapshot count is now 11,425; unchecked break-even against it changes from 310 to 318 proxy units per wrong output. Sparse complete-feed unchecked break-even changes from 121 to 129. Prices are synthetic penalties for full-output contract errors, not measured failure losses. The Boolean acceptance decision still need not be wrong when the returned vector is wrong.

## Verification

43 tests passed in 3.207 seconds. Two corrected JSON receipts and summaries are byte-identical. All corrected source hashes matched on independent readback. Compared every one of 6,336 policy-step records with v1: inputs, world identities, returned values and error flags unchanged; corrected cost exactly equals old cost plus two per dirty-output total update. All consequence cost identities and winners recomputed. Three strict-winner cells changed, explicitly recorded above. Old v1, gate, and graph receipts unchanged.

The detailed mechanism boundaries in docs/history-v1-results.md still apply. Current quantitative claims must cite v1.1, not that historical readout. This remains a finite polynomial dynamic computation, not AI training, a general search lower bound, a physical energy result or P/NP evidence.
