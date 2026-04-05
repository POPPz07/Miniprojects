# 📸 Streamlit App - Visual Guide

This document describes what each page looks like and what users will see.

---

## 🏠 HOME PAGE

### Layout
```
┌─────────────────────────────────────────────────────────────┐
│  🎫 Customer Support Ticket Classification System           │
│     Comparing NLP (TF-IDF) vs Deep Learning (LSTM)         │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌──────────────────────┐  ┌──────────────────────┐       │
│  │ 📋 Problem Statement │  │ ✨ Our Solution      │       │
│  │                      │  │                      │       │
│  │ • Thousands of       │  │ 🔵 NLP Approach     │       │
│  │   tickets daily      │  │   - Fast & interpret│       │
│  │ • Manual work        │  │                      │       │
│  │ • Time consuming     │  │ 🟢 DL Approach      │       │
│  │                      │  │   - Semantic meaning │       │
│  └──────────────────────┘  └──────────────────────┘       │
│                                                             │
│  ┌────────┐  ┌────────┐  ┌────────┐  ┌────────┐          │
│  │   📝   │  │   🧹   │  │   🎯   │  │   🔄   │          │
│  │ Input  │→ │ Preproc│→ │ Classif│→ │ Duplic │          │
│  └────────┘  └────────┘  └────────┘  └────────┘          │
│                                                             │
│  ┌────────┐  ┌────────┐  ┌────────┐  ┌────────┐          │
│  │ ~90%   │  │ 10.31% │  │ 50.80% │  │ 98.75% │          │
│  │ Classif│  │ NLP F1 │  │ DL F1  │  │ DL Rec │          │
│  └────────┘  └────────┘  └────────┘  └────────┘          │
│                                                             │
│  ┌────────┐  ┌────────┐  ┌────────┐  ┌────────┐          │
│  │ 5,851  │  │   4    │  │ 80/20  │  │  ~33%  │          │
│  │ Samples│  │ Categor│  │ Split  │  │ Duplic │          │
│  └────────┘  └────────┘  └────────┘  └────────┘          │
└─────────────────────────────────────────────────────────────┘
```

### Colors
- Headers: Blue (#1f77b4)
- Problem box: Yellow gradient
- Solution box: Green gradient
- Workflow steps: White with blue accents
- Metrics: White cards with hover effect

---

## 🔍 ANALYZE TICKET PAGE

### Layout
```
┌─────────────────────────────────────────────────────────────┐
│  🔍 Analyze Single Ticket                                   │
│     Compare NLP and Deep Learning predictions side-by-side  │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  📝 Enter Ticket Text                                       │
│  ┌───────────────────────────────────────────────────────┐ │
│  │ My payment failed but I was charged twice...          │ │
│  │                                                       │ │
│  └───────────────────────────────────────────────────────┘ │
│                                                             │
│  [🚀 Analyze Ticket]  [🗑️ Clear]                          │
│                                                             │
│  ✅ Analysis complete!                                      │
│                                                             │
│  ┌──────────────────────┐  ┌──────────────────────┐       │
│  │ 🔵 NLP Results       │  │ 🟢 DL Results        │       │
│  │                      │  │                      │       │
│  │ Category: BILLING    │  │ Category: BILLING    │       │
│  │ Confidence: 95.23%   │  │ Confidence: 92.15%   │       │
│  │ ████████████░░░░     │  │ ████████████░░░░     │       │
│  │                      │  │                      │       │
│  │ Duplicate: ❌ No     │  │ Duplicate: ❌ No     │       │
│  │ Similarity: 0.5234   │  │ Similarity: 0.8912   │       │
│  │                      │  │                      │       │
│  │ Top 3 Similar:       │  │                      │       │
│  │ 1. 0.5234            │  │                      │       │
│  │ 2. 0.4891            │  │                      │       │
│  │ 3. 0.4567            │  │                      │       │
│  │                      │  │                      │       │
│  │ [Bar Chart]          │  │ [Bar Chart]          │       │
│  └──────────────────────┘  └──────────────────────┘       │
│                                                             │
│  📊 Quick Comparison                                        │
│  ┌────────┐  ┌────────┐  ┌────────┐                       │
│  │ ✅ Agree│  │ ✅ Agree│  │ 93.7%  │                       │
│  │ Category│  │ Duplic │  │ Avg Con│                       │
│  └────────┘  └────────┘  └────────┘                       │
└─────────────────────────────────────────────────────────────┘
```

### Colors
- NLP box: Blue gradient (#e3f2fd → #bbdefb)
- DL box: Green gradient (#e8f5e9 → #c8e6c9)
- Progress bars: Blue/Green
- Charts: Blue/Green bars

---

## 📦 BATCH PROCESSING PAGE

### Layout
```
┌─────────────────────────────────────────────────────────────┐
│  📦 Batch Processing                                        │
│     Process multiple tickets at once from CSV file          │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  📤 Upload CSV File                                         │
│  💡 Your CSV must contain a 'text' column                   │
│                                                             │
│  [Choose CSV file]  tickets.csv                            │
│                                                             │
│  ✅ Loaded 50 tickets                                       │
│                                                             │
│  📋 Preview                                                 │
│  ┌───────────────────────────────────────────────────────┐ │
│  │ id │ text                                              │ │
│  │ 1  │ My payment failed...                             │ │
│  │ 2  │ App keeps crashing...                            │ │
│  │ 3  │ Order hasn't arrived...                          │ │
│  └───────────────────────────────────────────────────────┘ │
│                                                             │
│  [🚀 Process All Tickets]                                  │
│                                                             │
│  🔄 Processing ticket 25/50...                             │
│  ████████████░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░     │
│                                                             │
│  ✅ Processing complete!                                    │
│                                                             │
│  📊 Results Summary                                         │
│  ┌────────┐  ┌────────┐  ┌────────┐  ┌────────┐          │
│  │   50   │  │   12   │  │   18   │  │  92%   │          │
│  │ Process│  │ NLP Dup│  │ DL Dup │  │ Agree  │          │
│  └────────┘  └────────┘  └────────┘  └────────┘          │
│                                                             │
│  📋 Detailed Results                                        │
│  ┌───────────────────────────────────────────────────────┐ │
│  │ id│text│nlp_cat│nlp_conf│nlp_dup│dl_cat│dl_conf│...  │ │
│  │ 1 │... │billing│ 95.2%  │  No   │bill..│ 92.1% │...  │ │
│  └───────────────────────────────────────────────────────┘ │
│                                                             │
│  [📥 Download Results CSV]                                 │
│                                                             │
│  📊 Category Distribution                                   │
│  ┌──────────────────────┐  ┌──────────────────────┐       │
│  │ NLP Categories       │  │ DL Categories        │       │
│  │ [Pie Chart]          │  │ [Pie Chart]          │       │
│  └──────────────────────┘  └──────────────────────┘       │
└─────────────────────────────────────────────────────────────┘
```

### Colors
- Upload area: Light blue
- Progress bar: Blue
- Summary metrics: White cards
- Pie charts: Blue/Green gradients

---

## 📊 MODEL COMPARISON PAGE

### Layout
```
┌─────────────────────────────────────────────────────────────┐
│  📊 Model Comparison                                        │
│     Detailed performance analysis of NLP vs DL              │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  🎯 Classification Performance                              │
│  Both models achieve similar accuracy (~90%)                │
│                                                             │
│  ┌───────────────────────────────────────────────────────┐ │
│  │ Metric    │ NLP (TF-IDF) │ DL (LSTM) │ Difference   │ │
│  │ Accuracy  │ 91.33%       │ 90.05%    │ -1.28%       │ │
│  │ Precision │ 91.81%       │ 90.11%    │ -1.70%       │ │
│  │ Recall    │ 91.33%       │ 90.05%    │ -1.28%       │ │
│  │ F1-Score  │ 91.42%       │ 90.05%    │ -1.37%       │ │
│  └───────────────────────────────────────────────────────┘ │
│                                                             │
│  💡 Both models perform similarly (~91% vs ~90%)            │
│                                                             │
│  [Bar Chart: Classification Metrics Comparison]            │
│                                                             │
│  🔄 Duplicate Detection Performance                         │
│  Deep Learning significantly outperforms NLP                │
│                                                             │
│  ┌───────────────────────────────────────────────────────┐ │
│  │ Metric    │ NLP      │ DL       │ Improvement       │ │
│  │ Accuracy  │ 63.01%   │ 34.95%   │ -44.5%            │ │
│  │ Precision │ 29.41%   │ 34.20%   │ +16.3%            │ │
│  │ Recall    │ 6.25%    │ 98.75%   │ +1480.0% 🟢       │ │
│  │ F1-Score  │ 10.31%   │ 50.80%   │ +392.7% 🟢        │ │
│  └───────────────────────────────────────────────────────┘ │
│                                                             │
│  ✅ DL achieves 98.75% recall vs NLP's 6.25%                │
│                                                             │
│  ┌──────────────────────┐  ┌──────────────────────┐       │
│  │ Duplicate Detection  │  │ DL Improvement       │       │
│  │ [Grouped Bar Chart]  │  │ [Bar Chart]          │       │
│  └──────────────────────┘  └──────────────────────┘       │
│                                                             │
│  🤔 Why Deep Learning Excels                                │
│  ┌──────────────────────┐  ┌──────────────────────┐       │
│  │ 🔵 NLP (TF-IDF)      │  │ 🟢 DL (LSTM)         │       │
│  │ Lexical similarity   │  │ Semantic meaning     │       │
│  │ 6.25% recall ❌      │  │ 98.75% recall ✅     │       │
│  └──────────────────────┘  └──────────────────────┘       │
│                                                             │
│  🔑 Key Takeaways                                           │
│  ┌──────────────────────┐  ┌──────────────────────┐       │
│  │ 🔵 NLP Strengths     │  │ 🟢 DL Strengths      │       │
│  │ ✅ Fast inference    │  │ ✅ Semantic          │       │
│  │ ✅ Interpretable     │  │ ✅ 98.75% recall     │       │
│  │ ✅ Good classif      │  │ ✅ 5x better F1      │       │
│  └──────────────────────┘  └──────────────────────┘       │
│                                                             │
│  💡 Recommendation: Hybrid Approach                         │
│  [Purple gradient box with recommendation]                 │
└─────────────────────────────────────────────────────────────┘
```

### Colors
- Tables: Styled with blue headers
- Improvement cells: Green background
- Charts: Blue (NLP) and Green (DL)
- Info boxes: Yellow/Green gradients
- Recommendation: Purple gradient

---

## ℹ️ ABOUT PAGE

### Layout
```
┌─────────────────────────────────────────────────────────────┐
│  ℹ️ About This Project                                      │
│     Technical details and implementation overview           │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  📖 Project Overview                                        │
│  [Gray box with project description]                       │
│                                                             │
│  🛠️ Tech Stack                                              │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │ 🔵 NLP       │  │ 🟢 DL        │  │ 🔧 Shared    │     │
│  │ • TF-IDF     │  │ • LSTM       │  │ • NLTK       │     │
│  │ • LogReg     │  │ • Embedding  │  │ • Streamlit  │     │
│  │ • Sklearn    │  │ • TensorFlow │  │ • Plotly     │     │
│  └──────────────┘  └──────────────┘  └──────────────┘     │
│                                                             │
│  📊 Dataset Information                                     │
│  ┌──────────────────────┐  ┌──────────────────────┐       │
│  │ 📈 Statistics        │  │ 🏷️ Categories        │       │
│  │ 5,851 samples        │  │ • Billing            │       │
│  │ 4,675 train          │  │ • Technical          │       │
│  │ 1,176 test           │  │ • Delivery           │       │
│  │ 4 categories         │  │ • Account            │       │
│  └──────────────────────┘  └──────────────────────┘       │
│                                                             │
│  👨‍💻 Implementation Details                                 │
│  [Tabs: Preprocessing | Architectures | Training]          │
│                                                             │
│  Tab 1: Preprocessing                                       │
│  ┌──────────────────────┐  ┌──────────────────────┐       │
│  │ Steps (code)         │  │ Example              │       │
│  │ 1. HTML decode       │  │ Input: "hasn't..."   │       │
│  │ 2. Contractions      │  │ Output: "payment..." │       │
│  │ 3. Lowercase         │  │                      │       │
│  │ 4. Punctuation       │  │                      │       │
│  │ 5. Stopwords         │  │                      │       │
│  │ 6. Lemmatization     │  │                      │       │
│  └──────────────────────┘  └──────────────────────┘       │
│                                                             │
│  📚 Data Source                                             │
│  [Blue box with Kaggle TWCS information]                   │
│                                                             │
│  [Footer with credits and tech stack]                      │
└─────────────────────────────────────────────────────────────┘
```

### Colors
- Overview box: Light gray
- Tech stack cards: White with borders
- Tabs: Blue active, gray inactive
- Code blocks: Dark background
- Footer: Light gray with blue text

---

## 🎨 SIDEBAR (All Pages)

### Layout
```
┌──────────────────┐
│ 🎫 Navigation    │
├──────────────────┤
│                  │
│ ⚪ Home          │
│ ⚪ Analyze Ticket│
│ ⚪ Batch Process │
│ ⚪ Model Compare │
│ ⚪ About         │
│                  │
├──────────────────┤
│                  │
│ 🎫 Ticket        │
│ Classification   │
│ System           │
│                  │
│ Version 1.0      │
│ NLP vs DL        │
└──────────────────┘
```

### Colors
- Background: Light gray (#f8f9fa)
- Active page: Blue highlight
- Text: Dark gray
- Footer: Centered, styled

---

## 🎨 Color Palette Summary

### Primary Colors
- **NLP Blue:** #1f77b4
- **DL Green:** #4caf50
- **Accent Orange:** #ff7f0e

### Backgrounds
- **Light Gray:** #f8f9fa
- **White:** #ffffff
- **Blue Gradient:** #e3f2fd → #bbdefb
- **Green Gradient:** #e8f5e9 → #c8e6c9

### Text
- **Dark:** #333333
- **Medium:** #666666
- **Light:** #999999

### Borders
- **Light:** #e0e0e0
- **Medium:** #dee2e6

---

## 📱 Responsive Design

### Desktop (>1200px)
- Full width layout
- Two-column comparisons
- Large charts
- Spacious padding

### Tablet (768px - 1200px)
- Adjusted column widths
- Stacked sections
- Medium charts

### Mobile (<768px)
- Single column layout
- Stacked comparisons
- Compact charts
- Touch-friendly buttons

---

## ✨ Interactive Elements

### Hover Effects
- Cards lift up (translateY(-2px))
- Shadow increases
- Border color changes

### Click Effects
- Buttons: Color change
- Links: Underline
- Charts: Tooltips

### Animations
- Progress bars: Smooth fill
- Page transitions: Fade in
- Loading: Spinner

---

## 🎯 User Experience Flow

### First-Time User
1. Lands on Home → Sees overview
2. Clicks "Analyze Ticket" → Tests with sample
3. Views results → Compares NLP vs DL
4. Clicks "Model Comparison" → Understands differences
5. Clicks "About" → Learns technical details

### Regular User
1. Goes directly to "Analyze Ticket"
2. Enters ticket text
3. Gets instant predictions
4. Compares results

### Batch User
1. Goes to "Batch Processing"
2. Uploads CSV
3. Processes tickets
4. Downloads results

---

This visual guide helps you understand what users will see and experience when using the application!
