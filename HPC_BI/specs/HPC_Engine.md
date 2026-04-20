# ⚡ HPC ENGINE — High Performance Computing Layer (C++ + OpenMP)

---

# 🎯 1. PURPOSE OF THIS MODULE

This module is responsible for:

- Performing **large-scale numerical computation**
- Demonstrating **parallel computing using OpenMP**
- Measuring and proving **performance improvement**
- Generating **scalability metrics for analysis and dashboard**

---

# 🧠 2. HPC CONCEPTS COVERED

This module explicitly demonstrates:

### ✅ Data Parallelism
Same computation applied across multiple data elements

### ✅ Parallel Reduction
Efficient computation of:
- Sum
- Average
- Min
- Max

### ✅ OpenMP Threading
- Multi-threaded execution
- Shared memory parallelism

### ✅ Performance Measurement
- Execution time
- Speedup
- Efficiency

---

# 📊 3. DATA INPUT CONTRACT

## Input File:
`data/online_retail.csv`

---

## Columns Used:

| Column | Purpose |
|--------|--------|
| Quantity | MIN / MAX |
| UnitPrice | AVG |
| Quantity × UnitPrice → TotalPrice | SUM |

---

## 🧠 Derived Calculation

### TotalPrice:
TotalPrice = Quantity × UnitPrice

---

# 🔧 4. PROCESSING ARCHITECTURE

---

## PHASE 1: DATA INGESTION

### Responsibilities:
- Read CSV efficiently
- Extract required numeric fields

### Steps:
1. Read file line-by-line
2. Parse:
   - Quantity
   - UnitPrice
3. Compute TotalPrice

---

### ⚠️ Dynamic Handling:

| Issue | Action |
|------|--------|
| Missing values | Skip row |
| Negative Quantity | Skip (returns) |
| Invalid parsing | Log error |

---

### ✔ Validation:
- Count of processed rows
- No crash during parsing

---

# ⚡ PHASE 2: SEQUENTIAL COMPUTATION

---

## 🎯 Goal:
Establish baseline performance

---

## Operations:

- Sum(TotalPrice)
- Avg(UnitPrice)
- Min(Quantity)
- Max(Quantity)

---

## Execution Model:
- Single-threaded loop
- Linear traversal

---

## ✔ Responsibility:
- Baseline computation

---

## ✔ Output:
- Computed values
- Execution time

---

# ⚡ PHASE 3: PARALLEL COMPUTATION

---

## 🎯 Goal:
Perform same computations using parallelism

---

## Implementation:

Use OpenMP:

- Parallel loops
- Reduction clauses

---

## Operations:

| Operation | OpenMP Type |
|----------|------------|
| SUM | reduction(+) |
| AVG | reduction(+) |
| MIN | reduction(min) |
| MAX | reduction(max) |

---

## Execution Model:
- Multi-threaded
- Shared memory

---

## ✔ Responsibility:
- HPC acceleration

---

## ✔ Validation:
- Results match sequential output EXACTLY

---

# ⏱️ PHASE 4: PERFORMANCE MEASUREMENT

---

## Metrics:

| Metric | Definition |
|--------|-----------|
| Sequential Time (Tseq) | Baseline execution |
| Parallel Time (Tpar) | Parallel execution |
| Speedup | Tseq / Tpar |
| Efficiency | Speedup / Threads |

---

## Measurement Method:
- High-resolution timer

---

# 🔥 PHASE 5: SCALABILITY TESTING (CRITICAL)

---

## 🎯 Purpose:
Prove HPC is useful for large datasets

---

## Data Sizes:

| Size | Rows |
|------|-----|
| Small | 10,000 |
| Medium | 50,000 |
| Large | 100,000 |
| Full | ~500,000 |

---

## Process:

For each dataset size:
1. Run sequential computation
2. Run parallel computation
3. Record metrics

---

## Output File:

### `data/hpc_scalability_metrics.csv`

---

## Format:

| data_size | seq_time | par_time | speedup | efficiency |

---

## ✔ Responsibility:
- Generate data for:
  - Dashboard
  - Impact analysis

---

# 📄 PHASE 6: OUTPUT GENERATION

---

## Output Files:

### 1. HPC Metrics:
`hpc_scalability_metrics.csv`

---

### 2. Computation Results:
`hpc_results_summary.csv`

---

## hpc_results_summary.csv:

| metric | value |
|--------|------|
| total_revenue | X |
| avg_price | X |
| min_quantity | X |
| max_quantity | X |

---

# ⚠️ 7. DYNAMIC EXECUTION GUIDELINES

---

## Memory Constraints:

If dataset too large:
- Use chunk processing

---

## Thread Control:

- Use optimal number of threads
- Avoid oversubscription

---

## Data Issues:

- Skip invalid rows
- Log issues

---

# 🔍 8. VALIDATION CHECKLIST

---

✔ Sequential and parallel both implemented  
✔ OpenMP used  
✔ Reduction operations used  
✔ Results match  
✔ Speedup measurable  
✔ Scalability demonstrated  

---

# 🧠 9. HPC IMPACT INTERPRETATION

---

## Expected Observations:

- Parallel time < Sequential time
- Speedup increases with data size
- Efficiency stabilizes

---

## Interpretation Example:

“Parallel processing reduces execution time significantly, especially for large datasets, demonstrating the effectiveness of HPC.”

---

# 🧠 10. VIVA DEFENSE (CRITICAL)

---

## Q: Where is HPC?

Answer:

- OpenMP parallel loops
- Reduction operations
- Performance measurement
- Scalability testing

---

## Q: Why not just Python?

Answer:

- Python abstracts parallelism
- C++ + OpenMP gives explicit control
- Demonstrates true HPC concepts

---

## Q: What is the real benefit?

Answer:

- Faster computation for large datasets
- Scalable processing
- Efficient resource usage

---

# 🚀 11. FINAL STATEMENT

This module is the **core HPC proof** of the project.

It demonstrates:
- Parallel computing
- Performance improvement
- Scalability

---