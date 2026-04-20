# 🚀 HPC + BI Retail Analytics Dashboard — FINAL UI REDESIGN SPECIFICATION

---

# 🎯 OBJECTIVE

Design a **clean, concise, and explainable Streamlit dashboard** that clearly demonstrates:

* What problem is solved
* What HPC does
* What BI does
* How both are connected
* What results are achieved

---

## ❗ CORE PRINCIPLE

> Same dataset → processed by HPC and BI → validated → insights generated

---

## ❗ IMPORTANT CONSTRAINTS

* Focus ONLY on HPC + BI (ML is secondary)
* No unnecessary pages or features
* No experimental storytelling (remove “System Journey”)
* Everything must be understandable in **2–3 minutes**

---

# 🧭 FINAL DASHBOARD STRUCTURE

---

## 1. OVERVIEW

## 2. HPC ENGINE

## 3. BI LAYER

## 4. SYSTEM INTEGRATION (HPC + BI + VALIDATION)

## 5. RESULTS & IMPACT

---

# 🧩 GLOBAL UI RULES (MANDATORY)

---

## Layout Structure (EVERY PAGE)

Each page MUST follow:

1. Title + short description (2 lines max)
2. KPI Row (4 columns)
3. Charts Section (2 charts per row)
4. Insight Section

---

## Chart Rules

Each chart MUST include:

* Title
* Axis labels
* 1-line explanation
* **Key Insight (mandatory)**

---

## Layout Constraints

* Maximum 2 charts per row
* Avoid long vertical stacking
* Use `st.columns()` for balance

---

## Content Rules

* No long paragraphs
* Use bullet points
* Use `st.expander()` for extra explanation

---

## Data Handling Rule

* ❌ DO NOT recompute anything
* ✅ ONLY read from CSV outputs

---

## ML Visibility Rule

* ML must NOT dominate
* Only show as supporting analysis

---

# 📄 PAGE-WISE IMPLEMENTATION

---

# 🟦 1. OVERVIEW PAGE

## Purpose:

Instant understanding of system

---

## Layout:

### Section 1 — Title

* HPC + BI Retail Analytics System

---

### Section 2 — Problem Statement

* Large dataset (~397K transactions)
* Need fast computation + meaningful insights

---

### Section 3 — Approach

* HPC → parallel computation (C++ OpenMP)
* BI → analytics & insights (Python)

---

### Section 4 — KPI Row (4 columns)

Data sources:

* `hpc_results_summary.csv`
* `bi_insights_summary.csv`

Metrics:

* Total Revenue
* Total Customers
* HPC Speedup
* Total Insights

---

### Section 5 — Architecture Diagram

Flow:

Raw Data → HPC
Raw Data → BI
→ Validation → Dashboard

---

### Section 6 — Key Message

* HPC ensures speed
* BI ensures insights
* Validation ensures correctness

---

# 🟦 2. HPC ENGINE PAGE

## Purpose:

Explain HPC role clearly

---

## Section 1 — Role of HPC

* Handles large-scale computation
* Uses parallel processing
* Improves execution speed

---

## Section 2 — KPI Row

From:

* `hpc_results_summary.csv`

Metrics:

* Sequential Time
* Parallel Time
* Speedup
* Efficiency

---

## Section 3 — Thread Scaling Chart

From:

* `hpc_thread_scaling.csv`

Mapping:

* X-axis → threads
* Y-axis → speedup
* Y2-axis → efficiency

Chart type:

* Line chart

---

## Section 4 — Performance Breakdown

From:

* HPC logs / breakdown file

Chart:

* Bar chart

---

## Section 5 — Computations Performed

List:

* Revenue
* RFM
* Percentiles
* Correlation
* Top-K

---

## Section 6 — Key Insight

* Parallel processing improves speed
* But limited by overhead and memory

---

# 🟩 3. BI LAYER PAGE

## Purpose:

Show business insights

---

## Section 1 — Role of BI

* Data cleaning
* Feature engineering
* Insight generation

---

## Section 2 — KPI Row

From:

* BI outputs

Metrics:

* Clean records
* Customers
* RFM segments
* Outlier types

---

## Section 3 — RFM Segmentation

From:

* `rfm_analysis.csv`

Mapping:

* X-axis → segment
* Y-axis → count

Chart:

* Bar chart

---

## Section 4 — Revenue Analysis

From:

* `eda_revenue_by_segment.csv`

Chart:

* Bar chart

---

## Section 5 — Temporal Trends

From:

* `eda_revenue_by_month.csv`

Chart:

* Line chart

---

## Section 6 — Top Customers

From:

* `eda_top_customers.csv`

Chart:

* Bar chart

---

## Section 7 — Outlier Analysis

From:

* `eda_outliers.csv`

Display:

* Expanders

---

## Section 8 — Key Insight

* BI converts data into actionable decisions

---

# 🟪 4. SYSTEM INTEGRATION PAGE

## Purpose:

Explain connection between HPC and BI

---

## Section 1 — Relationship

* Same dataset
* Independent processing
* Results compared

---

## Section 2 — Validation Summary

From:

* `validation_report.csv`

Display:

* Table

---

## Section 3 — Consistency Metrics

Show:

* Revenue (HPC vs BI)
* Customer count
* RFM count

---

## Section 4 — Key Result

* 0.0000% difference

---

## Section 5 — ML (MINIMAL)

ONLY:

* Brief mention
* No deep focus

---

## Section 6 — Key Insight

* System is accurate and reliable

---

# 🟨 5. RESULTS & IMPACT PAGE

## Purpose:

Final summary

---

## Section 1 — Key Results

* Revenue
* Customers
* Insights

---

## Section 2 — Contribution Table

| Component  | Role     |
| ---------- | -------- |
| HPC        | Speed    |
| BI         | Insights |
| Validation | Accuracy |

---

## Section 3 — Business Impact

* Faster analytics
* Better decisions
* Reliable results

---

## Section 4 — Final Conclusion

* HPC + BI together create a complete system

---

# 🎨 DESIGN GUIDELINES

---

## Colors

* HPC → Blue
* BI → Green
* Validation → Purple

---

## Visual Style

* Clean cards
* Minimal text
* Consistent spacing

---

# ❌ REMOVE COMPLETELY

---

* System Journey page
* Separate ML page
* Experimental details
* Over-detailed theory

---

# ✅ FINAL GOAL

---

A viewer should understand:

1. What the system does
2. What HPC does
3. What BI does
4. How they connect
5. What results are achieved

---

## 🏁 SUCCESS CRITERIA

---

If someone can understand the project in **under 3 minutes**,
this dashboard is successful.

---
