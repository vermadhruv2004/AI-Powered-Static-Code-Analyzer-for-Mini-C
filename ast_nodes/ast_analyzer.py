# ast_analyzer.py
# Performs static analysis on the AST

from ast_nodes.ast_builder import (
    ProgramNode,
    DeclarationNode,
    AssignmentNode,
    IfNode,
    BinaryOpNode,
    IdentifierNode,
    NumberNode
)

# --------------------------------------------------
# AST Analyzer Class
# --------------------------------------------------

class ASTAnalyzer:
    def __init__(self):
        self.declared_vars = set()
        self.used_vars = set()
        self.unused_vars = set()

        self.max_depth = 0
        self.current_depth = 0

        self.if_count = 0
        self.assignment_count = 0

        self.warnings = []

    # --------------------------------------------------
    # Entry point
    # --------------------------------------------------
    def analyze(self, ast_root):
        self._visit(ast_root)
        self._finalize()
        return self._report()

    # --------------------------------------------------
    # Visitor dispatcher
    # --------------------------------------------------
    def _visit(self, node):
        if node is None:
            return

        self.current_depth += 1
        self.max_depth = max(self.max_depth, self.current_depth)

        if isinstance(node, ProgramNode):
            for stmt in node.statements:
                self._visit(stmt)

        elif isinstance(node, DeclarationNode):
            self.declared_vars.add(node.identifier)

        elif isinstance(node, AssignmentNode):
            self.assignment_count += 1
            self.used_vars.add(node.identifier)
            self._visit(node.expression)

        elif isinstance(node, IfNode):
            self.if_count += 1
            self._visit(node.condition)
            for stmt in node.body:
                self._visit(stmt)

        elif isinstance(node, BinaryOpNode):
            self._visit(node.left)
            self._visit(node.right)

        elif isinstance(node, IdentifierNode):
            self.used_vars.add(node.name)

        elif isinstance(node, NumberNode):
            pass  # No action needed

        self.current_depth -= 1

    # --------------------------------------------------
    # Post-processing
    # --------------------------------------------------
    def _finalize(self):
        self.unused_vars = self.declared_vars - self.used_vars

        for var in self.unused_vars:
            self.warnings.append(
                f"Warning: Variable '{var}' declared but never used"
            )

        if self.max_depth > 10:
            self.warnings.append(
                f"Warning: High AST depth ({self.max_depth}) — code may be complex"
            )

    # --------------------------------------------------
    # Analysis Report
    # --------------------------------------------------
    def _report(self):
        return {
            "declared_variables": list(self.declared_vars),
            "used_variables": list(self.used_vars),
            "unused_variables": list(self.unused_vars),
            "ast_max_depth": self.max_depth,
            "if_statements": self.if_count,
            "assignments": self.assignment_count,
            "warnings": self.warnings
        }


# --------------------------------------------------
# Testing the AST Analyzer
# --------------------------------------------------
if __name__ == "__main__":
    from ast_builder import build_ast

    parse_tree = (
        'program',
        [
            ('declaration', 'int', 'a'),
            ('declaration', 'int', 'b'),
            ('assign', 'a', ('number', 10)),
            ('if',
             ('binop', '>', ('identifier', 'a'), ('number', 5)),
             [
                 ('assign', 'a',
                  ('binop', '+', ('identifier', 'a'), ('number', 1)))
             ])
        ]
    )

    ast = build_ast(parse_tree)

    analyzer = ASTAnalyzer()
    report = analyzer.analyze(ast)

    print("AST Analysis Report:")
    for key, value in report.items():
        print(f"{key}: {value}")
