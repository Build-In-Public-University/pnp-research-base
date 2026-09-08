"""Independent tiny exhaustive oracle for the containing-problem boundary."""
import itertools
import unittest


class QuantifierBoundaryTests(unittest.TestCase):
    def test_every_clause_has_witness_but_conjunction_has_none(self):
        assignments = list(itertools.product([False, True], repeat=3))
        clauses = list(itertools.product([False, True], repeat=3))
        def check(assignment, clause):
            return any(a == sign for a, sign in zip(assignment, clause))
        self.assertEqual([sum(check(a, c) for a in assignments) for c in clauses], [7] * 8)
        self.assertEqual(sum(all(check(a, c) for c in clauses) for a in assignments), 0)

    def test_conflicting_witnesses_do_not_prove_unsatisfiability(self):
        # (x OR y) and (not x OR y): x differs in two chosen local witnesses,
        # but y=True supplies a global witness. Rejection is not UNSAT.
        clauses = (lambda x, y: x or y, lambda x, y: not x or y)
        self.assertTrue(clauses[0](True, False))
        self.assertTrue(clauses[1](False, False))
        self.assertTrue(all(c(False, True) for c in clauses))
