# data_flow_analyzer.py
# Performs Data Flow Analysis on Control Flow Graph (CFG)

from cfg.cfg_builder import CFGNode, ControlFlowGraph


# --------------------------------------------------
# Data Flow Analyzer
# --------------------------------------------------

class DataFlowAnalyzer:
    def __init__(self, cfg: ControlFlowGraph):
        self.cfg = cfg
        self.in_sets = {}
        self.out_sets = {}

        self.warnings = []

    # --------------------------------------------------
    # Main analysis function
    # --------------------------------------------------
    def analyze(self):
        """
        Forward data-flow analysis to detect:
        - Use before initialization
        - Dead assignments
        """

        # Initialize IN and OUT sets
        for node in self.cfg.nodes:
            self.in_sets[node.id] = set()
            self.out_sets[node.id] = set()

        changed = True
        while changed:
            changed = False
            for node in self.cfg.nodes:
                in_set = self._compute_in(node)
                out_set = self._compute_out(node, in_set)

                if in_set != self.in_sets[node.id] or out_set != self.out_sets[node.id]:
                    self.in_sets[node.id] = in_set
                    self.out_sets[node.id] = out_set
                    changed = True

        self._detect_issues()

        return self._report()

    # --------------------------------------------------
    # IN[n] = union of OUT[pred]
    # --------------------------------------------------
    def _compute_in(self, node):
        in_set = set()
        for pred in self._predecessors(node):
            in_set |= self.out_sets[pred.id]
        return in_set

    # --------------------------------------------------
    # OUT[n] = GEN ∪ (IN − KILL)
    # --------------------------------------------------
    def _compute_out(self, node, in_set):
        gen, kill = self._gen_kill(node)
        return gen | (in_set - kill)

    # --------------------------------------------------
    # GEN / KILL computation
    # --------------------------------------------------
    def _gen_kill(self, node):
        gen = set()
        kill = set()

        label = node.label

        # Assignment: x = ...
        if "=" in label and not label.startswith("if"):
            var = label.split("=")[0].strip()
            gen.add(var)
            kill.add(var)

        return gen, kill

    # --------------------------------------------------
    # Predecessor calculation
    # --------------------------------------------------
    def _predecessors(self, node):
        preds = []
        for n in self.cfg.nodes:
            if node in n.next:
                preds.append(n)
        return preds

    # --------------------------------------------------
    # Issue Detection
    # --------------------------------------------------
    def _detect_issues(self):
        for node in self.cfg.nodes:
            label = node.label

            # Detect use before initialization
            if "=" in label:
                rhs_vars = self._extract_rhs_vars(label)
                for var in rhs_vars:
                    if var not in self.in_sets[node.id]:
                        self.warnings.append(
                            f"Use before initialization: '{var}' in node {node.id}"
                        )

            # Dead assignment detection
            if "=" in label:
                var = label.split("=")[0].strip()
                used_later = False
                for succ in node.next:
                    if var in self.in_sets.get(succ.id, set()):
                        used_later = True
                if not used_later:
                    self.warnings.append(
                        f"Dead assignment: '{var}' at node {node.id}"
                    )

    # --------------------------------------------------
    # Helper: Extract RHS variables
    # --------------------------------------------------
    def _extract_rhs_vars(self, label):
        rhs = label.split("=")[1]
        tokens = rhs.replace("+", " ").replace("-", " ") \
                    .replace("*", " ").replace("/", " ") \
                    .split()
        return [tok for tok in tokens if tok.isidentifier()]

    # --------------------------------------------------
    # Report
    # --------------------------------------------------
    def _report(self):
        return {
            "in_sets": self.in_sets,
            "out_sets": self.out_sets,
            "warnings": self.warnings
        }


# --------------------------------------------------
# Testing the Data Flow Analyzer
# --------------------------------------------------
if __name__ == "__main__":
    from ast_nodes.ast_builder import build_ast
    from cfg.cfg_builder import CFGBuilder

    parse_tree = (
        'program',
        [
            ('declaration', 'int', 'a'),
            ('assign', 'a', ('number', 10)),
            ('assign', 'b', ('identifier', 'a')),   # b used before declaration
        ]
    )

    ast = build_ast(parse_tree)

    cfg = CFGBuilder().build(ast)

    analyzer = DataFlowAnalyzer(cfg)
    report = analyzer.analyze()

    print("Data Flow Analysis Report:")
    for w in report["warnings"]:
        print("-", w)
