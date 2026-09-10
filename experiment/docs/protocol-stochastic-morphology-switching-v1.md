# Stochastic morphology switching calibration v1

Generate a deterministic Markov demand path over `d={0.1,1.5,4.0}` for 500 periods using seed 1337. Compare stateless cheapest-now routing (threshold 1), symmetric switching-cost routing (enter/exit thresholds 1.25/0.75), and asymmetric adaptive morphology (thresholds 2.25/0.25). Operating costs are remote `3d`, local `d+2`; each policy pays its declared switch costs. Regret is measured against the cheaper always-remote or always-local baseline on the same realized path.
