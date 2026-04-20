# 📸 Screenshots and Sample Outputs Guide

**Purpose**: This guide provides instructions for capturing screenshots of all dashboard pages and generating sample output files for offline demonstration.

---

## 📋 Table of Contents

- [Dashboard Screenshots](#dashboard-screenshots)
- [Sample Output Files](#sample-output-files)
- [Screenshot Specifications](#screenshot-specifications)
- [Offline Demo Package](#offline-demo-package)

---

## 📸 Dashboard Screenshots

### Prerequisites
1. **Start Dashboard**: Run `streamlit run app.py` from `dashboard/` directory
2. **Verify Data**: Ensure all CSV files in `data/` directory are present
3. **Browser**: Use Chrome or Firefox for best rendering
4. **Resolution**: Set browser window to 1920x1080 for consistent screenshots

### Screenshot Checklist

#### 1. System Journey Page
**Filename**: `screenshots/01_system_journey.png`

**What to Capture**:
- [ ] Page title and introduction
- [ ] Timeline visualization showing iteration progression
- [ ] Performance progression charts (speedup, efficiency)
- [ ] Iteration 1 details panel (expanded)
- [ ] Thread scaling analysis table
- [ ] HPC limitations section

**Key Elements to Show**:
- Timeline with iteration markers
- Performance charts with annotations
- Iteration details with What/Why/Result/Learnings
- Thread scaling table showing optimal configuration (8 threads)

**Screenshot Instructions**:
1. Navigate to System Journey page
2. Scroll to top of page
3. Expand Iteration 1 details panel
4. Capture full page (use browser extension or scrolling screenshot tool)
5. Save as `screenshots/01_system_journey.png`

---

#### 2. HPC Analysis Page
**Filename**: `screenshots/02_hpc_analysis.png`

**What to Capture**:
- [ ] Page title and introduction
- [ ] Thread scaling visualization (speedup vs threads)
- [ ] Operation classification chart (parallelizable vs sequential)
- [ ] Performance breakdown chart (data loading, computation, output)
- [ ] RFM analysis results table
- [ ] Computational intensity metrics

**Key Elements to Show**:
- Thread scaling chart showing plateau at 8 threads
- Operation classification pie chart
- Performance breakdown showing 91.6% parallelizable
- RFM results with customer segments

**Screenshot Instructions**:
1. Navigate to HPC Analysis page
2. Scroll to top of page
3. Ensure all charts are fully rendered
4. Capture full page
5. Save as `screenshots/02_hpc_analysis.png`

---

#### 3. BI Insights Page
**Filename**: `screenshots/03_bi_insights.png`

**What to Capture**:
- [ ] Page title and introduction
- [ ] RFM segment distribution chart
- [ ] Customer concentration chart (Pareto analysis)
- [ ] Temporal trend charts (monthly, day of week, hourly)
- [ ] Revenue by country chart
- [ ] Outlier analysis section (5 types)
- [ ] Insights summary table

**Key Elements to Show**:
- RFM segments with Champions at 65.2% revenue
- Customer concentration showing top 211 customers = 50% revenue
- Temporal trends showing peak month, day, hour
- 5 outlier types with business interpretation

**Screenshot Instructions**:
1. Navigate to BI Insights page
2. Scroll to top of page
3. Ensure all charts are fully rendered
4. Capture full page
5. Save as `screenshots/03_bi_insights.png`

---

#### 4. ML Results Page
**Filename**: `screenshots/04_ml_results.png`

**What to Capture**:
- [ ] Page title and introduction
- [ ] Classification results (accuracy, precision, recall, F1)
- [ ] Feature importance bar chart
- [ ] Clustering results (silhouette score, cluster count)
- [ ] Cluster visualization (2D projection)
- [ ] Cluster profiles table

**Key Elements to Show**:
- Classification accuracy: 95.08%
- Feature importance showing top behavioral features
- Clustering silhouette score: 0.8958
- Cluster profiles with business interpretation

**Screenshot Instructions**:
1. Navigate to ML Results page
2. Scroll to top of page
3. Ensure all charts are fully rendered
4. Capture full page
5. Save as `screenshots/04_ml_results.png`

---

#### 5. Validation Page
**Filename**: `screenshots/05_validation.png`

**What to Capture**:
- [ ] Page title and introduction
- [ ] Validation summary table (4/4 checks passing)
- [ ] Revenue consistency chart
- [ ] Customer count consistency chart
- [ ] RFM count consistency chart
- [ ] Validation methodology section

**Key Elements to Show**:
- All 4 validation checks with PASS status
- Revenue difference: 0.0000%
- Customer count: 4,338 across all modules
- Validation timestamp

**Screenshot Instructions**:
1. Navigate to Validation page
2. Scroll to top of page
3. Ensure all charts are fully rendered
4. Capture full page
5. Save as `screenshots/05_validation.png`

---

#### 6. Conclusion Page
**Filename**: `screenshots/06_conclusion.png`

**What to Capture**:
- [ ] Page title and introduction
- [ ] System achievements section
- [ ] 5 key learnings section
- [ ] Future directions section
- [ ] Final thoughts

**Key Elements to Show**:
- System achievements with checkmarks
- 5 key learnings with detailed explanations
- Future directions with actionable items

**Screenshot Instructions**:
1. Navigate to Conclusion page
2. Scroll to top of page
3. Capture full page
4. Save as `screenshots/06_conclusion.png`

---

#### 7. Main App (Navigation)
**Filename**: `screenshots/00_main_app.png`

**What to Capture**:
- [ ] Sidebar with navigation menu
- [ ] Page titles for all 7 pages
- [ ] Quick stats in sidebar (if present)
- [ ] Main content area showing introduction

**Key Elements to Show**:
- All 7 pages listed in sidebar
- Clean navigation structure
- Professional styling

**Screenshot Instructions**:
1. Navigate to main app (introduction page)
2. Ensure sidebar is visible
3. Capture full page with sidebar
4. Save as `screenshots/00_main_app.png`

---

## 📁 Sample Output Files

### HPC Engine Sample Outputs

Create a `sample_outputs/hpc/` directory with representative samples:

#### 1. hpc_results_summary.csv (Sample)
```csv
metric,value
total_revenue,8911407.90
avg_unit_price,3.12
avg_transaction_size,22.40
min_quantity,1
max_quantity,80995
total_rows_processed,397884
computation_time,0.018143
```

#### 2. hpc_thread_scaling.csv (Sample)
```csv
data_size,seq_time,par_time,speedup,efficiency,threads
397884,0.023972,0.023298,1.0289,1.0289,1
397884,0.023972,0.025696,0.9329,0.4665,2
397884,0.023972,0.023339,1.0271,0.2568,4
397884,0.023972,0.022780,1.0523,0.1315,8
397884,0.023972,0.024429,0.9813,0.0613,16
```

#### 3. hpc_rfm_analysis.csv (Sample - First 10 rows)
```csv
customer_id,recency,frequency,monetary,rfm_score,segment
12346,326,1,77183.60,111,Lost
12347,2,182,4310.00,555,Champions
12348,75,31,1797.24,544,Champions
12349,19,73,1757.55,555,Champions
12350,310,17,334.40,215,Lost
```

### BI Layer Sample Outputs

Create a `sample_outputs/bi/` directory with representative samples:

#### 1. bi_insights_summary.csv (Sample - First 5 insights)
```csv
analysis_type,dimension,segment,metric,value,percentage,insight,business_meaning,generated_at,insight_id
overall,total,All,total_revenue,8911407.904,100.0,"Total revenue: $8,911,407.90",Baseline for all revenue comparisons,2026-04-16 00:39:53,1
segment,rfm_segment,Champions,revenue_contribution,5809341.07,65.18993555880664,"Champions contribute $5,809,341.07 (65.2%)",Highest value customers - prioritize retention and upsell,2026-04-16 00:39:53,2
segment,rfm_segment,Loyal Customers,revenue_contribution,1090973.5,12.242437017278746,"Loyal Customers contribute $1,090,973.50 (12.2%)",Consistent revenue source - maintain engagement,2026-04-16 00:39:53,3
```

#### 2. ml_classification_results.csv (Sample)
```csv
metric,value
accuracy,0.9508448540706606
precision,0.9523809523809523
recall,0.9508448540706606
f1_score,0.9516129032258065
```

#### 3. ml_clustering_results.csv (Sample)
```csv
metric,value
optimal_clusters,2
silhouette_score,0.8958167182320717
cluster_0_count,2169
cluster_1_count,2169
```

### Validation Sample Outputs

Create a `sample_outputs/validation/` directory:

#### validation_report.csv (Sample)
```csv
timestamp,check_name,status,message
2026-04-16 00:40:00,Revenue Consistency,PASS,Revenue difference: $0.00 (0.0000%)
2026-04-16 00:40:00,Customer Count Consistency,PASS,All modules have 4338 customers
2026-04-16 00:40:00,RFM Count Consistency,PASS,RFM customer counts match: 4338
2026-04-16 00:40:00,Data Integrity,PASS,All data integrity checks passed
```

---

## 📐 Screenshot Specifications

### Image Format
- **Format**: PNG (lossless compression)
- **Color Depth**: 24-bit RGB
- **Resolution**: 1920x1080 (Full HD)
- **DPI**: 96 DPI (standard screen resolution)

### File Naming Convention
```
screenshots/
├── 00_main_app.png              # Main app with navigation
├── 01_system_journey.png        # System Journey page
├── 02_hpc_analysis.png          # HPC Analysis page
├── 03_bi_insights.png           # BI Insights page
├── 04_ml_results.png            # ML Results page
├── 05_validation.png            # Validation page
└── 06_conclusion.png            # Conclusion page
```

### Screenshot Tools

**Browser Extensions**:
- **Chrome**: Full Page Screen Capture, Awesome Screenshot
- **Firefox**: Fireshot, Nimbus Screenshot

**Desktop Tools**:
- **Windows**: Snipping Tool, Greenshot
- **macOS**: Command+Shift+4, Skitch
- **Linux**: Shutter, Flameshot

**Command Line**:
```bash
# Using Selenium (Python)
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

options = Options()
options.add_argument('--headless')
options.add_argument('--window-size=1920,1080')

driver = webdriver.Chrome(options=options)
driver.get('http://localhost:8501')
driver.save_screenshot('screenshots/00_main_app.png')
driver.quit()
```

---

## 📦 Offline Demo Package

### Package Structure
```
offline_demo/
├── screenshots/                 # All dashboard screenshots
│   ├── 00_main_app.png
│   ├── 01_system_journey.png
│   ├── 02_hpc_analysis.png
│   ├── 03_bi_insights.png
│   ├── 04_ml_results.png
│   ├── 05_validation.png
│   └── 06_conclusion.png
├── sample_outputs/              # Sample data files
│   ├── hpc/
│   │   ├── hpc_results_summary.csv
│   │   ├── hpc_thread_scaling.csv
│   │   └── hpc_rfm_analysis.csv
│   ├── bi/
│   │   ├── bi_insights_summary.csv
│   │   ├── ml_classification_results.csv
│   │   └── ml_clustering_results.csv
│   └── validation/
│       └── validation_report.csv
├── documentation/               # All documentation files
│   ├── README.md
│   ├── SHOWCASE_GUIDE.md
│   ├── FAQ.md
│   ├── PROJECT_STATE.md
│   └── SYSTEM_CONTRACT.md
└── OFFLINE_DEMO_README.md      # Instructions for offline demo
```

### Creating Offline Demo Package

```bash
# Create directory structure
mkdir -p offline_demo/screenshots
mkdir -p offline_demo/sample_outputs/hpc
mkdir -p offline_demo/sample_outputs/bi
mkdir -p offline_demo/sample_outputs/validation
mkdir -p offline_demo/documentation

# Copy screenshots
cp screenshots/*.png offline_demo/screenshots/

# Copy sample outputs
cp data/hpc_results_summary.csv offline_demo/sample_outputs/hpc/
cp data/hpc_thread_scaling.csv offline_demo/sample_outputs/hpc/
cp data/hpc_rfm_analysis.csv offline_demo/sample_outputs/hpc/
cp data/bi_insights_summary.csv offline_demo/sample_outputs/bi/
cp data/ml_classification_results.csv offline_demo/sample_outputs/bi/
cp data/ml_clustering_results.csv offline_demo/sample_outputs/bi/
cp data/validation_report.csv offline_demo/sample_outputs/validation/

# Copy documentation
cp README.md offline_demo/documentation/
cp SHOWCASE_GUIDE.md offline_demo/documentation/
cp FAQ.md offline_demo/documentation/
cp PROJECT_STATE.md offline_demo/documentation/
cp SYSTEM_CONTRACT.md offline_demo/documentation/

# Create archive
tar -czf offline_demo.tar.gz offline_demo/
# or
zip -r offline_demo.zip offline_demo/
```

### OFFLINE_DEMO_README.md Content

```markdown
# Offline Demo Package

This package contains screenshots, sample outputs, and documentation for the HPC+BI Retail Analytics System.

## Contents

- **screenshots/**: Dashboard screenshots (7 pages)
- **sample_outputs/**: Sample data files (HPC, BI, Validation)
- **documentation/**: Complete system documentation

## Usage

1. **View Screenshots**: Open `screenshots/` directory
2. **Review Sample Outputs**: Open `sample_outputs/` directory
3. **Read Documentation**: Open `documentation/` directory

## Presentation Flow

1. Start with `documentation/SHOWCASE_GUIDE.md` for talking points
2. Use screenshots to illustrate key points
3. Reference sample outputs for data examples
4. Use `documentation/FAQ.md` for Q&A

## Key Metrics

- **Speedup**: 1.05x with 8 threads
- **ML Accuracy**: 95.08%
- **Validation**: 4/4 checks passing (0.0000% revenue difference)
- **Insights**: 25 actionable insights
- **Customers**: 4,338 customers, 6 RFM segments

## Contact

See `documentation/README.md` for contact information.
```

---

## ✅ Screenshot Capture Checklist

### Before Capturing
- [ ] Dashboard is running (`streamlit run app.py`)
- [ ] All data files are present in `data/` directory
- [ ] Browser window is set to 1920x1080 resolution
- [ ] All pages load without errors
- [ ] Charts render correctly

### During Capture
- [ ] Navigate to each page in order
- [ ] Wait for all charts to fully render
- [ ] Expand relevant sections (e.g., iteration details)
- [ ] Capture full page (use scrolling screenshot if needed)
- [ ] Save with correct filename

### After Capture
- [ ] Verify all 7 screenshots are captured
- [ ] Check image quality and resolution
- [ ] Ensure all key elements are visible
- [ ] Create offline demo package
- [ ] Test offline demo package

---

## 📊 Sample Output Generation Script

### Python Script: generate_sample_outputs.py

```python
import pandas as pd
import shutil
import os

def generate_sample_outputs():
    """Generate sample output files for offline demo."""
    
    # Create directories
    os.makedirs('sample_outputs/hpc', exist_ok=True)
    os.makedirs('sample_outputs/bi', exist_ok=True)
    os.makedirs('sample_outputs/validation', exist_ok=True)
    
    # HPC Outputs (first 10 rows or summary)
    hpc_files = [
        'hpc_results_summary.csv',
        'hpc_thread_scaling.csv',
        'hpc_rfm_analysis.csv',
        'hpc_correlation.csv',
        'hpc_topk_analysis.csv'
    ]
    
    for file in hpc_files:
        src = f'data/{file}'
        dst = f'sample_outputs/hpc/{file}'
        if os.path.exists(src):
            df = pd.read_csv(src)
            # Take first 10 rows for large files
            if len(df) > 10:
                df = df.head(10)
            df.to_csv(dst, index=False)
            print(f'Generated {dst}')
    
    # BI Outputs (first 10 rows or summary)
    bi_files = [
        'bi_insights_summary.csv',
        'rfm_analysis.csv',
        'ml_classification_results.csv',
        'ml_clustering_results.csv',
        'eda_outliers.csv'
    ]
    
    for file in bi_files:
        src = f'data/{file}'
        dst = f'sample_outputs/bi/{file}'
        if os.path.exists(src):
            df = pd.read_csv(src)
            # Take first 10 rows for large files
            if len(df) > 10:
                df = df.head(10)
            df.to_csv(dst, index=False)
            print(f'Generated {dst}')
    
    # Validation Outputs (full file)
    validation_files = ['validation_report.csv']
    
    for file in validation_files:
        src = f'data/{file}'
        dst = f'sample_outputs/validation/{file}'
        if os.path.exists(src):
            shutil.copy(src, dst)
            print(f'Generated {dst}')
    
    print('Sample outputs generated successfully!')

if __name__ == '__main__':
    generate_sample_outputs()
```

**Usage**:
```bash
python generate_sample_outputs.py
```

---

## 🎯 Key Takeaways

1. **Consistent Resolution**: Use 1920x1080 for all screenshots
2. **Full Page Capture**: Use scrolling screenshot tools for long pages
3. **Sample Outputs**: Include representative samples, not full datasets
4. **Offline Package**: Create self-contained package for presentations
5. **Documentation**: Include all documentation in offline package

---

**Last Updated**: 2026-04-16  
**Version**: 1.0  
**Maintained By**: System Development Team
