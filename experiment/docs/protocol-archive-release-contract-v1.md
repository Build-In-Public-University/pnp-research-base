# Archive release-contract calibration v1

Use the repository's actual `manifest.json` as the release payload inventory and a versioned compatibility declaration as the reader contract. The validator checks JSON structure, file presence, byte counts, and SHA-256 digests from the real repository checkout.

The transition contract requires a migration receipt when both the release manifest and compatibility declaration change in the same release. Compare an ordinary state checker (current files only) with a transition-aware checker receiving previous files and the declared changed-file set.

Run three paths: manifest-only, compatibility-only, and simultaneous. The current-state inputs for the simultaneous and a sequentially completed release can be identical; the transition record distinguishes whether both changes occurred atomically. The independent oracle is the contract validator itself, not a cached policy result.

This is a local release-protocol calibration over actual repository artifacts and temporary copies. The migration rule is a newly declared research-repo contract, not an existing production policy. No external release or deployment is performed.
