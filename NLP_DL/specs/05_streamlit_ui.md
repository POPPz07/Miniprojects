# 🖥️ Streamlit UI Specification

## Theme

- Light theme
- Colors:
  - Background: white / light gray
  - Primary: soft blue (#4A90E2)
  - Accent: teal (#50C9CE)

## Layout Sections

### 1. Header
- Project title
- Description

### 2. Input Section

Options:
- Text input (single ticket)
- CSV upload (bulk tickets)

### 3. Action Buttons

- "Analyze Ticket"
- "Batch Process"
- "Retrain Model" (optional)

### 4. Output Section

Display:

#### NLP Results
- Category
- Duplicate (Yes/No)
- Similarity score

#### DL Results
- Category
- Confidence score

### 5. Comparison Section

- Table: NLP vs DL

### 6. Visualization

- Confidence bar chart
- Similarity score indicator

### 7. Logs / Info

- Model version
- Dataset size

## Behavior

- Load trained models
- No training during inference
- Preprocessing runs on every input

## Notes

- No authentication needed
- Clean, minimal UI