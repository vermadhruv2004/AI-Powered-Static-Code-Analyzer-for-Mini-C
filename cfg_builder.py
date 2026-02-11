# cfg_builder.py
# Builds a Control Flow Graph (CFG) from AST

from ast_nodes.ast_builder import (
    ProgramNode,
    DeclarationNode,
    AssignmentNode,
    IfNode
)

# --------------------------------------------------
# CFG Node Definition
# --------------------------------------------------

class CFGNode:
    _id = 0

    def __init__(self, label):
        self.id = CFGNode._id
        CFGNode._id += 1

        self.label = label
        self.next = []   # outgoing edges

    def connect(self, node):
        self.next.append(node)

    def __str__(self):
        next_ids = [n.id for n in self.next]
        return f"Node({self.id}): {self.label} -> {next_ids}"


# --------------------------------------------------
# CFG Graph
# --------------------------------------------------

class ControlFlowGraph:
    def __init__(self):
        self.start = None
        self.nodes = []

    def add_node(self, node):
        self.nodes.append(node)
        return node


# --------------------------------------------------
# CFG Builder
# --------------------------------------------------

class CFGBuilder:
    def __init__(self):
        self.cfg = ControlFlowGraph()

    def build(self, ast_root):
        self.cfg.start = self._build_node(ast_root, None)
        return self.cfg

    # --------------------------------------------------
    # Recursive builder
    # --------------------------------------------------
    def _build_node(self, node, prev_node):

        # Program node
        if isinstance(node, ProgramNode):
            current = prev_node
            for stmt in node.statements:
                current = self._build_node(stmt, current)
            return current

        # Declaration
        elif isinstance(node, DeclarationNode):
            cfg_node = CFGNode(f"declare {node.identifier}")
            self.cfg.add_node(cfg_node)

            if prev_node:
                prev_node.connect(cfg_node)

            return cfg_node

        # Assignment
        elif isinstance(node, AssignmentNode):
            cfg_node = CFGNode(f"{node.identifier} = ...")
            self.cfg.add_node(cfg_node)

            if prev_node:
                prev_node.connect(cfg_node)

            return cfg_node

        # If statement
        elif isinstance(node, IfNode):
            cond_node = CFGNode("if condition")
            self.cfg.add_node(cond_node)

            if prev_node:
                prev_node.connect(cond_node)

            # Build IF body
            body_last = cond_node
            for stmt in node.body:
                body_last = self._build_node(stmt, body_last)

            # Merge node
            merge_node = CFGNode("merge")
            self.cfg.add_node(merge_node)

            cond_node.connect(body_last)   # true branch
            cond_node.connect(merge_node)  # false branch
            body_last.connect(merge_node)

            return merge_node

        else:
            return prev_node


# --------------------------------------------------
# Testing the CFG Builder
# --------------------------------------------------
if __name__ == "__main__":
    from ast_nodes.ast_builder import build_ast

    parse_tree = (
        'program',
        [
            ('declaration', 'int', 'a'),
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

    builder = CFGBuilder()
    cfg = builder.build(ast)

    print("CFG Nodes:")
    for node in cfg.nodes:
        print(node)
