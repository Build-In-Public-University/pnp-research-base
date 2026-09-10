# Capability-space routing calibration v1: results

The system starts at node `i` with local capability `{parity}`. The contract requires the composite capability `{parity, group}`. Node `j` contains `group`, but that capability is not initially known or reachable from `i`.

The least-cost valid route is:

\[
\text{discover}
\rightarrow
\text{move}
\rightarrow
\text{connect}
\rightarrow
\text{transfer}
\rightarrow
\text{compose}
\]

with modeled cost:

\[
1+5+2+2+1=11.
\]

Discovery changes knowledge of the capability graph but does not add the capability itself. Transfer changes the reachable capability set. Composition becomes valid only after `{group}` has been transferred beside local `{parity}`.

The experiment demonstrates:

\[
\boxed{
\mathcal K_t\xrightarrow{a_t}\mathcal K_{t+1}
}
\]

where actions can change which capabilities are reachable, not merely change the agent's belief about a fixed capability set.

This is a finite synthetic routing result. Costs, nodes, and capabilities are modeled; it is not a measurement of a physical network or a P/NP result.
