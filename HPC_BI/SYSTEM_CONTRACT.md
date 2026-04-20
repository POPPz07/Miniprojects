# 🔗 SYSTEM CONTRACT — Strict Input-Output Dependencies

**Purpose**: Define exact dependencies, data flows, and validation rules across all modules

---

## 📊 MODULE DEPENDENCY GRAPH

```
┌─────────────────┐
│ Online_Retail   │
│   Dataset       │
│ (data/*.csv)    │
└────────┬────────┘
         │
         ├──────────────────────────────────┐
         │                                  │
         ▼                                  ▼
┌─────────────────┐              ┌─────────────────┐
│  HPC ENGINE     │              │   BI LAYER      │
│  (C++ OpenMP)   │              │   (Python)      │
└────────┬────────┘              └────────┬────────┘
         │                                │
         │ Outputs:                       │ Outputs:
         │ • hpc_scalability_metrics.csv  │ • clean_data.csv
         │ • hpc_results_summary.csv      │ • bi_comparison_metrics.csv
         │ • logs/hpc_execution.log       │ • bi_insights_summary.csv
         │                                │ • ml_classification_results.csv
         │                                │ • ml_clustering_results.csv
         │                                │ • logs/bi_execution.log
         │                                │
         └────────────┬───────────────────┘
                      │
                      ▼
              ┌───────────────┐
              │  DASHBOARD    │
              │  (Streamlit)  │
              └───────────────┘
```

---

## 🎯 MODULE 1: HPC ENGINE

### **Input Contract**
| Input | Type | Source | Validation |
|-------|------|--------|------------|
| Dataset | CSV | `data/Online_Retail.csv` | File exists, readable, >0 rows |
| Columns | String | InvoiceNo, Quantity, UnitPrice | Columns exist |
| Data Types | Numeric | Quantity (int), UnitPrice (float) | Parseable to numeric |

### **Processing Contract**
| Operation | Input Columns | Output | Validation |
|-----------|---------------|--------|------------|
| TotalPrice | Quantity, UnitPrice | Quantity × UnitPrice | Result > 0 |
| SUM | TotalPrice | Total Revenue | Result > 0 |
| AVG | UnitPrice | Avg Price | Result > 0 |
| MIN | Quantity | Min Quantity | Result >= 0 |
| MAX | Quantity | Max Quantity | Result > MIN |

### **Output Contract**

#### **File 1: hpc_scalability_metrics.csv**
| Column | Type | Range | Validation |
|--------|------|-------|------------|
| data_size | int | [10000, 541909] | > 0 |
| seq_time | float | [0.001, 10.0] | > 0 |
| par_time | float | [0.001, 10.0] | > 0, < seq_time |
| speedup | float | [0.5, 10.0] | seq_time / par_time |
| efficiency | float | [0.1, 1.0] | speedup / threads |
| threads | int | [1, 64] | > 0 |

**Validation Rules**:
- ✅ par_time < seq_time (parallel should be faster)
- ✅ speedup = seq_time / par_time (±0.01 tolerance)
- ✅ efficiency = speedup / threads (±0.01 tolerance)
- ✅ All rows present for [10K, 50K, 100K, Full]

#### **File 2: hpc_results_summary.csv**
| Metric | Type | Range | Validation |
|--------|------|-------|------------|
| total_revenue | float | [1M, 100M] | > 0 |
| avg_unit_price | float | [0.01, 10000] | > 0 |
| min_quantity | int | [1, 1000] | >= 0 |
| max_quantity | int | [1000, 100000] | > min_quantity |
| total_rows_processed | int | [100000, 600000] | > 0 |

**Validation Rules**:
- ✅ max_quantity > min_quantity
- ✅ total_revenue > 0
- ✅ avg_unit_price > 0

### **Thread Scaling Analysis Contract**
| Thread Count | Expected Speedup Range | Expected Efficiency Range |
|--------------|------------------------|---------------------------|
| 1 | 1.0 | 1.0 |
| 2 | 1.5 - 2.0 | 0.75 - 1.0 |
| 4 | 2.5 - 3.5 | 0.625 - 0.875 |
| 8 | 3.5 - 6.0 | 0.438 - 0.75 |
| 16 | 4.0 - 10.0 | 0.25 - 0.625 |

**Validation**: Test with thread counts [1, 2, 4, 8] and record scaling behavior

---

## 🎯 MODULE 2: BI LAYER

### **Input Contract**
| Input | Type | Source | Validation |
|-------|------|--------|------------|
| Raw Dataset | CSV | `data/Online_Retail.csv` | File exists, >0 rows |
| HPC Metrics | CSV | `data/hpc_scalability_metrics.csv` | File exists (optional) |

### **Processing Contract - ETL**
| Step | Input | Output | Validation |
|------|-------|--------|------------|
| Load | Raw CSV | DataFrame | Shape > (0, 0) |
| Remove Missing CustomerID | DataFrame | Filtered DF | CustomerID.notna() |
| Remove Negative Quantity | DataFrame | Filtered DF | Quantity > 0 |
| Remove Invalid UnitPrice | DataFrame | Filtered DF | UnitPrice > 0 |
| Create TotalPrice | Quantity, UnitPrice | TotalPrice column | TotalPrice > 0 |

### **Feature Engineering Contract**

#### **Basic Features**
| Feature | Formula | Type | Validation |
|---------|---------|------|------------|
| TotalPrice | Quantity × UnitPrice | float | > 0 |

#### **Customer Aggregation Features**
| Feature | Formula | Type | Validation |
|---------|---------|------|------------|
| CustomerSpend | SUM(TotalPrice) per CustomerID | float | > 0 |
| PurchaseFrequency | COUNT(InvoiceNo) per CustomerID | int | >= 1 |
| AvgOrderValue | CustomerSpend / PurchaseFrequency | float | > 0 |

#### **Time-Based Features**
| Feature | Source | Type | Validation |
|---------|--------|------|------------|
| Month | InvoiceDate | int | [1, 12] |
| DayOfWeek | InvoiceDate | int | [0, 6] |
| Hour | InvoiceDate | int | [0, 23] |

#### **RFM Features**
| Feature | Formula | Type | Validation |
|---------|---------|------|------------|
| Recency | (max_date - last_purchase_date).days | int | >= 0 |
| Frequency | COUNT(InvoiceNo) per CustomerID | int | >= 1 |
| Monetary | SUM(TotalPrice) per CustomerID | float | > 0 |

### **Output Contract**

#### **File 1: clean_data.csv**
| Column | Type | Validation |
|--------|------|------------|
| InvoiceNo | string | Not null |
| StockCode | string | Not null |
| Quantity | int | > 0 |
| UnitPrice | float | > 0 |
| CustomerID | float | Not null |
| Country | string | Not null |
| InvoiceDate | datetime | Valid date |
| TotalPrice | float | > 0 |
| Month | int | [1, 12] |
| DayOfWeek | int | [0, 6] |
| Hour | int | [0, 23] |

**Validation Rules**:
- ✅ No missing CustomerID
- ✅ All Quantity > 0
- ✅ All UnitPrice > 0
- ✅ TotalPrice = Quantity × UnitPrice

#### **File 2: bi_comparison_metrics.csv**
| Metric | Raw | Processed | Improvement % |
|--------|-----|-----------|---------------|
| total_rows | int > 0 | int > 0 | float |
| missing_customerID | int >= 0 | 0 | -100.0 |
| negative_quantity | int >= 0 | 0 | -100.0 |
| invalid_unitprice | int >= 0 | 0 | -100.0 |
| usable_records | int > 0 | int > 0 | float |

**Validation Rules**:
- ✅ processed.missing_customerID = 0
- ✅ processed.negative_quantity = 0
- ✅ processed.invalid_unitprice = 0

#### **File 3: bi_insights_summary.csv**
**Schema**: `insight_category, insight_name, value, unit, interpretation, action`

| Category | Insight Name | Value Type | Unit | Validation |
|----------|--------------|------------|------|------------|
| revenue | total_revenue | float | currency | > 0 |
| revenue | top_country | string | text | Not null |
| revenue | top_country_revenue | float | currency | > 0 |
| revenue | top_country_contribution | float | percent | [0, 100] |
| customer | total_customers | int | count | > 0 |
| customer | avg_customer_spend | float | currency | > 0 |
| customer | top_10pct_revenue_contribution | float | percent | [0, 100] |
| time | peak_month | string | text | Valid month name |
| time | peak_hour | int | hour | [0, 23] |
| segmentation | num_clusters | int | count | [2, 10] |
| segmentation | high_value_customers | int | count | > 0 |
| ml | classification_accuracy | float | percent | [0, 100] |
| ml | clustering_silhouette_score | float | score | [-1, 1] |
| rfm | avg_recency | float | days | >= 0 |
| rfm | avg_frequency | float | count | >= 1 |
| rfm | avg_monetary | float | currency | > 0 |

#### **File 4: ml_classification_results.csv**
| Metric | Type | Range | Validation |
|--------|------|-------|------------|
| accuracy | float | [0.5, 1.0] | > 0.5 |
| precision | float | [0.5, 1.0] | > 0.5 |
| recall | float | [0.5, 1.0] | > 0.5 |
| f1_score | float | [0.5, 1.0] | > 0.5 |
| high_value_customers | int | > 0 | < total_customers |
| total_customers | int | > 0 | Matches clean data |
| high_value_threshold | float | > 0 | 75th percentile |

#### **File 5: ml_clustering_results.csv**
| Column | Type | Validation |
|--------|------|------------|
| cluster_id | int | [0, K-1] |
| cluster_name | string | Not null |
| customer_count | int | > 0 |
| avg_spend | float | > 0 |
| avg_frequency | float | >= 1 |
| avg_recency | float | >= 0 |

**Validation Rules**:
- ✅ SUM(customer_count) = total_customers
- ✅ All cluster_ids unique
- ✅ avg_spend increases with cluster value

---

## 🎯 MODULE 3: DASHBOARD

### **Input Contract**
| Input File | Required | Validation |
|------------|----------|------------|
| hpc_scalability_metrics.csv | ✅ Yes | File exists, valid schema |
| hpc_results_summary.csv | ✅ Yes | File exists, valid schema |
| bi_comparison_metrics.csv | ✅ Yes | File exists, valid schema |
| bi_insights_summary.csv | ✅ Yes | File exists, valid schema |
| ml_classification_results.csv | ✅ Yes | File exists, valid schema |
| ml_clustering_results.csv | ✅ Yes | File exists, valid schema |
| clean_data.csv | ⚠️ Optional | For raw data display |

### **Processing Contract**
| Page | Required Data | Validation |
|------|---------------|------------|
| Introduction | None | Always available |
| Dataset Explorer | clean_data.csv | File exists |
| HPC Performance Lab | hpc_*.csv | Both files exist |
| BI Insights Engine | bi_insights_summary.csv | File exists |
| ML Intelligence | ml_*.csv | Both files exist |
| System Comparison | All files | All files exist |
| Explainability Center | None | Always available |
| Final Impact | All files | All files exist |

---

## 🔍 CROSS-MODULE VALIDATION RULES

### **Rule 1: Revenue Consistency**
```
HPC.total_revenue ≈ BI.total_revenue (±1% tolerance)
```

### **Rule 2: Row Count Consistency**
```
HPC.total_rows_processed = BI.clean_data.row_count
```

### **Rule 3: Customer Count Consistency**
```
BI.total_customers = SUM(ml_clustering_results.customer_count)
```

### **Rule 4: High-Value Customer Consistency**
```
ml_classification.high_value_customers ≈ top_10pct_customers (±5% tolerance)
```

### **Rule 5: Time Sequence Validation**
```
HPC execution timestamp < BI execution timestamp < Dashboard load timestamp
```

---

## 🛡️ PIPELINE SAFETY RULES

### **Pre-Execution Checks**
1. ✅ Dataset exists at `data/Online_Retail.csv`
2. ✅ Dataset is readable and not corrupted
3. ✅ Output directories exist (`data/`, `logs/`)
4. ✅ No file locks on output files

### **Output Versioning Strategy**
```
Option 1: Clean old outputs (default)
  - Delete all files matching `data/*_metrics.csv`
  - Delete all files matching `data/*_results.csv`
  - Delete all files matching `logs/*.log`

Option 2: Version outputs (backup mode)
  - Rename existing files with timestamp suffix
  - Example: hpc_scalability_metrics.csv → hpc_scalability_metrics_20240115_102345.csv
```

### **Post-Execution Validation**
1. ✅ All expected output files exist
2. ✅ All output files have valid schemas
3. ✅ Cross-module validation rules pass
4. ✅ No error messages in logs

---

## 📊 INSIGHT INTERPRETATION LAYER

### **Revenue Insights**
| Insight | Business Meaning | Action |
|---------|------------------|--------|
| total_revenue | Total sales generated | Track against targets |
| top_country_contribution > 80% | Heavy geographic concentration | Diversify markets |
| top_10pct_revenue_contribution > 60% | Customer concentration risk | Expand customer base |

### **Customer Insights**
| Insight | Business Meaning | Action |
|---------|------------------|--------|
| avg_customer_spend | Customer lifetime value | Set acquisition cost limits |
| high_value_customers | VIP segment size | Create loyalty programs |
| avg_frequency < 3 | Low repeat purchase | Improve retention |

### **Time Insights**
| Insight | Business Meaning | Action |
|---------|------------------|--------|
| peak_month | Seasonal demand | Stock inventory accordingly |
| peak_hour | Traffic patterns | Optimize staffing |

### **Segmentation Insights**
| Insight | Business Meaning | Action |
|---------|------------------|--------|
| num_clusters | Customer diversity | Tailor marketing strategies |
| VIP cluster size < 10% | Elite customer base | Premium services |

### **RFM Insights**
| Insight | Business Meaning | Action |
|---------|------------------|--------|
| avg_recency > 90 days | Customer churn risk | Re-engagement campaigns |
| avg_frequency < 3 | Low loyalty | Improve product/service |
| avg_monetary | Revenue per customer | Upselling opportunities |

---

## 🧪 FEATURE VALIDATION RULES

### **Validation 1: TotalPrice Consistency**
```python
assert (clean_data['TotalPrice'] == clean_data['Quantity'] * clean_data['UnitPrice']).all()
```

### **Validation 2: CustomerSpend Consistency**
```python
assert customer_features['CustomerSpend'] == clean_data.groupby('CustomerID')['TotalPrice'].sum()
```

### **Validation 3: RFM Consistency**
```python
assert (rfm_features['Frequency'] == rfm_features['Monetary'] / rfm_features['AvgOrderValue']).all()
```

### **Validation 4: Time Feature Ranges**
```python
assert clean_data['Month'].between(1, 12).all()
assert clean_data['DayOfWeek'].between(0, 6).all()
assert clean_data['Hour'].between(0, 23).all()
```

### **Validation 5: ML Output Consistency**
```python
assert classification_results['high_value_customers'] <= classification_results['total_customers']
assert clustering_results['customer_count'].sum() == total_customers
```

---

## 🚨 ERROR HANDLING CONTRACT

### **HPC Engine Errors**
| Error | Cause | Action |
|-------|-------|--------|
| File not found | Dataset missing | Stop execution, log error |
| Parse error | Invalid data format | Skip row, log warning |
| Memory error | Dataset too large | Use chunk processing |
| Results mismatch | Parallel bug | Log error, use sequential results |

### **BI Layer Errors**
| Error | Cause | Action |
|-------|-------|--------|
| Missing columns | Wrong dataset | Stop execution, log error |
| All data filtered | Too aggressive cleaning | Relax filters, log warning |
| ML model failure | Insufficient data | Skip ML, log warning |
| Feature validation failure | Data inconsistency | Log error, stop execution |

### **Dashboard Errors**
| Error | Cause | Action |
|-------|-------|--------|
| Missing input file | Pipeline incomplete | Show error message, disable page |
| Schema mismatch | Wrong file version | Show error message, log issue |
| Chart rendering failure | Invalid data | Show error message, skip chart |

---

## 📝 LOGGING CONTRACT

### **Log Levels**
- **INFO**: Normal operations, milestones
- **WARNING**: Non-critical issues, data quality concerns
- **ERROR**: Critical failures, execution stops
- **DEBUG**: Detailed execution traces (optional)

### **Required Log Entries**
1. Module start/end timestamps
2. Input file validation results
3. Processing milestones (ETL steps, ML training)
4. Output file generation confirmations
5. Validation check results
6. Error messages with context

---

## ✅ FINAL SYSTEM GUARANTEE

After successful execution:
1. ✅ All output files exist with valid schemas
2. ✅ All cross-module validation rules pass
3. ✅ All logs show successful completion
4. ✅ Dashboard loads without errors
5. ✅ All insights have interpretations and actions
6. ✅ System demonstrates measurable HPC + BI impact

---

**End of System Contract**
