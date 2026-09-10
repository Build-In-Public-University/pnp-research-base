# Morphology transition-cost phase sweep v1

Use a deterministic continuous demand path of 500 periods, with values generated around the instantaneous operating crossover d=1. For each pair (S_RL,S_LR) in {0,2,6,10,20}^2, use a four-step threshold policy: enter local when d > 1 + S_RL/8 and exit to remote when d < 1 - S_LR/8. Report operating cost, transition cost, switch count, occupancy, regret against the best fixed morphology, and lock-in rate: periods in local while d<1 or remote while d>1. Costs are synthetic modeled quantities.
