# 🧠 AI-Powered Static Code Analyzer for Mini-C

An **AI-powered static analysis tool** that integrates **compiler design techniques** with **machine learning** to detect bug-prone and risky code in a **Mini-C language**.

This project is developed as part of **Project-Based Learning (PBL)** for the **Compiler Design** subject.

---

## 📌 Project Overview

This tool analyzes Mini-C source code **without executing it** (static analysis).  
It applies compiler frontend phases such as **lexical analysis, parsing, AST generation, and semantic analysis** to extract features.  
These features are then passed to **machine learning models** to predict whether the code is **BUGGY** or **CLEAN**.

A **Streamlit web interface** is included for interactive code analysis.

---

## 🚀 Key Features

- ✅ Lexical Analysis & Parsing (PLY)
- 🌳 Abstract Syntax Tree (AST) construction
- 🔀 Control Flow Graph (CFG) generation
- 📊 Data Flow Analysis (use-before-init, dead assignments)
- 🧮 Feature Extraction from compiler structures
- 🤖 Machine Learning (Random Forest Classifier)
- 🔍 Bug prediction with confidence score
- 🧠 Hybrid Decision System (Rule-based + ML override)
- 🌐 Streamlit Web Interface
- 📈 Feature Importance Visualization

---

## 🧩 Compiler Design Concepts Used

- Lexical Analysis
- Syntax Analysis (Parsing)
- Abstract Syntax Tree (AST)
- Symbol Table
- Semantic Analysis
- Static Feature Extraction

---

## 🤖 Machine Learning

- Algorithms used:
  - Logistic Regression
  - Support Vector Machine (SVM)
  - **Random Forest (Final Model)**

- Evaluation Metrics:
  - Accuracy
  - Precision
  - Recall
  - F1-score

- Hybrid decision:
  - **Rule-based override** if no hard bugs exist
  - ML used for risk estimation

---

## 🛠 Tech Stack

- **Language:** Python  
- **Compiler Tool:** PLY (Lex & Yacc)  
- **Machine Learning:** scikit-learn  
- **Model Storage:** joblib  
- **UI Framework:** Streamlit  

---

## 🏗️ Project Architecture

```
Source Code
   ↓
Lexer → Parser
   ↓
AST Construction
   ↓
CFG + Data Flow Analysis
   ↓
Feature Extraction
   ↓
ML Model (Random Forest)
   ↓
Prediction (Clean / Buggy)
```

---

## 📂 Project Structure

```
Compiler Project/
│
├── lexer_parser/        # Lexer & Parser (PLY)
├── ast_nodes/           # AST Builder & Analyzer
├── cfg/                 # Control Flow Graph Builder
├── data_flow/           # Data Flow Analyzer
├── features/            # Feature Extractor
├── dataset/             # Dataset generators & CSV
├── ml/                  # ML training, prediction & models
├── web/                 # (Optional) Flask version
├── streamlit_app.py     # Streamlit Web App
├── main.py              # CLI entry point
└── README.md
```

---

## 📊 Dataset

- Automatically generated (1000+ samples)
- Clean & buggy code samples
- Fully numeric and ML-ready
- Labeled using rule-based heuristics (weak supervision)

### Dataset Features
- `ast_max_depth`
- `unused_variables`
- `if_statements`
- `assignments`
- `cfg_nodes`
- `cfg_edges`
- `use_before_init`
- `dead_assignments`
- `label` (0 = Clean, 1 = Buggy)

---

## ▶️ How to Run (CLI)

### 1. Generate Dataset
```bash
python -m dataset.auto_dataset_generator
```

### 2. Train ML Model
```bash
python -m ml.train_model
```

### 3. Predict via CLI
```bash
python -m ml.predict
```

### 4. Run Full Pipeline
```bash
python main.py
```

---

## 📊 Sample Output

```
Prediction: BUGGY

Features:
total_vars: 1
unused_vars: 0
uninitialized_vars: 1
assignments: 0
conditions: 1
binary_ops: 1
loop_depth: 0
```

---

## 🔄 Processing Pipeline

```
Mini-C Code
 → Lexer
 → Parser
 → AST
 → Semantic Analysis
 → Feature Extraction
 → ML Classification
 → Bug Prediction
```

---

## 🎓 Academic Relevance

- Strong alignment with **Compiler Design syllabus**
- Demonstrates integration of **AI + Compiler Theory**
- Suitable for **Advanced Mini Project / PBL**

---

## 🧪 Supported Syntax

✔ Variable declaration  
✔ Assignment  
✔ Arithmetic expressions  
✔ Relational operators  
✔ `if` statements  

❌ Loops (`while`)  
❌ Function calls (`print`)  

(Handled gracefully with error messages)

---


## 🔮 Future Work

- Add loop support
- Support function calls
- Language extension (C++, Java)
- CI/CD integration
- Cloud deployment

---

## 👨‍🎓 Project Info

- **Project Type:** PBL (Advanced Mini Project)
- **Subject:** Compiler Design

---
