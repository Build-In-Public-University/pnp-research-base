import argparse,hashlib,json
from pathlib import Path
from pnp_architecture.morphology_transition_cost_phase_sweep_v1 import experiment
ROOT=Path(__file__).resolve().parents[2]
def main():
    p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True);p.add_argument('--summary',type=Path,required=True);a=p.parse_args();r=experiment();r['protocol_sha256']=hashlib.sha256((ROOT/'experiment/docs/protocol-morphology-transition-cost-phase-sweep-v1.md').read_bytes()).hexdigest();r['source_sha256']=hashlib.sha256((ROOT/'experiment/src/pnp_architecture/morphology_transition_cost_phase_sweep_v1.py').read_bytes()).hexdigest();a.output.write_text(json.dumps(r,sort_keys=True,indent=2)+'\n');lines=['# Morphology transition-cost phase sweep v1','', '| S_RL | S_LR | Heuristic | Optimal | Regret | H lock-in | O lock-in | Switches | Optimal switches |','|---:|---:|---:|---:|---:|---:|---:|---:|---:|'];lines += [f"| {x['S_RL']} | {x['S_LR']} | {x['total_cost']:.2f} | {x['optimal_cost']:.2f} | {x['regret_vs_optimal']:.2f} | {x['lock_in_rate']:.3f} | {x['optimal_lock_in_rate']:.3f} | {x['switches']} | {x['optimal_switches']} |" for x in r['rows']];a.summary.write_text('\n'.join(lines)+'\n');print('\n'.join(lines))
if __name__=='__main__':main()
