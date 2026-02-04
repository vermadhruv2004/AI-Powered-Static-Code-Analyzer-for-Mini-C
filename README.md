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

## 🎯 Objectives

- Apply compiler design concepts in a practical project
- Perform static code analysis using AST and semantic rules
- Extract meaningful features from source code
- Train ML models to predict bug-prone programs
- Provide an interactive UI using Streamlit

---

## 🧩 Compiler Design Concepts Used

- Lexical Analysis
- Syntax Analysis (Parsing)
- Abstract Syntax Tree (AST)
- Symbol Table
- Semantic Analysis
- Static Feature Extraction

---

## 🤖 Machine Learning Models

- Logistic Regression
- Random Forest (Primary model)
- Support Vector Machine (SVM)

**Evaluation Metrics**
- Accuracy
- Precision
- Recall
- F1-score

---

## 🛠 Tech Stack

- **Language:** Python  
- **Compiler Tool:** PLY (Lex & Yacc)  
- **Machine Learning:** scikit-learn  
- **Model Storage:** joblib  
- **UI Framework:** Streamlit  

---

## 📂 Project Structure

```
mini_c_analyzer/
│
├── app.py
├── lexer.py
├── parser.py
├── ast_nodes.py
├── symbol_table.py
├── semantic_analyzer.py
├── feature_extractor.py
├── predictor.py
├── train_model.py
├── ml_models.py
├── rf_model.pkl
├── scaler.pkl
│
├── dataset/
│   └── code_features.csv
│
├── requirements.txt
└── README.md
```

---

## 🚀 How to Run

### 1️⃣ Install Dependencies
```bash
pip install -r requirements.txt
```

### 2️⃣ Train ML Model (Run Once)
```bash
python train_model.py
```

### 3️⃣ Run Streamlit App
```bash
streamlit run app.py
```

---

## 🧪 Sample Mini-C Input

```c
int x;
if (x > 0) {
    print(x);
}
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

## ⚠ Limitations

- Supports only **Mini-C (subset of C)**
- Static analysis only (no execution)
- Small, manually labeled dataset
- Academic-use focused

---

## 🔮 Future Enhancements

- CFG & cyclomatic complexity
- AST/CFG visualization
- PDF/HTML report generation
- Extended Mini-C grammar

---

## 👨‍🎓 Project Info

- **Project Type:** PBL (Advanced Mini Project)
- **Subject:** Compiler Design

---
