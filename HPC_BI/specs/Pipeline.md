# ⚙️ PIPELINE — End-to-End Execution & Integration System

---

# 🎯 1. PURPOSE OF PIPELINE

This module is responsible for:

- Executing the entire system end-to-end
- Ensuring correct order of operations
- Generating all intermediate outputs
- Handling failures and dynamic issues
- Providing reproducible execution flow

---

# 🔗 2. SYSTEM EXECUTION FLOW
Dataset
↓
HPC Engine (Sequential + Parallel)
↓
HPC Metrics (Scalability + Performance)
↓
BI Layer (ETL + ML + Insights)
↓
BI Metrics + Insight Files
↓
Streamlit Dashboard

---

# 🧩 3. PHASE-WISE EXECUTION PLAN

---

# 🔹 PHASE 1: ENVIRONMENT SETUP

---

## Responsibilities:
- Ensure all dependencies are installed

---

## Requirements:

### HPC:
- C++ compiler (g++)
- OpenMP support

### BI:
- Python 3.x
- pandas
- numpy
- scikit-learn
- matplotlib / plotly

### Dashboard:
- streamlit

---

## ✔ Validation:
- All tools installed
- No dependency errors

---

# 🔹 PHASE 2: DATASET PREPARATION

---

## Responsibilities:
- Place dataset correctly

---

## Steps:

1. Download dataset
2. Rename to:
   `online_retail.csv`
3. Place in:
   `data/`

---

## ✔ Validation:
- File exists
- File readable

---

# 🔹 PHASE 3: HPC EXECUTION

---

## Responsibilities:
- Run sequential + parallel computations
- Perform scalability testing

---

## Steps:

### Step 1: Compile HPC Engine
- Compile C++ files with OpenMP support

---

### Step 2: Run Sequential Computation
- Process dataset
- Measure execution time

---

### Step 3: Run Parallel Computation
- Use OpenMP
- Measure execution time

---

### Step 4: Scalability Testing

Run computations for:
- 10K rows
- 50K rows
- 100K rows
- Full dataset

---

### Step 5: Generate Outputs

Create:

1. `hpc_scalability_metrics.csv`
2. `hpc_results_summary.csv`

---

## ✔ Validation:

✔ All sizes processed  
✔ Metrics generated  
✔ No mismatch between sequential & parallel  

---

# 🔹 PHASE 4: BI EXECUTION

---

## Responsibilities:
- Clean data
- Generate insights
- Run ML models

---

## Steps:

---

### Step 1: ETL

- Load dataset
- Clean data
- Generate `clean_data.csv`

---

### Step 2: Data Comparison Metrics

Generate:
`bi_comparison_metrics.csv`

---

### Step 3: Feature Engineering

- Create TotalPrice
- Create customer metrics

---

### Step 4: Exploratory Analysis

- Generate insights

---

### Step 5: Machine Learning

Run:
- Classification model
- Clustering model

---

### Step 6: Insight Generation

Generate:
`bi_insights_summary.csv`

---

## ✔ Validation:

✔ Clean dataset created  
✔ Comparison metrics created  
✔ ML outputs generated  
✔ Insights generated  

---

# 🔹 PHASE 5: DASHBOARD EXECUTION

---

## Responsibilities:
- Launch Streamlit UI
- Load all generated outputs

---

## Steps:

1. Load:
   - HPC metrics
   - BI metrics
   - Insight files

2. Render pages:
   - HPC analysis
   - BI insights
   - ML results
   - Comparison

---

## ✔ Validation:

✔ Dashboard loads successfully  
✔ All pages display data  
✔ No missing files  

---

# 🔹 PHASE 6: IMPACT VALIDATION (CRITICAL)

---

## Responsibilities:
Ensure system proves its value

---

## HPC Validation:

✔ Parallel faster than sequential  
✔ Speedup > 1  
✔ Scalability visible  

---

## BI Validation:

✔ Data cleaned  
✔ Insights extracted  
✔ ML models working  

---

## System Validation:

✔ Comparison (Before vs After) exists  
✔ Business insights visible  

---

# ⚠️ 4. DYNAMIC EXECUTION GUIDELINES

---

## Dataset Issues:

| Issue | Action |
|------|--------|
| Missing file | Stop execution |
| Corrupt file | Re-download |

---

## HPC Issues:

| Issue | Action |
|------|--------|
| Slow execution | Reduce dataset size |
| Memory issue | Use chunk processing |

---

## BI Issues:

| Issue | Action |
|------|--------|
| Missing data | Apply cleaning rules |
| Model failure | Adjust parameters |

---

## Dashboard Issues:

| Issue | Action |
|------|--------|
| Missing metrics | Check previous steps |
| Chart failure | Validate data format |

---

# 🔍 5. OUTPUT FILE SUMMARY

---

## HPC Outputs:

- hpc_scalability_metrics.csv
- hpc_results_summary.csv

---

## BI Outputs:

- clean_data.csv
- bi_comparison_metrics.csv
- bi_insights_summary.csv

---

## Dashboard Inputs:

- All above files

---

# 🧠 6. PIPELINE VALIDATION CHECKLIST

---

✔ All steps executed in order  
✔ No missing outputs  
✔ Dashboard displays results  
✔ System runs end-to-end  

---

# 🚀 7. FINAL SYSTEM GUARANTEE

After pipeline execution:

- HPC metrics are available
- BI insights are generated
- Dashboard is fully functional
- System demonstrates real impact

---

# 🧠 8. VIVA DEFENSE

---

## Q: How does system work end-to-end?

Answer:

- Dataset is processed by HPC engine
- Metrics generated
- BI layer extracts insights
- Dashboard visualizes results

---

## Q: How is correctness ensured?

Answer:

- Validation checks at every phase
- Matching sequential and parallel results
- Verified outputs

---

# 🚀 9. FINAL STATEMENT

This pipeline ensures:

- Full system integration
- Reproducibility
- Stability
- Clear demonstration of HPC + BI concepts