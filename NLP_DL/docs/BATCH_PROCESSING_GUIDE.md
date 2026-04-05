# 📦 Batch Processing Guide

Complete guide for processing multiple tickets using CSV files.

---

## 📋 Quick Start

1. Prepare CSV file with ticket data
2. Upload to Batch Processing page
3. Review validation summary
4. Click "Process All Tickets"
5. Download results

---

## 📥 Input CSV Format

### Required Column

Your CSV must contain ONE of these column names for ticket text:
- `text`
- `ticket_text`
- `description`
- `message`
- `content`
- `ticket`

### Optional Column

For ticket identification (auto-generated if missing):
- `id`
- `ticket_id`
- `number`

### Example Input

```csv
id,text
1,"My payment failed but I was charged twice"
2,"Cannot login to my account"
3,"Package not delivered yet"
```

---

## 📤 Output CSV Format

### Results CSV (`ticket_analysis_results.csv`)

**11 columns:**

| Column | Description | Example |
|--------|-------------|---------|
| `ticket_id` | Original ID or auto-generated | 124, "TKT-001", 1 |
| `text` | Ticket text (truncated to 100 chars) | "My payment failed but..." |
| `nlp_category` | NLP predicted category | billing, technical, delivery, account |
| `nlp_confidence` | NLP confidence percentage | 91.23% |
| `nlp_duplicate` | NLP duplicate detection | Yes, No |
| `nlp_similarity` | NLP similarity score | 0.8542 |
| `dl_category` | DL predicted category | billing, technical, delivery, account |
| `dl_confidence` | DL confidence percentage | 89.45% |
| `dl_duplicate` | DL duplicate detection | Yes, No |
| `dl_similarity` | DL similarity score | 0.9621 |
| `category_match` | Models agreement | ✅ (agree), ⚠️ (disagree) |

**Example Output:**
```csv
ticket_id,text,nlp_category,nlp_confidence,nlp_duplicate,nlp_similarity,dl_category,dl_confidence,dl_duplicate,dl_similarity,category_match
124,"My payment failed but...",billing,91.23%,No,0.5432,billing,89.45%,No,0.8234,✅
252,"Package not delivered...",delivery,88.67%,Yes,0.7821,delivery,87.12%,Yes,0.9621,✅
567j,"Cannot login to...",account,93.45%,No,0.4567,technical,85.23%,No,0.7845,⚠️
```

### Skipped Tickets CSV (`skipped_tickets.csv`)

**2 columns:**

| Column | Description | Example |
|--------|-------------|---------|
| `ticket_id` | Original ID or auto-generated | 534, "TKT-002" |
| `reason` | Why ticket was skipped | "Empty or null text", "Text too short" |

**Example Output:**
```csv
ticket_id,reason
534,Empty or null text
345l,Text too short (< 3 characters)
674e,Empty or null text
789,Processing error: Preprocessing failed
```

---

## 🎯 ID Handling

### Scenario 1: CSV with ID Column

**Input:**
```csv
id,text
124,My payment failed
534,Cannot login
252,Package not delivered
345l,Refund request
567j,Account locked
```

**Behavior:**
- ✅ Preserves original IDs exactly (124, 534, 252, 345l, 567j)
- Supports any format: numbers, strings, alphanumeric
- Converts to string to handle mixed formats

### Scenario 2: CSV with Only Text Column

**Input:**
```csv
text
My payment failed
Cannot login
Package not delivered
```

**Behavior:**
- ✅ Auto-generates sequential IDs (1, 2, 3, 4...)
- Uses row number (1-indexed)

### Scenario 3: Mixed Valid/Invalid Rows

**Input:**
```csv
id,text
124,My payment failed
534,
252,Package not delivered
345l,Hi
567j,Account locked
```

**Processing:**
- Row 1 (ID: 124) → ✅ Processed
- Row 2 (ID: 534) → ⚠️ Skipped (empty text)
- Row 3 (ID: 252) → ✅ Processed
- Row 4 (ID: 345l) → ⚠️ Skipped (text too short)
- Row 5 (ID: 567j) → ✅ Processed

**Output:**
- Results CSV: 124, 252, 567j
- Skipped CSV: 534, 345l

---

## ⚠️ Tickets Are Skipped When

1. **Empty or null text** - Text field is NaN, None, or empty string
2. **Text too short** - Less than 3 characters
3. **Processing error** - Preprocessing or model prediction fails

---

## 📊 Processing Summary

After processing, you'll see:

- **Total Rows** - All rows in CSV
- **Successfully Processed** - Valid tickets analyzed
- **Skipped** - Problematic tickets
- **Success Rate** - Percentage processed successfully

---

## 💡 Best Practices

### Data Quality

✅ **Do:**
- Use UTF-8 encoding
- Include ticket IDs for traceability
- Clean obvious formatting issues
- Test with small sample first

❌ **Don't:**
- Mix languages in same batch
- Include HTML/XML tags
- Use extremely long text (>1000 chars)
- Include sensitive PII data

### Performance

- **Small batches** (< 1,000): Process immediately
- **Medium batches** (1,000-10,000): Expect 1-2 minutes
- **Large batches** (10,000+): Expect 5-10 minutes

### Error Handling

- Review skipped tickets CSV
- Fix data quality issues
- Re-upload corrected tickets
- Merge results manually if needed

---

## 🔧 Troubleshooting

### Issue: "CSV must contain one of these columns..."

**Solution:** Rename your text column to `text` or `description`

### Issue: Many tickets skipped

**Solution:** Check for:
- Empty rows
- Very short text
- Special characters causing issues

### Issue: Slow processing

**Solution:**
- Split into smaller batches
- Close other applications
- Use faster machine

### Issue: Different results on re-run

**Solution:** This is normal due to:
- Model randomness (minimal)
- Preprocessing variations (rare)
- Results should be 99%+ consistent

---

## 📈 Example Workflow

### Step 1: Prepare Data

```csv
id,description
TICKET-001,"Payment failed twice"
TICKET-002,"Login not working"
TICKET-003,"Package delayed"
```

### Step 2: Upload & Validate

```
✅ Loaded 3 rows from CSV
📌 Using column 'description' for ticket text
📌 Using column 'id' for ticket ID

Total Rows: 3
Valid Tickets: 3
Invalid Rows: 0
```

### Step 3: Process

```
🔄 Processing ticket 1/3...
🔄 Processing ticket 2/3...
🔄 Processing ticket 3/3...
✅ Processing complete!
```

### Step 4: Review Results

```
Processing Summary:
├─ Total Rows: 3
├─ Successfully Processed: 3
├─ Skipped: 0
└─ Success Rate: 100.0%

Results Summary:
├─ Analyzed Tickets: 3
├─ NLP Duplicates: 0
├─ DL Duplicates: 0
└─ Category Agreement: 100.0%
```

### Step 5: Download

- `ticket_analysis_results.csv` - All predictions
- `skipped_tickets.csv` - Any skipped tickets (if applicable)

---

## 🎓 Advanced Tips

### Handling Large Files

For files > 50,000 rows:
1. Split into multiple CSVs
2. Process separately
3. Merge results using ticket IDs

### Custom ID Formats

Any format works:
- `TICKET-2024-001`
- `ABC-123-XYZ`
- `12345`
- `USER_001_ISSUE_5`

### Duplicate Detection Strategy

- **NLP duplicates**: More conservative (threshold: 0.6)
- **DL duplicates**: More aggressive (threshold: 0.95)
- **Recommendation**: Use DL for duplicate detection (98.75% recall)

### Category Disagreement

When models disagree (⚠️):
- Check confidence scores
- Higher confidence usually correct
- Review ticket manually if critical
- NLP slightly better for classification overall

---

## 📞 Support

For issues or questions:
- Check troubleshooting section
- Review example workflows
- Open GitHub issue
- Contact support

---

**Happy Processing! 🚀**
