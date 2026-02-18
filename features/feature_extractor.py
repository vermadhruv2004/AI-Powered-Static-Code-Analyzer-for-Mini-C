# feature_extractor.py
# Extracts numerical features from AST, CFG, and Data Flow Analysis

from ast_nodes.ast_analyzer import ASTAnalyzer
from cfg.cfg_builder import ControlFlowGraph
from data_flow.data_flow_analyzer import DataFlowAnalyzer


# --------------------------------------------------
# Feature Extractor
# --------------------------------------------------

class FeatureExtractor:
    def __init__(self):
        pass

    # --------------------------------------------------
    # Main feature extraction function
    # --------------------------------------------------
    def extract(self, ast_root, cfg: ControlFlowGraph):
        """
        Returns a dictionary of numeric features
        """

        # ---------- AST FEATURES ----------
        ast_analyzer = ASTAnalyzer()
        ast_report = ast_analyzer.analyze(ast_root)

        # ---------- DATA FLOW FEATURES ----------
        dfa = DataFlowAnalyzer(cfg)
        df_report = dfa.analyze()

        # ---------- CFG FEATURES ----------
        cfg_nodes = len(cfg.nodes)
        cfg_edges = sum(len(node.next) for node in cfg.nodes)

        # ---------- FEATURE VECTOR ----------
        features = {
            # AST-based
            "ast_max_depth": ast_report["ast_max_depth"],
            "unused_variables": len(ast_report["unused_variables"]),
            "if_statements": ast_report["if_statements"],
            "assignments": ast_report["assignments"],

            # CFG-based
            "cfg_nodes": cfg_nodes,
            "cfg_edges": cfg_edges,

            # Data-flow-based
            "use_before_init": sum(
                1 for w in df_report["warnings"]
                if "Use before initialization" in w
            ),
            "dead_assignments": sum(
                1 for w in df_report["warnings"]
                if "Dead assignment" in w
            ),
        }

        return features


# --------------------------------------------------
# Testing the Feature Extractor
# --------------------------------------------------
if __name__ == "__main__":
    from ast_nodes.ast_builder import build_ast
    from cfg.cfg_builder import CFGBuilder

    parse_tree = (
        'program',
        [
            ('declaration', 'int', 'a'),
            ('assign', 'a', ('number', 10)),
            ('assign', 'b', ('identifier', 'a')),
            ('if',
             ('binop', '>', ('identifier', 'a'), ('number', 5)),
             [
                 ('assign', 'a',
                  ('binop', '+', ('identifier', 'a'), ('number', 1)))
             ])
        ]
    )

    ast = build_ast(parse_tree)
    cfg = CFGBuilder().build(ast)

    extractor = FeatureExtractor()
    features = extractor.extract(ast, cfg)

    print("Extracted Features:")
    for k, v in features.items():
        print(f"{k}: {v}")
