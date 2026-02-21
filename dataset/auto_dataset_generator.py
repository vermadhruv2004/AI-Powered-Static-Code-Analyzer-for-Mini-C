# auto_dataset_generator.py
# Automatically generates a large ML-ready dataset from static analysis

import csv
import random
import string

from lexer_parser.parser import parser
from ast_nodes.ast_builder import build_ast
from cfg.cfg_builder import CFGBuilder
from features.feature_extractor import FeatureExtractor


# --------------------------------------------------
# Utility helpers
# --------------------------------------------------

def rand_var():
    return random.choice(string.ascii_lowercase)


def rand_num():
    return random.randint(1, 100)


# --------------------------------------------------
# Code Generators
# --------------------------------------------------

def generate_clean_code():
    v = rand_var()
    return f"""
    int {v};
    {v} = {rand_num()};
    if ({v} > {rand_num() // 2}) {{
        {v} = {v} + 1;
    }}
    """


def generate_unused_variable_bug():
    a, b = rand_var(), rand_var()
    return f"""
    int {a};
    int {b};
    {a} = {rand_num()};
    """


def generate_use_before_init_bug():
    a, b = rand_var(), rand_var()
    return f"""
    int {a};
    int {b};
    {b} = {a} + {rand_num()};
    """


def generate_dead_assignment_bug():
    a = rand_var()
    return f"""
    int {a};
    {a} = {rand_num()};
    {a} = {rand_num()};
    """


def generate_deep_nesting_bug(depth=4):
    v = rand_var()
    code = f"int {v};\n{v} = {rand_num()};\n"
    for i in range(depth):
        code += f"if ({v} > {i}) {{\n"
    code += f"{v} = {v} + 1;\n"
    code += "}\n" * depth
    return code


# --------------------------------------------------
# Labeling Logic
# --------------------------------------------------

def assign_label(features):
    if (
        features["use_before_init"] > 0
        or features["dead_assignments"] > 0
        or features["unused_variables"] > 0
        or features["ast_max_depth"] > 8
    ):
        return 1
    return 0


# --------------------------------------------------
# Analyze code → features
# --------------------------------------------------

def analyze(code):
    try:
        parse_tree = parser.parse(code)
        ast = build_ast(parse_tree)
        cfg = CFGBuilder().build(ast)

        extractor = FeatureExtractor()
        features = extractor.extract(ast, cfg)
        features["label"] = assign_label(features)

        return features
    except Exception:
        return None


# --------------------------------------------------
# Dataset generation
# --------------------------------------------------

def generate_dataset(samples_per_type=250, output_csv="dataset/large_static_dataset.csv"):
    dataset = []

    generators = [
        generate_clean_code,
        generate_unused_variable_bug,
        generate_use_before_init_bug,
        generate_dead_assignment_bug,
        lambda: generate_deep_nesting_bug(depth=random.randint(4, 7))
    ]

    while len(dataset) < samples_per_type * len(generators):
        gen = random.choice(generators)
        code = gen()

        features = analyze(code)
        if features:
            dataset.append(features)

    # Write CSV
    fieldnames = dataset[0].keys()
    with open(output_csv, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(dataset)

    print(f"✅ Dataset created: {output_csv}")
    print(f"📊 Total samples: {len(dataset)}")


# --------------------------------------------------
# Run
# --------------------------------------------------

if __name__ == "__main__":
    generate_dataset(samples_per_type=250)
