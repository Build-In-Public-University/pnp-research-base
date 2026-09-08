from dataclasses import asdict, dataclass


@dataclass(frozen=True)
class ProblemInstance:
    instance_id: str
    input_length: int
    certificate_length: int
    dependency_edges: int


@dataclass(frozen=True)
class Architecture:
    name: str
    nodes: int
    communication_hops: int
    replication_factor: int
    validation_rounds: int
    review_units: int


def run_case(problem: ProblemInstance, architecture: Architecture) -> dict:
    if problem.input_length < 1 or problem.certificate_length < 0:
        raise ValueError("invalid problem size")
    if min(architecture.nodes, architecture.communication_hops, architecture.replication_factor,
           architecture.validation_rounds) < 1:
        raise ValueError("architecture counts must be positive")
    # Formal layer: a deliberately linear certificate checker.
    local_verify_ops = problem.input_length + problem.certificate_length
    transport_ops = architecture.communication_hops * architecture.replication_factor
    coordination_ops = problem.dependency_edges * max(architecture.nodes - 1, 0)
    reproduction_ops = local_verify_ops * max(architecture.replication_factor - 1, 0)
    revalidation_ops = local_verify_ops * architecture.validation_rounds
    review_ops = architecture.review_units
    total = (local_verify_ops + transport_ops + coordination_ops +
             reproduction_ops + revalidation_ops + review_ops)
    return {
        "instance_id": problem.instance_id,
        "architecture": architecture.name,
        "input_length": problem.input_length,
        "certificate_length": problem.certificate_length,
        "dependency_edges": problem.dependency_edges,
        "local_verify_ops": local_verify_ops,
        "transport_ops": transport_ops,
        "coordination_ops": coordination_ops,
        "reproduction_ops": reproduction_ops,
        "revalidation_ops": revalidation_ops,
        "review_ops": review_ops,
        "network_ops": total - local_verify_ops,
        "total_lifecycle_ops": total,
        "formal_relation_held_fixed": True,
    }


def fixture() -> tuple[list[ProblemInstance], list[Architecture]]:
    problems = [
        ProblemInstance("sat-small", 16, 8, 3),
        ProblemInstance("sat-medium", 64, 32, 12),
        ProblemInstance("sat-large", 256, 128, 48),
    ]
    architectures = [
        Architecture("centralized", 1, 1, 1, 1, 1),
        Architecture("chain", 4, 3, 1, 1, 2),
        Architecture("star", 4, 3, 2, 2, 3),
        Architecture("dense", 4, 6, 2, 2, 5),
    ]
    return problems, architectures


def receipt() -> dict:
    problems, architectures = fixture()
    rows = [run_case(p, a) for p in problems for a in architectures]
    by_architecture = {}
    for row in rows:
        by_architecture.setdefault(row["architecture"], []).append(row)
    summary = {}
    for name, values in by_architecture.items():
        summary[name] = {
            "mean_local_verify_ops": sum(v["local_verify_ops"] for v in values) / len(values),
            "mean_network_ops": sum(v["network_ops"] for v in values) / len(values),
            "mean_total_lifecycle_ops": sum(v["total_lifecycle_ops"] for v in values) / len(values),
        }
    return {
        "protocol": "pnp-network-architecture-v0.1",
        "status": "synthetic_fixture",
        "claim_ids": ["CLAIM-001", "CLAIM-002"],
        "rows": rows,
        "summary": summary,
        "falsifiers": [
            "network_ops invariant across architectures",
            "architecture effect disappears after controlling local_verify_ops",
            "centralized baseline dominates at equal correctness",
        ],
    }
