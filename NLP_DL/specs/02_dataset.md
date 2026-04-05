# 📊 Dataset Specification

## Dataset Source
Customer Support on Twitter (Kaggle)

## Dataset Size
Use 15,000 – 20,000 samples

## Final Structure

ticket_id, text, category, is_duplicate

## Categories (Fixed)

1. billing
2. technical
3. delivery
4. account

## Labeling Strategy

Use keyword-based classification:

- billing → payment, refund, charge
- technical → error, issue, bug
- delivery → delivery, late, shipping
- account → login, password, account

## Duplicate Creation

For ~30% data:
- Modify sentences slightly
- Use synonyms, rephrasing

Example:
Original: "My payment failed"
Duplicate: "Payment did not go through"

## Cleaning Steps

- Remove URLs
- Remove @mentions
- Lowercase
- Remove extra spaces

## Output CSV must be clean and balanced across categories