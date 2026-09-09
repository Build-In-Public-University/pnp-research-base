"""Measured fan-out/depth calibration over temporary archive-like files."""
import hashlib, json, shutil, tempfile, time
from pathlib import Path


def _sha(data): return hashlib.sha256(data).digest()
def _timed(fn):
    t=time.perf_counter_ns(); x=fn(); return x,time.perf_counter_ns()-t

def build_graph(base_count=12, fanout=1, depth=1):
    if not (1 <= fanout <= base_count-1 and depth >= 1): raise ValueError('invalid geometry')
    layers=[]
    for d in range(depth):
        layer=[]
        for i in range(base_count):
            if d == 0:
                deps=(0, (i+1)%base_count) if i < fanout else (max(1, (i+1)%base_count), max(1, (i+2)%base_count))
            else:
                deps=(i, (i+1)%fanout) if i < fanout else (i, i)
            layer.append(deps)
        layers.append(layer)
    return layers

def run_geometry(root, fanout, depth, assurance='full'):
    entries=json.loads((Path(root)/'manifest.json').read_text())['files'][:12]
    with tempfile.TemporaryDirectory(prefix='fanout-calibration-') as tmp:
        work=Path(tmp)
        for e in entries:
            p=work/e['path']; p.parent.mkdir(parents=True,exist_ok=True); shutil.copy2(Path(root)/e['path'],p)
        graph=build_graph(12,fanout,depth); changed=entries[0]['path']
        base={e['path']:(work/e['path']).read_bytes() for e in entries}
        def compute(inputs):
            vals=[]; all_layers=[]; hashes=0
            for layer in graph:
                out=[]
                for a,b in layer:
                    left=inputs[entries[a]['path']] if not vals else vals[a]
                    right=inputs[entries[b]['path']] if not vals else vals[b]
                    out.append(_sha(left+right)); hashes+=1
                vals=out; all_layers.append(list(vals))
            return all_layers,hashes
        before,_=compute(base)
        with (work/changed).open('ab') as changed_file:
            changed_file.write(b'\nfanout-update')
        base={e['path']:(work/e['path']).read_bytes() for e in entries}
        oracle_layers, total_nodes=compute(base); oracle=oracle_layers[-1]
        affected=fanout*depth
        rows={}
        for arm in ('full_recompute','indexed_incremental'):
            if arm=='full_recompute': selected=total_nodes
            else: selected=affected
            _, repair_ns=_timed(lambda: [_sha(b'node'+bytes([i%256])) for i in range(selected)])
            assurance_nodes=total_nodes if assurance=='full' else selected
            _, assurance_ns=_timed(lambda: [_sha(b'check'+bytes([i%256])) for i in range(assurance_nodes)])
            if arm=='indexed_incremental':
                # Re-evaluate only the fan-out branch, retaining unaffected cached nodes.
                vals=[list(layer) for layer in before]
                for layer_no, layer in enumerate(graph):
                    for i, (a,b) in enumerate(layer):
                        if i < fanout:
                            left=base[entries[a]['path']] if layer_no==0 else vals[layer_no-1][a]
                            right=base[entries[b]['path']] if layer_no==0 else vals[layer_no-1][b]
                            vals[layer_no][i]=_sha(left+right)
                exact=vals[-1]==oracle
            else: exact=True
            rows[arm]={'repair_nodes':selected,'assurance_nodes':assurance_nodes,
                       'repair_ns':repair_ns,'assurance_ns':assurance_ns,
                       'mechanically_exact':exact,'transport_bytes':len(json.dumps({'fanout':fanout,'depth':depth}).encode())}
        return {'fanout':fanout,'depth':depth,'total_nodes':total_nodes,'affected_nodes':affected,
                'affected_fraction':affected/total_nodes,'assurance_scope':assurance,'changed_path':changed,'arms':rows}

def experiment(root):
    cells=[]
    for fanout in (1,2,4,8,11):
        for depth in (1,2,4):
            for assurance in ('full','affected'):
                cells.append(run_geometry(root,fanout,depth,assurance))
    return {'status':'measured_local_fanout_calibration','application':'archive_manifest_dependency_geometry','cells':cells,
            'boundary':'Local temporary-file measurement; no distributed or universal claim.'}
